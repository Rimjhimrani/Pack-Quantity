import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import io
import math

st.set_page_config(page_title="AgiloPack", layout="wide", page_icon="▪")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif;
    background: #f5f2ec !important;
    color: #111 !important;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: radial-gradient(circle, #c8c2b4 1px, transparent 1px);
    background-size: 28px 28px;
    opacity: 0.18;
    pointer-events: none;
    z-index: 0;
}

.block-container {
    max-width: 1100px !important;
    padding: 0 2rem 5rem 2rem !important;
    position: relative;
    z-index: 1;
}

.masthead {
    border-bottom: 3px solid #111;
    padding: 4rem 0 1.4rem 0;
    margin-bottom: 0;
    display: flex;
    align-items: baseline;
    gap: 1.6rem;
    animation: fadeSlideDown 0.5s ease both;
}
@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.masthead-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 4.4rem;
    letter-spacing: 5px;
    color: #111;
    line-height: 1;
}
.masthead-accent {
    display: inline-block;
    width: 11px; height: 11px;
    background: #e63329;
    border-radius: 50%;
    margin-bottom: 7px;
    animation: pulse 2.5s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50%       { transform: scale(1.35); opacity: 0.7; }
}
.masthead-tagline {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 2.5px;
    color: #999;
    text-transform: uppercase;
    border-left: 2px solid #ccc;
    padding-left: 1.1rem;
}
.masthead-version {
    margin-left: auto;
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 1.5px;
    color: #bbb;
    text-transform: uppercase;
    align-self: center;
}

.ribbon {
    display: flex;
    border-bottom: 1px solid #ddd;
    margin-bottom: 3rem;
    background: #fff;
    animation: fadeSlideDown 0.5s 0.1s ease both;
}
.rib-item {
    flex: 1;
    padding: 0.9rem 0;
    font-family: 'DM Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #bbb;
    text-align: center;
    border-right: 1px solid #eee;
    position: relative;
    transition: color 0.2s;
}
.rib-item:last-child { border-right: none; }
.rib-item.active { color: #111; font-weight: 500; }
.rib-item.active::after {
    content: '';
    position: absolute;
    bottom: -1px; left: 0; right: 0;
    height: 3px;
    background: #e63329;
    animation: expandX 0.35s ease both;
}
@keyframes expandX {
    from { transform: scaleX(0); }
    to   { transform: scaleX(1); }
}
.rib-item.done { color: #666; }
.rib-item.done::after {
    content: '';
    position: absolute;
    bottom: -1px; left: 0; right: 0;
    height: 3px;
    background: #111;
}
.rib-num {
    display: block;
    font-size: 1.15rem;
    font-family: 'Bebas Neue', sans-serif;
    letter-spacing: 2px;
    margin-bottom: 2px;
}

.sec-head {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.3rem;
    animation: fadeSlideDown 0.4s 0.15s ease both;
}
.sec-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5.5rem;
    line-height: 1;
    color: #e8e4dc;
    letter-spacing: 2px;
    user-select: none;
}
.sec-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.1rem;
    letter-spacing: 2.5px;
    color: #111;
}
.sec-rule {
    border: none;
    border-top: 1px solid #d5d0c8;
    margin-bottom: 2rem;
}
.sec-desc {
    font-size: 0.86rem;
    color: #777;
    line-height: 1.65;
    margin-bottom: 2rem;
    max-width: 560px;
    animation: fadeSlideDown 0.4s 0.2s ease both;
}

.bx-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0;
    border: 1px solid #ddd;
    margin-bottom: 2rem;
    overflow: hidden;
    background: #fff;
    animation: fadeSlideDown 0.4s 0.2s ease both;
}
.bx-item {
    padding: 1.1rem 1.3rem;
    border-right: 1px solid #eee;
    border-bottom: 1px solid #eee;
    background: #fff;
    transition: background 0.15s;
    position: relative;
    overflow: hidden;
}
.bx-item::before {
    content: '';
    position: absolute;
    inset: 0;
    background: #e63329;
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.2s ease;
    z-index: 0;
}
.bx-item:hover::before { transform: scaleX(1); }
.bx-item:hover .bx-name,
.bx-item:hover .bx-dims,
.bx-item:hover .bx-type,
.bx-item:hover .bx-tare { color: #fff; }
.bx-item:nth-child(4n) { border-right: none; }
.bx-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.05rem;
    letter-spacing: 1.5px;
    color: #111;
    margin-bottom: 4px;
    position: relative; z-index: 1;
    transition: color 0.15s;
}
.bx-dims {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: #999;
    position: relative; z-index: 1;
    transition: color 0.15s;
}
.bx-type {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    color: #bbb;
    margin-top: 3px;
    position: relative; z-index: 1;
    transition: color 0.15s;
}
.bx-tare {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    color: #ccc;
    margin-top: 2px;
    position: relative; z-index: 1;
    transition: color 0.15s;
}

