# Databricks notebook source
# MAGIC %md
# MAGIC # 99 · Teardown — remove everything this demo created
# MAGIC
# MAGIC Deletes the Databricks App and drops the demo schema (all tables). It does **not** touch the
# MAGIC catalog or the SQL warehouse.
# MAGIC
# MAGIC Safe to re-run — missing objects are ignored.

# COMMAND ----------

# MAGIC %pip install --upgrade databricks-sdk
# MAGIC %restart_python

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

dbutils.widgets.text("APP_NAME", "fleet-ecu-dashboard", "App name to delete")
APP_NAME = dbutils.widgets.get("APP_NAME").strip() or "fleet-ecu-dashboard"

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1 · Delete the app

# COMMAND ----------

from databricks.sdk import WorkspaceClient
w = WorkspaceClient()

try:
    w.apps.get(name=APP_NAME)
    w.apps.delete(name=APP_NAME)
    print(f"deleted app: {APP_NAME}")
except Exception as e:
    print(f"app '{APP_NAME}' not deleted (likely already gone): {str(e)[:160]}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2 · Drop the demo schema (all tables)

# COMMAND ----------

spark.sql(f"DROP SCHEMA IF EXISTS {CATALOG}.{SCHEMA} CASCADE")
print(f"dropped schema: {CATALOG}.{SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Done
# MAGIC App removed and schema dropped. Catalog and warehouse are untouched.
