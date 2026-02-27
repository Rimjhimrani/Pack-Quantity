import streamlit as st
import pandas as pd
import itertools
import io

st.set_page_config(page_title="AgiloPack", layout="wide", page_icon="▪")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif;
    background: #f7f4ef !important;
    color: #111 !important;
}

/* ─── LAYOUT SHELL ─── */
.block-container {
    max-width: 960px !important;
    padding: 0 2rem 4rem 2rem !important;
}

/* ─── MASTHEAD ─── */
.masthead {
    border-bottom: 3px solid #111;
    padding: 2.5rem 0 1.2rem 0;
    margin-bottom: 0;
    display: flex;
    align-items: baseline;
    gap: 1.4rem;
}
.masthead-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 4.2rem;
    letter-spacing: 4px;
    color: #111;
    line-height: 1;
}
.masthead-accent {
    display: inline-block;
    width: 10px; height: 10px;
    background: #e63329;
    border-radius: 50%;
    margin-bottom: 6px;
}
.masthead-tagline {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 2px;
    color: #888;
    text-transform: uppercase;
    border-left: 2px solid #ccc;
    padding-left: 1rem;
}

/* ─── STEP RIBBON ─── */
.ribbon {
    display: flex;
    border-bottom: 1px solid #ddd;
    margin-bottom: 3rem;
}
.rib-item {
    flex: 1;
    padding: 0.7rem 0;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #aaa;
    text-align: center;
    border-right: 1px solid #ddd;
    position: relative;
}
.rib-item:last-child { border-right: none; }
.rib-item.active {
    color: #111;
    font-weight: 500;
}
.rib-item.active::after {
    content: '';
    position: absolute;
    bottom: -1px; left: 0; right: 0;
    height: 3px;
    background: #e63329;
}
.rib-item.done { color: #555; }
.rib-num {
    display: block;
    font-size: 1.1rem;
    font-family: 'Bebas Neue', sans-serif;
    letter-spacing: 2px;
    margin-bottom: 2px;
}

/* ─── SECTION HEADING ─── */
.sec-head {
    display: flex;
    align-items: center;
    gap: 1.2rem;
    margin-bottom: 0.4rem;
}
.sec-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5rem;
    line-height: 1;
    color: #e8e4dc;
    letter-spacing: 2px;
    user-select: none;
}
.sec-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    letter-spacing: 2px;
    color: #111;
}
.sec-rule {
    border: none;
    border-top: 1px solid #ccc;
    margin-bottom: 2rem;
}
.sec-desc {
    font-size: 0.88rem;
    color: #555;
    line-height: 1.6;
    margin-bottom: 2rem;
    max-width: 540px;
}

/* ─── DATA PILL GRID ─── */
.pill-row {
    display: flex;
    gap: 0;
    margin-bottom: 2rem;
    border: 1px solid #ddd;
    border-radius: 0;
    overflow: hidden;
}
.pill {
    flex: 1;
    padding: 0.9rem 1.2rem;
    border-right: 1px solid #ddd;
    background: #fff;
}
.pill:last-child { border-right: none; }
.pill-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 3px;
}
.pill-val {
    font-family: 'DM Mono', monospace;
    font-size: 1rem;
    font-weight: 500;
    color: #111;
}

/* ─── BOX SELECTOR GRID ─── */
.bx-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0;
    border: 1px solid #ddd;
    margin-bottom: 2rem;
    overflow: hidden;
}
.bx-item {
    padding: 1rem 1.2rem;
    border-right: 1px solid #ddd;
    border-bottom: 1px solid #ddd;
    cursor: default;
    background: #fff;
    transition: background 0.15s;
}
.bx-item:nth-child(4n) { border-right: none; }
.bx-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1rem;
    letter-spacing: 1.5px;
    color: #111;
    margin-bottom: 4px;
}
.bx-dims {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #888;
}
.bx-vol {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: #bbb;
    margin-top: 4px;
}

