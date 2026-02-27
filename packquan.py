import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import itertools
import io
import re  # ← NEW: needed for Nesting % parsing

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
.bx-vol {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: #bbb;
    margin-top: 4px;
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

# ── BOXES (used in all-box evaluation) ────────────────────────────────────────
# Unchanged — same dict as before, now also used in auto-selection
BOXES = {
    "A": (120, 80, 80), "B": (200, 180, 120), "C": (360, 360, 100),
    "D": (400, 300, 220), "E": (600, 500, 400), "F": (850, 400, 250),
    "G": (1200, 1000, 250), "H": (1500, 1200, 1000),
}

# ── Engine ────────────────────────────────────────────────────────────────────
# UNCHANGED — same function as before
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

# ── NEW: Helpers to parse Excel column values ─────────────────────────────────

def parse_yes_no(val):
    """Convert 'Yes'/'No' (case-insensitive) to bool. Defaults to False."""
    if pd.isna(val):
        return False
    return str(val).strip().lower() in ("yes", "y", "true", "1")

def parse_nesting_pct(val):
    """
    Extract numeric % from strings like '20% along height', '35%', '0.2', etc.
    Returns float 0–100. Defaults to 0.
    """
    if pd.isna(val):
        return 0.0
    s = str(val).strip()
    # Already a plain number?
    try:
        f = float(s)
        # If it looks like a decimal fraction (0–1 range), convert
        return f * 100 if f <= 1.0 else f
    except ValueError:
        pass
    # Pull the first number out of strings like "20% along height"
    m = re.search(r"(\d+\.?\d*)", s)
    return float(m.group(1)) if m else 0.0

def parse_fragility(val):
    """Return 'Fragile' or 'Non-Fragile'."""
    return "Fragile" if parse_yes_no(val) else "Non-Fragile"

def lifespan_to_density_factor(val):
    """
    NEW: Lifespan affects how tightly we pack.
    Short-lived / consumable parts → pack densely (factor 1.0, no change).
    Long-lived / durable parts   → allow some space (factor 0.85 cap on util).
    Returns a multiplier applied to the parts-per-box count during scoring.
    Accepts strings like 'Short', 'Medium', 'Long', or numeric years.
    """
    if pd.isna(val):
        return 1.0
    s = str(val).strip().lower()
    if s in ("long", "high", "durable"):
        return 0.85   # prefer a box that isn't crammed to the limit
    if s in ("medium", "mid"):
        return 0.92
    # Try numeric years: ≥5 years → treat as long
    try:
        years = float(re.search(r"(\d+\.?\d*)", s).group(1))
        if years >= 5:
            return 0.85
        if years >= 2:
            return 0.92
    except Exception:
        pass
    return 1.0   # short / consumable → pack tight

# ── NEW: Auto-select best box for a single part row ──────────────────────────

def best_box_for_part(row):
    """
    Try every box in BOXES with the per-row packing rules from the Excel file.
    Returns a dict with the winning box key + calculate_fit result, or None.
    """
    fragile    = parse_fragility(row.get("Fragile", "No"))
    stacking   = parse_yes_no(row.get("Stacking", "Yes"))
    nested     = parse_yes_no(row.get("Nesting", "No"))
    nest_pct   = parse_nesting_pct(row.get("Nesting %", 0))
    density_f  = lifespan_to_density_factor(row.get("Lifespan", "Short"))
    part_dim   = (row["Width"], row["Length"], row["Height"])

    best_score, best_box_key, best_result = -1, None, None

    for box_key, box_dim in BOXES.items():
        res = calculate_fit(box_dim, part_dim, nested, nest_pct, stacking, fragile)
        if res is None:
            continue
        # Score = parts-per-box adjusted by lifespan density preference,
        # then use utilization as a tiebreaker
        score = res["count"] * density_f + res["util"] / 1000
        if score > best_score:
            best_score   = score
            best_box_key = box_key
            best_result  = res

    if best_result is None:
        return None
    return {
        "box_key":  best_box_key,
        "box_dims": BOXES[best_box_key],
        **best_result,
    }

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
# CHANGED: Steps reduced from 5 to 2 — Upload then Results
STEPS = ["Upload Data", "Results"]
cur = st.session_state.step
ribbon_html = '<div class="ribbon">'
for i, s in enumerate(STEPS, 1):
    cls = "active" if i == cur else ("done" if i < cur else "")
    ribbon_html += f'<div class="rib-item {cls}"><span class="rib-num">0{i}</span>{s}</div>'
ribbon_html += '</div>'
st.markdown(ribbon_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — UPLOAD  (replaces old steps 1–4)
# All box/nesting/handling configuration is now read from the Excel file.
# ─────────────────────────────────────────────────────────────────────────────
if cur == 1:
    st.markdown("""
    <div class="sec-head">
      <span class="sec-num">01</span>
      <span class="sec-title">Upload Part Data</span>
    </div>
    <hr class="sec-rule">
    <p class="sec-desc">
      Upload a CSV or Excel file containing your parts list. The file must include the columns:<br>
      <strong>Part Name, Length, Width, Height, Weight, Lifespan, Fragile, Stacking, Nesting, Nesting&nbsp;%</strong><br><br>
      Fragile / Stacking / Nesting accept <em>Yes</em> or <em>No</em>.
      Nesting&nbsp;% accepts values like <em>"20% along height"</em> or plain numbers.
      The best box from the standard catalogue will be chosen automatically for each part.
    </p>
    """, unsafe_allow_html=True)

    # Show available box catalogue for reference
    grid_html = '<div class="bx-grid">'
    for k, v in BOXES.items():
        grid_html += f"""<div class="bx-item">
          <div class="bx-name">Option {k}</div>
          <div class="bx-dims">{v[0]} × {v[1]} × {v[2]} mm</div>
          <div class="bx-vol">{v[0]*v[1]*v[2]:,} mm³</div>
        </div>"""
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Drop file here", type=["csv", "xlsx"])

    if uploaded_file:
        # ── Parse the file ──────────────────────────────────────────────────
        if 'raw_df' not in st.session_state:
            st.session_state.raw_df = (
                pd.read_csv(uploaded_file)
                if uploaded_file.name.endswith('.csv')
                else pd.read_excel(uploaded_file)
            )
        df = st.session_state.raw_df

        # ── NEW: Normalise column names (strip whitespace, title-case) ──────
        df.columns = [c.strip() for c in df.columns]

        # ── Validate required columns ───────────────────────────────────────
        REQUIRED = {"Part Name", "Length", "Width", "Height",
                    "Fragile", "Stacking", "Nesting", "Nesting %"}
        missing = REQUIRED - set(df.columns)
        if missing:
            st.error(f"Missing columns: {', '.join(sorted(missing))}")
            st.stop()

        # ── Coerce numeric dims ─────────────────────────────────────────────
        for c in ["Width", "Length", "Height"]:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        st.markdown(f"""
        <div class="pill-row">
          <div class="pill"><div class="pill-label">File</div>
            <div class="pill-val" style="font-size:0.8rem">{uploaded_file.name}</div></div>
          <div class="pill"><div class="pill-label">Rows</div>
            <div class="pill-val">{len(df)}</div></div>
          <div class="pill"><div class="pill-label">Columns</div>
            <div class="pill-val">{len(df.columns)}</div></div>
          <div class="pill"><div class="pill-label">Boxes in catalogue</div>
            <div class="pill-val">{len(BOXES)}</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.session_state.data['parts_df'] = df
        st.session_state.mapping_confirmed = True
        st.success(f"✓  {len(df)} parts loaded. Rules will be read from the file.")
        st.button("Run analysis →", on_click=next_step)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — RESULTS  (replaces old step 5)
# ─────────────────────────────────────────────────────────────────────────────
elif cur == 2:
    df = st.session_state.data['parts_df']
    results = []

    for _, row in df.iterrows():
        best = best_box_for_part(row)   # ← NEW: per-part auto box selection
        if best is None:
            continue

        # ── NEW: re-parse per-part flags for display ────────────────────────
        fragile   = parse_fragility(row.get("Fragile", "No"))
        stacking  = parse_yes_no(row.get("Stacking", "Yes"))
        nested    = parse_yes_no(row.get("Nesting", "No"))
        nest_pct  = parse_nesting_pct(row.get("Nesting %", 0))
        lifespan  = str(row.get("Lifespan", "—")).strip() if not pd.isna(row.get("Lifespan", float("nan"))) else "—"
        box_lbl   = f"Option {best['box_key']} ({best['box_dims'][0]}×{best['box_dims'][1]}×{best['box_dims'][2]})"

        results.append({
            "Part Name":       row["Part Name"],
            "Best Box":        box_lbl,
            "Parts / Box":     best["count"],
            "Orientation":     best["dims"],
            "Placement":       best["orientation"],
            "Utilization":     best["util"],
            "Unused (mm³)":    int(best["unused"]),
            # NEW columns sourced from file
            "Fragile":         fragile,
            "Stacking":        "Yes" if stacking else "No",
            "Nesting":         f"Yes ({nest_pct:.0f}%)" if nested else "No",
            "Lifespan":        lifespan,
        })

    res_df = pd.DataFrame(results)

    avg_util  = res_df["Utilization"].mean() if len(res_df) else 0
    best_part = res_df.loc[res_df["Utilization"].idxmax(), "Part Name"] if len(res_df) else "—"
    # Most common recommended box
    top_box   = res_df["Best Box"].value_counts().idxmax() if len(res_df) else "—"

    st.markdown("""
    <div class="sec-head">
      <span class="sec-num">02</span>
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
        <div class="stat-label">Top Box</div>
        <div class="stat-value" style="font-size:1rem;letter-spacing:0">{top_box}</div>
      </div>
      <div class="stat-cell">
        <div class="stat-label">Best Fit Part</div>
        <div class="stat-value" style="font-size:1.2rem;letter-spacing:0">{best_part}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Build results table ─────────────────────────────────────────────────
    rows_html = ""
    for _, row in res_df.iterrows():
        u = float(row["Utilization"])
        bar_color = "#2a9d5c" if u >= 60 else "#e63329"
        unused_val = int(row["Unused (mm³)"])
        rows_html += (
            f"<tr>"
            f"<td>{row['Part Name']}</td>"
            f"<td>{row['Best Box']}</td>"
            f"<td>{row['Parts / Box']}</td>"
            f"<td>{row['Orientation']}</td>"
            f"<td>{row['Placement']}</td>"
            f"<td>{u:.1f}%"
            f"<div style='background:#f0ece5;height:6px;width:100%;margin-top:4px;overflow:hidden'>"
            f"<div style='height:100%;width:{min(u,100):.1f}%;background:{bar_color}'></div></div></td>"
            f"<td>{unused_val:,}</td>"
            f"<td>{row['Fragile']}</td>"
            f"<td>{row['Stacking']}</td>"
            f"<td>{row['Nesting']}</td>"
            f"<td>{row['Lifespan']}</td>"
            f"</tr>"
        )

    table_html = f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&display=swap');
      body {{ margin:0; padding:0; background:transparent; }}
      table {{ width:100%; border-collapse:collapse; font-size:0.82rem;
               background:#fff; border:1px solid #ddd; font-family:'DM Mono',monospace; }}
      th {{ font-size:0.62rem; letter-spacing:1.5px; text-transform:uppercase;
            color:#999; padding:0.7rem 1rem; text-align:left;
            border-bottom:2px solid #111; background:#fff; white-space:nowrap; }}
      td {{ padding:0.85rem 1rem; border-bottom:1px solid #eee; color:#222;
            font-size:0.78rem; }}
      tr:last-child td {{ border-bottom:none; }}
      tr:hover td {{ background:#faf8f4; }}
    </style>
    <table>
      <thead><tr>
        <th>Part Name</th><th>Best Box</th><th>Parts / Box</th><th>Orientation</th>
        <th>Placement</th><th>Utilization</th><th>Unused (mm³)</th>
        <th>Fragile</th><th>Stacking</th><th>Nesting</th><th>Lifespan</th>
      </tr></thead>
      <tbody>{rows_html}</tbody>
    </table>
    """
    components.html(table_html, height=max(200, len(res_df) * 70 + 60), scrolling=True)

    # ── Export ──────────────────────────────────────────────────────────────
    output = io.BytesIO()
    export_df = res_df.rename(columns={"Unused (mm³)": "Unused (mm3)"})
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        export_df.to_excel(writer, index=False, sheet_name='AgiloPack')

    c1, c2 = st.columns([1, 1])
    with c1:
        st.download_button(
            "Download report (.xlsx)",
            data=output.getvalue(),
            file_name='AgiloPack_Analysis.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    with c2:
        st.button("Start over", on_click=reset_process)
