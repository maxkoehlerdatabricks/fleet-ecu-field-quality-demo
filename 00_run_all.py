# Databricks notebook source
# MAGIC %md
# MAGIC # 00 · Run all — one notebook that builds the whole demo
# MAGIC
# MAGIC Run this single notebook top to bottom and it runs every other notebook in order:
# MAGIC
# MAGIC | Order | Notebook | What it does |
# MAGIC |------:|----------|--------------|
# MAGIC | 1 | `01_simulate_raw` | Creates the schema + raw `bms_signal` table (healthy fleet + outliers). |
# MAGIC | 2 | `02_prepare`      | Builds the `bms_daily_vin` aggregate + `bms_band`. |
# MAGIC | 3 | `04_deploy_app`   | Creates + deploys the Databricks App and grants it read access. |
# MAGIC
# MAGIC `03_case_notebook` is the **optional** explainer with inline plots — run it by hand when you
# MAGIC want to walk the story; it is not needed to stand the demo up, so it is not run here.
# MAGIC
# MAGIC **The one input you must give:** the SQL warehouse id, in the widget below.

# COMMAND ----------

dbutils.widgets.text("WAREHOUSE_ID", "", "SQL Warehouse ID (required, for the app)")
WAREHOUSE_ID = dbutils.widgets.get("WAREHOUSE_ID").strip()
assert WAREHOUSE_ID, "Set the WAREHOUSE_ID widget (SQL Warehouses -> your warehouse -> copy the id)."

# Each child notebook runs with its own serverless context. Generous timeouts for the data build.
TIMEOUT = 3600

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1 · Simulate the raw telemetry

# COMMAND ----------

print(dbutils.notebook.run("./01_simulate_raw", TIMEOUT))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2 · Prepare the aggregate + band

# COMMAND ----------

print(dbutils.notebook.run("./02_prepare", TIMEOUT))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3 · Create + deploy the app
# MAGIC Passes the warehouse id through to `04_deploy_app`.

# COMMAND ----------

print(dbutils.notebook.run("./04_deploy_app", TIMEOUT, {"WAREHOUSE_ID": WAREHOUSE_ID}))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Done
# MAGIC The data is built and the app is deployed. The `04_deploy_app` output above prints the app URL.
# MAGIC Open `04_deploy_app` to see the clickable link, or run `databricks apps get fleet-ecu-dashboard`.
