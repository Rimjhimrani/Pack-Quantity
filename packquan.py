import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import itertools
import io
import re

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

/* Subtle dot-grid texture overlay */
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
    max-width: 1020px !important;
    padding: 0 2rem 5rem 2rem !important;
    position: relative;
    z-index: 1;
}

/* ── Masthead ── */
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

/* ── Ribbon ── */
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

/* ── Section Headers ── */
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

/* ── Box Catalogue Grid ── */
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
    transition: background 0.15s, transform 0.15s;
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
.bx-item:hover .bx-dims { color: #fff; }
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

/* ── Stat Grid ── */
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

/* ── Buttons ── */
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
    position: relative;
}
.stButton > button:hover {
    background: #e63329 !important;
    letter-spacing: 3.5px !important;
}
.stButton > button:active { transform: translateY(1px); }

[data-testid="stDownloadButton"] > button {
    background: #1a7d48 !important;
    color: #fff !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: #15603a !important;
}

/* ── Labels / Inputs ── */
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
    transition: border-color 0.2s !important;
}
div[data-testid="stSelectbox"] > div > div:focus-within,
div[data-testid="stNumberInput"] input:focus {
    border-color: #e63329 !important;
    box-shadow: none !important;
    outline: none !important;
}

[data-testid="stFileUploader"] {
    border: 2px dashed #ccc !important;
    border-radius: 0 !important;
    background: #fff !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #e63329 !important;
}

/* ── Info/Alert boxes ── */
div[data-testid="stAlert"] {
    border-radius: 0 !important;
    border-left: 3px solid #111 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
}

/* ── Checkbox ── */
.stCheckbox label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

