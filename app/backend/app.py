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
    rows = _query(f"""
        WITH s AS (
            SELECT vin, ts, cell_temp_max_c,
                   date(ts) AS day,
                   unix_timestamp(ts) - unix_timestamp(date_trunc('DAY', ts)) - 8*3600 AS t_sec
            FROM {RAW}
        ),
        ds AS (   -- coarse backbone for the overview (raw resolution kept on brush): ~1 pt / 3s
            SELECT vin, day, t_sec, cell_temp_max_c
            FROM s WHERE t_sec % 30 = 0
        ),
        hot AS (
            SELECT vin, date(ts) AS day,
                   round(sum(CASE WHEN cell_temp_max_c > {HOT_C} THEN 0.1 ELSE 0 END),1) AS hot_seconds,
                   round(max(cell_temp_max_c),1) AS peak_c
            FROM {RAW} GROUP BY vin, date(ts)
        )
        SELECT ds.vin, ds.day, ds.t_sec, ds.cell_temp_max_c, h.hot_seconds, h.peak_c
        FROM ds JOIN hot h ON ds.vin=h.vin AND ds.day=h.day
        ORDER BY ds.vin, ds.day, ds.t_sec
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
        WITH s AS (
            SELECT vin, date(ts) AS day, ts, pack_current_a, cell_temp_max_c,
                   row_number() OVER (PARTITION BY vin, date(ts) ORDER BY ts) AS rn
            FROM {RAW}
        ),
        hot AS (
            SELECT vin, date(ts) AS day,
                   round(sum(CASE WHEN cell_temp_max_c > {HOT_C} THEN 0.1 ELSE 0 END),1) AS hot_seconds
            FROM {RAW} GROUP BY vin, date(ts)
        )
        SELECT s.vin, s.day, s.pack_current_a, s.cell_temp_max_c, h.hot_seconds
        FROM s JOIN hot h ON s.vin=h.vin AND s.day=h.day
        WHERE s.rn % 60 = 0
        ORDER BY s.vin, s.day, s.rn
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
            SELECT DISTINCT vin, date(ts) AS day FROM (
                SELECT vin, ts, cell_temp_max_c,
                       unix_timestamp(ts) - unix_timestamp(date_trunc('DAY', ts)) - 8*3600 AS t_sec
                FROM {RAW})
            WHERE t_sec BETWEEN :lx AND :hx AND cell_temp_max_c BETWEEN :ly AND :hy
        """, {"lx": lo_x, "hx": hi_x, "ly": lo_y, "hy": hi_y})
    elif box.view == "phase":
        members = _query(f"""
            SELECT DISTINCT vin, date(ts) AS day FROM {RAW}
            WHERE pack_current_a BETWEEN :lx AND :hx AND cell_temp_max_c BETWEEN :ly AND :hy
        """, {"lx": lo_x, "hx": hi_x, "ly": lo_y, "hy": hi_y})
    else:  # density: box in (SoC, temp)
        members = _query(f"""
            SELECT DISTINCT vin, date(ts) AS day FROM {RAW}
            WHERE soc_pct BETWEEN :lx AND :hx AND cell_temp_max_c BETWEEN :ly AND :hy
        """, {"lx": lo_x, "hx": hi_x, "ly": lo_y, "hy": hi_y})

    pairs = [(m["vin"], str(m["day"])) for m in members][:12]
    if not pairs:
        return JSONResponse({"traces": [], "suspects": []})

    vin_list = ",".join(f"'{v}'" for v, _ in {(v, d) for v, d in pairs})
    # RAW member traces: full resolution around hot events + 1-in-10 backbone
    traces = _query(f"""
        SELECT vin, ts, cell_temp_max_c FROM (
            SELECT vin, ts, cell_temp_max_c,
                   row_number() OVER (PARTITION BY vin ORDER BY ts) AS rn
            FROM {RAW} WHERE vin IN ({vin_list}))
        WHERE cell_temp_max_c >= 48 OR rn % 10 = 0
        ORDER BY vin, ts
    """)
    # suspects table: forensic detail per member vin
    suspects = _query(f"""
        SELECT vin,
               round(max(odometer_km))                                       AS odometer_km,
               round(max(cell_temp_max_c),1)                                 AS peak_temp_c,
               round(sum(CASE WHEN cell_temp_max_c > {HOT_C} THEN 0.1 ELSE 0 END),1) AS hot_seconds,
               round(min(cell_voltage_min_v),3)                              AS min_voltage_v
        FROM {RAW} WHERE vin IN ({vin_list})
        GROUP BY vin ORDER BY hot_seconds DESC
    """)
    return JSONResponse({"traces": _json_safe(traces), "suspects": _json_safe(suspects)})


@app.get("/api/vehicle")
def vehicle(vin: str):
    """Bottom plot: ONE vehicle's RAW samples at full resolution. The frontend picks which
    two columns to plot based on the active view (temp vs time / SoC / pack_current)."""
    rows = _query(f"""
        SELECT ts,
               unix_timestamp(ts) - unix_timestamp(date_trunc('DAY', ts)) - 8*3600 AS t_sec,
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
        WITH s AS (
            SELECT cell_temp_max_c,
                   unix_timestamp(ts) - unix_timestamp(date_trunc('DAY', ts)) - 8*3600 AS t_sec
            FROM {RAW})
        SELECT floor(t_sec/30)*30 AS t_sec,
               round(percentile(cell_temp_max_c,0.5),2)  AS p50,
               round(percentile(cell_temp_max_c,0.95),2) AS p95
        FROM s GROUP BY 1 ORDER BY 1
    """)
    return JSONResponse({"band": _json_safe(rows)})


app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="static")
