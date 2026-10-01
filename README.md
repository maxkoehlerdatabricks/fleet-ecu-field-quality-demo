# Fleet ECU Field-Quality Demo

An EV **battery field-quality** monitoring demo. It shows why the dangerous signal in fleet
telemetry is never the average. It is the handful of packs that ran hot when they had no reason
to. Finding them requires keeping the **raw** signal rather than rolling it up.

The demo ships:

- **Synthetic raw telemetry** for a fleet of EVs (per-cell temperature, voltage, pack current at
  10 Hz), with a few packs that run hot injected as outliers.
- A **Databricks App** dashboard: a full-resolution raw-sample density plot you box-select, which
  fetches the suspect cars' raw traces + a forensic table, then drills into one vehicle's full raw
  scatter. The app also carries the whole story inline. The physics of a hot cell, why you need
  outlier detection, and what Power BI / Tableau can and cannot replicate.
- A **case notebook** (optional) that walks the story with inline plots.

It runs on **serverless Spark + a SQL warehouse**. **No Asset Bundles. No shell scripts.** Everything
is done by **running notebooks** in order.

---

## The case in one paragraph

A cell that climbs to 70 °C for eight seconds during a fast charge is a thermal event. It is a
precursor to accelerated aging and, at the extreme, thermal runaway. Averaged across a day, a pack,
and a fleet, it vanishes into a healthy-looking mid-thirties number. So you keep every raw sample,
plot the whole fleet, box-select the region where suspects sit, and drill into the raw trace of each
one. That "brush the population, fetch the raw member on demand" loop is what the dashboard
demonstrates. It is what an extract-based BI tool cannot do without pre-summarizing.

---

## Set up the demo

Everything runs by **running notebooks** in the workspace. There are no shell scripts to run.

### Step 1 — Clone the repo into your workspace

In your Databricks workspace: **Workspace → (your folder) → Create → Git folder**, and clone:

```
https://github.com/maxkoehlerdatabricks/fleet-ecu-field-quality-demo
```

(Or clone locally and import with `databricks workspace import-dir . <path>` — but the Git folder is
the simplest path and keeps everything in the workspace.)

### Step 2 — Set your catalog in `00_config.py`

Open `00_config.py` and set `CATALOG` (and `SCHEMA` if you want) to a Unity Catalog you can create a
schema in. That is the only required edit. The size and scenario knobs below it have working
defaults.

> The app reads `CATALOG` / `SCHEMA` from its own `app/app.yaml`. If you change them in `00_config.py`,
> change them in `app/app.yaml` too so the deployed app points at the same tables.

### Step 3 — Run the notebooks, in this order

Open each notebook and **Run all**. All of them use serverless Spark. There is no cluster to
configure.

| Order | Notebook | What it does | Input |
|------:|----------|--------------|-------|
| 1 | **`00_run_all`** | Runs everything below in order (01 → 02 → 04). The one notebook to run. | `WAREHOUSE_ID` widget |
| — | `01_simulate_raw` | Creates the schema + raw `bms_signal` table (healthy fleet + injected outliers). | — |
| — | `02_prepare` | Builds the `bms_daily_vin` aggregate + `bms_band` population band. | — |
| — | `03_case_notebook` | **Optional.** The explainer with inline plots. Run by hand to walk the story. | — |
| — | `04_deploy_app` | Creates + deploys the Databricks App and grants it read access. | `WAREHOUSE_ID` widget |

**The simplest path: just run `00_run_all`.** Set its `WAREHOUSE_ID` widget to your SQL warehouse id
(from **SQL Warehouses**; serverless is fine, it auto-starts), then **Run all**. It runs
`01_simulate_raw`, then `02_prepare`, then `04_deploy_app`, and the `04` output prints the app URL.

If you prefer to run them one at a time instead of `00_run_all`:

1. Run `01_simulate_raw` (Run all).
2. Run `02_prepare` (Run all).
3. Run `04_deploy_app` — set its `WAREHOUSE_ID` widget first, then Run all. It prints the app URL at
   the end.
4. (Optional) Run `03_case_notebook` to see the story with inline plots.

### Step 4 — Open the app

The last cell of `04_deploy_app` prints a clickable app URL. Open it. The dashboard loads the fleet
density plot; expand **"The story"** at the top for the physics and the BI comparison.

---

## Tear the demo down

