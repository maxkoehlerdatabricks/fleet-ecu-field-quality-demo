# -*- coding: utf-8 -*-
wf_css = open("/tmp/wf_css.txt", encoding="utf-8").read()
story_css = open("/tmp/story_css.txt", encoding="utf-8").read()
drawings = open("/tmp/drawings.html", encoding="utf-8").read()  # DRAWING 1..3 inside a .draw block sequence

tab_css = """
/* --- doc tabs --- */
.doctabs{position:sticky;top:0;z-index:20;display:flex;gap:0;justify-content:center;
  background:var(--ground);border-bottom:1px solid var(--line);flex-wrap:wrap}
.doctab{font-family:"IBM Plex Mono",monospace;font-size:13px;letter-spacing:.03em;
  padding:14px 22px;cursor:pointer;color:var(--slate);background:none;border:none;
  border-bottom:2px solid transparent}
.doctab:hover{color:var(--ink)}
.doctab.active{color:var(--ink);border-bottom-color:var(--hot);font-weight:600}
.doctab .idx{color:var(--hot);margin-right:7px;font-weight:600}
.panel-doc{display:none}
.panel-doc.active{display:block}
/* app-layout mock (top-to-bottom of the real screen) */
.applayout{display:flex;flex-direction:column;gap:10px;margin:22px 0 6px}
.applayout .lyr{background:var(--panel);border:1px solid var(--line);border-radius:10px;
  padding:14px 16px;box-shadow:var(--shadow);position:relative}
.applayout .lyr .tag2{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--cool);
  letter-spacing:.04em}
.applayout .lyr h4{font-family:"Inter Tight",sans-serif;font-size:15px;margin:3px 0 4px}
.applayout .lyr p{font-size:14px;color:var(--ink-soft);margin:0;max-width:none}
.applayout .down{align-self:center;color:var(--hot);font-family:"IBM Plex Mono",monospace;
  font-size:12px;margin:-4px 0}
.applayout .pillrow{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}
.applayout .pillrow span{font-size:10.5px;font-family:"IBM Plex Mono",monospace;
  background:color-mix(in srgb,var(--ground) 60%,var(--panel));border:1px solid var(--line);
  border-radius:10px;padding:2px 8px;color:var(--slate)}
.applayout .lyr.ctrl{border-left:3px solid var(--cool)}
.slidermock{display:flex;align-items:center;gap:12px;margin-top:10px;font-family:"IBM Plex Mono",monospace;font-size:12px}
.slidermock .lab{color:var(--slate)}
.slidermock .track{position:relative;flex:1;max-width:260px;height:6px;border-radius:3px;
  background:var(--line)}
.slidermock .fill{position:absolute;left:0;top:0;bottom:0;width:30%;border-radius:3px;background:var(--cool)}
.slidermock .knob{position:absolute;left:30%;top:50%;transform:translate(-50%,-50%);
  width:14px;height:14px;border-radius:50%;background:var(--cool);border:2px solid var(--panel)}
.slidermock .val{font-weight:600;color:var(--cool);min-width:2ch;text-align:right}
.verdict{background:color-mix(in srgb,var(--ok) 9%,var(--panel));
  border:1px solid color-mix(in srgb,var(--ok) 30%,var(--line));border-radius:12px;
  padding:20px 24px;margin:26px 0;font-size:17px}
.verdict b{color:var(--ok)}
.reasons{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin:24px 0 6px}
.reasons .rz{background:var(--panel);border:1px solid var(--line);border-radius:12px;
  padding:18px 20px;box-shadow:var(--shadow);border-left:3px solid var(--ok)}
.reasons .rz h4{font-family:"Inter Tight",sans-serif;font-size:15.5px;margin:0 0 6px}
.reasons .rz p{font-size:14.5px;color:var(--ink-soft);margin:0}
@media(max-width:600px){.reasons{grid-template-columns:1fr}}
.define{background:color-mix(in srgb,var(--cool) 7%,var(--panel));
  border:1px solid color-mix(in srgb,var(--cool) 26%,var(--line));border-radius:12px;
  padding:16px 20px;margin:20px 0}
.define p{font-size:14.5px;color:var(--ink);margin:0 0 8px;max-width:none}
.define p:last-child{margin-bottom:0}
.define ul{margin:6px 0 10px;padding-left:20px}
.define li{font-size:14px;color:var(--ink-soft);margin:3px 0}
.define b{color:var(--ink)}
.modes{margin:16px 0 6px}
.modes table{width:100%;border-collapse:collapse;font-size:13.5px;border:1px solid var(--line);border-radius:10px;overflow:hidden}
.modes th{text-align:left;font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.03em;
  text-transform:uppercase;color:var(--slate);font-weight:600;padding:10px 12px;
  background:color-mix(in srgb,var(--ground) 55%,var(--panel));border-bottom:1px solid var(--line);vertical-align:bottom}
.modes td{padding:9px 12px;border-bottom:1px solid var(--line);color:var(--ink-soft);vertical-align:top;
  font-size:12.5px;line-height:1.45}
.modes td.tl{font-weight:600;color:var(--ink);white-space:nowrap;vertical-align:top;
  border-right:1px solid var(--line);font-size:13.5px}
.modes tr:last-child td{border-bottom:none}
.modes tr.tool-top td{border-top:2px solid var(--line)}
.modes td b{color:var(--ink)}
/* axis label cell (leading colored tag) */
.modes td.ax{white-space:nowrap;border-right:1px solid var(--line);vertical-align:top}
.modes .tag{display:inline-block;font-family:"IBM Plex Mono",monospace;font-size:9.5px;
  letter-spacing:.06em;text-transform:uppercase;font-weight:600;padding:2px 7px;border-radius:5px}
.modes tr.scale .tag{background:color-mix(in srgb,var(--hot) 16%,transparent);color:var(--hot)}
.modes tr.fidel .tag{background:color-mix(in srgb,var(--warm) 18%,transparent);color:var(--warm)}
.modes tr.flow .tag{background:color-mix(in srgb,var(--cool) 16%,transparent);color:var(--cool)}
.modes tr.act .tag{background:color-mix(in srgb,var(--viol) 18%,transparent);color:var(--viol)}
.modes tr.layer .tag{background:color-mix(in srgb,var(--ok) 16%,transparent);color:var(--ok)}
.modes tr.maint .tag{background:color-mix(in srgb,var(--rose) 16%,transparent);color:var(--rose)}
.modes tr.cost .tag{background:color-mix(in srgb,var(--slate) 20%,transparent);color:var(--slate)}
.modes tr.talk .tag{background:color-mix(in srgb,var(--teal) 16%,transparent);color:var(--teal)}
.modes tr.sem .tag{background:color-mix(in srgb,var(--gold) 18%,transparent);color:var(--gold)}
/* faint left accent bar per axis, on the axis cell */
.modes td.ax{position:relative}
.modes td.ax::before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px}
.modes tr.scale td.ax::before{background:var(--hot)}
.modes tr.fidel td.ax::before{background:var(--warm)}
.modes tr.flow td.ax::before{background:var(--cool)}
.modes tr.act td.ax::before{background:var(--viol)}
.modes tr.layer td.ax::before{background:var(--ok)}
.modes tr.maint td.ax::before{background:var(--rose)}
.modes tr.cost td.ax::before{background:var(--slate)}
.modes tr.talk td.ax::before{background:var(--teal)}
.modes tr.sem td.ax::before{background:var(--gold)}
/* both-mode rows get a subtle tint so the span reads as "either mode" */
.modes tr.flow td.span,.modes tr.act td.span,.modes tr.layer td.span,
.modes tr.maint td.span,.modes tr.cost td.span,
.modes tr.talk td.span,.modes tr.sem td.span{
  background:color-mix(in srgb,var(--ground) 45%,var(--panel))}
.modes td.span .lead{color:var(--ink);font-weight:600}
.modes td.mono{font-family:"IBM Plex Mono",monospace;font-size:11px;color:var(--slate)}
.scale-inline{color:var(--hot);font-weight:600}
.fidel-inline{color:var(--warm);font-weight:600}
.flow-inline{color:var(--cool);font-weight:600}
.act-inline{color:var(--viol);font-weight:600}
.layer-inline{color:var(--ok);font-weight:600}
.modes-note{font-size:13.5px;color:var(--ink-soft);margin:12px 2px 0}
.modes-note b{color:var(--ink)}
.field{background:color-mix(in srgb,var(--warm) 10%,var(--panel));
  border:1px solid color-mix(in srgb,var(--warm) 35%,var(--line));border-radius:12px;
  padding:16px 20px;margin:22px 0}
.field .fl{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.08em;
  text-transform:uppercase;color:var(--warm);font-weight:600;margin-bottom:6px}
.field p{font-size:14.5px;color:var(--ink-soft);margin:0 0 8px;max-width:none}
.field p:last-child{margin-bottom:0}
.field ol{margin:0 0 8px;padding-left:22px}
.field li{font-size:14.5px;color:var(--ink-soft);margin:2px 0}
.field b{color:var(--ink)}
.drawfig{margin:22px 0 6px}
.drawfig svg{width:100%;height:auto;display:block;border-radius:12px;
  background:color-mix(in srgb,var(--ground) 55%,var(--panel));border:1px solid var(--line);padding:8px}
.drawfig figcaption{font-size:13px;color:var(--slate);margin-top:10px;max-width:65ch}
"""

