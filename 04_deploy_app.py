# Databricks notebook source
# MAGIC %md
# MAGIC # 04 · Deploy the Databricks App — from this notebook, no shell scripts
# MAGIC
# MAGIC Everything the old `deploy/deploy.sh` did now happens here, inside a notebook, using the
# MAGIC Databricks SDK. Run this **after** `01_simulate_raw` and `02_prepare` have built the tables.
# MAGIC
# MAGIC It will:
# MAGIC 1. upgrade `databricks-sdk` in the notebook (the serverless runtime ships an older one that
# MAGIC    lacks the Apps API), then restart Python,
# MAGIC 2. figure out where this project lives in the workspace (so the app source path is correct),
# MAGIC 3. create the app `fleet-ecu-dashboard` with a `sql-warehouse` resource (idempotent),
# MAGIC 4. wait for the app compute to be ACTIVE,
# MAGIC 5. deploy the app code from `<project>/app`,
# MAGIC 6. grant the app's service principal read access to the demo schema,
# MAGIC 7. print the app URL.
# MAGIC
# MAGIC You only need to set **one** thing: `WAREHOUSE_ID` in the widget below (or the first cell).

# COMMAND ----------

# MAGIC %pip install --upgrade databricks-sdk
# MAGIC %restart_python

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

# MAGIC %md
# MAGIC ## Settings
# MAGIC `WAREHOUSE_ID` is the only required input. Find it under **SQL Warehouses** (serverless is fine).
# MAGIC `APP_NAME` can stay as-is.

# COMMAND ----------

dbutils.widgets.text("WAREHOUSE_ID", "", "SQL Warehouse ID (required)")
dbutils.widgets.text("APP_NAME", "fleet-ecu-dashboard", "App name")
dbutils.widgets.text("APP_SOURCE_PATH", "", "App source path override (optional, absolute /Workspace/... path)")

WAREHOUSE_ID    = dbutils.widgets.get("WAREHOUSE_ID").strip()
APP_NAME        = dbutils.widgets.get("APP_NAME").strip() or "fleet-ecu-dashboard"
APP_SOURCE_OVERRIDE = dbutils.widgets.get("APP_SOURCE_PATH").strip()

assert WAREHOUSE_ID, "Set the WAREHOUSE_ID widget (SQL Warehouses -> your warehouse -> copy the id)."
print(f"App    : {APP_NAME}")
print(f"Target : {CATALOG}.{SCHEMA}")
print(f"WH id  : {WAREHOUSE_ID}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Locate this project in the workspace
# MAGIC The app source is the `app/` folder next to this notebook. We derive the absolute workspace
# MAGIC path of this notebook, so the deploy works no matter where you imported the project.

# COMMAND ----------

import time
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.apps import App, AppResource, AppResourceSqlWarehouse, \
    AppResourceSqlWarehouseSqlWarehousePermission

w = WorkspaceClient()

# The Apps deploy API needs an ABSOLUTE path that starts with /Workspace. notebookPath()
# returns a /Users/... path (no /Workspace prefix), so we add it. You can also set the
# APP_SOURCE_PATH widget explicitly to skip the auto-derivation entirely.
if APP_SOURCE_OVERRIDE:
    APP_SOURCE = APP_SOURCE_OVERRIDE
    print(f"App source : {APP_SOURCE}  (from APP_SOURCE_PATH widget)")
else:
    nb_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
    PROJECT_DIR = nb_path.rsplit("/", 1)[0]      # folder holding 00_config, 01_..., app/
    if not PROJECT_DIR.startswith("/Workspace"):
        PROJECT_DIR = "/Workspace" + PROJECT_DIR  # deploy API requires the /Workspace prefix
    APP_SOURCE = f"{PROJECT_DIR}/app"
    print(f"Notebook   : {nb_path}")
    print(f"Project    : {PROJECT_DIR}")
    print(f"App source : {APP_SOURCE}")

assert APP_SOURCE.startswith("/Workspace/"), \
    f"App source path must be an absolute /Workspace/... path, got: {APP_SOURCE}"

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1 · Create the app (idempotent)
# MAGIC If the app already exists we reuse it. The `sql-warehouse` resource is what the app's
# MAGIC `DATABRICKS_WAREHOUSE_HTTP_PATH` env (`valueFrom: sql-warehouse` in `app.yaml`) resolves to.

# COMMAND ----------

wh_resource = AppResource(
    name="sql-warehouse",
    sql_warehouse=AppResourceSqlWarehouse(
        id=WAREHOUSE_ID,
        permission=AppResourceSqlWarehouseSqlWarehousePermission.CAN_USE,
    ),
)

try:
    existing = w.apps.get(name=APP_NAME)
    print(f"app '{APP_NAME}' already exists (state: {existing.compute_status.state if existing.compute_status else '?'}) — reusing")
except Exception:
    print(f"creating app '{APP_NAME}' ...")
    w.apps.create_and_wait(
        app=App(
            name=APP_NAME,
            description="Fleet EV battery field-quality dashboard: full-resolution density, "
                        "lasso -> raw-trace pushdown, single-vehicle drill.",
            resources=[wh_resource],
        )
    )
    print("created.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2 · Wait for app compute to be ACTIVE

# COMMAND ----------

for i in range(40):
    app = w.apps.get(name=APP_NAME)
    state = app.compute_status.state.value if app.compute_status and app.compute_status.state else "UNKNOWN"
    print(f"  compute: {state}")
    if state == "ACTIVE":
        break
    time.sleep(15)
else:
    raise RuntimeError("app compute did not become ACTIVE in time")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3 · Deploy the app code from `<project>/app`

# COMMAND ----------

from databricks.sdk.service.apps import AppDeployment

dep = w.apps.deploy_and_wait(app_name=APP_NAME,
                             app_deployment=AppDeployment(source_code_path=APP_SOURCE))
print(f"deployment status: {dep.status.state.value if dep.status and dep.status.state else '?'}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4 · Grant the app's service principal read access to the demo schema
# MAGIC Genie-free, but the app queries the tables as its own service principal, so it needs
# MAGIC USE CATALOG / USE SCHEMA / SELECT on the demo schema.

# COMMAND ----------

app = w.apps.get(name=APP_NAME)
sp = app.service_principal_client_id
print(f"service principal: {sp}")

if sp:
    for stmt in [
        f"GRANT USE CATALOG ON CATALOG {CATALOG} TO `{sp}`",
        f"GRANT USE SCHEMA  ON SCHEMA  {CATALOG}.{SCHEMA} TO `{sp}`",
        f"GRANT SELECT      ON SCHEMA  {CATALOG}.{SCHEMA} TO `{sp}`",
    ]:
        spark.sql(stmt)
        print("  ok:", stmt)
else:
    print("WARNING: no service_principal_client_id on the app — grant skipped.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Done — open the app

# COMMAND ----------

app = w.apps.get(name=APP_NAME)
print("App URL:", app.url)
displayHTML(f'<h3>App deployed</h3><p><a href="{app.url}" target="_blank">{app.url}</a></p>')
