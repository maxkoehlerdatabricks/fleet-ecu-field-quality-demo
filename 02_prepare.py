# Databricks notebook source
# MAGIC %md
# MAGIC # 02 - Prepare left-plot aggregate
# MAGIC Builds `bms_daily_vin`: one row per **(vin, odometer bucket)** with cell-temp
# MAGIC percentiles and hot-second counts.
# MAGIC
# MAGIC **This is the split that makes the App fast.** The left plot never scans the raw
# MAGIC table live; it hexbins this small aggregate. The raw table is only touched on brush,
# MAGIC for the handful of VINs inside the box (see the App).

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

from pyspark.sql import functions as F

spark.sql(f"USE {CATALOG}.{SCHEMA}")

# odometer bucket width (km). Small set: 2000 km buckets.
ODO_BUCKET_KM = 2000

# COMMAND ----------

raw = spark.table(RAW_TABLE)

daily = (
    raw
    .withColumn("odometer_bucket_km",
                (F.floor(F.col("odometer_km") / ODO_BUCKET_KM) * ODO_BUCKET_KM).cast("int"))
    .groupBy("vin", "odometer_bucket_km")
    .agg(
        F.round(F.expr("percentile(cell_temp_max_c, 0.50)"), 2).alias("cell_temp_p50"),
        F.round(F.expr("percentile(cell_temp_max_c, 0.99)"), 2).alias("cell_temp_p99"),
        F.round(F.max("cell_temp_max_c"), 2).alias("cell_temp_max"),
        F.round(F.min("cell_voltage_min_v"), 3).alias("cell_voltage_min"),
        F.sum(F.when(F.col("cell_temp_max_c") > 55, 1.0 / HZ).otherwise(0.0)).alias("hot_seconds"),
        F.sum(F.when(F.col("event_type") == "dc_charge", 1).otherwise(0)).alias("dc_charge_samples"),
        F.count("*").alias("n_samples"),
    )
)

(daily.write
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(DAILY_TABLE))

print(f"{DAILY_TABLE}: {spark.table(DAILY_TABLE).count():,} rows "
      f"(one per vin x {ODO_BUCKET_KM}km bucket)")

# COMMAND ----------

# MAGIC %md
# MAGIC ## The population band
# MAGIC For the left plot / notebook we also want the healthy fleet envelope per odometer bucket
# MAGIC (median and p95 of the per-vin p99). The right plot overlays raw traces on this band.

# COMMAND ----------

band = (
    spark.table(DAILY_TABLE)
    .groupBy("odometer_bucket_km")
    .agg(
        F.round(F.expr("percentile(cell_temp_p99, 0.50)"), 2).alias("band_p50"),
        F.round(F.expr("percentile(cell_temp_p99, 0.95)"), 2).alias("band_p95"),
        F.count("*").alias("n_vins"),
    )
    .orderBy("odometer_bucket_km")
)
band.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{CATALOG}.{SCHEMA}.bms_band")
display(band)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Quick look: the left-plot data
# MAGIC Scatter of every (vin, bucket): X = odometer, Y = p99 cell temp. Bad cars pop above the band.

# COMMAND ----------

display(
    spark.table(DAILY_TABLE).join(spark.table(VIN_TABLE), "vin")
    .select("vin", "odometer_bucket_km", "cell_temp_p99", "hot_seconds", "is_bad")
    .orderBy(F.desc("cell_temp_p99"))
)
