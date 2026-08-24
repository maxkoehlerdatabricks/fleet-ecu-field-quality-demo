# Databricks notebook source
# MAGIC %md
# MAGIC # 01 - Simulate raw BMS signals
# MAGIC Generates the raw fact table `bms_signal`: per-car, high-frequency battery signals
# MAGIC with a physically plausible **healthy fleet** plus a few injected **thermal outliers**
# MAGIC (packs that run hot early in their life).
# MAGIC
# MAGIC This is the data that **cannot be aggregated** for outlier work: a hot event lasts
# MAGIC seconds and is invisible in any daily/per-car average.
# MAGIC
# MAGIC Scales with the knobs in `00_config`. Uses Spark so turning `N_CARS`/`N_DAYS` up just works.

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql import types as T
import math

# Catalog + schema are created by 00_config (best-effort catalog, always schema). Just USE it.
spark.sql(f"USE {CATALOG}.{SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Vehicle dimension
# MAGIC One row per VIN: a starting odometer (fleet-age spread) and a `is_bad` flag.

# COMMAND ----------

import random
random.seed(RANDOM_SEED)   # deterministic fleet; RANDOM_SEED lives in 00_config

n_bad = max(1, round(N_CARS * BAD_CAR_FRAC))
bad_ids = set(random.sample(range(N_CARS), n_bad))

veh_rows = []
for i in range(N_CARS):
    vin = f"WVWDEMO{i:010d}"                      # 17-char pseudo-VIN
    odo0 = random.uniform(ODO_START_MIN_KM, ODO_START_MAX_KM)
    veh_rows.append((vin, i, float(odo0), i in bad_ids))

veh = spark.createDataFrame(
    veh_rows, schema=T.StructType([
        T.StructField("vin", T.StringType()),
        T.StructField("car_idx", T.IntegerType()),
        T.StructField("odo_start_km", T.DoubleType()),
        T.StructField("is_bad", T.BooleanType()),
    ]))
veh.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(VIN_TABLE)
print(f"{VIN_TABLE}: {N_CARS} cars, {n_bad} bad -> {sorted(bad_ids)}")
display(spark.table(VIN_TABLE))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Raw signal generation
# MAGIC For each car and day we simulate one driving trip of `DRIVE_H` hours at `HZ`.
# MAGIC We build the time grid with `explode(sequence(...))`, then compute signals as
# MAGIC functions of time-of-trip, SoC, and vehicle health. Everything is a column
# MAGIC expression so Spark parallelizes across the whole fleet.

# COMMAND ----------

samples_per_trip = int(DRIVE_H * 3600 * HZ)
base_ts = F.expr("timestamp('2026-08-01 08:00:00')")

# grid: one row per (vin, day, sample)
grid = (
    veh
    .withColumn("day", F.explode(F.sequence(F.lit(0), F.lit(N_DAYS - 1))))
    .withColumn("s",   F.explode(F.sequence(F.lit(0), F.lit(samples_per_trip - 1))))
)

# time within trip (sec) and absolute timestamp
grid = grid.withColumn("t_sec", F.col("s") / F.lit(float(HZ)))
grid = grid.withColumn(
    "ts",
    (F.unix_timestamp(base_ts) + F.col("day") * 86400 + F.col("t_sec")).cast("timestamp"),
)

# odometer accrues: each trip adds ~ DRIVE_H * avg_speed(km/h); ~40 km/h avg city
km_per_trip = DRIVE_H * 40.0
grid = grid.withColumn(
    "odometer_km",
    F.col("odo_start_km") + F.col("day") * F.lit(km_per_trip) + (F.col("t_sec") / 3600.0) * 40.0,
)

# COMMAND ----------

# deterministic-ish pseudo-random per row (no python UDF -> stays fast at scale)
noise = lambda seed: (F.rand(seed) - F.lit(0.5))

# SoC: starts ~90%, drains linearly over the trip to ~40%
grid = grid.withColumn(
    "soc_pct",
    F.greatest(F.lit(5.0), F.lit(90.0) - (F.col("t_sec") / (DRIVE_H * 3600.0)) * 50.0) + noise(1) * 2.0,
)

# ambient temp: mild daily variation
grid = grid.withColumn("ambient_temp_c", F.lit(24.0) + F.sin(F.col("t_sec") / 1800.0) * 3.0 + noise(2) * 1.0)

# pack current: discharge while driving, with load swings (accel/regen)
grid = grid.withColumn(
    "pack_current_a",
    F.lit(-60.0) + F.sin(F.col("t_sec") / 15.0) * 40.0 + noise(3) * 20.0,   # negative = discharge
)

# --- Cell temperature: THE outlier signal --------------------------------
# Healthy envelope: baseline that drifts UP slowly with mileage (aging),
# plus load-driven warming, plus ambient, plus small noise.
odo_drift = (F.col("odometer_km") / 100000.0) * 8.0          # +8C per 100k km, healthy aging
load_warm = F.abs(F.col("pack_current_a")) / 10.0            # warmer under load
healthy_temp = (
    F.lit(HEALTHY_BASELINE_C)                                # fleet baseline (00_config)
    + odo_drift + load_warm + (F.col("ambient_temp_c") - 24.0) * 0.5 + noise(4) * 1.5
)

# Bad cars: a thermal EXCURSION. A hot spike that lasts a few seconds, recurring,
# far above what their (often low) mileage would justify. This is the anomaly the
# left plot must surface and the right plot must show as a raw trace.
# Trigger: short 8-second windows every ~5 min; amplitude = SPIKE_AMPLITUDE_C (00_config).
in_spike = (F.col("s") % (5 * 60 * HZ)).between(0, 8 * HZ)   # 8-second spike every 5 min
spike_amp = F.lit(SPIKE_AMPLITUDE_C) + noise(5) * 6.0
bad_temp = healthy_temp + F.when(in_spike, spike_amp).otherwise(F.lit(3.0))  # bad cars run warm even between spikes

grid = grid.withColumn(
    "cell_temp_max_c",
    F.when(F.col("is_bad"), bad_temp).otherwise(healthy_temp),
)

# cell voltage: sags with SoC and (for bad cars) a bit more
grid = grid.withColumn(
    "cell_voltage_min_v",
    F.lit(3.2) + (F.col("soc_pct") / 100.0) * 0.9 + noise(6) * 0.02
      - F.when(F.col("is_bad"), F.lit(0.05)).otherwise(F.lit(0.0)),
)

# event type: first 20% of trip is a DC charge, rest driving (toy)
grid = grid.withColumn(
    "event_type",
    F.when(F.col("t_sec") < DRIVE_H * 3600.0 * 0.2, F.lit("dc_charge")).otherwise(F.lit("drive")),
)

# COMMAND ----------

raw = grid.select(
    "vin",
    "ts",
    F.round("odometer_km", 1).alias("odometer_km"),
    F.round("soc_pct", 2).alias("soc_pct"),
    F.round("cell_temp_max_c", 2).alias("cell_temp_max_c"),
    F.round("cell_voltage_min_v", 3).alias("cell_voltage_min_v"),
    F.round("pack_current_a", 1).alias("pack_current_a"),
    F.round("ambient_temp_c", 2).alias("ambient_temp_c"),
    "event_type",
)

(raw.write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .partitionBy("event_type")            # small set: cheap partitioning; scale -> partition by date(ts)
    .saveAsTable(RAW_TABLE))

n = spark.table(RAW_TABLE).count()
print(f"{RAW_TABLE}: {n:,} raw rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Sanity check
# MAGIC Healthy vs bad cell-temp distribution — the bad cars should have a fat high tail.

# COMMAND ----------

display(
    spark.table(RAW_TABLE).join(spark.table(VIN_TABLE), "vin")
    .groupBy("is_bad")
    .agg(
        F.round(F.avg("cell_temp_max_c"), 1).alias("avg_temp"),
        F.round(F.expr("percentile(cell_temp_max_c, 0.99)"), 1).alias("p99_temp"),
        F.round(F.max("cell_temp_max_c"), 1).alias("max_temp"),
        F.count("*").alias("rows"),
    )
)
