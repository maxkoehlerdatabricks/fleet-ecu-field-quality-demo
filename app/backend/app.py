"""Fleet ECU dashboard — Databricks App backend.

The single left-plot visualization is the raw-sample density plot; brushing it drives a shared
right-hand detail panel and a single-vehicle drill.

  GET  /api/density     -> server-binned 2D density of RAW samples (SoC x cell-temp), log counts.
                           Tableau's hexbin is coarse/pre-aggregated and smears lone outliers away;
                           this is the full-resolution histogram.
  POST /api/brush       -> right panel: given a rectangle in (SoC, temp), resolve the member VINs
                           and LAZILY FETCH their raw traces + a suspects table. The pushdown an
                           extract-based tool cannot do on demand.
  GET  /api/vehicle     -> bottom panel: one vehicle's raw samples at full resolution.
  GET  /api/stats       -> live fleet size for the header.
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
    """Run a query, return rows. (Data path — bytes-scanned is captured separately by _query_m.)"""
    with _connect() as conn, conn.cursor() as cur:
        cur.execute(q, params or {})
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]


def _read_bytes(cur):
    """Best-effort: pull bytes-scanned from the connector's query metrics. Returns None if this
    connector version doesn't expose it (the frontend then just omits the 'scanned' figure)."""
    try:
        m = cur.query_metrics() if hasattr(cur, "query_metrics") else None
        if m is None and hasattr(cur, "active_result_set"):
            m = getattr(cur.active_result_set, "query_metrics", None)
        if isinstance(m, dict):
            return m.get("read_bytes") or m.get("bytesRead") or m.get("read_bytes_total")
    except Exception:
        pass
    return None


def _query_m(q, params=None):
    """Like _query but also returns best-effort bytes-scanned: (rows, read_bytes|None)."""
    with _connect() as conn, conn.cursor() as cur:
        cur.execute(q, params or {})
        cols = [c[0] for c in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]
        return rows, _read_bytes(cur)


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
def _stats_cached():
    """Fleet size shown in the header. Reads live from the tables so it is always correct
    for whatever N_CARS the data was built with."""
    r = _query(f"""
        SELECT (SELECT count(*)           FROM {RAW})  AS raw_rows,
               (SELECT count(DISTINCT vin) FROM {RAW})  AS n_cars,
               (SELECT count(DISTINCT day) FROM {RAW})  AS n_days,
               (SELECT count(DISTINCT vin) FROM {DAILY}
                WHERE hot_seconds > 0)                  AS n_hot
    """)[0]
    return r


@app.get("/api/stats")
def stats():
    return JSONResponse(_json_safe([_stats_cached()])[0])


@lru_cache(maxsize=1)
def _density_cached():
    """View B: server-side 2D histogram of RAW samples over (SoC bucket, temp bucket)."""
    rows, rb = _query_m(f"""
        SELECT
            floor(soc_pct/2)*2                AS soc_bin,
            floor(cell_temp_max_c/1)*1        AS temp_bin,
            count(*)                          AS n,
            round(log10(count(*)),3)          AS log_n
        FROM {RAW}
        GROUP BY 1,2
        ORDER BY 1,2
    """)
    return {"rows": _json_safe(rows), "scanned_bytes": rb}


@app.get("/api/density")
def density():
    c = _density_cached()
    return JSONResponse({"cells": c["rows"], "scanned_bytes": c["scanned_bytes"], "hot_c": HOT_C})


# ---------------------------------------------------------------------------
# Brush: the rectangle is in the active view's coordinate space. We resolve which
# (vin, day) member traces pass through the box, then fetch their RAW detail.
# ---------------------------------------------------------------------------

class Box(BaseModel):
    x0: float; x1: float; y0: float; y1: float   # rectangle in (State of Charge, cell temp)
    sample_size: int = 30                        # max vehicles to bring into the middle panel


@app.post("/api/brush")
def brush(box: Box):
    lo_x, hi_x = min(box.x0, box.x1), max(box.x0, box.x1)
    lo_y, hi_y = min(box.y0, box.y1), max(box.y0, box.y1)
    n = max(1, min(int(box.sample_size), 200))   # clamp the user-chosen sample size

    # Density brush: the box is in (SoC, temp). Count all vins with a sample inside it, then take
    # the SAMPLE-SIZE hottest of them (peak temp) so the selection is meaningful, not arbitrary.
    n_members_row = _query(f"""
        SELECT count(DISTINCT vin) AS n FROM {RAW}
        WHERE soc_pct BETWEEN :lx AND :hx AND cell_temp_max_c BETWEEN :ly AND :hy
    """, {"lx": lo_x, "hx": hi_x, "ly": lo_y, "hy": hi_y})
    n_members = n_members_row[0]["n"]
    if not n_members:
        return JSONResponse({"traces": [], "suspects": [], "n_members": 0, "n_sampled": 0})

    sampled = _query(f"""
        SELECT vin FROM (
            SELECT vin, max(cell_temp_max_c) AS pk FROM {RAW}
            WHERE soc_pct BETWEEN :lx AND :hx AND cell_temp_max_c BETWEEN :ly AND :hy
            GROUP BY vin ORDER BY pk DESC LIMIT {n})
    """, {"lx": lo_x, "hx": hi_x, "ly": lo_y, "hy": hi_y})
    sampled_vins = [r["vin"] for r in sampled]
    all_list = ",".join(f"'{v}'" for v in sampled_vins)

    # RAW traces: keep FULL resolution around the hot events (>=48C, the diagnostic part) plus a
    # sparse 1-in-20 backbone. To protect the browser we draw traces for at most the 8 hottest of
    # the sampled cars; the suspects table below summarizes ALL sampled cars.
    trace_vins = sampled_vins[:8]
    trace_list = ",".join(f"'{v}'" for v in trace_vins)
    traces, rb = _query_m(f"""
        SELECT vin, ts, cell_temp_max_c FROM (
            SELECT vin, ts, cell_temp_max_c, t_sec
            FROM {RAW} WHERE vin IN ({trace_list}))
        WHERE cell_temp_max_c >= 48 OR t_sec % 20 = 0
        ORDER BY vin, ts
    """)
    suspects = _query(f"""
        SELECT vin,
               round(max(odometer_km))                                       AS odometer_km,
               round(max(cell_temp_max_c),1)                                 AS peak_temp_c,
               round(sum(CASE WHEN cell_temp_max_c > {HOT_C} THEN 0.1 ELSE 0 END),1) AS hot_seconds,
               round(min(cell_voltage_min_v),3)                              AS min_voltage_v
        FROM {RAW} WHERE vin IN ({all_list})
        GROUP BY vin ORDER BY hot_seconds DESC, peak_temp_c DESC
    """)
    return JSONResponse({"traces": _json_safe(traces), "suspects": _json_safe(suspects),
                         "n_members": n_members, "n_sampled": len(sampled_vins),
                         "n_traced": len(trace_vins), "scanned_bytes": rb})


@app.get("/api/vehicle")
def vehicle(vin: str):
    """Bottom plot: ONE vehicle's RAW samples at full resolution. The frontend picks which
    two columns to plot based on the active view (temp vs time / SoC / pack_current)."""
    rows, rb = _query_m(f"""
        SELECT ts, t_sec,
               soc_pct, pack_current_a, cell_temp_max_c, cell_voltage_min_v, event_type
        FROM {RAW}
        WHERE vin = :vin
        ORDER BY ts
    """, {"vin": vin})
    return JSONResponse({"vin": vin, "samples": _json_safe(rows), "scanned_bytes": rb, "hot_c": HOT_C})


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
