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

# ── BOXES with size-bracket tiers ────────────────────────────────────────────
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

def tier_candidates(part_dim):
    max_dim = max(part_dim)
    for upper, keys in TIER_BANDS:
        if max_dim <= upper:
            return keys
    return ["G", "H"]

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
            best_info = {"count": best_count, "dims": f"{ow}x{ol}x{oh}",
                         "orientation": labels[idx[2]],
                         "used_vol": round(best_count * p[0]*p[1]*p[2], 2)}
    if not best_info: return None
    bvol = bw * bl * bh
    best_info["util"] = round((best_info["used_vol"] / bvol) * 100, 2)
    best_info["unused"] = round(bvol - best_info["used_vol"], 2)
    return best_info

# ── Helpers to parse Excel column values ──────────────────────────────────────
def parse_yes_no(val):
    if pd.isna(val):
        return False
    return str(val).strip().lower() in ("yes", "y", "true", "1")

def parse_nesting_pct(val):
    if pd.isna(val):
        return 0.0
    s = str(val).strip()
    try:
        f = float(s)
        return f * 100 if f <= 1.0 else f
    except ValueError:
        pass
    m = re.search(r"(\d+\.?\d*)", s)
    return float(m.group(1)) if m else 0.0

def parse_fragility(val):
    return "Fragile" if parse_yes_no(val) else "Non-Fragile"

def lifespan_to_density_factor(val):
    if pd.isna(val):
        return 1.0
    s = str(val).strip().lower()
    if s in ("long", "high", "durable"):
        return 0.85
    if s in ("medium", "mid"):
        return 0.92
    try:
        years = float(re.search(r"(\d+\.?\d*)", s).group(1))
        if years >= 5:
            return 0.85
        if years >= 2:
            return 0.92
    except Exception:
        pass
    return 1.0

# ── Auto-select best box for a single part row ────────────────────────────────
def best_box_for_part(row, overrides=None):
    """
    Select best box using size-bracket tiers.
    If `overrides` dict is provided, those values replace the row's handling fields.
    """
    # Apply overrides if supplied (single-row manual override feature)
    def get_field(field):
        if overrides and field in overrides:
            return overrides[field]
        return row.get(field, None)

    fragile   = parse_fragility(get_field("Fragile"))
    stacking  = parse_yes_no(get_field("Stacking") if get_field("Stacking") is not None else "Yes")
    nested    = parse_yes_no(get_field("Nesting"))
    nest_pct  = parse_nesting_pct(get_field("Nesting %"))
    density_f = lifespan_to_density_factor(row.get("Lifespan", "Short"))
    part_dim  = (row["Width"], row["Length"], row["Height"])
    max_dim   = max(part_dim)

    tier_order = []
    matched = False
    for upper, keys in TIER_BANDS:
        if not matched and max_dim <= upper:
            matched = True
        if matched:
            tier_order.append(keys)

    if not tier_order:
        tier_order = [keys for _, keys in TIER_BANDS]

    for candidate_keys in tier_order:
        best_score, best_box_key, best_result = -1, None, None

        for box_key in candidate_keys:
            box_dim = BOXES[box_key]
            res = calculate_fit(box_dim, part_dim, nested, nest_pct, stacking, fragile)
            if res is None:
                continue
            score = res["count"] * density_f + res["util"] / 1000
            if score > best_score:
                best_score   = score
                best_box_key = box_key
                best_result  = res

        if best_result is not None:
            tier_name = next(
                (["Small", "Medium", "Large", "Very Large"][i]
                 for i, (_, keys) in enumerate(TIER_BANDS)
                 if best_box_key in keys),
                "—"
            )
            return {
                "box_key":   best_box_key,
                "box_dims":  BOXES[best_box_key],
                "tier":      tier_name,
                **best_result,
            }

    return None

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
STEPS = ["Upload Data", "Results"]
cur = st.session_state.step
ribbon_html = '<div class="ribbon">'
for i, s in enumerate(STEPS, 1):
    cls = "active" if i == cur else ("done" if i < cur else "")
    ribbon_html += f'<div class="rib-item {cls}"><span class="rib-num">0{i}</span>{s}</div>'
