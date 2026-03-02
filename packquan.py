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
    background: #f7f4ef !important;
    color: #111 !important;
}

.block-container {
    max-width: 960px !important;
    padding: 0 2rem 4rem 2rem !important;
}

.masthead {
    border-bottom: 3px solid #111;
    padding: 4.5rem 0 1.2rem 0;
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
}
.stButton > button:hover { background: #e63329 !important; }

[data-testid="stDownloadButton"] > button {
    background: #2a9d5c !important;
    color: #fff !important;
}

div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stFileUploader"] label,
.stRadio label, [data-testid="stWidgetLabel"] p {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: #666 !important;
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
            best_info = {"count": best_count, "dims": f"{ow}x{ol}x{oh}",
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

# ── Logic Controller ─────────────────────────────────────────────────────────

def run_analysis(df, box_mode, custom_box_dim=None, single_part_rules=None):
    results = []
    for _, row in df.iterrows():
        # Source handling rules
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
            # Predefined Catalogue Auto-Selection
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

# ── UI Layout ────────────────────────────────────────────────────────────────

st.markdown(f"""
<div class="masthead">
  <div><span class="masthead-logo">AgiloPack</span><span class="masthead-accent"></span></div>
  <div class="masthead-tagline">Box Space Utilization</div>
</div>
""", unsafe_allow_html=True)

STEPS = ["Upload Data", "Results"]
ribbon_html = '<div class="ribbon">'
for i, s in enumerate(STEPS, 1):
    cls = "active" if i == st.session_state.step else ("done" if i < st.session_state.step else "")
    ribbon_html += f'<div class="rib-item {cls}"><span class="rib-num">0{i}</span>{s}</div>'
ribbon_html += '</div>'
st.markdown(ribbon_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1: UPLOAD & CONFIG
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.step == 1:
    st.markdown("""
    <div class="sec-head"><span class="sec-num">01</span><span class="sec-title">Upload & Configuration</span></div>
    <hr class="sec-rule">
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Drop part file here", type=["csv", "xlsx"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        df.columns = [c.strip() for c in df.columns]
        
        is_single = len(df) == 1
        st.info(f"Mode: {'Single Part' if is_single else 'Bulk Analysis'} ({len(df)} rows detected)")

        # Box Mode Selection
        box_mode = st.radio("Box Selection Mode", ["Predefined Catalogue", "Manual Box Size Entry"], horizontal=True)
        
        custom_box = None
        if box_mode == "Manual Box Size Entry":
            c1, c2, c3 = st.columns(3)
            bl = c1.number_input("Box Length (mm)", value=400)
            bw = c2.number_input("Box Width (mm)", value=300)
            bh = c3.number_input("Box Height (mm)", value=200)
            custom_box = (bl, bw, bh)
        else:
            grid_html = '<div class="bx-grid">'
            for k, v in BOXES.items():
                grid_html += f'<div class="bx-item"><div class="bx-name">Option {k}</div><div class="bx-dims">{v[0]}×{v[1]}×{v[2]}</div></div>'
            grid_html += '</div>'
            st.markdown(grid_html, unsafe_allow_html=True)

        # Handling Rules Selection
        sp_rules = None
        if is_single:
            st.markdown("### Handling Rules")
            c1, c2, c3, c4 = st.columns(4)
            frag = c1.checkbox("Fragile")
            stack = c2.checkbox("Stacking allowed", value=True)
            nest = c3.checkbox("Nesting allowed")
            nest_p = c4.number_input("Nesting %", value=0) if nest else 0
            sp_rules = {'fragile': frag, 'stacking': stack, 'nesting': nest, 'nest_pct': nest_p}
        else:
            st.markdown("<p style='font-size:0.75rem; color:#888;'>Rules (Fragile, Stacking, Nesting) will be read from file.</p>", unsafe_allow_html=True)

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
# STEP 2: RESULTS
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.step == 2:
    res_df = st.session_state.data['results_df']
    
    st.markdown("""<div class="sec-head"><span class="sec-num">02</span><span class="sec-title">Results</span></div><hr class="sec-rule">""", unsafe_allow_html=True)

    if res_df.empty:
        st.error("No valid fits found. Ensure box dimensions are larger than part dimensions.")
        if st.button("Back"): st.session_state.step = 1; st.rerun()
    else:
        avg_util = res_df["Utilization"].mean()
        st.markdown(f"""
        <div class="stat-grid">
          <div class="stat-cell"><div class="stat-label">Parts Analysed</div><div class="stat-value">{len(res_df)}</div></div>
          <div class="stat-cell"><div class="stat-label">Avg Utilization</div><div class="stat-value red">{avg_util:.1f}%</div></div>
          <div class="stat-cell"><div class="stat-label">Best Fit</div><div class="stat-value">{res_df['Utilization'].max():.1f}%</div></div>
          <div class="stat-cell"><div class="stat-label">Total Fit</div><div class="stat-value">{res_df['Parts / Box'].sum()}</div></div>
        </div>
        """, unsafe_allow_html=True)

        rows_html = ""
        for _, row in res_df.iterrows():
            u = float(row["Utilization"])
            bar_color = "#2a9d5c" if u >= 60 else "#e63329"
            rows_html += f"""
            <tr>
                <td>{row['Part Name']}</td>
                <td>{row['Best Box']}</td>
                <td>{row['Parts / Box']}</td>
                <td>{row['Orientation']}</td>
                <td>{u:.1f}%<div style='background:#f0ece5;height:4px;width:100%;margin-top:4px;'><div style='height:100%;width:{min(u,100):.1f}%;background:{bar_color}'></div></div></td>
                <td>{row['Fragile']}</td>
                <td>{row['Stacking']}</td>
                <td>{row['Nesting']}</td>
                <td>{row['Lifespan']}</td>
            </tr>"""

        table_html = f"""
        <style>
          table {{ width:100%; border-collapse:collapse; font-family:'DM Mono',monospace; background:#fff; border:1px solid #ddd; }}
          th {{ font-size:0.6rem; letter-spacing:1px; text-transform:uppercase; color:#999; padding:0.7rem; text-align:left; border-bottom:2px solid #111; }}
          td {{ padding:0.8rem; border-bottom:1px solid #eee; font-size:0.75rem; color:#222; }}
        </style>
        <table><thead><tr><th>Part Name</th><th>Box Used</th><th>Count</th><th>Orientation</th><th>Utilization</th><th>Fragile</th><th>Stack</th><th>Nest</th><th>Lifespan</th></tr></thead>
        <tbody>{rows_html}</tbody></table>"""
        
        components.html(table_html, height=400, scrolling=True)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            res_df.to_excel(writer, index=False, sheet_name='AgiloPack')
        
        st.download_button("Download Excel Report", data=output.getvalue(), file_name='AgiloPack_Results.xlsx')
        if st.button("Start Over"): reset_process()