merged_css = wf_css + "\n" + story_css + "\n" + tab_css

head = ('<title>Fleet EV Battery — Field-Quality Monitor</title>\n'
'<link rel="preconnect" href="https://fonts.googleapis.com">\n'
'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter+Tight:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">\n'
'<style>' + merged_css + '</style>\n')

tabs = ('<div class="doctabs">\n'
'  <button class="doctab active" data-tab="why"><span class="idx">1</span>Why Databricks Apps</button>\n'
'  <button class="doctab" data-tab="story"><span class="idx">2</span>Example: Outlier Detection for EV Batteries</button>\n'
'  <button class="doctab" data-tab="workflow"><span class="idx">3</span>App Workflow</button>\n'
'  <button class="doctab" data-tab="tools"><span class="idx">4</span>Tool Comparison</button>\n'
'</div>\n')

# ---------------- TAB 1: flowing narrative ----------------
tab_why = '''<div class="panel-doc active" id="tab-why">
<header>
  <div class="hero">
    <div class="eyebrow">Databricks demo · visualizing massive data</div>
    <h1>Why Databricks Apps</h1>
    <p class="lede">For interactive visualization of <strong>massive data</strong>, a Databricks App
      does what classic BI tools like Power BI, Tableau and Qlik cannot. The example here is a fleet
      of EV batteries — the point is general.</p>
  </div>
</header>

<div class="wrap">

<section>
  <div class="eyebrow">The reasons</div>
  <h2>Five reasons it’s a Databricks App</h2>
  <div class="reasons">
    <div class="rz"><h4>Full fidelity</h4>
      <p>BI charts cap at a few thousand marks and sample the rest, so rare outliers vanish. The App
        renders every raw sample as a full-resolution picture.</p></div>
    <div class="rz"><h4>Scales with the fleet</h4>
      <p>Add more vehicles and a BI extract keeps growing until loads and refreshes stall. The App
        queries bounded slices in the lakehouse, so response time stays flat as the fleet grows.</p></div>
    <div class="rz"><h4>One platform to maintain</h4>
      <p>A separate BI tool is another system to license, secure, refresh and govern beside the
        lakehouse. The App runs on the data platform you already have — one place, one copy, one story.</p></div>
    <div class="rz"><h4>Licensing you can save</h4>
      <p>Per-seat BI licenses recur for every viewer. A Databricks App serves users on compute you
        already run, avoiding a separate dashboarding subscription.</p></div>
    <div class="rz"><h4>Interaction BI can’t do</h4>
      <p>It’s a real app: a lasso that triggers a server-side raw fetch, a sample-size control, a drill
        to one vehicle’s complete raw signal — none of it resident in the browser.</p></div>
  </div>
  <p class="verdict">To <b>see and interrogate massive data at full fidelity</b> — not just chart a
    summary — a Databricks App is the right tool; a resident-extract BI tool is the wrong shape.</p>
</section>
</div>
</div>
'''

tab1 = '''<div class="panel-doc" id="tab-story">
<header>
  <div class="hero">
    <div class="eyebrow">Example case · fleet EV battery</div>
    <h1>The outlier in the pack</h1>
    <p class="lede">The example that carries this demo: a fleet of EV batteries. Each pack reports its
      hottest cell’s temperature ten times a second. The job — find the one pack, among hundreds, that
      runs too hot.</p>
    <div class="ramp"></div>
    <div class="ramp-labels mono">
      <span>28&nbsp;°C&nbsp;nominal</span><span>45&nbsp;°C&nbsp;elevated</span>
      <span class="hotlab">55&nbsp;°C&nbsp;→&nbsp;thermal&nbsp;risk</span>
    </div>
  </div>
</header>

<div class="wrap">

<section>
  <div class="eyebrow">Why an average hides it</div>
  <h2>The fault is never the average</h2>
  <p class="sub">A hot pack is a rare, seconds-long spike. Any average — over time, cells, or the fleet
    — erases it. The demo fleet: 200 cars, 21.6&nbsp;million raw samples.</p>
  <div class="proof">
    <div class="stat cool"><div class="k">Fleet median</div><div class="v">39.1</div>
      <div class="u">°C — what an average shows</div></div>
    <div class="stat"><div class="k">Top 0.1%</div><div class="v">62.8</div>
      <div class="u">°C — past the risk line</div></div>
    <div class="stat hot"><div class="k">Hottest</div><div class="v">72.5</div>
      <div class="u">°C — from 30 of 200 cars</div></div>
  </div>
</section>

<section>
  <div class="eyebrow">What happened to the battery</div>
  <h2>A hot outlier is a defect you can name</h2>
  <p class="sub">The signal is cell temperature — so reading the outlier is reading a physical failure.</p>
DRAWINGS
</section>
</div>
</div>
'''

tab1 = tab1.replace("DRAWINGS", drawings)

