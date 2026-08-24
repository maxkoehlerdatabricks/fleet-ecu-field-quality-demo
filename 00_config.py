# Databricks notebook source
# MAGIC %md
# MAGIC # 00 · Config — the single source of truth for the demo
# MAGIC
# MAGIC Every other notebook (`01_simulate_raw`, `02_prepare`, `03_case_notebook`) pulls this in
# MAGIC with `%run ./00_config`. Change a value **here** and it propagates everywhere — you never
# MAGIC edit the same number in two places.
# MAGIC
# MAGIC ## What you edit for a new workspace
# MAGIC 1. **`CATALOG`** — the Unity Catalog to build in (created below if missing & you have rights).
# MAGIC 2. **`SCHEMA`** — the schema inside it (always created below if missing).
# MAGIC 3. **Data-size knobs** — `N_CARS`, `N_DAYS`, `HZ`, `DRIVE_H`. Start small, scale later.
# MAGIC
# MAGIC After changing size knobs, re-run `01_simulate_raw` and `02_prepare`. Nothing else changes.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1 · Destination — catalog & schema

# COMMAND ----------

# >>> EDIT THESE FOR A NEW WORKSPACE <<<
CATALOG = "serverless_stable_7qzrfp_catalog"   # Unity Catalog to build in
SCHEMA  = "field_telemetry_demo"               # schema created inside CATALOG

# Whether to attempt creating the catalog. Creating a catalog needs CREATE CATALOG on the
# metastore, which many users do NOT have (managed catalogs are often pre-provisioned). Leave
# True to try-and-continue; if it fails we assume the catalog already exists and move on.
CREATE_CATALOG_IF_MISSING = True

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2 · Data-size knobs — START SMALL, scale later
# MAGIC Default (20 cars × 3 days × 10 Hz) ≈ **2.16 M** raw rows: fast to build, outliers clearly
# MAGIC visible. Raise `N_CARS` / `N_DAYS` for a bigger fleet; the simulation is Spark-parallel so
# MAGIC it scales. `HZ` drives resolution *and* row count linearly.

# COMMAND ----------

N_CARS  = 20      # number of vehicles in the fleet
N_DAYS  = 3       # days of history per vehicle
HZ      = 10      # sample rate of the fast signals (samples per second)
DRIVE_H = 1.0     # hours driven per car per day (one trip/day for the small set)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3 · Scenario knobs — how the outliers behave
# MAGIC These shape the *story*: how many packs are faulty and how hard they run hot. Tune these to
# MAGIC make the anomaly more obvious (bigger `SPIKE_AMPLITUDE_C`) or more subtle.

# COMMAND ----------

# Fraction of cars that are "bad" — packs that run hot early in life. A few is enough for the
# left-plot density to show clear anomalies above the healthy band. 0.15 of 20 -> 3 cars.
BAD_CAR_FRAC = 0.15

# The hot threshold (deg C). A sample above this counts toward `hot_seconds`. THIS IS SHARED:
# 01_simulate_raw, 02_prepare AND the App must all use the same value or the metrics disagree.
# Defined once here so they can't drift apart.
HOT_THRESHOLD_C = 55.0

# Healthy fleet baseline cell temperature (deg C) at zero mileage / no load. The whole normal
# population sits around this, drifting up slowly with mileage and load.
HEALTHY_BASELINE_C = 28.0

# How far a bad car's thermal spike rises above its healthy curve (deg C, before noise). Bigger
# = more obvious outlier. This is the main dial for "how visible is the anomaly".
SPIKE_AMPLITUDE_C = 22.0

# Random seed — makes the whole synthetic fleet deterministic and re-runnable to the same result.
# Change it to draw a different (but statistically equivalent) fleet.
RANDOM_SEED = 42

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4 · Fleet aging & aggregate granularity

# COMMAND ----------

# Starting odometer spread (km): cars enter the fleet at different ages, so the healthy
# cell-temp envelope drifts up across the population.
ODO_START_MIN_KM = 500
ODO_START_MAX_KM = 90000

# Odometer bucket width (km) for the 02_prepare aggregate (bms_daily_vin). Each (vin, bucket)
# is one point in the left-plot overview. Smaller = finer resolution + more aggregate rows;
# scale this up as the fleet grows.
ODO_BUCKET_KM = 2000

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5 · Derived table names (do not edit)

# COMMAND ----------

RAW_TABLE   = f"{CATALOG}.{SCHEMA}.bms_signal"       # raw fast signals (the big one)
DAILY_TABLE = f"{CATALOG}.{SCHEMA}.bms_daily_vin"    # per-(vin, odo bucket) aggregate: left-plot source
VIN_TABLE   = f"{CATALOG}.{SCHEMA}.vehicle"          # dim: one row per vin
BAND_TABLE  = f"{CATALOG}.{SCHEMA}.bms_band"         # population percentile band per odo bucket

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6 · Create catalog (best-effort) & schema (always)
# MAGIC Safe to re-run — everything is `IF NOT EXISTS`.

# COMMAND ----------

# Catalog: try to create it, but do not fail the run if we lack CREATE CATALOG on the metastore
# (a managed catalog is usually pre-provisioned). We continue assuming it already exists.
if CREATE_CATALOG_IF_MISSING:
    try:
        spark.sql(f"CREATE CATALOG IF NOT EXISTS {CATALOG}")
        print(f"catalog ok: {CATALOG} (created or already present)")
    except Exception as e:
        print(f"catalog create skipped for {CATALOG} — assuming it already exists.\n  reason: {str(e)[:160]}")
else:
    print(f"catalog create disabled; assuming {CATALOG} exists.")

# Schema: always create if missing (this only needs CREATE SCHEMA on the catalog).
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")
print(f"schema ok: {CATALOG}.{SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7 · Echo the resolved config

# COMMAND ----------

print(f"Target        : {CATALOG}.{SCHEMA}")
print(f"Fleet         : {N_CARS} cars x {N_DAYS} days @ {HZ} Hz, {DRIVE_H} h/day")
print(f"Outliers      : {BAD_CAR_FRAC:.0%} of cars, spike +{SPIKE_AMPLITUDE_C}C over {HOT_THRESHOLD_C}C threshold")
print(f"Odo buckets   : {ODO_BUCKET_KM} km wide, start {ODO_START_MIN_KM}-{ODO_START_MAX_KM} km")
print(f"Seed          : {RANDOM_SEED}")
est_rows = int(N_CARS * N_DAYS * DRIVE_H * 3600 * HZ)
print(f"Est. raw rows : ~{est_rows:,}")