ribbon_html += '</div>'
st.markdown(ribbon_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — UPLOAD
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
        if 'raw_df' not in st.session_state:
            st.session_state.raw_df = (
                pd.read_csv(uploaded_file)
                if uploaded_file.name.endswith('.csv')
                else pd.read_excel(uploaded_file)
            )
        df = st.session_state.raw_df
        df.columns = [c.strip() for c in df.columns]

        REQUIRED = {"Part Name", "Length", "Width", "Height",
                    "Fragile", "Stacking", "Nesting", "Nesting %"}
        missing = REQUIRED - set(df.columns)
        if missing:
            st.error(f"Missing columns: {', '.join(sorted(missing))}")
            st.stop()

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

        # ── Single-row manual override ────────────────────────────────────────
        # Only shown when exactly one part is uploaded. Multi-row uploads skip
        # this block entirely and always use Excel-driven values.
        if len(df) == 1:
            st.markdown("---")
            st.markdown("""
            <p class="sec-desc" style="margin-bottom:0.5rem">
              <strong>Single part detected.</strong> Optionally override the handling
              rules from the file before running the analysis.
            </p>
            """, unsafe_allow_html=True)

            override_enabled = st.toggle(
                "Enable manual override", value=False, key="override_toggle"
            )

            if override_enabled:
                col1, col2 = st.columns(2)
                with col1:
                    ov_fragile  = st.selectbox("Fragile",  ["No", "Yes"], key="ov_fragile")
                    ov_stacking = st.selectbox("Stacking", ["Yes", "No"], key="ov_stacking")
                with col2:
                    ov_nesting  = st.selectbox("Nesting",  ["No", "Yes"], key="ov_nesting")
                    ov_nest_pct = st.number_input(
                        "Nesting %", min_value=0.0, max_value=100.0,
                        value=0.0, step=1.0, key="ov_nest_pct"
                    )

                # Store overrides so Step 2 can read them
                st.session_state.data['overrides'] = {
                    "Fragile":   ov_fragile,
                    "Stacking":  ov_stacking,
                    "Nesting":   ov_nesting,
                    "Nesting %": ov_nest_pct,
                }
            else:
                # Clear any previously stored overrides when toggle is off
                st.session_state.data.pop('overrides', None)

        st.button("Run analysis →", on_click=next_step)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — RESULTS
# ─────────────────────────────────────────────────────────────────────────────
elif cur == 2:
    df = st.session_state.data['parts_df']
    # Overrides only exist for single-row uploads where the user enabled the toggle
    overrides = st.session_state.data.get('overrides', None)
    results = []

    for _, row in df.iterrows():
        # Pass overrides only for single-row uploads; None for bulk (no effect)
        row_overrides = overrides if (len(df) == 1 and overrides) else None
        best = best_box_for_part(row, overrides=row_overrides)
        if best is None:
            continue

        # Determine display values: prefer overrides for the single-row case
        def display_field(field):
            if row_overrides and field in row_overrides:
                return row_overrides[field]
            return row.get(field, None)

        fragile   = parse_fragility(display_field("Fragile"))
        stacking  = parse_yes_no(display_field("Stacking") if display_field("Stacking") is not None else "Yes")
        nested    = parse_yes_no(display_field("Nesting"))
        nest_pct  = parse_nesting_pct(display_field("Nesting %"))
        lifespan  = str(row.get("Lifespan", "—")).strip() if not pd.isna(row.get("Lifespan", float("nan"))) else "—"
        box_lbl   = f"Option {best['box_key']} ({best['box_dims'][0]}×{best['box_dims'][1]}×{best['box_dims'][2]})"

        results.append({
            "Part Name":       row["Part Name"],
            "Tier":            best.get("tier", "—"),
            "Best Box":        box_lbl,
            "Parts / Box":     best["count"],
            "Orientation":     best["dims"],
            "Placement":       best["orientation"],
            "Utilization":     best["util"],
            "Unused (mm³)":    int(best["unused"]),
            "Fragile":         fragile,
            "Stacking":        "Yes" if stacking else "No",
            "Nesting":         f"Yes ({nest_pct:.0f}%)" if nested else "No",
            "Lifespan":        lifespan,
        })

    res_df = pd.DataFrame(results)

    avg_util  = res_df["Utilization"].mean() if len(res_df) else 0
    best_part = res_df.loc[res_df["Utilization"].idxmax(), "Part Name"] if len(res_df) else "—"
    top_box   = res_df["Best Box"].value_counts().idxmax() if len(res_df) else "—"

    # Show a notice if overrides were applied
    if overrides:
        st.info("ℹ️  Manual override applied — handling rules from the toggle were used instead of the file.")

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

    rows_html = ""
    for _, row in res_df.iterrows():
        u = float(row["Utilization"])
        bar_color = "#2a9d5c" if u >= 60 else "#e63329"
        unused_val = int(row["Unused (mm³)"])
        tier_colors = {"Small": "#4a90d9", "Medium": "#e6a817",
                       "Large": "#e63329",  "Very Large": "#7b47c2"}
        tier = row.get("Tier", "—")
        tier_bg = tier_colors.get(tier, "#aaa")

        rows_html += (
            f"<tr>"
            f"<td>{row['Part Name']}</td>"
            f"<td><span style='background:{tier_bg};color:#fff;padding:2px 8px;"
            f"font-size:0.6rem;letter-spacing:1px;text-transform:uppercase'>"
            f"{tier}</span></td>"
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
        <th>Part Name</th><th>Tier</th><th>Best Box</th><th>Parts / Box</th>
        <th>Orientation</th><th>Placement</th><th>Utilization</th><th>Unused (mm³)</th>
        <th>Fragile</th><th>Stacking</th><th>Nesting</th><th>Lifespan</th>
      </tr></thead>
      <tbody>{rows_html}</tbody>
    </table>
    """
    components.html(table_html, height=max(200, len(res_df) * 70 + 60), scrolling=True)

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