/* ── Radio ── */
.stRadio > div {
    gap: 0 !important;
}
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
    transition: background 0.15s !important;
}
.stRadio > div > label:last-child { border-right: 1px solid #ddd !important; }
.stRadio > div > label:has(input:checked) {
    background: #e63329 !important;
    color: #fff !important;
    border-color: #e63329 !important;
}

/* ── Download notice ── */
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

# ── Global Box Data ──────────────────────────────────────────────────────────
BOXES = {
    "A": (120,  80,   80),
    "B": (200,  180,  120),
    "C": (360,  360,  100),
    "D": (400,  300,  220),
    "E": (600,  500,  400),
    "F": (850,  400,  250),
    "G": (1200, 1000, 250),
    "H": (1500, 1200, 1000),
}

TIER_BANDS = [
    (150,  ["A", "B"]),
    (380,  ["C", "D"]),
    (900,  ["E", "F"]),
    (float("inf"), ["G", "H"]),
]

# ── State ──────────────────────────────────────────────────────────────────────
if 'step' not in st.session_state: st.session_state.step = 1
if 'data' not in st.session_state: st.session_state.data = {}

def next_step(): st.session_state.step += 1
def reset_process():
    for k in list(st.session_state.keys()): del st.session_state[k]
    st.rerun()

# ── Helpers ──────────────────────────────────────────────────────────────────
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

def parse_yes_no(val):
    if pd.isna(val): return False
    return str(val).strip().lower() in ("yes", "y", "true", "1")

def parse_nesting_pct(val):
    if pd.isna(val): return 0.0
    s = str(val).strip()
    try:
        f = float(s)
        return f * 100 if f <= 1.0 else f
    except ValueError:
        m = re.search(r"(\d+\.?\d*)", s)
        return float(m.group(1)) if m else 0.0

def lifespan_to_density_factor(val):
    if pd.isna(val): return 1.0
    s = str(val).strip().lower()
    if s in ("long", "high", "durable"): return 0.85
    if s in ("medium", "mid"): return 0.92
    return 1.0

def run_analysis(df, box_mode, custom_box_dim=None, single_part_rules=None):
    results = []
    for _, row in df.iterrows():
        if single_part_rules:
            fragile   = "Fragile" if single_part_rules['fragile'] else "Non-Fragile"
            stacking  = single_part_rules['stacking']
            nested    = single_part_rules['nesting']
            nest_pct  = single_part_rules['nest_pct']
        else:
            fragile   = "Fragile" if parse_yes_no(row.get("Fragile", "No")) else "Non-Fragile"
            stacking  = parse_yes_no(row.get("Stacking", "Yes"))
            nested    = parse_yes_no(row.get("Nesting", "No"))
            nest_pct  = parse_nesting_pct(row.get("Nesting %", 0))

        part_dim  = (row["Width"], row["Length"], row["Height"])
        density_f = lifespan_to_density_factor(row.get("Lifespan", "Short"))
        best_score, best_box_key, best_res = -1, None, None

        if box_mode == "Manual":
            best_res = calculate_fit(custom_box_dim, part_dim, nested, nest_pct, stacking, fragile)
            best_box_key = "Custom"
        else:
            max_p = max(part_dim)
            tier_order = []
            matched = False
            for upper, keys in TIER_BANDS:
                if not matched and max_p <= upper: matched = True
                if matched: tier_order.append(keys)
            for candidate_keys in tier_order:
                for b_key in candidate_keys:
                    res = calculate_fit(BOXES[b_key], part_dim, nested, nest_pct, stacking, fragile)
                    if res:
                        score = res["count"] * density_f + res["util"] / 1000
                        if score > best_score:
                            best_score, best_box_key, best_res = score, b_key, res
                if best_res: break

        if best_res:
            box_display = f"Option {best_box_key}" if best_box_key != "Custom" else f"Manual ({custom_box_dim[0]}×{custom_box_dim[1]}×{custom_box_dim[2]})"
            results.append({
                "Part Name": row["Part Name"],
                "Best Box": box_display,
                "Parts / Box": best_res["count"],
                "Orientation": best_res["dims"],
                "Placement": best_res["orientation"],
                "Utilization": best_res["util"],
                "Unused (mm³)": int(best_res["unused"]),
                "Fragile": fragile,
                "Stacking": "Yes" if stacking else "No",
                "Nesting": f"Yes ({nest_pct:.0f}%)" if nested else "No",
                "Lifespan": str(row.get("Lifespan", "—"))
            })
    return pd.DataFrame(results)

# ── Masthead ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
  <div>
    <span class="masthead-logo">AgiloPack 2</span><span class="masthead-accent"></span>
  </div>
  <div class="masthead-tagline">Box Space Utilization</div>
  <div class="masthead-version">v2.0</div>
</div>
""", unsafe_allow_html=True)

# ── Ribbon ───────────────────────────────────────────────────────────────────
STEPS = ["Upload & Config", "Results"]
ribbon_html = '<div class="ribbon">'
for i, s in enumerate(STEPS, 1):
    cls = "active" if i == st.session_state.step else ("done" if i < st.session_state.step else "")
    ribbon_html += f'<div class="rib-item {cls}"><span class="rib-num">0{i}</span>{s}</div>'
ribbon_html += '</div>'
st.markdown(ribbon_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.step == 1:
    st.markdown("""
    <div class="sec-head">
      <span class="sec-num">01</span>
      <span class="sec-title">Upload & Configuration</span>
    </div>
    <hr class="sec-rule">
    <p class="sec-desc">Upload a CSV or Excel file containing part dimensions. Single-part files unlock manual handling rules; bulk files read rules from columns.</p>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Drop part file here", type=["csv", "xlsx"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        df.columns = [c.strip() for c in df.columns]

        is_single = len(df) == 1
        mode_label = "Single Part" if is_single else "Bulk Analysis"
        st.info(f"⬡  Mode detected: **{mode_label}** — {len(df)} row{'s' if len(df) != 1 else ''} loaded")

        st.markdown("<br>", unsafe_allow_html=True)

        box_mode = st.radio("Box selection mode", ["Predefined Catalogue", "Manual Box Size Entry"], horizontal=True)

        custom_box = None
        if box_mode == "Manual Box Size Entry":
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            bl = c1.number_input("Box Length (mm)", value=400, step=10)
            bw = c2.number_input("Box Width (mm)", value=300, step=10)
            bh = c3.number_input("Box Height (mm)", value=200, step=10)
            custom_box = (bl, bw, bh)
        else:
            st.markdown("<br>", unsafe_allow_html=True)
            grid_html = '<div class="bx-grid">'
            for k, v in BOXES.items():
                grid_html += f'<div class="bx-item"><div class="bx-name">Option {k}</div><div class="bx-dims">{v[0]}×{v[1]}×{v[2]} mm</div></div>'
            grid_html += '</div>'
            st.markdown(grid_html, unsafe_allow_html=True)

        sp_rules = None
        if is_single:
            st.markdown("---")
            st.markdown("""
            <div style="font-family:'DM Mono',monospace; font-size:0.66rem; letter-spacing:2px;
                        text-transform:uppercase; color:#888; margin-bottom:0.8rem;">
                Handling Rules
            </div>
            """, unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            frag  = c1.checkbox("Fragile")
            stack = c2.checkbox("Stacking allowed", value=True)
            nest  = c3.checkbox("Nesting allowed")
            nest_p = c4.number_input("Nesting %", value=0, min_value=0, max_value=100) if nest else 0
            sp_rules = {'fragile': frag, 'stacking': stack, 'nesting': nest, 'nest_pct': nest_p}
        else:
            st.markdown("""
            <p style='font-family:"DM Mono",monospace; font-size:0.68rem; letter-spacing:1px;
                      color:#aaa; margin-top:1rem;'>
                ↳ Handling rules (Fragile, Stacking, Nesting) will be read from file columns.
            </p>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Run Analysis →"):
            st.session_state.data['results_df'] = run_analysis(
                df,
                "Catalogue" if box_mode == "Predefined Catalogue" else "Manual",
                custom_box,
                sp_rules
            )
            st.session_state.step = 2
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.step == 2:
    res_df = st.session_state.data['results_df']

    st.markdown("""
    <div class="sec-head">
      <span class="sec-num">02</span>
      <span class="sec-title">Results</span>
    </div>
    <hr class="sec-rule">
    """, unsafe_allow_html=True)

    if res_df.empty:
        st.error("No valid fits found. Ensure box dimensions are larger than part dimensions.")
        if st.button("← Back"):
            st.session_state.step = 1
            st.rerun()
    else:
        avg_util = res_df["Utilization"].mean()
        best_util = res_df["Utilization"].max()
        total_fit = res_df["Parts / Box"].sum()

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
            <div class="stat-label">Best Fit</div>
            <div class="stat-value">{best_util:.1f}%</div>
          </div>
          <div class="stat-cell">
            <div class="stat-label">Total Parts Fit</div>
            <div class="stat-value">{total_fit}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Build table rows
        rows_html = ""
        for i, row in res_df.iterrows():
            u = float(row["Utilization"])
            bar_color = "#2a9d5c" if u >= 60 else ("#f4a300" if u >= 35 else "#e63329")
            frag_badge = (
                '<span style="background:#e63329;color:#fff;padding:2px 7px;font-size:0.58rem;letter-spacing:1px;">FRAGILE</span>'
                if row['Fragile'] == 'Fragile' else
                '<span style="background:#eee;color:#888;padding:2px 7px;font-size:0.58rem;letter-spacing:1px;">SAFE</span>'
            )
            stack_badge = (
                '<span style="background:#d4edda;color:#1a6b38;padding:2px 6px;font-size:0.58rem;letter-spacing:1px;">YES</span>'
                if row['Stacking'] == 'Yes' else
                '<span style="background:#f8d7da;color:#721c24;padding:2px 6px;font-size:0.58rem;letter-spacing:1px;">NO</span>'
            )
            rows_html += f"""
            <tr>
                <td style="font-weight:500;">{row['Part Name']}</td>
                <td>{row['Best Box']}</td>
                <td style="font-family:'Bebas Neue',sans-serif;font-size:1.3rem;letter-spacing:1px;">{row['Parts / Box']}</td>
                <td style="color:#666;">{row['Orientation']}</td>
                <td>
                    <span style="font-weight:500;color:{bar_color};">{u:.1f}%</span>
                    <div style="background:#f0ece5;height:3px;width:100%;margin-top:5px;border-radius:0;">
                        <div style="height:100%;width:{min(u,100):.1f}%;background:{bar_color};transition:width 0.6s ease;"></div>
                    </div>
                </td>
                <td>{frag_badge}</td>
                <td>{stack_badge}</td>
                <td style="color:#888;font-size:0.7rem;">{row['Nesting']}</td>
                <td style="color:#aaa;font-size:0.7rem;text-transform:uppercase;letter-spacing:1px;">{row['Lifespan']}</td>
            </tr>"""

        table_html = f"""
        <style>
          @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Bebas+Neue&family=DM+Sans:wght@400;500&display=swap');
          * {{ box-sizing: border-box; }}
          body {{ margin: 0; background: transparent; }}
          table {{
            width: 100%; border-collapse: collapse;
            font-family: 'DM Mono', monospace;
            background: #fff;
            border: 1px solid #ddd;
          }}
          thead tr {{
            background: #111;
          }}
          th {{
            font-size: 0.58rem; letter-spacing: 1.5px; text-transform: uppercase;
            color: #aaa; padding: 0.9rem 1rem; text-align: left;
            font-weight: 400; white-space: nowrap;
          }}
          td {{
            padding: 0.85rem 1rem; border-bottom: 1px solid #f0ece5;
            font-size: 0.74rem; color: #222; vertical-align: middle;
          }}
          tbody tr {{ transition: background 0.12s; }}
          tbody tr:hover {{ background: #faf8f4; }}
          tbody tr:last-child td {{ border-bottom: none; }}
        </style>
        <table>
          <thead>
            <tr>
              <th>Part Name</th><th>Box Used</th><th>Count</th>
              <th>Dims (W×L×H)</th><th>Utilization</th>
              <th>Fragile</th><th>Stack</th><th>Nest</th><th>Lifespan</th>
            </tr>
          </thead>
          <tbody>{rows_html}</tbody>
        </table>"""

        components.html(table_html, height=420, scrolling=True)

        st.markdown("<br>", unsafe_allow_html=True)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            res_df.to_excel(writer, index=False, sheet_name='AgiloPack')

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

        st.markdown('<p class="dl-hint">Excel · All results · Formatted</p>', unsafe_allow_html=True)
