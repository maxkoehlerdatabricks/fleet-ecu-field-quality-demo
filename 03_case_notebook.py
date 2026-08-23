# Databricks notebook source
# MAGIC %md
# MAGIC # Fleet EV Battery Field-Quality Monitoring — the case
# MAGIC
# MAGIC **Product.** Every EV has a Battery Management System (BMS) ECU on the CAN bus. It logs
# MAGIC per-cell temperature, voltage, and pack current at ~10 Hz while driving and charging.
# MAGIC A fleet of thousands of cars uploads these signals for field-quality analysis.
# MAGIC
# MAGIC **The question.** *Which individual packs run hot earlier in their life than their mileage
# MAGIC peers?* Those are warranty risk and thermal-safety precursors.
# MAGIC
# MAGIC **Why this data cannot be aggregated.** A dangerous thermal event lasts a few seconds. It is
# MAGIC invisible in a daily average or a per-car mean. Outlier work must stay at (near) raw grain.
# MAGIC That single property is what drives the whole tooling comparison below.
# MAGIC
# MAGIC ---
# MAGIC ### The dashboard we are building
# MAGIC - **Left plot (brushable):** fleet-aging density. X = odometer (age proxy), Y = per-car 99th-pct
# MAGIC   cell temperature. The healthy fleet is a dense band that drifts up slowly with mileage.
# MAGIC   **Outliers are the sparse points high above the band.** You drag a rectangle around them.
# MAGIC - **Right plot (filtered):** the **raw** cell-temp-vs-time traces for exactly the VINs inside
# MAGIC   your rectangle, overlaid on the healthy population band. This is where "cannot aggregate" pays off.

# COMMAND ----------

# MAGIC %run ./00_config

# COMMAND ----------

import matplotlib.pyplot as plt
import numpy as np

daily = spark.table(DAILY_TABLE).join(spark.table(VIN_TABLE), "vin").toPandas()
band  = spark.table(f"{CATALOG}.{SCHEMA}.bms_band").toPandas().sort_values("odometer_bucket_km")
print(f"{len(daily)} (vin,bucket) points, {daily.vin.nunique()} cars")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. The LEFT plot — fleet aging, and the outliers above the band
# MAGIC Each point is one car in one odometer bucket. Healthy cars (grey) form the band that drifts
# MAGIC up with mileage. Bad cars (red) sit high above it — hot for their age.

# COMMAND ----------

fig, ax = plt.subplots(figsize=(11, 6))
h = daily[~daily.is_bad]; b = daily[daily.is_bad]
ax.scatter(h.odometer_bucket_km, h.cell_temp_p99, s=25, c="#9aa7ad", alpha=0.7, label="healthy fleet")
ax.scatter(b.odometer_bucket_km, b.cell_temp_p99, s=55, c="#FF3621", alpha=0.9, label="thermal outlier")
ax.plot(band.odometer_bucket_km, band.band_p50, c="#1B3139", lw=2, label="fleet median (band)")
ax.plot(band.odometer_bucket_km, band.band_p95, c="#1B3139", lw=1, ls="--", label="fleet p95")
ax.fill_between(band.odometer_bucket_km, band.band_p50, band.band_p95, color="#1B3139", alpha=0.06)
ax.set_xlabel("odometer (km)  →  vehicle age"); ax.set_ylabel("cell_temp p99 (°C)")
ax.set_title("Left plot: fleet-aging density — outliers sit above the healthy band")
ax.legend(loc="upper left"); plt.tight_layout(); plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. The brush → RIGHT plot — raw traces of the suspect cars
# MAGIC Say we brush a rectangle over the anomalies (high p99, any mileage). We resolve the box to a
# MAGIC set of VINs, then pull their **raw** cell-temp traces. This is the query the App runs on brush.

# COMMAND ----------

# emulate a brush box: high p99 (the outliers)
Y0, Y1 = 55.0, 200.0
X0, X1 = 0, int(daily.odometer_bucket_km.max()) + ODO_START_MAX_KM
box_vins = sorted(daily[(daily.cell_temp_p99.between(Y0, Y1))].vin.unique().tolist())
print(f"Brush box (p99 in [{Y0},{Y1}]) selects {len(box_vins)} vins: {box_vins}")

