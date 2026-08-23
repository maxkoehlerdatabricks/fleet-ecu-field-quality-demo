# Databricks notebook source
# MAGIC %md
# MAGIC # 00 - Config
# MAGIC Shared parameters for the Fleet ECU field-quality demo.
# MAGIC
# MAGIC **Size knobs** live here. Start small; scale up later by changing `N_CARS` / `N_DAYS`
# MAGIC and re-running `01_simulate_raw` and `02_prepare`. Nothing else changes.

# COMMAND ----------

# ============================================================================
#  >>> EDIT THESE TWO FOR A NEW WORKSPACE <<<
#  CATALOG : an existing Unity Catalog you can create schemas in.
#  SCHEMA  : created by 01_simulate_raw if it does not exist.
#  (The SQL warehouse id is NOT set here -- the notebooks use Spark, and the
#   App reads its warehouse from an app resource. See README section "Deploy".)
# ============================================================================
CATALOG = "serverless_stable_7qzrfp_catalog"
SCHEMA  = "field_telemetry_demo"

# --- Size knobs (START SMALL) ----------------------------------------------
# 20 cars x 3 days x 10 Hz x ~1h/day driving  ->  ~13M raw rows
N_CARS   = 20        # number of vehicles in the fleet
N_DAYS   = 3         # days of history
HZ       = 10        # sample rate of the fast signals (samples/sec)
DRIVE_H  = 1.0       # hours driven per car per day (one trip/day for the small set)

# --- Outlier injection ------------------------------------------------------
# Fraction of cars that are "bad" (run hot early in life). Keep a few so the
# left-plot density has visible anomalies above the healthy band.
BAD_CAR_FRAC = 0.15  # ~3 of 20 cars

# --- Fleet aging ------------------------------------------------------------
# Each car gets a starting odometer; healthy cell-temp envelope drifts up slowly
# with mileage. Bad cars sit high above the band for their mileage.
ODO_START_MIN_KM = 500
ODO_START_MAX_KM = 90000

# --- Table names ------------------------------------------------------------
RAW_TABLE   = f"{CATALOG}.{SCHEMA}.bms_signal"       # raw fast signals (the big one)
DAILY_TABLE = f"{CATALOG}.{SCHEMA}.bms_daily_vin"    # per-(vin, odo bucket) aggregate: left-plot source
VIN_TABLE   = f"{CATALOG}.{SCHEMA}.vehicle"          # dim: one row per vin

# COMMAND ----------

print(f"Target: {CATALOG}.{SCHEMA}")
print(f"Fleet:  {N_CARS} cars x {N_DAYS} days @ {HZ} Hz, {DRIVE_H} h/day")
est_rows = int(N_CARS * N_DAYS * DRIVE_H * 3600 * HZ)
print(f"Est. raw rows: ~{est_rows:,}")
