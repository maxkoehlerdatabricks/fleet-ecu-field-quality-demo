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
'  <button class="doctab" data-tab="story"><span class="idx">2</span>The Case</button>\n'
'  <button class="doctab" data-tab="workflow"><span class="idx">3</span>App Workflow</button>\n'
'  <button class="doctab" data-tab="tools"><span class="idx">4</span>Tools</button>\n'
'</div>\n')

# ---------------- TAB 1: flowing narrative ----------------
tab_why = '''<div class="panel-doc active" id="tab-why">
<header>
  <div class="hero">
    <div class="eyebrow">Databricks demo · visualizing massive data</div>
    <h1>Why Databricks Apps</h1>
    <p class="lede">This demo makes one argument: for interactive visualization of <strong>massive
      data</strong> — hundreds of millions of raw rows you need to see, not just summarize — a
      <strong>Databricks App</strong> does what classic BI tools like Power BI, Tableau and Qlik
      structurally cannot. The rest of this document proves it on a concrete example. The example is a
      fleet of EV batteries; the point is general.</p>
  </div>
</header>

<div class="wrap">

<section>
  <div class="eyebrow">The problem, in general</div>
  <h2>Massive data is hard to <em>visualize</em>, not just to store</h2>
  <p class="sub">Storing billions of rows is a solved problem. Letting a human <em>see</em> them —
    interactively, at full detail, to find the rare thing that matters — is where the classic BI tools
    hit a wall. Two limits do it.</p>
  <div class="proof">
    <div class="stat"><div class="k">Rendering ceiling</div><div class="v" style="font-size:26px">~10³–10⁴</div>
      <div class="u">marks a BI chart will draw — then it samples or aggregates the rest</div></div>
    <div class="stat"><div class="k">Data residency</div><div class="v" style="font-size:26px">1 : 1</div>
      <div class="u">a copy of the data (extract / imported model) must be loaded, and it grows with the data</div></div>
    <div class="stat hot"><div class="k">The casualty</div><div class="v" style="font-size:26px">outliers</div>
      <div class="u">the rare rows are exactly what sampling and aggregation erase</div></div>
  </div>
  <p class="callout">A classic BI tool stays fast by keeping a resident copy of the data and drawing
    only a few thousand marks. As the data grows it must summarize harder — and for finding the rare,
    important row, the summary is where the answer disappears.</p>
</section>

<section>
  <div class="eyebrow">The Databricks App answer</div>
  <h2>Keep the data in the lakehouse; move only what the eye needs</h2>
  <p class="sub">A Databricks App is a lightweight web app served next to the lakehouse. It never loads
    a resident copy and never tries to draw everything. Instead it does two things classic BI cannot
    combine at scale:</p>
  <div class="mean">
    <div class="cell"><h4><span class="dot" style="background:var(--ok)"></span>Full-resolution overview</h4>
      <p>The whole dataset is aggregated <em>in the warehouse</em> into a picture that keeps the rare
        cell visible — no client-side point cap, no sampling of the tail.</p></div>
    <div class="cell"><h4><span class="dot" style="background:var(--ok)"></span>Raw detail on demand</h4>
      <p>Any selection becomes a bounded query that fetches just those raw rows from the lakehouse —
        data that was never loaded into the browser.</p></div>
    <div class="cell"><h4><span class="dot" style="background:var(--cool)"></span>Flat with scale</h4>
      <p>Every interaction is a bounded query, so ten times the data barely changes the response time.
        No growing extract, no refresh cliff.</p></div>
    <div class="cell"><h4><span class="dot" style="background:var(--cool)"></span>Custom interaction</h4>
      <p>It is a real app, so it can do things a BI canvas can’t — a lasso that triggers a server-side
        fetch, a sample-size control, a drill that pulls one entity’s full raw signal.</p></div>
  </div>
</section>

<section>
  <div class="eyebrow">This demo, in one line each</div>
  <h2>How the rest of the document proves it</h2>
  <p class="sub">The argument is carried by a concrete example so it stays honest and testable.</p>
  <ul class="products">
    <li><div><div class="pname">2 · The Case</div><div class="psig mono">the example</div></div>
      <p>A fleet of EV batteries. The thing worth finding — a pack running too hot — is a rare, raw,
        seconds-long signal that any average hides. This is the <em>massive-data-visualization</em>
        problem in concrete form.</p></li>
    <li><div><div class="pname">3 · App Workflow</div><div class="psig mono">the solution, working</div></div>
      <p>The live Databricks App, top to bottom: a full-resolution fleet picture, a lasso with a
        sample-size control, and a drill to one vehicle’s complete raw trace.</p></li>
    <li><div><div class="pname">4 · Tools</div><div class="psig mono">the head-to-head</div></div>
      <p>The same three steps attempted in Tableau, Power BI and Qlik — where each falls back to a
        summary, and why. Plus reaction time as the fleet grows.</p></li>
  </ul>
  <p class="verdict">The takeaway you should leave with: <b>when the job is to see and interrogate
    massive data at full fidelity — not just chart a summary of it — a Databricks App is the right
    tool, and a resident-extract BI tool like Power BI is the wrong shape for it.</b> The battery is
    just where you can watch that play out.</p>
</section>
</div>
</div>
'''