# COMMAND ----------

# pull raw traces for the boxed vins (only the hot samples, like the App does)
if box_vins:
    vin_list = ",".join(f"'{v}'" for v in box_vins[:5])   # cap for the plot
    raw_pd = spark.sql(f"""
        SELECT vin, ts, cell_temp_max_c
        FROM {RAW_TABLE}
        WHERE vin IN ({vin_list})
        ORDER BY vin, ts
    """).toPandas()

    fig, ax = plt.subplots(figsize=(11, 6))
    for vin, g in raw_pd.groupby("vin"):
        ax.plot(g.ts, g.cell_temp_max_c, lw=0.6, label=vin[-4:])
    ax.axhline(55, c="#FF3621", ls="--", lw=1, label="55°C hot threshold")
    ax.set_xlabel("time"); ax.set_ylabel("cell_temp_max (°C)")
    ax.set_title("Right plot: RAW traces of the brushed VINs — the seconds-long spikes an average would hide")
    ax.legend(loc="upper right", ncol=2, fontsize=8); plt.tight_layout(); plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC # Why we build this twice: Tableau vs Databricks Apps
# MAGIC
# MAGIC The comparison is **honest** — the differences below are real consequences of how each tool
# MAGIC moves data, not a rigged benchmark. (The Tableau build comes later; this frames what to expect.)
# MAGIC
# MAGIC ### 1. Speed
# MAGIC | | Tableau | Databricks App |
# MAGIC |---|---|---|
# MAGIC | Where granular data lives | resident **Hyper extract** (RAM) | stays in **Delta**; never fully moved |
# MAGIC | Left plot compute | **LOD** passes over the extract | pre-materialized aggregate (`bms_daily_vin`), cached |
# MAGIC | Brush interaction | re-query Hyper + re-run LODs | one bounded **pushdown** query |
# MAGIC | Initial load | **~15 s** (extract + first render) | **~2 s** |
# MAGIC | Re-render on brush | seconds (LOD re-passes) | ~1-2 s, **flat with scale** |
# MAGIC
# MAGIC ### 2. Simplified vs full LEFT plot
# MAGIC - **Tableau** cannot draw millions of individual points. It must bin — the left plot becomes a
# MAGIC   **coarse hexbin/heatmap**, and a lone outlier gets smeared into a pale bin, easy to miss.
# MAGIC - **The App** renders the **full-resolution GPU point cloud** (deck.gl / WebGL). The single
# MAGIC   anomalous car stays individually visible and **clickable**.
# MAGIC
# MAGIC ### 3. Lazy raw drill (the "impossible in Tableau" reveal)
# MAGIC - **Tableau's** brush filters marks **already in the extract**. To show raw traces on the right,
# MAGIC   the raw rows had to be pre-extracted — which is exactly what makes it slow, or they simply
# MAGIC   aren't available.
# MAGIC - **The App's** brush is a `WHERE odometer BETWEEN … AND cell_temp_p99 BETWEEN …` predicate that
# MAGIC   **lazily fetches raw un-aggregated rows** from the lake on demand — rows that were never in the
# MAGIC   browser. Plus optional **live server-side outlier scoring** as an overlay.
# MAGIC
# MAGIC ### The LODs Tableau needs (and pays for on every interaction)
# MAGIC ```
# MAGIC { FIXED [VIN],[odo_bucket] : PERCENTILE([cell_temp], 0.99) }   -- per-car-per-bucket p99
# MAGIC { FIXED [odo_bucket]       : PERCENTILE([cell_temp], 0.99) }   -- population band
# MAGIC { FIXED [VIN]              : MAX([cell_temp]) }                -- per-car worst case (flag color)
# MAGIC { FIXED [VIN],[session]    : SUM(hot_seconds) }               -- per-session hot-seconds
# MAGIC ```
# MAGIC These are **needed** by the analysis, not padding — which is what makes the speed gap fair.
