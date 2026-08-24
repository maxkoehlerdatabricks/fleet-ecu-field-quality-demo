# Fleet ECU Field-Quality Demo

An EV **battery field-quality** monitoring demo. It shows why the dangerous signal in fleet
telemetry is never the average — it is the handful of packs that ran hot when they had no reason
to — and why finding them requires keeping the **raw** signal rather than rolling it up.

The demo ships:

- **Synthetic raw telemetry** for a fleet of EVs (per-cell temperature, voltage, pack current at
  10 Hz), with a few packs that run hot injected as outliers.
- A **Databricks App** dashboard with three brushable fleet visualizations and a drill-down:
  box-select the suspects → see their raw traces + a forensic table → click one vehicle → see its
  full-resolution raw scatter.
- A **case notebook** that explains the story with inline plots and states the Tableau-vs-Apps framing.
- A standalone **story page** (`story.html`) explaining what the plots mean and what outliers mean
  physically for the battery and other tested products.

It runs on **serverless Spark + a SQL warehouse**. **No Asset Bundles.**

---

## The case in one paragraph

A cell that climbs to 70 °C for eight seconds during a fast charge is a thermal event — a precursor
to accelerated aging and, at the extreme, thermal runaway. Averaged across a day, a pack, and a
fleet, it vanishes into a healthy-looking mid-thirties number. So you keep every raw sample, plot
the whole fleet, brush the region where suspects sit, and drill into the raw trace of each one.
That "brush the population → fetch the raw member on demand" loop is what the dashboard demonstrates
— and what an extract-based BI tool cannot do without pre-summarizing.

---

## Repository layout

```
00_config.py          # <-- EDIT: CATALOG / SCHEMA + data-size knobs (N_CARS, N_DAYS, HZ)
01_simulate_raw.py    # creates the schema + raw bms_signal table (healthy fleet + outliers)
02_prepare.py         # builds the bms_daily_vin aggregate + bms_band
03_case_notebook.py   # explains the case with inline plots + Tableau-vs-Apps framing
story.html            # standalone narrative page (open in any browser)
app/                  # the Databricks App
  app.yaml            #   command + env (CATALOG/SCHEMA, warehouse from a resource)
  requirements.txt
  backend/app.py      #   FastAPI: /api/curves /api/density /api/phase /api/vehicle /api/brush /api/band
  frontend/index.html #   Plotly UI (vendored locally in frontend/vendor/)
deploy/
  deploy.sh           # one-shot deploy to a new workspace (edit 5 vars at top)
  run_sql.py          # helper: run one SQL statement via the SDK
  run_pipeline.json   # jobs-submit spec for simulate -> prepare
  app_create.json     # app creation spec (sql-warehouse resource)
```

---

## Prerequisites

1. **Databricks CLI** v0.2xx+ (tested on v1.8.0), authenticated to your workspace:
   ```bash
   databricks auth login --profile <PROFILE>
   ```
2. A **Unity Catalog** you can create a schema in.
3. A **SQL warehouse** (serverless is fine — it auto-starts). Note its id from
   *Settings → SQL Warehouses*.
4. Python 3 locally with `databricks-sdk` (`pip install databricks-sdk`) — used by `run_sql.py`.

---

## Deploy to a new workspace

### Option A — one-shot script (recommended)

Edit the five variables at the top of `deploy/deploy.sh`:

```bash
PROFILE="my-workspace"                 # your databricks CLI profile
USER_EMAIL="you@example.com"           # your workspace user
CATALOG="my_catalog"                   # must match 00_config.py
WAREHOUSE_ID="0123456789abcdef"        # your SQL warehouse id
APP_NAME="fleet-ecu-dashboard"
```

Also set the **same** `CATALOG` in `00_config.py` (line ~13) and in `app/app.yaml` (the `CATALOG`
env value). Then:

```bash
bash deploy/deploy.sh
```

The script: imports the project into the workspace → creates the schema → runs the
simulate→prepare pipeline as a one-off job → creates the app with a `sql-warehouse` resource →
deploys the app code → grants the app's service principal read access to the demo schema →
prints the app URL.

### Option B — step by step (what the script does)

Run these in order. `<WS>` = `/Workspace/Users/<you@example.com>/fleet-ecu-demo`.

1. **Set the catalog.** Edit `CATALOG` (and `SCHEMA` if you want) in `00_config.py` and the
   `CATALOG` env in `app/app.yaml` so both match.

2. **Import the project** into the workspace:
   ```bash
   databricks workspace import-dir . <WS> --overwrite -p <PROFILE>
   ```

3. **Run the notebooks in this order** (they use serverless Spark; no cluster to configure):

   | Order | Notebook | What it does |
   |------:|----------|--------------|
   | 1 | `01_simulate_raw` | Creates the schema and the raw `bms_signal` table. |
   | 2 | `02_prepare` | Builds `bms_daily_vin` (left-plot aggregate) and `bms_band`. |
   | 3 | `03_case_notebook` | Optional — the explainer with inline plots. Run interactively. |

   `00_config` is **not run on its own**; `01`/`02`/`03` pull it in via `%run ./00_config`.

   You can run `01`+`02` by hand in the notebook UI, or headless as a job:
   ```bash
   # edit deploy/run_pipeline.json paths to your <WS>, then:
   databricks jobs submit --json @deploy/run_pipeline.json -p <PROFILE>
   ```