tab1 = '''<div class="panel-doc" id="tab-story">
<header>
  <div class="hero">
    <div class="eyebrow">Example case · fleet EV battery</div>
    <h1>The outlier in the pack</h1>
    <p class="lede">The example that carries this demo: a monitor for the <strong>traction batteries
      of a fleet of electric vehicles</strong>. Every pack streams the temperature of its hottest cell,
      ten times a second. The job is to find the one battery, among hundreds, that runs too hot — before
      it becomes a failure. It is a textbook case of needing to <em>see</em> a rare signal inside massive
      raw data.</p>
    <div class="ramp"></div>
    <div class="ramp-labels mono">
      <span>28&nbsp;°C&nbsp;nominal</span><span>45&nbsp;°C&nbsp;elevated</span>
      <span class="hotlab">55&nbsp;°C&nbsp;→&nbsp;thermal&nbsp;risk</span>
    </div>
  </div>
</header>

<div class="wrap">

<section>
  <div class="eyebrow">The product</div>
  <h2>An EV battery, watched one cell at a time</h2>
  <p class="sub">Each vehicle carries a traction battery — a <em>pack</em> of many <em>modules</em>,
    each a stack of <em>cells</em>. A Battery Management System reports the temperature of the hottest
    cell in the pack, about ten times a second, for every car in the fleet.</p>
  <p>A cell that climbs to 70&nbsp;°C for a few seconds during a fast charge is a thermal event — a
    precursor to accelerated aging, capacity loss, and, at the extreme, thermal runaway. One bad cell,
    buried among thousands, is enough to move the number. Finding that pack while it is still just an
    outlier is the whole point of the monitor.</p>
</section>

<section>
  <div class="eyebrow">Why an average hides the fault</div>
  <h2>The dangerous signal is never the average</h2>
  <p class="sub">The fault is a rare, seconds-long deviation. Averaging — over time, over the cells in
    a pack, over the fleet — is exactly what erases it.</p>
  <p>These are the numbers from the demo fleet — 200 cars, three days, 21.6&nbsp;million raw samples:</p>
  <div class="proof">
    <div class="stat cool"><div class="k">Fleet median</div><div class="v">39.1</div>
      <div class="u">°C — what an average dashboard shows</div></div>
    <div class="stat"><div class="k">Top 0.1% of samples</div><div class="v">62.8</div>
      <div class="u">°C — already past the risk line</div></div>
    <div class="stat hot"><div class="k">Hottest sample</div><div class="v">72.5</div>
      <div class="u">°C — from 30 of 200 cars</div></div>
  </div>
  <p class="callout">The whole fleet looks fine at 39&nbsp;°C. The truth — a 72&nbsp;°C excursion on a
    handful of cars — lives in a fraction of a percent of the data. You cannot aggregate your way to
    it. You have to keep every raw sample and go hunting.</p>
</section>

<section>
  <div class="eyebrow">What happened to the battery</div>
  <h2>Reading the outlier is reading a physical failure</h2>
  <p class="sub">The signal is cell temperature, so a hot outlier is a defect you can name. Here is the
    pack, where the number comes from, and what has gone wrong in the cell that runs hot.</p>
DRAWINGS
</section>

<section>
  <div class="eyebrow">What comes next</div>
  <h2>From the fault to finding it</h2>
  <p class="sub">The outlier is real, physical, and rare — a fraction of a percent of the data, alive
    only at the raw sample grain. The next tab, <strong>App Workflow</strong>, shows how the dashboard
    lets you find it: from the whole fleet, down to the one vehicle, without ever averaging the signal
    away.</p>
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
    <div class="eyebrow">Fleet EV Battery · field-quality monitor</div>
    <h1>Why this only works on Databricks&nbsp;Apps</h1>
    <p class="lede">The workflow depends on two things at once: showing a full-resolution picture of
      hundreds of millions of raw samples, and fetching the raw rows behind any selection on demand.
      That combination is outside the model of the classic BI tools. Here is the argument, step by
      step, then the reason it holds.</p>
  </div>
</header>

<div class="wrap">

<section>
  <div class="eyebrow">The root difference</div>
  <h2>Where the data lives decides what the tool can do</h2>
  <p class="sub">Tableau, Power BI and Qlik are all excellent BI tools. But each keeps granular data
    <em>resident</em> — a Hyper extract, an imported model, an in-memory table — and each can only
    render a few thousand marks on a chart. The Databricks App keeps the data in the lakehouse and
    fetches only what each step needs.</p>
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
    <figcaption>A BI tool front-loads a resident copy and renders a capped number of marks, so it must
      summarize. The App leaves the raw data in the lakehouse and each interaction is a bounded query.</figcaption>
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
      <div class="r app yes"><span class="tn">Databricks App</span><span class="mk">✓</span><p>Bins every raw sample in the lakehouse. The outlier cell is drawn.</p></div>
      <div class="r no"><span class="tn">Tableau</span><span class="mk">✕</span><p>Bins into a coarse hexbin to stay fast. The lone hot cell is pooled away.</p></div>
      <div class="r no"><span class="tn">Power BI</span><span class="mk">✕</span><p>Caps a scatter at ~3.5k points (~10k sampled). It drops the rare cell.</p></div>
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
  <div class="rtnote">Illustrative, for a fleet in the hundreds of vehicles / billions of raw samples.
    BI figures reflect building and loading a resident extract / in-memory model (or a slow DirectQuery
    round-trip) plus the first render; the App figure is a pre-materialized aggregate served from the warehouse.</div>
  <p style="margin-top:22px"><strong>Why the App stays flat as the fleet grows.</strong> Its overview
    reads a small pre-computed aggregate, and each lasso is a <em>bounded</em> pushdown query — it
    touches only the sampled vehicles’ rows (helped by clustering the raw table on vehicle id), never
    the whole dataset. Ten times the vehicles barely moves the interaction cost. <strong>Why the BI
    tools degrade:</strong> their speed depends on holding granular data resident, so as the fleet
    grows the extract / model grows, the load and every refresh slow down, and to stay responsive the
    tool summarizes harder — the one thing outlier work cannot afford.</p>
</section>

<section>
  <div class="eyebrow">The picture in one chart</div>
  <h2>Why massive data breaks classic BI visuals</h2>
  <p class="sub">It is a general problem, not specific to batteries. A chart can only render so many
    marks, and a classic BI tool must first load the data it draws from. So as the dataset grows, the
    fraction it can actually show you shrinks — and it fills the gap by summarizing.</p>

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

  <p><strong>The two things that break, in general.</strong> First, <em>rendering</em>: no browser chart
    draws a billion marks, so every tool has a ceiling — the honest question is what it does when the data
    exceeds it. Second, <em>residency</em>: a classic BI tool must load a copy of the data it visualizes
    (an extract, an imported model), and that copy grows with the data until load times and memory make it
    impractical. The App avoids both by keeping the data in the lakehouse and only ever moving a bounded,
    already-shaped result to the screen.</p>
</section>

<section>
  <div class="eyebrow">The conclusion</div>
  <h2>Why it can only be the Databricks App</h2>
  <p class="sub">Line the two requirements up against the one architectural fact and the answer falls out.</p>
  <p>The workflow needs, at the same time: <strong>(1)</strong> a full-resolution view of hundreds of
    millions of raw samples — no sampling, no coarse bins, or the outlier disappears; and
    <strong>(2)</strong> the raw rows behind any brushed region, fetched on demand — because the
    diagnosis lives in the raw shape, not a summary.</p>
  <p>Tableau, Power BI and Qlik can each do neither at fleet scale, for the same root reason: they
    render from a <em>resident copy</em> and cap the marks they draw, so they must summarize to stay
    responsive, and their selection works only over what is already loaded. Turning up the data makes
    both problems worse.</p>
  <p class="verdict">The Databricks App inverts that. The raw data <b>never leaves the lakehouse</b>:
    the overview is a full-resolution aggregate computed there, and every lasso is a fresh
    <b>bounded query</b> that fetches only the rows that step needs — the density grid, then the
    sampled vehicles’ raw traces, then one vehicle’s full signal. Nothing large is ever resident, so
    it renders the outlier <b>and</b> reaches the raw detail, and it stays fast as the fleet grows.
    That is why the workflow is native to a Databricks App and not to a resident-extract BI tool.</p>
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
