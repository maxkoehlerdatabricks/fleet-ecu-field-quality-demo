#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Fleet ECU demo -- one-shot deploy to a NEW Databricks workspace.
# No Asset Bundles. Uses the Databricks CLI + a jobs-submit run.
#
# Prereqs:
#   - Databricks CLI v0.2xx installed and a profile authenticated:
#       databricks auth login --profile <PROFILE>
#   - A Unity Catalog you can create a schema in.
#   - A SQL warehouse (serverless is fine).
#
# Edit the five variables below, then run:  bash deploy/deploy.sh
# ---------------------------------------------------------------------------
set -euo pipefail

# ===== EDIT THESE =====
PROFILE="CHANGE_ME_PROFILE"                       # databricks CLI profile name
USER_EMAIL="CHANGE_ME@example.com"                # your workspace user (for the /Workspace path)
CATALOG="CHANGE_ME_CATALOG"                        # must match 00_config.py CATALOG
WAREHOUSE_ID="CHANGE_ME_WAREHOUSE_ID"              # SQL warehouse id (Settings > SQL Warehouses)
APP_NAME="fleet-ecu-dashboard"
# ======================

SCHEMA="field_telemetry_demo"                      # must match 00_config.py SCHEMA
WS_DIR="/Workspace/Users/${USER_EMAIL}/fleet-ecu-demo"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "==> 1/6  Import project into the workspace"
databricks workspace import-dir "${REPO_ROOT}" "${WS_DIR}" --overwrite -p "${PROFILE}"

echo "==> 2/6  Create the schema (catalog must already exist)"
python3 "${REPO_ROOT}/deploy/run_sql.py" "${PROFILE}" "${WAREHOUSE_ID}" \
  "CREATE SCHEMA IF NOT EXISTS ${CATALOG}.${SCHEMA}"

echo "==> 3/6  Run the data pipeline (simulate -> prepare) as a one-off job"
RUN_JSON="$(mktemp)"
sed "s#/Workspace/Users/CHANGE_ME/fleet-ecu-demo#${WS_DIR}#g" \
  "${REPO_ROOT}/deploy/run_pipeline.json" > "${RUN_JSON}"
databricks jobs submit --json "@${RUN_JSON}" -p "${PROFILE}"
echo "    pipeline finished"

echo "==> 4/6  Create the app (idempotent; ignore ALREADY_EXISTS)"
APP_JSON="$(mktemp)"
sed "s#CHANGE_ME_WAREHOUSE_ID#${WAREHOUSE_ID}#g" \
  "${REPO_ROOT}/deploy/app_create.json" > "${APP_JSON}"
databricks apps create --json "@${APP_JSON}" -p "${PROFILE}" || echo "    app may already exist -- continuing"

echo "==> 5/6  Wait for app compute to be ACTIVE, then deploy the code"
for i in $(seq 1 40); do
  st="$(databricks apps get "${APP_NAME}" -p "${PROFILE}" -o json | python3 -c 'import sys,json;print(json.load(sys.stdin).get("compute_status",{}).get("state"))')"
  echo "    compute: ${st}"
  [ "${st}" = "ACTIVE" ] && break
  sleep 15
done
databricks apps deploy "${APP_NAME}" --source-code-path "${WS_DIR}/app" -p "${PROFILE}"

echo "==> 6/6  Grant the app's service principal read access to the demo schema"
SP="$(databricks apps get "${APP_NAME}" -p "${PROFILE}" -o json | python3 -c 'import sys,json;print(json.load(sys.stdin).get("service_principal_client_id",""))')"
if [ -n "${SP}" ]; then
  python3 "${REPO_ROOT}/deploy/run_sql.py" "${PROFILE}" "${WAREHOUSE_ID}" "GRANT USE CATALOG ON CATALOG ${CATALOG} TO \`${SP}\`"
  python3 "${REPO_ROOT}/deploy/run_sql.py" "${PROFILE}" "${WAREHOUSE_ID}" "GRANT USE SCHEMA ON SCHEMA ${CATALOG}.${SCHEMA} TO \`${SP}\`"
  python3 "${REPO_ROOT}/deploy/run_sql.py" "${PROFILE}" "${WAREHOUSE_ID}" "GRANT SELECT ON SCHEMA ${CATALOG}.${SCHEMA} TO \`${SP}\`"
fi

URL="$(databricks apps get "${APP_NAME}" -p "${PROFILE}" -o json | python3 -c 'import sys,json;print(json.load(sys.stdin).get("url",""))')"
echo ""
echo "DONE. Open the app:  ${URL}"