.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0;
    border: 1px solid #ddd;
    overflow: hidden;
    margin-bottom: 2.5rem;
    background: #fff;
    animation: fadeSlideDown 0.4s 0.1s ease both;
}
.stat-cell {
    padding: 1.6rem 1.8rem;
    border-right: 1px solid #eee;
    position: relative;
}
.stat-cell:last-child { border-right: none; }
.stat-cell::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: #e8e4dc;
}
.stat-cell:first-child::after { background: #111; }
.stat-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #aaa;
    margin-bottom: 8px;
}
.stat-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.6rem;
    letter-spacing: 1px;
    color: #111;
    line-height: 1;
}
.stat-value.red { color: #e63329; }

.stButton > button {
    background: #111 !important;
    color: #f5f2ec !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.76rem !important;
    letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    padding: 0.8rem 2.8rem !important;
    transition: background 0.2s, letter-spacing 0.2s !important;
}
.stButton > button:hover {
    background: #e63329 !important;
    letter-spacing: 3.5px !important;
}

[data-testid="stDownloadButton"] > button {
    background: #1a7d48 !important;
    color: #fff !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: #15603a !important;
}

div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stFileUploader"] label,
.stRadio label, [data-testid="stWidgetLabel"] p {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.67rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #888 !important;
}

div[data-testid="stSelectbox"] > div > div,
div[data-testid="stNumberInput"] input {
    background: #fff !important;
    border: 1px solid #ddd !important;
    border-radius: 0 !important;
    font-family: 'DM Mono', monospace !important;
}

[data-testid="stFileUploader"] {
    border: 2px dashed #ccc !important;
    border-radius: 0 !important;
    background: #fff !important;
}
[data-testid="stFileUploader"]:hover { border-color: #e63329 !important; }

div[data-testid="stAlert"] {
    border-radius: 0 !important;
    border-left: 3px solid #111 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
}

.stRadio > div { gap: 0 !important; }
.stRadio > div > label {
    border: 1px solid #ddd !important;
    border-right: none !important;
    padding: 0.5rem 1rem !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    background: #fff !important;
    cursor: pointer;
}
.stRadio > div > label:last-child { border-right: 1px solid #ddd !important; }
.stRadio > div > label:has(input:checked) {
    background: #e63329 !important;
    color: #fff !important;
    border-color: #e63329 !important;
}

.weight-badge {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 0.25rem 0.7rem;
    margin-bottom: 1.5rem;
    border: 1px solid;
}
.weight-badge.detected    { color: #1a7d48; border-color: #1a7d48; background: #f0faf5; }
.weight-badge.not-detected { color: #999;   border-color: #ccc;    background: #fafafa; }

.dl-hint {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 1.5px;
    color: #aaa;
    text-transform: uppercase;
    margin-top: 0.4rem;
}

footer { display: none !important; }
#MainMenu { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Box Catalogue (dimensions + tare weights from Excel template) ─────────────
BOXES = {
    "A": {"dims": (120,  80,   80),  "tare": 0.4,   "type": "Bin"},
    "B": {"dims": (200,  180,  120), "tare": 0.5,   "type": "Bin"},
    "C": {"dims": (300,  240,  120), "tare": 0.6,   "type": "Bin"},
    "D": {"dims": (400,  300,  220), "tare": 0.8,   "type": "Bin"},
    "E": {"dims": (600,  500,  400), "tare": 1.0,   "type": "Bin"},
    "F": {"dims": (800,  600,  600), "tare": 15.0,  "type": "Customized Box/Trolley/Supplier Box"},
    "G": {"dims": (1200, 1000, 1000),"tare": 40.0,  "type": "Customized Box/Trolley/Supplier Box"},
    "H": {"dims": (1650, 1200, 1000),"tare": 100.0, "type": "Customized Box/Trolley/Supplier Box"},
}

# ── Formula Logic (exact Excel replication) ───────────────────────────────────

def rounddown(x):
    return math.floor(x) if x >= 0 else math.ceil(x)


def calc_qty(box_L, box_W, box_H, part_L, part_W, part_H, unit_weight, tare, has_weight):
    """
    Exact Excel formula — 2 orientation options:

    Option 1 (Length–Length):
      cols  = ROUNDDOWN(box_L / part_L)
      rows  = ROUNDDOWN(box_W / part_W)
      layer = IF(ROUNDDOWN(box_H / part_H) >= 1, 1, 0)   ← inclusive >=
      Qty   = cols × rows × layer

    Option 2 (Length–Width):
      cols  = ROUNDDOWN(box_L / part_W)
      rows  = ROUNDDOWN(box_W / part_L)
      layer = IF(ROUNDDOWN(box_H / part_H) > 1, 1, 0)    ← strict > (must exceed 1)
      Qty   = cols × rows × layer

    Box Weight = Qty × Unit Weight + Tare  (only when unit weight present)
    """
    h_ratio = rounddown(box_H / part_H)

    o1_qty = rounddown(box_L / part_L) * rounddown(box_W / part_W) * (1 if h_ratio >= 1 else 0)
    o1_wt  = round(o1_qty * unit_weight + tare, 3) if (has_weight and unit_weight is not None) else ""

    o2_qty = rounddown(box_L / part_W) * rounddown(box_W / part_L) * (1 if h_ratio > 1 else 0)
    o2_wt  = round(o2_qty * unit_weight + tare, 3) if (has_weight and unit_weight is not None) else ""

    options = [
        {"option": "Option 1 (L–L)", "qty": o1_qty, "box_weight": o1_wt,
         "per_axis": f"rd(bL/pL)={rounddown(box_L/part_L)} × rd(bW/pW)={rounddown(box_W/part_W)} × H-ratio:{h_ratio}"},
        {"option": "Option 2 (L–W)", "qty": o2_qty, "box_weight": o2_wt,
         "per_axis": f"rd(bL/pW)={rounddown(box_L/part_W)} × rd(bW/pL)={rounddown(box_W/part_L)} × H-ratio:{h_ratio}"},
    ]
    best = max(options, key=lambda x: x["qty"])
    return options, best


def run_analysis(df, box_mode, custom_box=None, custom_tare=0.0, has_weight=False):
    results = []

    for _, row in df.iterrows():
        part_L    = float(row["Length"])
        part_W    = float(row["Width"])
        part_H    = float(row["Height"])
        part_name = str(row.get("Part Name", f"Part {_+1}"))

        unit_w = None
        if has_weight:
            val = row.get("Unit Weight", None)
            try:
                unit_w = float(val) if val is not None and str(val).strip() != "" else None
            except (ValueError, TypeError):
                unit_w = None

        boxes_to_run = {"Custom": {"dims": custom_box, "tare": custom_tare, "type": "Manual Entry"}} \
                       if box_mode == "Manual" else BOXES

        for bkey, bdata in boxes_to_run.items():
            box_L, box_W, box_H = bdata["dims"]
            tare = bdata["tare"]
            opts, best = calc_qty(box_L, box_W, box_H, part_L, part_W, part_H, unit_w, tare, has_weight)
            label = bkey if box_mode == "Manual" else f"Option {bkey}"
            results.append({
                "Part Name":        part_name,
                "Part L×W×H (mm)":  f"{part_L:.0f}×{part_W:.0f}×{part_H:.0f}",
                "Unit Weight (kg)": unit_w if unit_w is not None else "",
                "Box":              label,
                "Box Type":         bdata["type"],
                "Box L×W×H (mm)":   f"{box_L}×{box_W}×{box_H}",
                "Best Option":      best["option"],
                "Best Qty / Box":   best["qty"],
                "Box Weight (kg)":  best["box_weight"],
                "Per Axis":         best["per_axis"],
                "Opt1 Qty":         opts[0]["qty"],
                "Opt1 Wt":          opts[0]["box_weight"],
                "Opt2 Qty":         opts[1]["qty"],
                "Opt2 Wt":          opts[1]["box_weight"],
            })
    return pd.DataFrame(results)


# ── Session State ─────────────────────────────────────────────────────────────
if 'step' not in st.session_state: st.session_state.step = 1
if 'data' not in st.session_state: st.session_state.data = {}

def reset_process():
    for k in list(st.session_state.keys()): del st.session_state[k]
    st.rerun()

# ── Masthead ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
  <div>
    <span class="masthead-logo">AgiloPack</span><span class="masthead-accent"></span>
  </div>
  <div class="masthead-tagline">Box Space Utilization</div>
  <div class="masthead-version">v5.0 · Excel Formula Engine</div>
</div>
""", unsafe_allow_html=True)

STEPS = ["Upload & Config", "Results"]
ribbon_html = '<div class="ribbon">'
for i, s in enumerate(STEPS, 1):
    cls = "active" if i == st.session_state.step else ("done" if i < st.session_state.step else "")
    ribbon_html += f'<div class="rib-item {cls}"><span class="rib-num">0{i}</span>{s}</div>'
ribbon_html += '</div>'
st.markdown(ribbon_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — Upload & Config
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.step == 1:
    st.markdown("""
    <div class="sec-head">
      <span class="sec-num">01</span>
      <span class="sec-title">Upload & Configuration</span>
    </div>
    <hr class="sec-rule">
    <p class="sec-desc">Upload a CSV or Excel file with part dimensions. Required columns: <strong>Part Name, Length, Width, Height</strong>. Optional: <strong>Unit Weight</strong> — if present, box weight is auto-calculated as <em>Qty × Unit Weight + Box Tare</em>.</p>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Drop part file here (CSV or Excel)", type=["csv", "xlsx"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        df.columns = [c.strip() for c in df.columns]

        has_weight = "Unit Weight" in df.columns
        st.info(f"⬡  {len(df)} row{'s' if len(df) != 1 else ''} loaded — columns: {', '.join(df.columns.tolist())}")

        if has_weight:
            st.markdown('<div class="weight-badge detected">⬡ Unit Weight detected — Box Weight = Qty × Unit Weight + Box Tare</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="weight-badge not-detected">○ No Unit Weight column — Box Weight column will be empty</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        box_mode = st.radio("Box selection mode", ["Predefined Catalogue", "Manual Box Size Entry"], horizontal=False)

        st.markdown("""
        <div style="font-family:'DM Mono',monospace;font-size:0.62rem;letter-spacing:1.5px;
                    text-transform:uppercase;color:#aaa;margin:0.4rem 0 1.2rem 0;">
            ↳ Opt 1 (L–L): rd(bL/pL) × rd(bW/pW) × IF(rd(bH/pH) ≥ 1, 1, 0)
            &nbsp;|&nbsp;
            Opt 2 (L–W): rd(bL/pW) × rd(bW/pL) × IF(rd(bH/pH) &gt; 1, 1, 0)
        </div>
        """, unsafe_allow_html=True)

        custom_box  = None
        custom_tare = 0.0
        if box_mode == "Manual Box Size Entry":
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            bl = c1.number_input("Box Length (mm)", value=400, step=10)
            bw = c2.number_input("Box Width (mm)",  value=300, step=10)
            bh = c3.number_input("Box Height (mm)", value=200, step=10)
            custom_box = (bl, bw, bh)
            if has_weight:
                custom_tare = c4.number_input("Box Tare Weight (kg)", value=0.0, step=0.1)
        else:
            st.markdown("<br>", unsafe_allow_html=True)
            grid_html = '<div class="bx-grid">'
            for k, v in BOXES.items():
                d = v["dims"]
                grid_html += f'''<div class="bx-item">
                    <div class="bx-name">Option {k}</div>
                    <div class="bx-dims">{d[0]}×{d[1]}×{d[2]} mm</div>
                    <div class="bx-type">{v["type"]}</div>
                    <div class="bx-tare">tare: {v["tare"]} kg</div>
                </div>'''
            grid_html += '</div>'
            st.markdown(grid_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Run Analysis →"):
            st.session_state.data['results_df'] = run_analysis(
                df,
                "Catalogue" if box_mode == "Predefined Catalogue" else "Manual",
                custom_box, custom_tare, has_weight
            )
            st.session_state.data['has_weight'] = has_weight
            st.session_state.step = 2
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — Results
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.step == 2:
    res_df     = st.session_state.data['results_df']
    has_weight = st.session_state.data.get('has_weight', False)

    st.markdown("""
    <div class="sec-head">
      <span class="sec-num">02</span>
      <span class="sec-title">Results</span>
    </div>
    <hr class="sec-rule">
    """, unsafe_allow_html=True)

    if res_df.empty:
        st.error("No valid fits found. Check that box dimensions are larger than part dimensions.")
        if st.button("← Back"):
            st.session_state.step = 1
            st.rerun()
    else:
        parts_count = res_df["Part Name"].nunique()
        best_qty    = int(res_df["Best Qty / Box"].max())
        avg_qty     = res_df["Best Qty / Box"].mean()

        weight_numeric = pd.to_numeric(res_df["Box Weight (kg)"], errors='coerce')
        max_wt   = weight_numeric.max() if has_weight else None
        stat4_v  = f"{max_wt:.1f} kg" if max_wt is not None else "N/A"
        stat4_fs = "2.6rem" if max_wt is not None else "1.5rem"

        st.markdown(f"""
        <div class="stat-grid">
          <div class="stat-cell">
            <div class="stat-label">Parts Analysed</div>
            <div class="stat-value">{parts_count}</div>
          </div>
          <div class="stat-cell">
            <div class="stat-label">Best Qty / Box</div>
            <div class="stat-value red">{best_qty}</div>
          </div>
          <div class="stat-cell">
            <div class="stat-label">Avg Qty / Box</div>
            <div class="stat-value">{avg_qty:.1f}</div>
          </div>
          <div class="stat-cell">
            <div class="stat-label">Max Box Weight</div>
            <div class="stat-value" style="font-size:{stat4_fs};">{stat4_v}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        rows_html = ""
        for _, row in res_df.iterrows():
            qty       = int(row["Best Qty / Box"])
            qty_color = "#2a9d5c" if qty >= 10 else ("#f4a300" if qty >= 4 else ("#e63329" if qty == 0 else "#111"))
            wt_val    = row["Box Weight (kg)"]
            wt_disp   = f"{wt_val} kg" if wt_val != "" else "—"
            o1_wt_d   = str(row["Opt1 Wt"]) + " kg" if row["Opt1 Wt"] != "" else "—"
            o2_wt_d   = str(row["Opt2 Wt"]) + " kg" if row["Opt2 Wt"] != "" else "—"
            rows_html += f"""
            <tr>
                <td style="font-weight:500;">{row['Part Name']}</td>
                <td style="color:#666;font-size:0.68rem;">{row['Part L×W×H (mm)']}</td>
                <td>{row['Box']}</td>
                <td style="font-size:0.65rem;color:#888;">{row['Box L×W×H (mm)']}</td>
                <td style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:{qty_color};">{qty}</td>
                <td style="color:#555;font-size:0.72rem;">{row['Best Option']}</td>
                <td style="color:#333;">{wt_disp}</td>
                <td style="color:#aaa;font-size:0.64rem;">
                    Opt1: {row['Opt1 Qty']} qty / {o1_wt_d}<br>
                    Opt2: {row['Opt2 Qty']} qty / {o2_wt_d}
                </td>
            </tr>"""

        table_html = f"""
        <style>
          @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Bebas+Neue&family=DM+Sans:wght@400;500&display=swap');
          * {{ box-sizing: border-box; }}
          body {{ margin: 0; background: transparent; }}
          table {{ width:100%;border-collapse:collapse;font-family:'DM Mono',monospace;background:#fff;border:1px solid #ddd; }}
          thead tr {{ background:#111; }}
          th {{ font-size:0.58rem;letter-spacing:1.5px;text-transform:uppercase;color:#aaa;padding:0.9rem 1rem;text-align:left;font-weight:400;white-space:nowrap; }}
          td {{ padding:0.85rem 1rem;border-bottom:1px solid #f0ece5;font-size:0.74rem;color:#222;vertical-align:middle; }}
          tbody tr:hover {{ background:#faf8f4; }}
          tbody tr:last-child td {{ border-bottom:none; }}
        </style>
        <table>
          <thead>
            <tr>
              <th>Part Name</th><th>Part Dims</th><th>Box</th><th>Box Dims</th>
              <th>Best Qty</th><th>Best Option</th><th>Box Weight</th><th>Opt1 / Opt2 Detail</th>
            </tr>
          </thead>
          <tbody>{rows_html}</tbody>
        </table>"""

        components.html(table_html, height=max(420, len(res_df) * 56 + 80), scrolling=True)

        st.markdown("<br>", unsafe_allow_html=True)

        output = io.BytesIO()
        export_cols = [
            "Part Name", "Part L×W×H (mm)", "Unit Weight (kg)",
            "Box", "Box Type", "Box L×W×H (mm)",
            "Best Option", "Best Qty / Box", "Box Weight (kg)", "Per Axis",
            "Opt1 Qty", "Opt1 Wt", "Opt2 Qty", "Opt2 Wt",
        ]
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            res_df[export_cols].to_excel(writer, index=False, sheet_name='AgiloPack')
            wb = writer.book
            ws = writer.sheets['AgiloPack']
            hdr_fmt = wb.add_format({'bold': True, 'bg_color': '#111111', 'font_color': '#cccccc',
                                      'font_name': 'Arial', 'font_size': 9, 'border': 1})
            for ci, col in enumerate(export_cols):
                ws.write(0, ci, col, hdr_fmt)
                ws.set_column(ci, ci, max(len(col) + 2, 14))

        col1, col2 = st.columns([1, 5])
        with col1:
            st.download_button(
                "↓ Download Report",
                data=output.getvalue(),
                file_name='AgiloPack_Results.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        with col2:
            if st.button("↺ Start Over"):
                reset_process()

        st.markdown('<p class="dl-hint">Excel · 2 orientations · Box Weight = Qty × Unit Weight + Tare</p>', unsafe_allow_html=True)
