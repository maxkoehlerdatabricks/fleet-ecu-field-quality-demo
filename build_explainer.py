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
.modes td{padding:10px 12px;border-bottom:1px solid var(--line);color:var(--ink-soft);vertical-align:top}
.modes td.tl{font-weight:600;color:var(--ink);white-space:nowrap}
.modes tr:last-child td{border-bottom:none}
.modes td b{color:var(--ink)}
.modes-note{font-size:13.5px;color:var(--ink-soft);margin:12px 2px 0}
.modes-note b{color:var(--ink)}
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
        outlier still leaves its mark. A <b>sample-size slider</b> (default 30) sets how many vehicles
        the next step will pull.</p>
    </div>
    <div class="down">↓ &nbsp; box-select (lasso) the hot region</div>
    <div class="lyr">
      <div class="tag2">MIDDLE PLOT + TABLE · the sampled suspects</div>
      <h4>Overlaid raw curves + a forensic table</h4>
      <p>The rectangle becomes a query. It takes the <em>N hottest</em> vehicles in the region and
        fetches their <b>raw</b> temperature-vs-time traces on demand — overlaid, the failing pack’s
        line peels upward in repeating spikes. Beside them, a table lists each sampled vehicle with its
        peak temperature, seconds spent hot, mileage and lowest voltage — sortable evidence, worst first.</p>
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
  <div class="eyebrow">The root difference</div>
  <h2>Where the data lives decides what the tool can do</h2>
  <p class="sub">Assume the deployed server products — Tableau Server, the Power BI Service, Qlik Sense
    Enterprise. By default each serves interactive charts from a <em>resident copy</em>, and each
    renders only a few thousand marks per chart.</p>

  <p><b>What the “resident copy” is:</b> a second, materialized copy of the data held <em>on the BI
    server</em> and kept in sync with the source by scheduled refresh jobs. Each tool has two modes —
    pre-load the copy, or query the source live and hold no copy:</p>

  <div class="modes">
    <table>
      <thead><tr><th>Tool</th><th>Pre-loaded &mdash; a resident copy</th><th>DirectQuery / live &mdash; no resident copy</th></tr></thead>
      <tbody>
        <tr><td class="tl">Tableau Server</td>
            <td>Published <b>Hyper extract</b> on the server; rebuilt by scheduled extract refreshes.</td>
            <td><b>Live connection</b>: each interaction queries the source; nothing materialized on the server.</td></tr>
        <tr><td class="tl">Power BI Service</td>
            <td><b>Import</b> semantic model in the capacity’s in-memory VertiPaq engine; scheduled dataset refreshes.</td>
            <td><b>DirectQuery</b>: SQL sent to the source per interaction; no import model held.</td></tr>
        <tr><td class="tl">Qlik Sense Enterprise</td>
            <td>QVF <b>app loaded into the engine’s RAM</b>; scheduled reload tasks.</td>
            <td><b>Direct Query / ODAG</b>: queries pushed to the source; not held in the in-memory engine.</td></tr>
      </tbody>
    </table>
    <p class="modes-note">Pre-loaded = a governed <b>duplicate</b> that must be capacity-sized, is only
      current as of the last refresh, and grows and slows as the fleet grows. DirectQuery / live drops
      the copy but adds a source round-trip on every user’s every interaction. <b>Either way, the chart
      still caps the marks it draws</b> — so neither mode can render the full plot.</p>
  </div>

  <p>The Databricks App holds <em>no</em> materialized copy on any server: it reads the lakehouse
    directly and fetches only what each step needs (its one small overview aggregate is a governed
    table in the lakehouse, not a separate resident engine to size and refresh).</p>
  <figure class="drawfig">
    <svg viewBox="0 0 720 210" role="img" aria-label="Classic BI tools load a resident copy of the data and render a capped number of marks; the Databricks App queries the lakehouse and fetches only what each step needs">
      <!-- BI side -->
      <text x="170" y="24" text-anchor="middle" font-family="IBM Plex Mono" font-size="12" fill="var(--hot)">CLASSIC BI TOOL</text>
      <rect x="40" y="40" width="120" height="46" rx="6" fill="none" stroke="currentColor" stroke-width="1.3"/>
      <text x="100" y="68" text-anchor="middle" font-family="IBM Plex Mono" font-size="11" fill="currentColor">lakehouse</text>
      <line x1="160" y1="63" x2="215" y2="63" stroke="var(--hot)" stroke-width="1.5" marker-end="url(#a1)"/>
      <text x="188" y="55" text-anchor="middle" font-family="IBM Plex Mono" font-size="9.5" fill="var(--hot)">big load</text>
      <rect x="218" y="40" width="120" height="46" rx="6" fill="none" stroke="var(--hot)" stroke-width="1.6"/>
      <text x="278" y="62" text-anchor="middle" font-family="IBM Plex Mono" font-size="10.5" fill="var(--hot)">resident copy</text>
      <text x="278" y="77" text-anchor="middle" font-family="IBM Plex Mono" font-size="9" fill="var(--slate)">extract / model</text>
      <line x1="278" y1="90" x2="278" y2="120" stroke="currentColor" stroke-width="1.3" marker-end="url(#a1)"/>
      <rect x="218" y="124" width="120" height="40" rx="6" fill="none" stroke="currentColor" stroke-width="1.3"/>
      <text x="278" y="148" text-anchor="middle" font-family="IBM Plex Mono" font-size="10" fill="currentColor">~few k marks</text>
      <text x="278" y="184" text-anchor="middle" font-family="IBM Plex Mono" font-size="9.5" fill="var(--hot)">must summarize to fit</text>
      <!-- App side -->
      <text x="545" y="24" text-anchor="middle" font-family="IBM Plex Mono" font-size="12" fill="var(--ok)">DATABRICKS APP</text>
      <rect x="415" y="40" width="120" height="46" rx="6" fill="none" stroke="currentColor" stroke-width="1.3"/>
      <text x="475" y="62" text-anchor="middle" font-family="IBM Plex Mono" font-size="11" fill="currentColor">lakehouse</text>
      <text x="475" y="77" text-anchor="middle" font-family="IBM Plex Mono" font-size="9" fill="var(--slate)">all raw stays here</text>
      <line x1="535" y1="55" x2="600" y2="55" stroke="var(--ok)" stroke-width="1.5" marker-end="url(#a2)"/>
      <text x="567" y="47" text-anchor="middle" font-family="IBM Plex Mono" font-size="9.5" fill="var(--ok)">bounded query</text>
      <line x1="600" y1="72" x2="535" y2="72" stroke="var(--ok)" stroke-width="1.5" marker-end="url(#a2b)"/>
      <text x="567" y="86" text-anchor="middle" font-family="IBM Plex Mono" font-size="9.5" fill="var(--ok)">only rows needed</text>
      <rect x="603" y="40" width="96" height="80" rx="6" fill="none" stroke="var(--ok)" stroke-width="1.6"/>
      <text x="651" y="76" text-anchor="middle" font-family="IBM Plex Mono" font-size="10.5" fill="var(--ok)">browser</text>
      <text x="651" y="92" text-anchor="middle" font-family="IBM Plex Mono" font-size="9" fill="var(--slate)">holds ~nothing</text>
      <text x="545" y="150" text-anchor="middle" font-family="IBM Plex Mono" font-size="9.5" fill="var(--ok)">full-res aggregate + raw on demand</text>
      <defs>
        <marker id="a1" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><polygon points="0,0 9,4.5 0,9" fill="var(--hot)"/></marker>
        <marker id="a2" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><polygon points="0,0 9,4.5 0,9" fill="var(--ok)"/></marker>
        <marker id="a2b" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><polygon points="0,0 9,4.5 0,9" fill="var(--ok)"/></marker>
      </defs>
    </svg>
    <figcaption>In its default mode a BI tool front-loads a resident copy and renders a capped number
      of marks, so it must summarize. (A query-live mode — Tableau live, Power BI DirectQuery, Qlik
      Direct Query — skips the copy but keeps the mark cap and adds a per-click round-trip.) The App
      leaves the raw data in the lakehouse and each interaction is a bounded query.</figcaption>
  </figure>
