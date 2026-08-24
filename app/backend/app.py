"""Fleet ECU dashboard — Databricks App backend.

Serves THREE candidate left-plot visualizations (switchable in the UI), each of which is
"full-resolution in Apps, only-aggregated in Tableau", plus a shared right-hand detail panel.

Left-plot data endpoints (all read from the small aggregate or a downsampled raw slice; the
huge raw table is only fully touched on brush, bounded to the VINs inside the box):

  GET  /api/curves      -> View A: overlaid raw cell-temp curves (one per vin/day), x = sec into trip.
                           Tableau can only draw an aggregated percentile band, never the raw curves.
  GET  /api/density     -> View B: server-binned 2D density of RAW samples (SoC x cell-temp), log counts.
                           Tableau's hexbin is coarse/pre-aggregated and smears lone outliers away.
  GET  /api/phase       -> View C: per-cycle phase-portrait trajectories (pack_current x cell-temp).
                           Thousands of raw loops -- impossible in Tableau's mark model.

  POST /api/brush       -> shared right panel: given the active view + a rectangle, resolve the member
                           VINs and LAZILY FETCH their raw traces + a suspects table. The pushdown an
                           extract-based tool cannot do on demand.
"""
import os
from pathlib import Path
from functools import lru_cache
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from databricks import sql
from databricks.sdk.core import Config

CATALOG = os.getenv("CATALOG", "serverless_stable_7qzrfp_catalog")
SCHEMA  = os.getenv("SCHEMA", "field_telemetry_demo")
RAW     = f"{CATALOG}.{SCHEMA}.bms_signal"
DAILY   = f"{CATALOG}.{SCHEMA}.bms_daily_vin"
BAND    = f"{CATALOG}.{SCHEMA}.bms_band"
VEH     = f"{CATALOG}.{SCHEMA}.vehicle"
HOT_C   = 55.0   # hot threshold (deg C). MUST match HOT_THRESHOLD_C in 00_config.py
                 # (the App is a separate deployed service and can't import the notebook config).

# Overview curve/phase plots overlay one line per car-day. Past a few dozen cars that is both
# unreadable and too many points for the browser, so we cap how many cars the OVERVIEW samples.
# We ALWAYS keep the hot cars (the story) and fill the rest with a deterministic hash sample of
# healthy cars so the ribbon still looks dense. The brush + single-vehicle drill always hit the
# full raw table, so nothing is hidden -- only the overview backbone is subsampled.
OVERVIEW_MAX_CARS = int(os.getenv("OVERVIEW_MAX_CARS", "40"))

_wh = (os.getenv("DATABRICKS_WAREHOUSE_HTTP_PATH") or os.getenv("SQL_HTTP_PATH")
       or os.getenv("WAREHOUSE_ID", ""))
WAREHOUSE_HTTP_PATH = _wh if _wh.startswith("/sql/") else f"/sql/1.0/warehouses/{_wh}"
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

app = FastAPI(title="Fleet ECU Dashboard")


def _connect():
    cfg = Config()
    return sql.connect(
        server_hostname=cfg.host.replace("https://", ""),
        http_path=WAREHOUSE_HTTP_PATH,
        credentials_provider=lambda: cfg.authenticate,
    )


def _query(q, params=None):
    with _connect() as conn, conn.cursor() as cur:
        cur.execute(q, params or {})
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]


def _json_safe(rows):
    out = []
    for r in rows:
        d = {}
        for k, v in r.items():
            if hasattr(v, "isoformat"):
                d[k] = v.isoformat()
            elif hasattr(v, "__float__") and not isinstance(v, (int, float, bool)):
                d[k] = float(v)
            else:
                d[k] = v
        out.append(d)
    return out