# ---------------- TAB 2: the app workflow, top to bottom ----------------
tab_workflow = '''<div class="panel-doc" id="tab-workflow">
<header>
  <div class="hero">
    <div class="eyebrow">Fleet EV Battery · field-quality monitor</div>
    <h1>How the dashboard works</h1>
    <p class="lede">The screen reads top to bottom, and so does the investigation. You descend from a
      picture of the whole fleet, to a sampled group of suspects, to the raw signal of one vehicle —
      the raw data always within reach, never summarized away.</p>
  </div>
</header>

<div class="wrap">
<section>
  <div class="eyebrow">The app, top to bottom</div>
  <h2>Three plots, three altitudes</h2>
  <p class="sub">Each step down the screen increases the resolution of the data and narrows the
    question. This is the exact top-to-bottom layout of the dashboard.</p>

  <div class="applayout">
    <div class="lyr">
      <div class="tag2">TOP · header</div>
      <h4>Fleet at a glance</h4>
      <p>Live counters show the size of what you are looking at.</p>
      <div class="pillrow"><span>200 vehicles</span><span>21.6M raw samples</span><span>3 days</span><span>30 running hot</span></div>
    </div>
    <div class="down">↓</div>
    <div class="lyr">
      <div class="tag2">UPPER PLOT · the aggregated picture</div>
      <h4>Raw-sample density — state of charge × cell temperature</h4>
      <p>Every raw sample from every vehicle is binned into a fine grid and colored by count. The fleet
        is one dense cloud; the eye goes to the faint hot cells floating above it — packs that reached
        temperatures no healthy battery should at that charge state. Nothing is averaged, so a rare
        outlier still leaves its mark.</p>
    </div>
    <div class="down">↓ &nbsp; box-select (lasso) the hot region</div>
    <div class="lyr ctrl">
      <div class="tag2">CONTROL · between the upper and middle plots</div>
      <h4>Sample-size slider</h4>
      <p>Before the raw curves are pulled, you set how many vehicles to bring down from the lasso’d
        region. The slider defaults to <b>30</b> and takes the <em>N hottest</em> vehicles — trading
        breadth for how much raw data the next step fetches and overlays.</p>
      <div class="slidermock">
        <span class="lab">sample size</span>
        <span class="track"><span class="fill"></span><span class="knob"></span></span>
        <span class="val">30</span>
      </div>
    </div>
    <div class="down">↓ &nbsp; the N hottest vehicles</div>
    <div class="lyr">
      <div class="tag2">MIDDLE PLOT + TABLE · the sampled suspects</div>
      <h4>Overlaid raw curves + a forensic table</h4>
      <p>The N sampled vehicles’ <b>raw</b> temperature-vs-time traces are fetched on demand and
        overlaid — the failing pack’s line peels upward in repeating spikes. Beside them, a table lists
        each sampled vehicle with its peak temperature, seconds spent hot, mileage and lowest voltage —
        sortable evidence, worst first.</p>
    </div>
    <div class="down">↓ &nbsp; click a row in the table</div>
    <div class="lyr">
      <div class="tag2">BOTTOM PLOT · one vehicle in full</div>
      <h4>That vehicle’s complete raw signal</h4>
      <p>Click a suspect and the dashboard fetches <em>every raw sample</em> for that one vehicle — a
        hundred thousand points — and draws its full-resolution trace: the exact shape of each thermal
        excursion, when it happened, how long it lasted, how the pack recovered. This is the evidence
        for a warranty claim or a field-quality report.</p>
    </div>
  </div>
  <p>At no point is the raw signal thrown away. That is what makes the outlier findable — and, as the
    next tab explains, it is exactly what a resident-extract BI tool cannot do at fleet scale.</p>
</section>
</div>
</div>
'''