</section>

<section>
  <div class="eyebrow">Step by step</div>
  <h2>Each step, in Tableau, Power BI and Qlik</h2>
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
  <div class="eyebrow">Reaction time on mass data</div>
  <h2>Hundreds of vehicles, billions of raw points</h2>
  <p class="sub">Where the data lives also decides how the tool behaves as the fleet grows.</p>
  <div class="rt">
    <div class="row head"><span>Tool</span><span>Initial load / first interactive view</span><span>time</span></div>
    <div class="row"><span class="tool-name">Databricks App</span><div class="bar fast"><span style="width:14%"></span></div><span class="t">~2 s</span></div>
    <div class="row"><span class="tool-name">Tableau</span><div class="bar slow"><span style="width:100%"></span></div><span class="t">~15 s</span></div>
    <div class="row"><span class="tool-name">Power BI</span><div class="bar mid"><span style="width:70%"></span></div><span class="t">~10 s</span></div>
    <div class="row"><span class="tool-name">Qlik</span><div class="bar mid"><span style="width:65%"></span></div><span class="t">~9 s</span></div>
  </div>
  <div class="rtnote">Illustrative, for hundreds of vehicles / billions of raw samples. BI figures =
    load a resident extract/model (or a slow DirectQuery round-trip) + first render; the App = a
    pre-materialized aggregate from the warehouse. <b>The App stays flat as the fleet grows</b> (each
    lasso is a bounded query); <b>BI degrades</b> (the resident copy grows with the data).</div>
</section>