# ---------------------------------------------------------------------------
# A "trace" (curve) identity is (vin, day). We compute seconds-into-trip from ts.
# hot_seconds per trace = samples above HOT_C / sample-rate; drives the color.
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _curves_cached():
    """View A: overlaid raw cell-temp curves, downsampled to ~1 pt/sec for the fleet overview."""
    # Per-vin hot summary comes from the small bms_daily_vin aggregate (200 rows), NOT a raw scan.
    # We only touch the raw table for the actual backbone points of the selected cars.
    rows = _query(f"""
        WITH vhot AS (   -- per-vin hot summary from the pre-built aggregate
            SELECT vin, round(sum(hot_seconds),1) AS hot_seconds, round(max(cell_temp_max),1) AS peak_c
            FROM {DAILY} GROUP BY vin
        ),
        shown AS (       -- always keep hot cars; fill up to OVERVIEW_MAX_CARS with a hash sample
            SELECT vin, hot_seconds, peak_c FROM vhot
            WHERE hot_seconds > 0
               OR pmod(abs(hash(vin)), (SELECT count(*) FROM vhot)) < {OVERVIEW_MAX_CARS}
        )
        SELECT r.vin, r.day, r.t_sec, r.cell_temp_max_c, s.hot_seconds, s.peak_c
        FROM {RAW} r JOIN shown s ON r.vin = s.vin
        WHERE r.t_sec % 30 = 0
        ORDER BY r.vin, r.day, r.t_sec
    """)
    return _json_safe(rows)


@app.get("/api/curves")
def curves():
    return JSONResponse({"curves": _curves_cached(), "hot_c": HOT_C})


@lru_cache(maxsize=1)
def _density_cached():
    """View B: server-side 2D histogram of RAW samples over (SoC bucket, temp bucket)."""
    rows = _query(f"""
        SELECT
            floor(soc_pct/2)*2                AS soc_bin,
            floor(cell_temp_max_c/1)*1        AS temp_bin,
            count(*)                          AS n,
            round(log10(count(*)),3)          AS log_n
        FROM {RAW}
        GROUP BY 1,2
        ORDER BY 1,2
    """)
    return _json_safe(rows)


@app.get("/api/density")
def density():
    return JSONResponse({"cells": _density_cached(), "hot_c": HOT_C})


@lru_cache(maxsize=1)
def _phase_cached():
    """View C: phase-portrait trajectories, pack_current vs cell_temp, per (vin, day), downsampled."""
    rows = _query(f"""
        WITH vhot AS (
            SELECT vin, round(sum(hot_seconds),1) AS hot_seconds FROM {DAILY} GROUP BY vin
        ),
        shown AS (       -- same fleet subsample as the curves overview
            SELECT vin, hot_seconds FROM vhot
            WHERE hot_seconds > 0
               OR pmod(abs(hash(vin)), (SELECT count(*) FROM vhot)) < {OVERVIEW_MAX_CARS}
        )
        SELECT r.vin, r.day, r.pack_current_a, r.cell_temp_max_c, s.hot_seconds
        FROM {RAW} r JOIN shown s ON r.vin = s.vin
        WHERE r.t_sec % 30 = 0
        ORDER BY r.vin, r.day, r.t_sec
    """)
    return _json_safe(rows)


@app.get("/api/phase")
def phase():
    return JSONResponse({"points": _phase_cached(), "hot_c": HOT_C})


# ---------------------------------------------------------------------------
# Brush: the rectangle is in the active view's coordinate space. We resolve which
# (vin, day) member traces pass through the box, then fetch their RAW detail.
# ---------------------------------------------------------------------------

class Box(BaseModel):
    view: str            # 'curves' | 'density' | 'phase'
    x0: float; x1: float; y0: float; y1: float