Run **`99_teardown`** (Run all). It deletes the app and drops the demo schema (all tables). It does
**not** touch the catalog or the warehouse. Safe to re-run.

---

## How the dashboard reads, top to bottom

1. **Header counters** — fleet size: vehicles, raw samples, days, how many are running hot.
2. **The story** (collapsible) — why a hot outlier matters, the three physics diagrams
   (pack → module → cell, healthy vs failing cell, I²R heating), and a table of what Power BI /
   Tableau can and cannot replicate.
3. **Density plot** — a full-resolution 2D histogram of every raw sample (State of Charge × cell
   temperature). The fleet is one dense cloud; outliers are faint hot cells floating above it. This
   is the plot you **box-select**.
4. **Sample-size slider** — how many of the hottest brushed vehicles to pull into the next panel.
5. **Suspect group** — the sampled vehicles' raw temperature-vs-time traces, overlaid, plus a
   forensic table (peak °C, hot-seconds, mileage, min voltage), worst first.
6. **Single-vehicle detail** — the hottest suspect's full raw scatter, drawn automatically; click
   any table row to switch vehicle.

Flow: **box-select** the hot region → suspect group appears → the hottest car is drilled
automatically → click any row to inspect a different one.

---

## Configuration — everything lives in `00_config.py`

`00_config.py` is the single source of truth. Every other notebook pulls it in via
`%run ./00_config`, so you change a value once and it propagates.

**Destination** (edit for a new workspace)
```python
CATALOG = "my_catalog"            # Unity Catalog to build in
SCHEMA  = "field_telemetry_demo"  # schema inside it
```

**Data size** (start small, scale later)
```python
N_CARS  = 200   # vehicles          HZ      = 10    # sample rate (Hz)
N_DAYS  = 3     # days of history    DRIVE_H = 1.0   # hours driven per car per day
```
Default ≈ 21.6 M raw rows. Raise `N_CARS` / `N_DAYS` and re-run `01_simulate_raw` + `02_prepare`;
the Spark simulation parallelizes as you scale.

**Scenario** (how the outliers behave)
```python
BAD_CAR_FRAC       = 0.15   # fraction of cars that run hot
HOT_THRESHOLD_C    = 55.0   # hot threshold — shared by 01, 02 AND the App (keep them equal)
HEALTHY_BASELINE_C = 28.0   # normal fleet cell temp
SPIKE_AMPLITUDE_C  = 22.0   # how far outliers rise above healthy — the main "visibility" dial
RANDOM_SEED        = 42     # deterministic fleet; change for a different draw
```

> **Note:** the App (`app/backend/app.py`) keeps its own `HOT_C` constant because it is a separate
> deployed service that cannot import the notebook config. If you change `HOT_THRESHOLD_C`, change
> `HOT_C` to match (it is commented there).

---

## Tables produced

| Table | Grain | Used by |
|-------|-------|---------|
| `bms_signal` | one row per (vin, 10 Hz sample) — the raw fact | brush + single-vehicle drill |
| `bms_daily_vin` | one row per (vin, odometer bucket) — aggregate | overview counters |
| `bms_band` | population percentile band per odometer bucket | overlay |
| `vehicle` | one row per vin (dim) | joins / labels |

The heavy `bms_signal` is only scanned bounded to the VINs the query needs. That bounded pushdown is
the App's speed advantage over an extract-based tool. `bms_signal` persists the derived `day` and
`t_sec` columns and is liquid-clustered by `(vin, cell_temp_max_c)` so the brush and drill queries
skip straight to the rows they need.

---

## Repository layout

```
00_config.py          # <-- EDIT: CATALOG / SCHEMA + data-size knobs
00_run_all.py         # runs 01 -> 02 -> 04 in order (the one notebook to run)
01_simulate_raw.py    # creates the schema + raw bms_signal table
02_prepare.py         # builds bms_daily_vin + bms_band
03_case_notebook.py   # OPTIONAL explainer with inline plots
04_deploy_app.py      # creates + deploys the Databricks App (SDK, from the notebook)
99_teardown.py        # deletes the app + drops the schema
app/                  # the Databricks App
  app.yaml            #   command + env (CATALOG/SCHEMA, warehouse from a resource)
  requirements.txt
  backend/app.py      #   FastAPI: /api/density /api/brush /api/vehicle /api/band /api/stats
  frontend/index.html #   Plotly UI + the inline story (physics diagrams + BI comparison)
```