4. **Create + deploy the app:**
   ```bash
   # set the warehouse id in deploy/app_create.json, then:
   databricks apps create --json @deploy/app_create.json -p <PROFILE>
   # wait until compute is ACTIVE (databricks apps get fleet-ecu-dashboard -o json)
   databricks apps deploy fleet-ecu-dashboard --source-code-path <WS>/app -p <PROFILE>
   ```

5. **Grant the app read access.** The app runs as its own service principal (get its id from
   `databricks apps get fleet-ecu-dashboard -o json` → `service_principal_client_id`), which needs:
   ```sql
   GRANT USE CATALOG ON CATALOG <catalog> TO `<sp_client_id>`;
   GRANT USE SCHEMA  ON SCHEMA  <catalog>.field_telemetry_demo TO `<sp_client_id>`;
   GRANT SELECT      ON SCHEMA  <catalog>.field_telemetry_demo TO `<sp_client_id>`;
   ```
   (`deploy/run_sql.py <profile> <warehouse_id> "<sql>"` runs these across CLI versions.)

6. **Open the app** at the URL from `databricks apps get fleet-ecu-dashboard -o json` → `url`.

---

## Configuration — everything lives in `00_config.py`

`00_config.py` is the single source of truth. Every other notebook pulls it in via
`%run ./00_config`, so you change a value once and it propagates. It is organized in sections:

**Destination** (edit for a new workspace)
```python
CATALOG = "my_catalog"            # Unity Catalog to build in
SCHEMA  = "field_telemetry_demo"  # schema inside it
CREATE_CATALOG_IF_MISSING = True  # best-effort catalog create (needs CREATE CATALOG on metastore)
```
`00_config` creates the **schema** (always) and attempts the **catalog** (continues gracefully if
you lack the privilege — managed catalogs are usually pre-provisioned).

**Data size** (start small, scale later)
```python
N_CARS  = 20    # vehicles          HZ      = 10    # sample rate (Hz)
N_DAYS  = 3     # days of history    DRIVE_H = 1.0   # hours driven per car per day
```
Default ≈ 2.16 M raw rows. Raise `N_CARS`/`N_DAYS` and **re-run `01_simulate_raw` + `02_prepare`**;
the Spark simulation parallelizes as you scale.

**Scenario** (how the outliers behave)
```python
BAD_CAR_FRAC       = 0.15   # fraction of cars that run hot
HOT_THRESHOLD_C    = 55.0   # hot threshold — shared by 01, 02 AND the App (keep them equal)
HEALTHY_BASELINE_C = 28.0   # normal fleet cell temp
SPIKE_AMPLITUDE_C  = 22.0   # how far outliers rise above healthy — the main "visibility" dial
RANDOM_SEED        = 42     # deterministic fleet; change for a different draw
```

**Aging / granularity**
```python
ODO_START_MIN_KM = 500 ; ODO_START_MAX_KM = 90000   # fleet age spread
ODO_BUCKET_KM    = 2000                              # left-plot aggregate resolution
```

> **Note:** the App (`app/backend/app.py`) keeps its own `HOT_C` constant because it is a separate
> deployed service that cannot import the notebook config. If you change `HOT_THRESHOLD_C`, change
> `HOT_C` to match (it is commented there).

---

## The dashboard — how to use it

Three tabs, each a different way to make an outlier show itself:

| Tab | Left plot | X / Y | Outlier looks like |
|-----|-----------|-------|--------------------|
| **A · Overlaid raw curves** | every car-day's raw temp curve | time-in-trip / temp | a curve that peels up out of the ribbon |
| **B · Raw-sample density** | 2D histogram of all raw samples | state of charge / temp | faint hot cells above the main cloud |
| **C · Phase portrait** | current–temperature loops | pack current / temp | a loop that bulges hot |

Flow: **box-select** (drag a rectangle) over the suspects on the left → the **suspect group**
panel appears with their raw traces + a table → **click a vehicle row** → the **single-vehicle**
panel appears with that car's full-resolution raw scatter (axes match the active tab).

---

## Tables produced

| Table | Grain | Used by |
|-------|-------|---------|
| `bms_signal` | one row per (vin, 10 Hz sample) — the raw fact | brush + single-vehicle drill |
| `bms_daily_vin` | one row per (vin, odometer bucket) — aggregate | overview / left plots |
| `bms_band` | population percentile band per odometer bucket | right-panel overlay |
| `vehicle` | one row per vin (dim) | joins / labels |

The heavy `bms_signal` is only fully scanned on brush, bounded to the VINs inside the box — that
bounded pushdown is the App's speed advantage over an extract-based tool.

---

## Tableau counterpart — NOT built yet

This repo is the Databricks App side. The Tableau build is deferred and documented in
`03_case_notebook` ("Why we build this twice"): the resident Hyper extract, the stacked
`FIXED` LOD expressions the analysis needs, and where Tableau's ~15 s load and its coarse
*aggregated-only* left plot come from — versus the App's full-resolution plots and on-demand raw
drill.

---

## Teardown

```sql
DROP SCHEMA IF EXISTS <catalog>.field_telemetry_demo CASCADE;
```
```bash
databricks apps delete fleet-ecu-dashboard -p <PROFILE>
```
This does not touch the catalog or the warehouse.