# ---------------- TAB 2: why only Databricks Apps ----------------
tab2 = '''<div class="panel-doc" id="tab-tools">
<header>
  <div class="hero">
    <div class="eyebrow">Tool comparison · Databricks Apps vs classic BI</div>
    <h1>Why this only works on Databricks&nbsp;Apps</h1>
    <p class="lede">The workflow needs two things at once: a full-resolution picture of hundreds of
      millions of raw samples, and the raw rows behind any selection on demand. Classic BI can’t do
      both at scale.</p>
  </div>
</header>

<div class="wrap">

<section>
  <div class="eyebrow">The root bottleneck</div>
  <h2>Summary</h2>

  <div class="modes">
    <table>
      <thead><tr><th>Tool</th><th></th><th>Pre-loaded &mdash; a resident copy on the server</th><th>DirectQuery / live &mdash; no resident copy</th></tr></thead>
      <tbody>
        <!-- TABLEAU -->
        <tr class="tool-top scale"><td class="tl" rowspan="9">Tableau<br>Server</td>
            <td class="ax"><span class="tag">Scale</span></td>
            <td>At raw grain the extract is the size of the raw data (GB–TB) and refresh scales with it — it stops fitting as the fleet grows.</td>
            <td>VizQL emits many SQL per dashboard — one filter on a 5-chart view fires ≥10 queries; COUNTD / LOD compile to costly subqueries.</td></tr>
        <tr class="fidel"><td class="ax"><span class="tag">Fidelity</span></td>
            <td>Shrink it to a summary extract to fit, and the outlier is gone.</td>
            <td>The viz still caps marks, so the query is aggregated before it draws.</td></tr>
        <tr class="flow"><td class="ax"><span class="tag">Workflow</span></td>
            <td class="span" colspan="2">Drill-through and filter actions re-slice loaded / summarized data; no step re-issues a new query to <em>fetch raw rows</em> it never loaded.</td></tr>
        <tr class="act"><td class="ax"><span class="tag">Actions</span></td>
            <td class="span" colspan="2">Renders only. Running code, writing a row or sending a mail needs a bolted-on extension / webhook, not the tool itself.</td></tr>
        <tr class="layer"><td class="ax"><span class="tag">Layers</span></td>
            <td class="span" colspan="2">A fixed chart catalog (plus dual-axis / reference-line tricks). No open plotting grammar to stack arbitrary layers in one figure.</td></tr>
        <tr class="maint"><td class="ax"><span class="tag">Maintenance</span></td>
            <td class="span" colspan="2">A separate server to size, patch and govern, with extracts to schedule — and a second copy of the data to keep in sync.</td></tr>
        <tr class="cost"><td class="ax"><span class="tag">Cost</span></td>
            <td class="span" colspan="2">Per-seat viewer licences plus the server, and duplicate storage for the resident extract.</td></tr>
        <tr class="talk"><td class="ax"><span class="tag">Talk-to-data</span></td>
            <td class="span" colspan="2">Ask Data / Pulse answer in natural language, but only over the tool’s own data source — not a conversational layer on the governed lakehouse.</td></tr>
        <tr class="sem"><td class="ax"><span class="tag">Semantics</span></td>
            <td class="span" colspan="2">Measures and LOD calcs live inside the workbook / data source, so definitions sit in the BI tool and drift between tools — not central at the data.</td></tr>

        <!-- POWER BI -->
        <tr class="tool-top scale"><td class="tl" rowspan="9">Power BI<br>Service</td>
            <td class="ax"><span class="tag">Scale</span></td>
            <td>Raw grain must fit in capacity RAM and grows with the fleet — pre-aggregate to fit.</td>
            <td>Each visual fires 1+ queries, re-issued on every slicer; a 5-visual tab can generate 100+. DAX &amp; DistinctCount → subquery-heavy SQL.</td></tr>
        <tr class="fidel"><td class="ax"><span class="tag">Fidelity</span></td>
            <td>Once pre-aggregated, the outlier is no longer in the model.</td>
            <td>The ~3.5k–10k mark cap forces a GROUP BY / top-N first.</td></tr>
        <tr class="flow"><td class="ax"><span class="tag">Workflow</span></td>
            <td class="span" colspan="2">Slicers and cross-filters re-slice the loaded model; there is no brush that pushes a new predicate to fetch raw rows on demand.</td></tr>
        <tr class="act"><td class="ax"><span class="tag">Actions</span></td>
            <td class="span" colspan="2">Power Automate / write-back buttons exist, but as add-on integrations — the dashboard itself doesn’t run your code or job.</td></tr>
        <tr class="layer"><td class="ax"><span class="tag">Layers</span></td>
            <td class="span" colspan="2">Built-in visuals plus custom visuals, but not a free grammar-of-graphics: no arbitrary layered composition in a single figure.</td></tr>
        <tr class="maint"><td class="ax"><span class="tag">Maintenance</span></td>
            <td class="span" colspan="2">A capacity to size and a semantic model to refresh and govern, kept in sync with the source — a second platform to run.</td></tr>
        <tr class="cost"><td class="ax"><span class="tag">Cost</span></td>
            <td class="span" colspan="2">Per-user / capacity licensing, plus duplicate storage and memory for the Import model.</td></tr>
        <tr class="talk"><td class="ax"><span class="tag">Talk-to-data</span></td>
            <td class="span" colspan="2">Q&amp;A / Copilot answer in natural language, but over the semantic model — scoped to what was modeled in Power BI, not the governed lakehouse.</td></tr>
        <tr class="sem"><td class="ax"><span class="tag">Semantics</span></td>
            <td class="span" colspan="2">Measures live in the DAX semantic model inside Power BI, duplicated and re-governed per report — not central at the data.</td></tr>

        <!-- QLIK -->
        <tr class="tool-top scale"><td class="tl" rowspan="9">Qlik Sense<br>Enterprise</td>
            <td class="ax"><span class="tag">Scale</span></td>
            <td>Raw grain must fit in engine RAM and reload scales with it.</td>
            <td>Each object sends its own SQL, re-issued on every selection; COUNT(DISTINCT) → correlated subqueries. (In-memory default fires no SQL.)</td></tr>
        <tr class="fidel"><td class="ax"><span class="tag">Fidelity</span></td>
            <td>Summarize to fit and the outlier is gone.</td>
            <td>The chart caps marks, so the pushed query is aggregated.</td></tr>
        <tr class="flow"><td class="ax"><span class="tag">Workflow</span></td>
            <td class="span" colspan="2">Associative selection is powerful, but over data already in memory; a slider that re-sizes a raw fetch from the source isn’t part of the model.</td></tr>
        <tr class="act"><td class="ax"><span class="tag">Actions</span></td>
            <td class="span" colspan="2">Renders and selects. Triggering a job or an email needs external automation, not the sheet itself.</td></tr>
        <tr class="layer"><td class="ax"><span class="tag">Layers</span></td>
            <td class="span" colspan="2">A fixed chart set plus extensions; no ggplot / Plotly-style layering of arbitrary geoms in one plot.</td></tr>
        <tr class="maint"><td class="ax"><span class="tag">Maintenance</span></td>
            <td class="span" colspan="2">A separate engine node to size and a QVF app to reload and govern, kept in sync with the source.</td></tr>
        <tr class="cost"><td class="ax"><span class="tag">Cost</span></td>
            <td class="span" colspan="2">Per-user licensing plus the engine, and duplicate storage/RAM for the in-memory app.</td></tr>
        <tr class="talk"><td class="ax"><span class="tag">Talk-to-data</span></td>
            <td class="span" colspan="2">Insight Advisor / Answers give natural-language search, but over the loaded app model — not a conversational layer on the governed lakehouse.</td></tr>
        <tr class="sem"><td class="ax"><span class="tag">Semantics</span></td>
            <td class="span" colspan="2">Master items and load-script logic define the model inside the Qlik app, duplicated per app — not central at the data.</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section>
  <div class="eyebrow">Functionality</div>
  <h2>Workflow</h2>
  <p class="sub">An App is a program: the interface <b>builds itself as you click</b> — a new plot appears
    only when you reach that step, backed by a fresh query. A dashboard is a <b>fixed set of visuals</b>;
    clicking only filters what is already there.</p>
  <div class="draw">
    <figure>
      <svg viewBox="0 0 720 250" role="img" aria-label="The Databricks App runs a funnel of three queries — an aggregate over all data, a bounded fetch of a selected region, and a drill to one vehicle's raw rows — each a new query to the lakehouse; a BI dashboard runs the same steps only over the single copy it loaded up front and cannot fetch new raw rows">
        <!-- APP lane -->
        <text x="14" y="40" font-family="IBM Plex Mono" font-size="12" fill="var(--ok)">DATABRICKS APP</text>
        <text x="14" y="55" font-family="IBM Plex Mono" font-size="9.5" fill="var(--slate)">UI builds as you click</text>
        <g font-family="IBM Plex Mono" font-size="10.5">
          <rect x="150" y="30" width="130" height="46" rx="7" fill="none" stroke="var(--ok)" stroke-width="1.6"/>
          <text x="215" y="50" text-anchor="middle" fill="currentColor">aggregate</text>
          <text x="215" y="64" text-anchor="middle" fill="var(--slate)" font-size="9">density over ALL</text>
          <rect x="320" y="30" width="130" height="46" rx="7" fill="none" stroke="var(--ok)" stroke-width="1.6"/>
          <text x="385" y="50" text-anchor="middle" fill="currentColor">bounded fetch</text>
          <text x="385" y="64" text-anchor="middle" fill="var(--slate)" font-size="9">brush → WHERE</text>
          <rect x="490" y="30" width="130" height="46" rx="7" fill="none" stroke="var(--ok)" stroke-width="1.6"/>
          <text x="555" y="50" text-anchor="middle" fill="currentColor">drill to one</text>
          <text x="555" y="64" text-anchor="middle" fill="var(--slate)" font-size="9">raw 10 Hz trace</text>
        </g>
        <line x1="280" y1="53" x2="318" y2="53" stroke="var(--ok)" stroke-width="1.6" marker-end="url(#wf)"/>
        <line x1="450" y1="53" x2="488" y2="53" stroke="var(--ok)" stroke-width="1.6" marker-end="url(#wf)"/>
        <text x="299" y="46" text-anchor="middle" font-family="IBM Plex Mono" font-size="8.5" fill="var(--ok)">narrow</text>
        <text x="469" y="46" text-anchor="middle" font-family="IBM Plex Mono" font-size="8.5" fill="var(--ok)">narrow</text>
        <!-- lakehouse feeds every step -->
        <rect x="150" y="96" width="470" height="30" rx="6" fill="none" stroke="var(--slate)" stroke-width="1.1" stroke-dasharray="4 4"/>
        <text x="385" y="115" text-anchor="middle" font-family="IBM Plex Mono" font-size="10" fill="var(--slate)">lakehouse — raw grain, queried fresh at each step</text>
        <line x1="215" y1="96" x2="215" y2="78" stroke="var(--slate)" stroke-width="1" marker-end="url(#wfg)"/>
        <line x1="385" y1="96" x2="385" y2="78" stroke="var(--slate)" stroke-width="1" marker-end="url(#wfg)"/>
        <line x1="555" y1="96" x2="555" y2="78" stroke="var(--slate)" stroke-width="1" marker-end="url(#wfg)"/>

        <!-- BI lane -->
        <text x="14" y="172" font-family="IBM Plex Mono" font-size="12" fill="var(--hot)">CLASSIC BI</text>
        <text x="14" y="187" font-family="IBM Plex Mono" font-size="9.5" fill="var(--slate)">fixed visuals, laid out</text>
        <g font-family="IBM Plex Mono" font-size="10.5">
          <rect x="150" y="162" width="130" height="46" rx="7" fill="none" stroke="currentColor" stroke-width="1.3"/>
          <text x="215" y="182" text-anchor="middle" fill="currentColor">view</text>
          <text x="215" y="196" text-anchor="middle" fill="var(--slate)" font-size="9">on loaded copy</text>
          <rect x="320" y="162" width="130" height="46" rx="7" fill="none" stroke="currentColor" stroke-width="1.3"/>
          <text x="385" y="182" text-anchor="middle" fill="currentColor">filter / drill</text>
          <text x="385" y="196" text-anchor="middle" fill="var(--slate)" font-size="9">re-slice same copy</text>
          <rect x="490" y="162" width="130" height="46" rx="7" fill="none" stroke="var(--hot)" stroke-width="1.6"/>
          <text x="555" y="182" text-anchor="middle" fill="var(--hot)">raw rows?</text>
          <text x="555" y="196" text-anchor="middle" fill="var(--hot)" font-size="9">not loaded → can’t</text>
        </g>
        <line x1="280" y1="185" x2="318" y2="185" stroke="currentColor" stroke-width="1.3" marker-end="url(#wfk)"/>
        <line x1="450" y1="185" x2="488" y2="185" stroke="var(--hot)" stroke-width="1.6" marker-end="url(#wfh)"/>
        <!-- one resident copy under first two only -->
        <rect x="150" y="228" width="300" height="20" rx="5" fill="none" stroke="var(--hot)" stroke-width="1.2"/>
        <text x="300" y="242" text-anchor="middle" font-family="IBM Plex Mono" font-size="9.5" fill="var(--hot)">one resident copy — loaded up front, never re-queried</text>
        <line x1="215" y1="228" x2="215" y2="210" stroke="var(--hot)" stroke-width="1" marker-end="url(#wfh2)"/>
        <line x1="385" y1="228" x2="385" y2="210" stroke="var(--hot)" stroke-width="1" marker-end="url(#wfh2)"/>
        <defs>
          <marker id="wf" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><polygon points="0,0 8,4 0,8" fill="var(--ok)"/></marker>
          <marker id="wfg" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><polygon points="0,0 8,4 0,8" fill="var(--slate)"/></marker>
          <marker id="wfk" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><polygon points="0,0 8,4 0,8" fill="currentColor"/></marker>
          <marker id="wfh" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><polygon points="0,0 8,4 0,8" fill="var(--hot)"/></marker>
          <marker id="wfh2" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><polygon points="0,0 8,4 0,8" fill="var(--hot)"/></marker>
        </defs>
      </svg>
      <figcaption>Each App step is a fresh query to the lakehouse, narrowing to one vehicle’s raw trace.
        A dashboard runs on the one copy it loaded, so raw rows it never loaded have nowhere to come from.</figcaption>
    </figure>
  </div>
</section>

<section>
  <div class="eyebrow">Functionality</div>
  <h2>Actions</h2>
  <p class="sub">Finding the hot pack is only half the job — someone has to <em>do</em> something. An App is
    an application: a button runs backend code, so the next step happens in place. A dashboard renders; the
    action is a manual handoff to another tool or person, and that gap is where the process slows down.</p>
  <div class="draw">
    <h3>What happens after the outlier is found</h3>
    <figure>
      <svg viewBox="0 0 720 210" role="img" aria-label="After finding the outlier, the Databricks App runs the follow-up action directly from a button — opening a ticket, emailing the owner, or triggering a job — in one continuous flow; a BI dashboard has to hand off manually to export, another tool, or a person before the action can happen, adding a slow gap">
        <!-- APP row -->
        <text x="14" y="42" font-family="IBM Plex Mono" font-size="12" fill="var(--ok)">DATABRICKS APP</text>
        <g font-family="IBM Plex Mono" font-size="10.5">
          <rect x="185" y="26" width="120" height="42" rx="7" fill="none" stroke="currentColor" stroke-width="1.3"/>
          <text x="245" y="51" text-anchor="middle" fill="currentColor">outlier found</text>
          <rect x="345" y="26" width="110" height="42" rx="7" fill="none" stroke="var(--viol)" stroke-width="1.7"/>
          <text x="400" y="45" text-anchor="middle" fill="var(--viol)">▸ button</text>
          <text x="400" y="59" text-anchor="middle" fill="var(--slate)" font-size="8.5">in the app</text>
          <rect x="495" y="18" width="210" height="58" rx="7" fill="none" stroke="var(--ok)" stroke-width="1.6"/>
          <text x="600" y="38" text-anchor="middle" fill="var(--ok)">backend runs it</text>
          <text x="600" y="53" text-anchor="middle" fill="var(--slate)" font-size="9">open ticket · email owner</text>
          <text x="600" y="66" text-anchor="middle" fill="var(--slate)" font-size="9">trigger job / notebook</text>
        </g>
        <line x1="305" y1="47" x2="343" y2="47" stroke="currentColor" stroke-width="1.3" marker-end="url(#ac)"/>
        <line x1="455" y1="47" x2="493" y2="47" stroke="var(--ok)" stroke-width="1.6" marker-end="url(#aco)"/>
        <text x="360" y="90" font-family="IBM Plex Mono" font-size="9.5" fill="var(--ok)">one continuous flow — seconds</text>

        <!-- BI row -->
        <text x="14" y="140" font-family="IBM Plex Mono" font-size="12" fill="var(--hot)">CLASSIC BI</text>
        <g font-family="IBM Plex Mono" font-size="10.5">
          <rect x="185" y="124" width="120" height="42" rx="7" fill="none" stroke="currentColor" stroke-width="1.3"/>
          <text x="245" y="149" text-anchor="middle" fill="currentColor">outlier found</text>
          <!-- manual gap -->
          <rect x="345" y="120" width="150" height="50" rx="7" fill="color-mix(in srgb,var(--hot) 9%,var(--panel))" stroke="var(--hot)" stroke-width="1.5" stroke-dasharray="5 4"/>
          <text x="420" y="139" text-anchor="middle" fill="var(--hot)">✋ manual step</text>
          <text x="420" y="153" text-anchor="middle" fill="var(--slate)" font-size="8.5">export · switch tool</text>
          <text x="420" y="164" text-anchor="middle" fill="var(--slate)" font-size="8.5">email a person</text>
          <rect x="535" y="124" width="170" height="42" rx="7" fill="none" stroke="currentColor" stroke-width="1.3"/>
          <text x="620" y="143" text-anchor="middle" fill="currentColor">action, elsewhere</text>
          <text x="620" y="157" text-anchor="middle" fill="var(--slate)" font-size="9">in another system</text>
        </g>
        <line x1="305" y1="145" x2="343" y2="145" stroke="currentColor" stroke-width="1.3" marker-end="url(#ack)"/>
        <line x1="495" y1="145" x2="533" y2="145" stroke="var(--hot)" stroke-width="1.5" marker-end="url(#ach)"/>
        <text x="360" y="188" font-family="IBM Plex Mono" font-size="9.5" fill="var(--hot)">hand-off breaks the flow — hours to days</text>
        <defs>
          <marker id="ac" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><polygon points="0,0 8,4 0,8" fill="currentColor"/></marker>
          <marker id="aco" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><polygon points="0,0 8,4 0,8" fill="var(--ok)"/></marker>
          <marker id="ack" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><polygon points="0,0 8,4 0,8" fill="currentColor"/></marker>
          <marker id="ach" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><polygon points="0,0 8,4 0,8" fill="var(--hot)"/></marker>
        </defs>
      </svg>
      <figcaption>The App closes the loop in one place — a button calls backend code that opens the ticket,
        emails the owner or kicks off a job. A dashboard ends at the chart; the follow-up is a manual
        hand-off to another tool or person, and that break is the slow part.</figcaption>
    </figure>
    <div class="reads">Power BI has Power Automate buttons and Tableau has extensions, so an action is
      <em>possible</em> — but as bolted-on glue, not the tool running your own code. <b>An App is code, so
      the action lives right next to the analysis.</b></div>
  </div>
</section>

<section>
  <div class="eyebrow">Functionality</div>
  <h2>Layers</h2>
  <p class="sub"><b>Plotly</b> and <b>ggplot2</b> build a figure as a stack of layers, added almost
    endlessly — a density base, raw traces, a threshold, annotations — all in one plot. A BI tool gives
    you a fixed chart type; the App renders these figures directly.</p>
  <div class="draw">
    <figure>
      <svg viewBox="0 0 720 300" role="img" aria-label="A grammar-of-graphics figure is composed of layers added in order: a density or ribbon layer at the bottom, then a confidence band, individual raw lines, a mean line, points, a threshold rule, and text annotations on top — each layer drawn over the previous one, and more can always be added">
        <!-- exploded stack on the left -->
        <g font-family="IBM Plex Mono" font-size="10">
          <!-- each layer as a tilted card, offset upward -->
          <g transform="translate(60,210)">
            <rect x="0" y="0" width="200" height="42" rx="5" fill="color-mix(in srgb,var(--cool) 14%,var(--panel))" stroke="var(--cool)" stroke-width="1.2"/>
            <text x="12" y="18" fill="currentColor">1 · density / ribbon base</text>
            <text x="12" y="33" fill="var(--slate)" font-size="8.5">geom_ribbon / add_ribbons</text>
          </g>
          <g transform="translate(60,168)">
            <rect x="0" y="0" width="200" height="42" rx="5" fill="color-mix(in srgb,var(--warm) 14%,var(--panel))" stroke="var(--warm)" stroke-width="1.2"/>
            <text x="12" y="18" fill="currentColor">2 · confidence band</text>
            <text x="12" y="33" fill="var(--slate)" font-size="8.5">geom_smooth (se)</text>
          </g>
          <g transform="translate(60,126)">
            <rect x="0" y="0" width="200" height="42" rx="5" fill="color-mix(in srgb,var(--slate) 16%,var(--panel))" stroke="var(--slate)" stroke-width="1.2"/>
            <text x="12" y="18" fill="currentColor">3 · individual raw lines</text>
            <text x="12" y="33" fill="var(--slate)" font-size="8.5">geom_line, one per vehicle</text>
          </g>
          <g transform="translate(60,84)">
            <rect x="0" y="0" width="200" height="42" rx="5" fill="color-mix(in srgb,var(--ok) 14%,var(--panel))" stroke="var(--ok)" stroke-width="1.2"/>
            <text x="12" y="18" fill="currentColor">4 · points + error bars</text>
            <text x="12" y="33" fill="var(--slate)" font-size="8.5">geom_point / geom_errorbar</text>
          </g>
          <g transform="translate(60,42)">
            <rect x="0" y="0" width="200" height="42" rx="5" fill="color-mix(in srgb,var(--hot) 12%,var(--panel))" stroke="var(--hot)" stroke-width="1.2"/>
            <text x="12" y="18" fill="currentColor">5 · threshold + annotations</text>
            <text x="12" y="33" fill="var(--slate)" font-size="8.5">geom_hline / annotate</text>
          </g>
          <text x="160" y="24" text-anchor="middle" fill="var(--slate)" font-size="9">… add more, almost endlessly ↑</text>
        </g>
        <!-- equals arrow -->
        <text x="300" y="160" text-anchor="middle" font-family="IBM Plex Mono" font-size="22" fill="var(--slate)">=</text>
        <!-- composited result on the right -->
        <g transform="translate(340,40)">
          <rect x="0" y="0" width="340" height="230" rx="8" fill="none" stroke="currentColor" stroke-width="1.3"/>
          <!-- axes -->
          <line x1="34" y1="196" x2="322" y2="196" stroke="var(--slate)" stroke-width="1"/>
          <line x1="34" y1="24" x2="34" y2="196" stroke="var(--slate)" stroke-width="1"/>
          <!-- layer 1: ribbon base -->
          <path d="M34,150 L110,140 L180,120 L250,132 L322,116 L322,196 L34,196 Z" fill="color-mix(in srgb,var(--cool) 22%,transparent)" stroke="none"/>
          <!-- layer 2: confidence band -->
          <path d="M34,120 L110,108 L180,86 L250,100 L322,80 L322,110 L250,128 L180,112 L110,132 L34,144 Z" fill="color-mix(in srgb,var(--warm) 26%,transparent)" stroke="none"/>
          <!-- layer 3: raw lines -->
          <polyline points="34,140 110,120 180,74 250,110 322,92" fill="none" stroke="var(--slate)" stroke-width="1" opacity="0.7"/>
          <polyline points="34,152 110,132 180,96 250,120 322,104" fill="none" stroke="var(--slate)" stroke-width="1" opacity="0.5"/>
          <!-- layer 3b: the hot outlier line -->
          <polyline points="34,150 110,128 180,52 250,116 322,100" fill="none" stroke="var(--hot)" stroke-width="1.8"/>
          <!-- layer 4: points -->
          <g fill="var(--ok)"><circle cx="110" cy="120" r="2.6"/><circle cx="180" cy="74" r="2.6"/><circle cx="250" cy="110" r="2.6"/><circle cx="322" cy="92" r="2.6"/></g>
          <!-- layer 5: threshold + annotation -->
          <line x1="34" y1="64" x2="322" y2="64" stroke="var(--hot)" stroke-width="1.3" stroke-dasharray="5 4"/>
          <text x="316" y="58" text-anchor="end" font-family="IBM Plex Mono" font-size="9" fill="var(--hot)">threshold</text>
          <circle cx="180" cy="52" r="9" fill="none" stroke="var(--hot)" stroke-width="1.4"/>
          <text x="180" y="30" text-anchor="middle" font-family="IBM Plex Mono" font-size="9" fill="var(--hot)">outlier</text>
          <text x="170" y="220" text-anchor="middle" font-family="IBM Plex Mono" font-size="9.5" fill="var(--slate)">all layers, one figure</text>
        </g>
      </svg>
      <figcaption>Layer order is draw order: each layer overlays the last, so one figure carries the
        base, the raw curves, points, a threshold and labels at once. A BI chart type can’t be composed this way.</figcaption>
    </figure>
    <div class="reads">It’s the App’s density-plus-raw-overlay view: the hot trace stays visible
      <b>because it’s its own layer on top</b>.</div>
  </div>
</section>

<section>
  <div class="eyebrow">Functionality</div>
  <h2>Fidelity</h2>
  <p class="sub">Take the app’s three steps in turn. One short, traceable line per tool.</p>

  <div class="legend">
    <span><i style="background:var(--ok)"></i> works</span>
    <span><i style="background:var(--warm)"></i> partial / degraded</span>
    <span><i style="background:var(--hot)"></i> not possible cleanly</span>
  </div>

  <div class="cmp-step"><p class="h">Step 1</p><h3>Show the full-resolution density of every raw sample</h3>
    <div class="cmp">
      <div class="r app yes"><span class="tn">Databricks App</span><span class="mk">✓</span><p>The outlier cell is drawn.</p></div>
      <div class="r no"><span class="tn">Tableau</span><span class="mk">✕</span><p>Bins into a coarse hexbin to stay fast. The lone hot cell is pooled away.</p></div>
      <div class="r no"><span class="tn">Power BI</span><span class="mk">✕</span><p>Caps a scatter at ~3.5k points (~10k only with the high-density sampling setting on), so it may not draw every point.</p></div>
      <div class="r no"><span class="tn">Qlik</span><span class="mk">✕</span><p>Chart engine caps points too. At fleet scale it aggregates the cell away.</p></div>
    </div>
  </div>

  <div class="cmp-step"><p class="h">Step 2 · the lasso</p><h3>Turn the rectangle into a fetch of raw rows from the source</h3>
    <div class="cmp">
      <div class="r app yes"><span class="tn">Databricks App</span><span class="mk">✓</span><p>The box becomes a <span class="mono">WHERE</span> query. It pulls raw rows on demand.</p></div>
      <div class="r part"><span class="tn">Tableau</span><span class="mk">~</span><p>The lasso only selects marks already in the extract. It cannot fetch new raw rows.</p></div>
      <div class="r no"><span class="tn">Power BI</span><span class="mk">✕</span><p>No native brush that pushes a predicate to the source. Filtering runs on the loaded model.</p></div>
      <div class="r part"><span class="tn">Qlik</span><span class="mk">~</span><p>Selection is great, but only over data already loaded in memory. Not a lakehouse fetch.</p></div>
    </div>
    <p class="modes-note">In <b>DirectQuery / live</b> mode a selection <em>can</em> reach the source —
      but it feeds a chart that still caps marks, so the fetched raw rows can’t all be drawn; the App’s
      lasso both fetches and renders them.</p>
  </div>

  <div class="cmp-step"><p class="h">Step 2 · the overlay</p><h3>Overlay the sampled vehicles’ raw curves, one line each</h3>
    <div class="cmp">
      <div class="r app yes"><span class="tn">Databricks App</span><span class="mk">✓</span><p>Draws each sampled vehicle’s raw trace. The failing curve’s shape is visible.</p></div>
      <div class="r no"><span class="tn">Tableau</span><span class="mk">✕</span><p>Too many marks. It falls back to a percentile band. The individual shape is lost.</p></div>
      <div class="r no"><span class="tn">Power BI</span><span class="mk">✕</span><p>Point cap plus line aggregation. A true raw overlay is not possible.</p></div>
      <div class="r no"><span class="tn">Qlik</span><span class="mk">✕</span><p>Same rendering ceiling. Hundreds of raw curves cannot be drawn honestly.</p></div>
    </div>
  </div>

  <div class="cmp-step"><p class="h">Step 2 · the sampling slider</p><h3>Set how many vehicles the fetch pulls — a live control on the query</h3>
    <div class="cmp">
      <div class="r app yes"><span class="tn">Databricks App</span><span class="mk">✓</span><p>A slider parameterises the pushdown query (take the N hottest). Move it, the query re-runs and re-fetches.</p></div>
      <div class="r no"><span class="tn">Tableau</span><span class="mk">✕</span><p>A parameter can filter marks already loaded, but it can’t change how many raw rows are fetched into the fetch itself.</p></div>
      <div class="r no"><span class="tn">Power BI</span><span class="mk">✕</span><p>Slicers filter the loaded model; there’s no control that re-shapes a raw-row fetch on demand.</p></div>
      <div class="r no"><span class="tn">Qlik</span><span class="mk">✕</span><p>Selections filter the in-memory model; a slider that resizes a raw fetch from the source isn’t the model.</p></div>
    </div>
    <p class="modes-note">This is a control on the <em>query</em>, not on already-loaded marks — it decides
      how much raw data the next fetch brings back. It only makes sense when the app owns the fetch, which
      is why the BI tools have no equivalent.</p>
  </div>

  <div class="cmp-step"><p class="h">Step 3</p><h3>Drill to one vehicle’s full 10 Hz raw trace (~100k points)</h3>
    <div class="cmp">
      <div class="r app yes"><span class="tn">Databricks App</span><span class="mk">✓</span><p>Fetches that one vehicle’s every raw point on click. Nothing pre-loaded.</p></div>
      <div class="r part"><span class="tn">Tableau</span><span class="mk">~</span><p>Works only if those rows were extracted up front. The extract then balloons.</p></div>
      <div class="r part"><span class="tn">Power BI</span><span class="mk">~</span><p>DirectQuery can fetch the vehicle, but the visual still caps and thins the points.</p></div>
      <div class="r part"><span class="tn">Qlik</span><span class="mk">~</span><p>The raw points must be in the in-memory model first, and the chart still caps them.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="eyebrow">Functionality</div>
  <h2>Scale</h2>
  <p class="sub">The seconds a dashboard takes to open depend on how much data it must move. As the fleet
    grows, the classic BI tools climb — and past a point they stop working, because the resident copy no
    longer fits or the live queries no longer return in time. The App stays in seconds: its overview reads
    one pre-computed aggregate, so it grows only gently with the fleet instead of scaling with the raw data.</p>
  <div class="rt">
    <div class="row head"><span>Fleet</span><span>Classic BI — first interactive view</span><span></span></div>
    <div class="row"><span class="tool-name">~20 cars</span><div class="bar mid"><span style="width:20%"></span></div><span class="t">~4 s</span></div>
    <div class="row"><span class="tool-name">~200 cars</span><div class="bar mid"><span style="width:55%"></span></div><span class="t">~15 s</span></div>
    <div class="row"><span class="tool-name">~2,000 cars</span><div class="bar slow"><span style="width:90%"></span></div><span class="t">minutes</span></div>
    <div class="row"><span class="tool-name">fleet-wide</span><div class="bar slow"><span style="width:100%"></span></div><span class="t breaks">breaks</span></div>
  </div>
  <div class="rt" style="margin-top:14px">
    <div class="row head"><span>Fleet</span><span>Databricks App — first interactive view</span><span></span></div>
    <div class="row"><span class="tool-name">~200 cars</span><div class="bar fast"><span style="width:12%"></span></div><span class="t">~2–3 s</span></div>
    <div class="row"><span class="tool-name">fleet-wide</span><div class="bar fast"><span style="width:20%"></span></div><span class="t">a few s</span></div>
  </div>
  <div class="rtnote">Illustrative. The BI number is a raw-grain extract/model refresh (or a live-query
    round-trip) plus first render — both scale with the data, so the time rises with the fleet and
    eventually the copy won’t fit / the query won’t return. <b>The App’s overview is a bounded query
    against a pre-materialized aggregate</b>, so it reads a fixed-size summary rather than the raw data —
    the first view stays in seconds and grows only gently as the fleet grows.</div>
</section>

<section>
  <div class="eyebrow">Functionality</div>
  <h2>Maintenance</h2>
  <p class="sub">A classic BI tool is a second platform bolted onto the lakehouse. It has to be sized,
    kept in sync, and governed on its own.</p>
  <div class="cmp-step">
    <div class="cmp">
      <div class="r no"><span class="tn">Classic BI</span><span class="mk">✕</span><p>A separate server to size and patch, extracts/models to schedule and refresh, and a second copy of the data to secure and keep in sync with the source.</p></div>
      <div class="r no"><span class="tn">Classic BI</span><span class="mk">✕</span><p>Access is governed twice — once in Unity Catalog, again in the BI tool — so permissions drift and the resident copy can go stale between refreshes.</p></div>
      <div class="r app yes"><span class="tn">Databricks App</span><span class="mk">✓</span><p>Runs on the lakehouse you already have. No extracts to refresh, no second copy to secure — it reads live tables under the same Unity Catalog governance.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="eyebrow">Functionality</div>
  <h2>Cost</h2>
  <p class="sub">The two cost lines a classic BI deployment adds on top of the lakehouse — seats and a
    second copy of the data — are the two the App doesn’t have.</p>
  <div class="cmp-step">
    <div class="cmp">
      <div class="r no"><span class="tn">Classic BI</span><span class="mk">✕</span><p>Per-seat dashboard subscriptions for every viewer, plus a dedicated capacity/server to license and run.</p></div>
      <div class="r no"><span class="tn">Classic BI</span><span class="mk">✕</span><p>The resident extract/model is a duplicate of the raw data — extra storage and memory that grows with the fleet.</p></div>
      <div class="r app yes"><span class="tn">Databricks App</span><span class="mk">✓</span><p>Served on existing Databricks compute, billed per use. No per-seat licence, and no second copy of the data to store.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="eyebrow">Functionality</div>
  <h2>Talk-to-data</h2>
  <p class="sub">The BI tools all have natural-language features. But they answer over the tool’s <b>own
    model</b> — scoped to what was loaded and modeled there. A Databricks App can ask the <b>governed
    lakehouse directly</b>, e.g. by embedding a Genie space, so the question reaches the real data.</p>
  <div class="draw">
    <figure>
      <svg viewBox="0 0 720 190" role="img" aria-label="A Databricks App or Genie answers a natural-language question directly against the governed lakehouse; a BI tool's natural-language feature answers only over the tool's own loaded model, one step removed from the data">
        <!-- APP row -->
        <text x="14" y="40" font-family="IBM Plex Mono" font-size="12" fill="var(--ok)">DATABRICKS APP / GENIE</text>
        <g font-family="IBM Plex Mono" font-size="10.5">
          <rect x="230" y="24" width="120" height="42" rx="7" fill="none" stroke="currentColor" stroke-width="1.3"/>
          <text x="290" y="43" text-anchor="middle" fill="currentColor">“ask a question”</text>
          <text x="290" y="57" text-anchor="middle" fill="var(--slate)" font-size="9">natural language</text>
          <rect x="560" y="24" width="145" height="42" rx="7" fill="none" stroke="var(--ok)" stroke-width="1.6"/>
          <text x="632" y="43" text-anchor="middle" fill="var(--ok)">governed lakehouse</text>
          <text x="632" y="57" text-anchor="middle" fill="var(--slate)" font-size="9">the real, raw data</text>
        </g>
        <line x1="350" y1="45" x2="558" y2="45" stroke="var(--ok)" stroke-width="1.6" marker-end="url(#tk1)"/>
        <text x="454" y="38" text-anchor="middle" font-family="IBM Plex Mono" font-size="9" fill="var(--ok)">asks directly</text>

        <!-- BI row -->
        <text x="14" y="128" font-family="IBM Plex Mono" font-size="12" fill="var(--hot)">CLASSIC BI · NL</text>
        <g font-family="IBM Plex Mono" font-size="10.5">
          <rect x="230" y="112" width="120" height="42" rx="7" fill="none" stroke="currentColor" stroke-width="1.3"/>
          <text x="290" y="131" text-anchor="middle" fill="currentColor">Q&amp;A / Copilot</text>
          <text x="290" y="145" text-anchor="middle" fill="var(--slate)" font-size="9">Insight Advisor</text>
          <rect x="405" y="112" width="120" height="42" rx="7" fill="none" stroke="var(--hot)" stroke-width="1.5"/>
          <text x="465" y="131" text-anchor="middle" fill="var(--hot)">tool’s model</text>
          <text x="465" y="145" text-anchor="middle" fill="var(--slate)" font-size="9">loaded extract</text>
          <rect x="585" y="112" width="120" height="42" rx="7" fill="none" stroke="currentColor" stroke-width="1.1" stroke-dasharray="4 4"/>
          <text x="645" y="135" text-anchor="middle" fill="var(--slate)">lakehouse</text>
        </g>
        <line x1="350" y1="133" x2="403" y2="133" stroke="currentColor" stroke-width="1.3" marker-end="url(#tkk)"/>
        <line x1="525" y1="133" x2="583" y2="133" stroke="var(--slate)" stroke-width="1.1" stroke-dasharray="4 4"/>
        <text x="465" y="176" text-anchor="middle" font-family="IBM Plex Mono" font-size="9" fill="var(--hot)">answers only over what was modeled — a step removed from the data</text>
        <defs>
          <marker id="tk1" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><polygon points="0,0 8,4 0,8" fill="var(--ok)"/></marker>
          <marker id="tkk" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><polygon points="0,0 8,4 0,8" fill="currentColor"/></marker>
        </defs>
      </svg>
      <figcaption>A BI tool’s natural-language answer is only as complete as the model it was given. Genie
        (embedded in the App) asks the governed lakehouse itself.</figcaption>
    </figure>
  </div>
</section>

<section>
  <div class="eyebrow">Functionality</div>
  <h2>Semantics</h2>
  <p class="sub">The <b>semantic layer</b> — what “scrap rate” or “on-time” means — lives <b>inside</b> each
    BI tool (DAX model, LOD calcs, master items), so every tool keeps its own copy and they drift. On
    Databricks it lives <b>once, at the data</b> (Unity Catalog metric views), and every consumer — the
    App, Genie, any tool — reads the same definition.</p>
  <div class="draw">
    <figure>
      <svg viewBox="0 0 720 240" role="img" aria-label="On Databricks the semantic layer sits centrally at the data in Unity Catalog and every consumer reads the same definition; with classic BI each tool holds its own copy of the definitions, which drift apart">
        <!-- CENTRAL (left) -->
        <text x="150" y="24" text-anchor="middle" font-family="IBM Plex Mono" font-size="12" fill="var(--ok)">CENTRAL — AT THE DATA</text>
        <rect x="95" y="36" width="110" height="44" rx="7" fill="none" stroke="var(--ok)" stroke-width="1.7"/>
        <text x="150" y="54" text-anchor="middle" font-family="IBM Plex Mono" font-size="10.5" fill="var(--ok)">metric layer</text>
        <text x="150" y="68" text-anchor="middle" font-family="IBM Plex Mono" font-size="8.5" fill="var(--slate)">Unity Catalog</text>
        <g stroke="var(--ok)" stroke-width="1.4">
          <line x1="150" y1="80" x2="70" y2="150" marker-end="url(#se1)"/>
          <line x1="150" y1="80" x2="150" y2="150" marker-end="url(#se1)"/>
          <line x1="150" y1="80" x2="230" y2="150" marker-end="url(#se1)"/>
        </g>
        <g font-family="IBM Plex Mono" font-size="9.5">
          <rect x="34" y="152" width="72" height="34" rx="6" fill="none" stroke="currentColor" stroke-width="1.1"/>
          <text x="70" y="173" text-anchor="middle" fill="currentColor">App</text>
          <rect x="114" y="152" width="72" height="34" rx="6" fill="none" stroke="currentColor" stroke-width="1.1"/>
          <text x="150" y="173" text-anchor="middle" fill="currentColor">Genie</text>
          <rect x="194" y="152" width="72" height="34" rx="6" fill="none" stroke="currentColor" stroke-width="1.1"/>
          <text x="230" y="173" text-anchor="middle" fill="currentColor">any tool</text>
        </g>
        <text x="150" y="212" text-anchor="middle" font-family="IBM Plex Mono" font-size="9.5" fill="var(--ok)">one definition · governed once</text>

        <!-- divider -->
        <line x1="360" y1="20" x2="360" y2="222" stroke="var(--line)" stroke-width="1"/>

        <!-- SILOED (right) -->
        <text x="540" y="24" text-anchor="middle" font-family="IBM Plex Mono" font-size="12" fill="var(--hot)">SILOED — IN EACH TOOL</text>
        <g font-family="IBM Plex Mono" font-size="9.5">
          <rect x="410" y="46" width="90" height="46" rx="6" fill="none" stroke="var(--hot)" stroke-width="1.4"/>
          <text x="455" y="66" text-anchor="middle" fill="var(--hot)">Tableau</text>
          <text x="455" y="80" text-anchor="middle" fill="var(--slate)" font-size="8">LOD calcs</text>
          <rect x="515" y="46" width="90" height="46" rx="6" fill="none" stroke="var(--hot)" stroke-width="1.4"/>
          <text x="560" y="66" text-anchor="middle" fill="var(--hot)">Power BI</text>
          <text x="560" y="80" text-anchor="middle" fill="var(--slate)" font-size="8">DAX model</text>
          <rect x="620" y="46" width="90" height="46" rx="6" fill="none" stroke="var(--hot)" stroke-width="1.4"/>
          <text x="665" y="66" text-anchor="middle" fill="var(--hot)">Qlik</text>
          <text x="665" y="80" text-anchor="middle" fill="var(--slate)" font-size="8">master items</text>
        </g>
        <!-- each its own copy of defs -->
        <g stroke="var(--hot)" stroke-width="1.2" stroke-dasharray="4 3">
          <line x1="455" y1="92" x2="455" y2="150" marker-end="url(#se2)"/>
          <line x1="560" y1="92" x2="560" y2="150" marker-end="url(#se2)"/>
          <line x1="665" y1="92" x2="665" y2="150" marker-end="url(#se2)"/>
        </g>
        <g font-family="IBM Plex Mono" font-size="8.5" fill="var(--slate)">
          <rect x="425" y="152" width="60" height="26" rx="5" fill="none" stroke="var(--line)" stroke-width="1"/>
          <text x="455" y="169" text-anchor="middle">own copy</text>
          <rect x="530" y="152" width="60" height="26" rx="5" fill="none" stroke="var(--line)" stroke-width="1"/>
          <text x="560" y="169" text-anchor="middle">own copy</text>
          <rect x="635" y="152" width="60" height="26" rx="5" fill="none" stroke="var(--line)" stroke-width="1"/>
          <text x="665" y="169" text-anchor="middle">own copy</text>
        </g>
        <text x="560" y="212" text-anchor="middle" font-family="IBM Plex Mono" font-size="9.5" fill="var(--hot)">three definitions · they drift</text>
        <defs>
          <marker id="se1" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><polygon points="0,0 8,4 0,8" fill="var(--ok)"/></marker>
          <marker id="se2" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><polygon points="0,0 8,4 0,8" fill="var(--hot)"/></marker>
        </defs>
      </svg>
      <figcaption>Define the metric once at the data and every consumer agrees; define it inside each tool
        and the same question gets three answers.</figcaption>
    </figure>
  </div>
</section>
</div>
</div>
'''

script = ("<script>\n"
"document.querySelectorAll('.doctab').forEach(t=>t.onclick=()=>{\n"
"  const id=t.dataset.tab;\n"
"  document.querySelectorAll('.doctab').forEach(x=>x.classList.toggle('active',x===t));\n"
"  document.querySelectorAll('.panel-doc').forEach(p=>p.classList.toggle('active',p.id==='tab-'+id));\n"
"  window.scrollTo(0,0);\n});\n</script>\n")

out = head + tabs + tab_why + tab1 + tab_workflow + tab2 + script
open("dashboard-explainer.html", "w", encoding="utf-8").write(out)

# validate
t = open("dashboard-explainer.html", encoding="utf-8").read()
print("div balance:", t.count("<div"), t.count("</div>"), "OK" if t.count("<div")==t.count("</div>") else "MISMATCH")
import re
ids = re.findall(r'id="([^"]+)"', t)
dupes = {i for i in ids if ids.count(i) > 1}
print("duplicate ids:", dupes or "none")