@app.post("/api/brush")
def brush(box: Box):
    lo_x, hi_x = min(box.x0, box.x1), max(box.x0, box.x1)
    lo_y, hi_y = min(box.y0, box.y1), max(box.y0, box.y1)

    if box.view == "curves":
        # member = any (vin,day) with a raw sample inside (t_sec in [x], temp in [y])
        members = _query(f"""
            SELECT DISTINCT vin, day FROM {RAW}
            WHERE t_sec BETWEEN :lx AND :hx AND cell_temp_max_c BETWEEN :ly AND :hy
        """, {"lx": lo_x, "hx": hi_x, "ly": lo_y, "hy": hi_y})
    elif box.view == "phase":
        members = _query(f"""
            SELECT DISTINCT vin, day FROM {RAW}
            WHERE pack_current_a BETWEEN :lx AND :hx AND cell_temp_max_c BETWEEN :ly AND :hy
        """, {"lx": lo_x, "hx": hi_x, "ly": lo_y, "hy": hi_y})
    else:  # density: box in (SoC, temp)
        members = _query(f"""
            SELECT DISTINCT vin, day FROM {RAW}
            WHERE soc_pct BETWEEN :lx AND :hx AND cell_temp_max_c BETWEEN :ly AND :hy
        """, {"lx": lo_x, "hx": hi_x, "ly": lo_y, "hy": hi_y})

    # Cap the number of member vins whose RAW traces we ship (keeps the browser + payload sane
    # no matter how wide the brush is). The suspects table below still summarizes ALL members.
    uniq_vins = list({m["vin"] for m in members})[:6]
    if not uniq_vins:
        return JSONResponse({"traces": [], "suspects": [], "n_members": 0})

    vin_list = ",".join(f"'{v}'" for v in uniq_vins)
    # RAW member traces: keep FULL resolution around the hot events (>=48C, the diagnostic part)
    # plus a sparse 1-in-20 backbone so the baseline line stays continuous. Still raw rows.
    traces = _query(f"""
        SELECT vin, ts, cell_temp_max_c FROM (
            SELECT vin, ts, cell_temp_max_c, t_sec
            FROM {RAW} WHERE vin IN ({vin_list}))
        WHERE cell_temp_max_c >= 48 OR t_sec % 20 = 0
        ORDER BY vin, ts
    """)
    # suspects table: forensic detail for ALL brushed members (capped at 40 rows for the table),
    # worst-first. This summarizes the whole selection, not just the vins we drew traces for.
    all_vins = list({m["vin"] for m in members})[:40]
    all_list = ",".join(f"'{v}'" for v in all_vins)
    suspects = _query(f"""
        SELECT vin,
               round(max(odometer_km))                                       AS odometer_km,
               round(max(cell_temp_max_c),1)                                 AS peak_temp_c,
               round(sum(CASE WHEN cell_temp_max_c > {HOT_C} THEN 0.1 ELSE 0 END),1) AS hot_seconds,
               round(min(cell_voltage_min_v),3)                              AS min_voltage_v
        FROM {RAW} WHERE vin IN ({all_list})
        GROUP BY vin ORDER BY hot_seconds DESC
    """)
    return JSONResponse({"traces": _json_safe(traces), "suspects": _json_safe(suspects),
                         "n_members": len({m["vin"] for m in members}), "n_traced": len(uniq_vins)})


@app.get("/api/vehicle")
def vehicle(vin: str):
    """Bottom plot: ONE vehicle's RAW samples at full resolution. The frontend picks which
    two columns to plot based on the active view (temp vs time / SoC / pack_current)."""
    rows = _query(f"""
        SELECT ts, t_sec,
               soc_pct, pack_current_a, cell_temp_max_c, cell_voltage_min_v, event_type
        FROM {RAW}
        WHERE vin = :vin
        ORDER BY ts
    """, {"vin": vin})
    return JSONResponse({"vin": vin, "samples": _json_safe(rows), "hot_c": HOT_C})


@app.get("/api/band")
def band():
    """Population percentile band for the right-panel overlay (aggregated -- what Tableau is limited to)."""
    rows = _query(f"""
        SELECT floor(t_sec/30)*30 AS t_sec,
               round(percentile(cell_temp_max_c,0.5),2)  AS p50,
               round(percentile(cell_temp_max_c,0.95),2) AS p95
        FROM {RAW} GROUP BY 1 ORDER BY 1
    """)
    return JSONResponse({"band": _json_safe(rows)})


app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="static")