<section>
  <div class="eyebrow">The picture in one chart</div>
  <h2>Why massive data breaks classic BI visuals</h2>
  <p class="sub">A chart renders only so many marks — whether the data is loaded resident or queried
    live — so as the dataset grows, the fraction it can show shrinks, and it fills the gap by
    summarizing.</p>

  <figure class="drawfig">
    <svg viewBox="0 0 720 340" role="img" aria-label="As data volume grows on a log scale, a classic BI tool's rendered detail stays flat at a few thousand marks while the data it must represent climbs, opening a widening blind spot; the Databricks App tracks the data because it queries bounded slices instead of rendering everything">
      <!-- axes -->
      <line x1="70" y1="40" x2="70" y2="270" stroke="currentColor" stroke-width="1.2"/>
      <line x1="70" y1="270" x2="680" y2="270" stroke="currentColor" stroke-width="1.2"/>
      <text x="70" y="300" text-anchor="middle" font-family="IBM Plex Mono" font-size="11" fill="var(--slate)">thousands</text>
      <text x="250" y="300" text-anchor="middle" font-family="IBM Plex Mono" font-size="11" fill="var(--slate)">millions</text>
      <text x="430" y="300" text-anchor="middle" font-family="IBM Plex Mono" font-size="11" fill="var(--slate)">100s of millions</text>
      <text x="620" y="300" text-anchor="middle" font-family="IBM Plex Mono" font-size="11" fill="var(--slate)">billions</text>
      <text x="375" y="325" text-anchor="middle" font-family="IBM Plex Mono" font-size="11.5" fill="var(--ink-soft)">data volume (raw samples) →</text>
      <text x="30" y="155" text-anchor="middle" font-family="IBM Plex Mono" font-size="11.5" fill="var(--ink-soft)" transform="rotate(-90 30 155)">fidelity you can actually see →</text>

      <!-- "the data" reference line: climbs with volume -->
      <polyline points="70,250 250,180 430,110 620,55" fill="none" stroke="var(--ink-soft)" stroke-width="1.5" stroke-dasharray="5 4"/>
      <text x="600" y="44" text-anchor="end" font-family="IBM Plex Mono" font-size="11" fill="var(--ink-soft)">the data that exists</text>

      <!-- blind spot: area between BI ceiling and the data line -->
      <path d="M70,250 L250,180 L430,110 L620,55 L620,232 L430,232 L250,232 L70,232 Z"
            fill="var(--hot)" opacity="0.10"/>
      <text x="470" y="175" font-family="IBM Plex Mono" font-size="12" fill="var(--hot)">the blind spot</text>
      <text x="470" y="192" font-family="IBM Plex Mono" font-size="10.5" fill="var(--hot)">summarized / sampled away</text>

      <!-- classic BI ceiling: flat at a few thousand rendered marks -->
      <line x1="70" y1="232" x2="680" y2="232" stroke="var(--hot)" stroke-width="2.4"/>
      <circle cx="70" cy="232" r="3.5" fill="var(--hot)"/>
      <text x="76" y="224" font-family="IBM Plex Mono" font-size="11" fill="var(--hot)">classic BI tool · ~few thousand marks (flat)</text>

      <!-- Databricks App: tracks the data (full fidelity via bounded queries) -->
      <polyline points="70,250 250,180 430,110 620,55" fill="none" stroke="var(--ok)" stroke-width="2.6"/>
      <circle cx="620" cy="55" r="4" fill="var(--ok)"/>
      <text x="612" y="72" text-anchor="end" font-family="IBM Plex Mono" font-size="11" fill="var(--ok)">Databricks App · full fidelity</text>
    </svg>
    <figcaption>A classic BI tool renders a fixed ceiling of marks no matter how much data exists, so the
      gap between “what’s in the data” and “what you can see” widens with scale — and it closes that gap
      by summarizing, which erases the rare outlier. The App tracks the data instead, because it never
      renders everything: it shows a full-resolution aggregate and fetches raw detail in bounded slices.</figcaption>
  </figure>

  <p><strong>Two things break:</strong> <em>rendering</em> (no chart draws a billion marks) and
    <em>residency</em> (the loaded copy grows with the data). The App avoids both — it keeps data in
    the lakehouse and moves only a bounded, already-shaped result to the screen.</p>
</section>

<section>
  <div class="eyebrow">The conclusion</div>
  <h2>Why it can only be the Databricks App</h2>
  <p class="sub">The fidelity argument is decisive on its own — and the same architecture wins on the
    operational points from tab 1 too.</p>
  <div class="reasons">
    <div class="rz"><h4>Fidelity</h4><p>Renders every raw sample and fetches raw detail on demand; BI must summarize.</p></div>
    <div class="rz"><h4>Scalability</h4><p>More vehicles = bigger BI extract and slower refresh; the App’s bounded queries stay flat.</p></div>
    <div class="rz"><h4>Maintenance</h4><p>No separate BI system to license, refresh and govern — it runs on the lakehouse you already have.</p></div>
    <div class="rz"><h4>Licensing</h4><p>No per-seat dashboard subscription; users are served on existing compute.</p></div>
  </div>
  <p class="verdict">The raw data <b>never leaves the lakehouse</b>: a full-resolution aggregate for the
    overview, and a fresh <b>bounded query</b> for every drill. So a Databricks App sees the outlier
    <b>and</b> reaches the raw detail, stays fast as the fleet grows, and needs no separate BI tool to
    license and maintain.</p>
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