/* ─── STAT GRID ─── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0;
    border: 1px solid #ddd;
    overflow: hidden;
    margin-bottom: 2.5rem;
    background: #fff;
}
.stat-cell {
    padding: 1.4rem 1.6rem;
    border-right: 1px solid #ddd;
}
.stat-cell:last-child { border-right: none; }
.stat-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 6px;
}
.stat-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    letter-spacing: 1px;
    color: #111;
    line-height: 1;
}
.stat-value.red { color: #e63329; }

/* ─── TABLE ─── */
.results-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.82rem;
    background: #fff;
    border: 1px solid #ddd;
    margin-bottom: 2rem;
}
.results-table th {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #999;
    padding: 0.7rem 1rem;
    text-align: left;
    border-bottom: 2px solid #111;
    background: #fff;
    white-space: nowrap;
}
.results-table td {
    padding: 0.85rem 1rem;
    border-bottom: 1px solid #eee;
    color: #222;
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
}
.results-table tr:last-child td { border-bottom: none; }
.results-table tr:hover td { background: #faf8f4; }
.util-bar-wrap {
    background: #f0ece5;
    border-radius: 0;
    height: 6px;
    width: 100%;
    margin-top: 4px;
    overflow: hidden;
}
.util-bar {
    height: 100%;
    background: #e63329;
    transition: width 0.6s ease;
}
.util-high { background: #2a9d5c; }

/* ─── TOGGLE SECTION ─── */
.toggle-row {
    display: flex;
    gap: 0;
    border: 1px solid #ddd;
    overflow: hidden;
    margin-bottom: 2rem;
    background: #fff;
}
.toggle-opt {
    flex: 1;
    padding: 1rem 1.2rem;
    border-right: 1px solid #ddd;
    cursor: default;
}
.toggle-opt:last-child { border-right: none; }
.toggle-label {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1rem;
    letter-spacing: 1.5px;
    color: #111;
}
.toggle-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: #999;
    margin-top: 3px;
}

/* ─── STREAMLIT OVERRIDES ─── */
.stButton > button {
    background: #111 !important;
    color: #f7f4ef !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 0.75rem 2.5rem !important;
    transition: background 0.15s !important;
    box-shadow: none !important;
    font-weight: 500 !important;
}
.stButton > button:hover {
    background: #e63329 !important;
    transform: none !important;
    box-shadow: none !important;
}

[data-testid="stDownloadButton"] > button {
    background: #2a9d5c !important;
    color: #fff !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: #1e7a46 !important;
}

div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stFileUploader"] label,
.stRadio label, .stCheckbox label,
[data-testid="stWidgetLabel"] p {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: #666 !important;
    font-weight: 400 !important;
}

div[data-testid="stSelectbox"] > div > div,
div[data-testid="stNumberInput"] input {
    background: #fff !important;
    border: 1px solid #ddd !important;
    border-radius: 0 !important;
    color: #111 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}

div[data-testid="stSlider"] > div {
    accent-color: #e63329;
}

.stSuccess, [data-testid="stAlert"] {
    background: #eef8f3 !important;
    border: 1px solid #2a9d5c !important;
    border-radius: 0 !important;
    color: #1a5c35 !important;
}
.stSuccess p { color: #1a5c35 !important; }

[data-testid="stFileUploader"] {
    border: 2px dashed #ccc !important;
    border-radius: 0 !important;
    background: #fff !important;
}

.stDataFrame { display: none; }

div[data-baseweb="radio"] label span { color: #111 !important; }
div[data-baseweb="checkbox"] label span { color: #111 !important; }

[data-testid="stVerticalBlock"] { gap: 0.6rem !important; }

footer { display: none !important; }
#MainMenu { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── State ──────────────────────────────────────────────────────────────────────
for k, v in [('step', 1), ('data', {}), ('mapping_confirmed', False)]:
    if k not in st.session_state:
        st.session_state[k] = v

def next_step(): st.session_state.step += 1
def reset_process():
    for k in list(st.session_state.keys()): del st.session_state[k]
    st.rerun()

# ── Engine ────────────────────────────────────────────────────────────────────
def calculate_fit(box_dim, part_dim, nested, nest_pct, stacking, fragile):
    bl, bw, bh = box_dim
    p = list(part_dim)
    labels = {0: "Breadthwise", 1: "Lengthwise", 2: "Heightwise"}
    best_count, best_info = 0, None
    for idx in itertools.permutations([0, 1, 2]):
        ow, ol, oh = p[idx[0]], p[idx[1]], p[idx[2]]
        if fragile == "Fragile" and idx[2] != 2: continue
        cols, rows = bw // ow, bl // ol
        per_layer = cols * rows
        if per_layer <= 0: continue
        if not stacking:
            total = per_layer
        elif nested:
            inc = oh * (nest_pct / 100)
            layers = 1 + int((bh - oh) // inc) if (bh >= oh and inc > 0) else 1
            total = per_layer * max(1, layers)
        else:
            total = per_layer * (bh // oh)
        if total > best_count:
            best_count = int(total)
            best_info = {"count": best_count, "dims": f"{ow}×{ol}×{oh}",
                         "orientation": labels[idx[2]],
                         "used_vol": round(best_count * p[0]*p[1]*p[2], 2)}
    if not best_info: return None
    bvol = bw * bl * bh
    best_info["util"] = round((best_info["used_vol"] / bvol) * 100, 2)
    best_info["unused"] = round(bvol - best_info["used_vol"], 2)
    return best_info

# ── Masthead ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
  <div>
    <span class="masthead-logo">AgiloPack</span><span class="masthead-accent"></span>
  </div>
  <div class="masthead-tagline">Box Space Utilization</div>
</div>
""", unsafe_allow_html=True)

# ── Step Ribbon ───────────────────────────────────────────────────────────────
STEPS = ["Box", "Data", "Nesting", "Handling", "Results"]
cur = st.session_state.step
ribbon_html = '<div class="ribbon">'
for i, s in enumerate(STEPS, 1):
    cls = "active" if i == cur else ("done" if i < cur else "")
    ribbon_html += f'<div class="rib-item {cls}"><span class="rib-num">0{i}</span>{s}</div>'
ribbon_html += '</div>'
st.markdown(ribbon_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — BOX
# ─────────────────────────────────────────────────────────────────────────────
if cur == 1:
    st.markdown("""
    <div class="sec-head">
      <span class="sec-num">01</span>
      <span class="sec-title">Select Box Size</span>
    </div>
    <hr class="sec-rule">
    <p class="sec-desc">Choose a standard shipping configuration or define custom dimensions in millimetres (L × W × H).</p>
    """, unsafe_allow_html=True)

    BOXES = {
        "A": (120, 80, 80), "B": (200, 180, 120), "C": (360, 360, 100),
        "D": (400, 300, 220), "E": (600, 500, 400), "F": (850, 400, 250),
        "G": (1200, 1000, 250), "H": (1500, 1200, 1000),
    }

    grid_html = '<div class="bx-grid">'
    for k, v in BOXES.items():
        grid_html += f"""<div class="bx-item">
          <div class="bx-name">Option {k}</div>
          <div class="bx-dims">{v[0]} × {v[1]} × {v[2]} mm</div>
          <div class="bx-vol">{v[0]*v[1]*v[2]:,} mm³</div>
        </div>"""
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

    box_type = st.radio("Input type", ["Predefined", "Custom"], horizontal=True)

    if box_type == "Predefined":
        opts = {f"Option {k} — {v[0]}×{v[1]}×{v[2]}": v for k, v in BOXES.items()}
        sel = st.selectbox("Box selection", list(opts.keys()))
        dims = opts[sel]
    else:
        c1, c2, c3 = st.columns(3)
        l = c1.number_input("Length (mm)", min_value=1.0, value=50.0)
        w = c2.number_input("Width (mm)", min_value=1.0, value=50.0)
        h = c3.number_input("Height (mm)", min_value=1.0, value=50.0)
        dims = (l, w, h)

    st.session_state.data['box'] = dims
    st.markdown(f"""
    <div class="pill-row">
      <div class="pill"><div class="pill-label">Length</div><div class="pill-val">{dims[0]} mm</div></div>
      <div class="pill"><div class="pill-label">Width</div><div class="pill-val">{dims[1]} mm</div></div>
      <div class="pill"><div class="pill-label">Height</div><div class="pill-val">{dims[2]} mm</div></div>
      <div class="pill"><div class="pill-label">Volume</div><div class="pill-val">{int(dims[0]*dims[1]*dims[2]):,} mm³</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.button("Continue →", on_click=next_step)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — DATA
# ─────────────────────────────────────────────────────────────────────────────
elif cur == 2:
    st.markdown("""
    <div class="sec-head">
      <span class="sec-num">02</span>
      <span class="sec-title">Upload Part Data</span>
    </div>
    <hr class="sec-rule">
    <p class="sec-desc">Upload a CSV or Excel file with your parts list, then map columns to the correct dimension fields.</p>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Drop file here", type=["csv", "xlsx"])

    if uploaded_file:
        if 'raw_df' not in st.session_state:
            st.session_state.raw_df = (
                pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv')
                else pd.read_excel(uploaded_file)
            )
        df = st.session_state.raw_df
        st.markdown(f"""
        <div class="pill-row">
          <div class="pill"><div class="pill-label">File</div><div class="pill-val" style="font-size:0.8rem">{uploaded_file.name}</div></div>
          <div class="pill"><div class="pill-label">Rows</div><div class="pill-val">{len(df)}</div></div>
          <div class="pill"><div class="pill-label">Columns</div><div class="pill-val">{len(df.columns)}</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<p class="sec-desc" style="margin-top:1rem">Map your file columns:</p>', unsafe_allow_html=True)
        cols = df.columns.tolist()
        c1, c2, c3, c4 = st.columns(4)
        n_col = c1.selectbox("Part name column", cols)
        w_col = c2.selectbox("Width column", cols)
        l_col = c3.selectbox("Length column", cols)
        h_col = c4.selectbox("Height column", cols)

        if st.button("Confirm mapping →"):
            mapped = df[[n_col, w_col, l_col, h_col]].copy()
            mapped.columns = ['Part_Name', 'Width', 'Length', 'Height']
            for c in ['Width', 'Length', 'Height']:
                mapped[c] = pd.to_numeric(mapped[c], errors='coerce').fillna(0)
            st.session_state.data['parts_df'] = mapped
            st.session_state.mapping_confirmed = True

        if st.session_state.mapping_confirmed:
            st.success(f"✓  {len(st.session_state.data['parts_df'])} parts mapped and ready.")
            st.button("Continue →", on_click=next_step)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — NESTING
# ─────────────────────────────────────────────────────────────────────────────
elif cur == 3:
    st.markdown("""
    <div class="sec-head">
      <span class="sec-num">03</span>
      <span class="sec-title">Nesting Configuration</span>
    </div>
    <hr class="sec-rule">
    <p class="sec-desc">If parts can be placed inside one another (e.g. stacked cups), enable nesting and set the insertion depth as a percentage of part height.</p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="toggle-row">
      <div class="toggle-opt">
        <div class="toggle-label">Nesting</div>
        <div class="toggle-sub">Allows parts to sit inside each other</div>
      </div>
      <div class="toggle-opt">
        <div class="toggle-label">No Nesting</div>
        <div class="toggle-sub">Each part occupies its full volume</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    is_nested = st.checkbox("Enable nesting")
    nest_pct = 0

    if is_nested:
        nest_pct = st.slider("Nesting depth (% of part height)", 1, 100, 20)
        st.markdown(f"""
        <div class="pill-row">
          <div class="pill"><div class="pill-label">Depth</div><div class="pill-val">{nest_pct}%</div></div>
          <div class="pill"><div class="pill-label">Space Saved</div><div class="pill-val">{100 - nest_pct}%</div></div>
          <div class="pill"><div class="pill-label">Added Height</div><div class="pill-val">{nest_pct}% per part</div></div>
        </div>
        """, unsafe_allow_html=True)

    st.session_state.data.update({'nested': is_nested, 'nest_pct': nest_pct})
    st.button("Continue →", on_click=next_step)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — HANDLING
# ─────────────────────────────────────────────────────────────────────────────
elif cur == 4:
    st.markdown("""
    <div class="sec-head">
      <span class="sec-num">04</span>
      <span class="sec-title">Handling Rules</span>
    </div>
    <hr class="sec-rule">
    <p class="sec-desc">Define physical packing constraints. Fragile parts must remain upright; non-stackable parts are packed in a single layer.</p>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        stacking_opt = st.radio("Stacking", ["Allowed", "Not allowed"])
    with c2:
        fragility_opt = st.selectbox("Fragility", ["Non-Fragile", "Fragile"])

    stacking = (stacking_opt == "Allowed")
    fragility = fragility_opt

    st.markdown(f"""
    <div class="pill-row" style="margin-top:1.5rem">
      <div class="pill"><div class="pill-label">Stacking</div><div class="pill-val">{"Allowed" if stacking else "Disabled"}</div></div>
      <div class="pill"><div class="pill-label">Fragility</div><div class="pill-val">{fragility}</div></div>
      <div class="pill"><div class="pill-label">Orientation Locked</div><div class="pill-val">{"Yes" if fragility == "Fragile" else "No"}</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.session_state.data.update({'stacking': stacking, 'fragility': fragility})
    st.button("Run analysis →", on_click=next_step)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — RESULTS
# ─────────────────────────────────────────────────────────────────────────────
elif cur == 5:
    box = st.session_state.data['box']
    df = st.session_state.data['parts_df']
    results = []

    for _, row in df.iterrows():
        res = calculate_fit(
            box, (row['Width'], row['Length'], row['Height']),
            st.session_state.data['nested'], st.session_state.data['nest_pct'],
            st.session_state.data['stacking'], st.session_state.data['fragility']
        )
        if res:
            results.append({
                "Part Name": row['Part_Name'],
                "Parts / Box": res['count'],
                "Orientation": res['dims'],
                "Placement": res['orientation'],
                "Utilization": res['util'],
                "Unused (mm³)": int(res['unused'])
            })

    res_df = pd.DataFrame(results)
    avg_util = res_df["Utilization"].mean() if len(res_df) else 0
    box_vol = box[0] * box[1] * box[2]
    best_part = res_df.loc[res_df["Utilization"].idxmax(), "Part Name"] if len(res_df) else "—"

    st.markdown("""
    <div class="sec-head">
      <span class="sec-num">05</span>
      <span class="sec-title">Results</span>
    </div>
    <hr class="sec-rule">
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stat-grid">
      <div class="stat-cell">
        <div class="stat-label">Parts Analysed</div>
        <div class="stat-value">{len(res_df)}</div>
      </div>
      <div class="stat-cell">
        <div class="stat-label">Avg Utilization</div>
        <div class="stat-value red">{avg_util:.1f}%</div>
      </div>
      <div class="stat-cell">
        <div class="stat-label">Box Volume</div>
        <div class="stat-value">{box_vol:,}</div>
      </div>
      <div class="stat-cell">
        <div class="stat-label">Best Part</div>
        <div class="stat-value" style="font-size:1.2rem;letter-spacing:0">{best_part}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Custom table
    table_html = """
    <table class="results-table">
      <thead>
        <tr>
          <th>Part Name</th>
          <th>Parts / Box</th>
          <th>Orientation</th>
          <th>Placement</th>
          <th>Utilization</th>
          <th>Unused (mm³)</th>
        </tr>
      </thead>
      <tbody>
    """
    for _, row in res_df.iterrows():
        u = row["Utilization"]
        bar_cls = "util-bar util-high" if u >= 60 else "util-bar"
        table_html += f"""
        <tr>
          <td>{row["Part Name"]}</td>
          <td>{row["Parts / Box"]}</td>
          <td>{row["Orientation"]}</td>
          <td>{row["Placement"]}</td>
          <td>
            {u:.1f}%
            <div class="util-bar-wrap"><div class="{bar_cls}" style="width:{min(u,100):.1f}%"></div></div>
          </td>
          <td>{row["Unused (mm³)"]:,}</td>
        </tr>"""
    table_html += "</tbody></table>"
    st.markdown(table_html, unsafe_allow_html=True)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        res_df.to_excel(writer, index=False, sheet_name='AgiloPack')

    c1, c2 = st.columns([1, 1])
    with c1:
        st.download_button("Download report (.xlsx)", data=output.getvalue(),
                           file_name='AgiloPack_Analysis.xlsx',
                           mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    with c2:
        st.button("Start over", on_click=reset_process)
