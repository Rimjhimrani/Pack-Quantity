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
    max-width: 980px !important;
    padding: 0 2rem 4rem 2rem !important;
}

/* ── Masthead ── */
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

/* ── Ribbon ── */
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
.rib-item.active { color: #111; font-weight: 500; }
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

/* ── Section headers ── */
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
.sec-rule { border: none; border-top: 1px solid #ccc; margin-bottom: 2rem; }
.sec-desc {
    font-size: 0.88rem;
    color: #555;
    line-height: 1.6;
    margin-bottom: 2rem;
    max-width: 580px;
}

/* ── Mode badge ── */
.mode-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    border: 1px solid #ddd;
    padding: 0.5rem 1rem;
    background: #fff;
    margin-bottom: 1.5rem;
}
.mode-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #e63329;
    flex-shrink: 0;
}
.mode-dot.green { background: #2a9d5c; }
.mode-text {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #555;
}

/* ── Pill row ── */
.pill-row {
    display: flex;
    gap: 0;
    margin-bottom: 2rem;
    border: 1px solid #ddd;
    overflow: hidden;
}
.pill { flex: 1; padding: 0.9rem 1.2rem; border-right: 1px solid #ddd; background: #fff; }
.pill:last-child { border-right: none; }
.pill-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 3px;
}
.pill-val { font-family: 'DM Mono', monospace; font-size: 1rem; font-weight: 500; color: #111; }

/* ── Box grid ── */
.bx-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0;
    border: 1px solid #ddd;
    margin-bottom: 2rem;
    overflow: hidden;
}
.bx-item { padding: 1rem 1.2rem; border-right: 1px solid #ddd; border-bottom: 1px solid #ddd; background: #fff; }
.bx-item:nth-child(4n) { border-right: none; }
.bx-item:nth-child(5), .bx-item:nth-child(6),
.bx-item:nth-child(7), .bx-item:nth-child(8) { border-bottom: none; }
.bx-name { font-family: 'Bebas Neue', sans-serif; font-size: 1rem; letter-spacing: 1.5px; color: #111; margin-bottom: 4px; }
.bx-dims { font-family: 'DM Mono', monospace; font-size: 0.7rem; color: #888; }
.bx-vol  { font-family: 'DM Mono', monospace; font-size: 0.65rem; color: #bbb; margin-top: 4px; }

/* ── Stat grid ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0;
    border: 1px solid #ddd;
    overflow: hidden;
    margin-bottom: 2.5rem;
    background: #fff;
}
.stat-cell { padding: 1.4rem 1.6rem; border-right: 1px solid #ddd; }
.stat-cell:last-child { border-right: none; }
.stat-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 6px;
}
.stat-value { font-family: 'Bebas Neue', sans-serif; font-size: 2.2rem; letter-spacing: 1px; color: #111; line-height: 1; }
.stat-value.red { color: #e63329; }

/* ── Config panels ── */
.config-panel {
    border: 1px solid #ddd;
    background: #fff;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.5rem;
}
.config-panel.accent { border-left: 3px solid #111; background: #fafaf8; }
.config-title { font-family: 'Bebas Neue', sans-serif; font-size: 1.1rem; letter-spacing: 2px; color: #111; margin-bottom: 0.3rem; }
.config-sub { font-family: 'DM Mono', monospace; font-size: 0.65rem; letter-spacing: 1.2px; text-transform: uppercase; color: #aaa; margin-bottom: 1rem; }

/* ── Buttons ── */
.stButton > button {
    background: #111 !important; color: #f7f4ef !important;
    border: none !important; border-radius: 0 !important;
    font-family: 'DM Mono', monospace !important; font-size: 0.78rem !important;
    letter-spacing: 2px !important; text-transform: uppercase !important;
    padding: 0.75rem 2.5rem !important; transition: background 0.15s !important;
    box-shadow: none !important; font-weight: 500 !important;
}
.stButton > button:hover { background: #e63329 !important; }
[data-testid="stDownloadButton"] > button { background: #2a9d5c !important; color: #fff !important; }
[data-testid="stDownloadButton"] > button:hover { background: #1e7a46 !important; }

/* ── Form labels ── */
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stFileUploader"] label,
div[data-testid="stRadio"] label,
.stCheckbox label,
[data-testid="stWidgetLabel"] p {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important; letter-spacing: 1.5px !important;
    text-transform: uppercase !important; color: #666 !important; font-weight: 400 !important;
}
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stNumberInput"] input {
    background: #fff !important; border: 1px solid #ddd !important;
    border-radius: 0 !important; color: #111 !important;
    font-family: 'DM Mono', monospace !important; font-size: 0.85rem !important;
}
.stSuccess, [data-testid="stAlert"] {
    background: #eef8f3 !important; border: 1px solid #2a9d5c !important;
    border-radius: 0 !important; color: #1a5c35 !important;
}
[data-testid="stFileUploader"] {
    border: 2px dashed #ccc !important; border-radius: 0 !important; background: #fff !important;
}
.stDataFrame { display: none; }
[data-testid="stVerticalBlock"] { gap: 0.6rem !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Session state
# ─────────────────────────────────────────────────────────────────────────────
for k, v in [('step', 1), ('data', {}), ('mapping_confirmed', False)]:
    if k not in st.session_state:
        st.session_state[k] = v

def next_step(): st.session_state.step += 1
def reset_process():
    for k in list(st.session_state.keys()): del st.session_state[k]
    st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# Box catalogue
# ─────────────────────────────────────────────────────────────────────────────
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
    (150,          ["A", "B"]),
    (380,          ["C", "D"]),
    (900,          ["E", "F"]),
    (float("inf"), ["G", "H"]),
]

# ─────────────────────────────────────────────────────────────────────────────
# Parsing helpers  (UNCHANGED)
# ─────────────────────────────────────────────────────────────────────────────
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
        pass
    m = re.search(r"(\d+\.?\d*)", s)
    return float(m.group(1)) if m else 0.0

def parse_fragility(val):
    return "Fragile" if parse_yes_no(val) else "Non-Fragile"

def lifespan_to_density_factor(val):
    if pd.isna(val): return 1.0
    s = str(val).strip().lower()
    if s in ("long", "high", "durable"): return 0.85
    if s in ("medium", "mid"): return 0.92
    try:
        years = float(re.search(r"(\d+\.?\d*)", s).group(1))
        if years >= 5: return 0.85
        if years >= 2: return 0.92
    except Exception:
        pass
    return 1.0

# ─────────────────────────────────────────────────────────────────────────────
# Core fit engine  (UNCHANGED)
# ─────────────────────────────────────────────────────────────────────────────
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
            best_info = {
                "count": best_count,
                "dims": f"{ow}x{ol}x{oh}",
                "orientation": labels[idx[2]],
                "used_vol": round(best_count * p[0] * p[1] * p[2], 2),
            }
    if not best_info: return None
    bvol = bw * bl * bh
    best_info["util"]   = round((best_info["used_vol"] / bvol) * 100, 2)
    best_info["unused"] = round(bvol - best_info["used_vol"], 2)
    return best_info

# ─────────────────────────────────────────────────────────────────────────────
# Rule-source resolver
# Completely separates UI-driven (single-part) from Excel-driven (multi-part).
# ui_handling is a dict for single-part mode, or None for multi-part mode.
# ─────────────────────────────────────────────────────────────────────────────
def _resolve_handling(row, ui_handling):
    """
    Returns (fragile_str, stacking_bool, nested_bool, nest_pct_float).
    Source is determined exclusively by whether ui_handling is provided.
    No fallback mixing between sources.
    """
    if ui_handling is not None:
        # Single-part: UI is the only source
        fragile  = parse_fragility(ui_handling["Fragile"])
        stacking = parse_yes_no(ui_handling["Stacking"])
        nested   = parse_yes_no(ui_handling["Nesting"])
        nest_pct = float(ui_handling["Nesting %"])
    else:
        # Multi-part: Excel row is the only source
        fragile  = parse_fragility(row.get("Fragile", "No"))
        stacking = parse_yes_no(row.get("Stacking", "Yes"))
        nested   = parse_yes_no(row.get("Nesting", "No"))
        nest_pct = parse_nesting_pct(row.get("Nesting %", 0))
    return fragile, stacking, nested, nest_pct

# ─────────────────────────────────────────────────────────────────────────────
# Box selection — two fully separate paths, no cross-contamination
# ─────────────────────────────────────────────────────────────────────────────
def catalogue_best_box(row, ui_handling=None):
    """
    Option A — auto-select from predefined catalogue using size-bracket tiers.
    ui_handling: dict for single-part, None for multi-part.
    """
    fragile, stacking, nested, nest_pct = _resolve_handling(row, ui_handling)
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
            res = calculate_fit(BOXES[box_key], part_dim, nested, nest_pct, stacking, fragile)
            if res is None: continue
            score = res["count"] * density_f + res["util"] / 1000
            if score > best_score:
                best_score, best_box_key, best_result = score, box_key, res
        if best_result is not None:
            tier_name = next(
                (["Small", "Medium", "Large", "Very Large"][i]
                 for i, (_, keys) in enumerate(TIER_BANDS) if best_box_key in keys), "—"
            )
            return {
                "box_key":   best_box_key,
                "box_dims":  BOXES[best_box_key],
                "box_label": f"Option {best_box_key} ({BOXES[best_box_key][0]}×{BOXES[best_box_key][1]}×{BOXES[best_box_key][2]})",
                "tier":      tier_name,
                **best_result,
            }
    return None


def manual_box_fit(row, box_dim, ui_handling=None):
    """
    Option B — evaluate fit against one user-supplied box only.
    No catalogue lookup. box_dim = (L, W, H) floats.
    ui_handling: dict for single-part, None for multi-part.
    """
    fragile, stacking, nested, nest_pct = _resolve_handling(row, ui_handling)
    part_dim = (row["Width"], row["Length"], row["Height"])
    res = calculate_fit(box_dim, part_dim, nested, nest_pct, stacking, fragile)
    if res is None: return None
    return {
        "box_key":   "CUSTOM",
        "box_dims":  box_dim,
        "box_label": f"Custom ({box_dim[0]:.0f}×{box_dim[1]:.0f}×{box_dim[2]:.0f})",
        "tier":      "Custom",
        **res,
    }

# ─────────────────────────────────────────────────────────────────────────────
# Masthead
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
  <div>
    <span class="masthead-logo">AgiloPack</span><span class="masthead-accent"></span>
  </div>
  <div class="masthead-tagline">Box Space Utilization</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Step ribbon
# ─────────────────────────────────────────────────────────────────────────────
STEPS = ["Upload & Configure", "Results"]
cur = st.session_state.step
ribbon_html = '<div class="ribbon">'
for i, s in enumerate(STEPS, 1):
    cls = "active" if i == cur else ("done" if i < cur else "")
    ribbon_html += f'<div class="rib-item {cls}"><span class="rib-num">0{i}</span>{s}</div>'
ribbon_html += '</div>'
st.markdown(ribbon_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — UPLOAD & CONFIGURE
# ─────────────────────────────────────────────────────────────────────────────
if cur == 1:
    st.markdown("""
    <div class="sec-head">
      <span class="sec-num">01</span>
      <span class="sec-title">Upload &amp; Configure</span>
    </div>
    <hr class="sec-rule">
    <p class="sec-desc">
      Choose your box definition mode, then upload your parts file.
      Required columns and available controls adapt automatically based on upload size.
    </p>
    """, unsafe_allow_html=True)

    # ── 1a: Box definition mode ────────────────────────────────────────────
    st.markdown("""
    <div class="config-panel">
      <div class="config-title">Box Definition Mode</div>
      <div class="config-sub">Choose how boxes are defined for this run</div>
    </div>
    """, unsafe_allow_html=True)

    box_mode = st.radio(
        "Box mode",
        ["Option A – Predefined catalogue  (auto-select best box per part)",
         "Option B – Manual box size  (one custom box applied to all parts)"],
        key="box_mode_radio",
        label_visibility="collapsed",
    )
    use_catalogue = box_mode.startswith("Option A")

    # ── 1b: Custom box inputs (Option B only) ──────────────────────────────
    custom_box_dim = None
    if not use_catalogue:
        st.markdown("""
        <div class="config-panel accent" style="margin-top:1rem">
          <div class="config-title">Custom Box Dimensions</div>
          <div class="config-sub">This box will be applied uniformly to every part (mm)</div>
        </div>
        """, unsafe_allow_html=True)
        cb1, cb2, cb3 = st.columns(3)
        with cb1:
            cb_l = st.number_input("Box Length (mm)", min_value=1.0, value=400.0, step=1.0, key="cb_l")
        with cb2:
            cb_w = st.number_input("Box Width (mm)",  min_value=1.0, value=300.0, step=1.0, key="cb_w")
        with cb3:
            cb_h = st.number_input("Box Height (mm)", min_value=1.0, value=220.0, step=1.0, key="cb_h")
        custom_box_dim = (cb_l, cb_w, cb_h)

    # ── 1c: Catalogue reference (Option A only) ────────────────────────────
    if use_catalogue:
        st.markdown("<p class='sec-desc' style='margin-top:1.2rem;margin-bottom:0.6rem'>"
                    "Standard box catalogue — engine auto-selects the best match per part:</p>",
                    unsafe_allow_html=True)
        grid_html = '<div class="bx-grid">'
        for k, v in BOXES.items():
            grid_html += (f'<div class="bx-item"><div class="bx-name">Option {k}</div>'
                          f'<div class="bx-dims">{v[0]} × {v[1]} × {v[2]} mm</div>'
                          f'<div class="bx-vol">{v[0]*v[1]*v[2]:,} mm³</div></div>')
        grid_html += '</div>'
        st.markdown(grid_html, unsafe_allow_html=True)

    # ── 1d: File upload ────────────────────────────────────────────────────
    st.markdown("---")
    uploaded_file = st.file_uploader("Drop parts file here (.csv or .xlsx)", type=["csv", "xlsx"])

    if uploaded_file:
        if 'raw_df' not in st.session_state:
            st.session_state.raw_df = (
                pd.read_csv(uploaded_file)
                if uploaded_file.name.endswith('.csv')
                else pd.read_excel(uploaded_file)
            )
        df = st.session_state.raw_df.copy()
        df.columns = [c.strip() for c in df.columns]

        is_single = (len(df) == 1)

        # ── Column validation — requirements differ by upload mode ─────────
        # Single-part: Fragile/Stacking/Nesting/Nesting % come from UI → NOT required
        # Multi-part:  all handling cols MUST be in the file → required
        BASE_REQUIRED    = {"Part Name", "Length", "Width", "Height"}
        HANDLING_COLS    = {"Fragile", "Stacking", "Nesting", "Nesting %"}
        required         = BASE_REQUIRED if is_single else BASE_REQUIRED | HANDLING_COLS
        missing          = required - set(df.columns)

        if missing:
            if is_single:
                st.error(f"Single-part mode requires: {', '.join(sorted(missing))}")
            else:
                st.error(
                    f"Multi-part mode requires all handling columns. "
                    f"Missing: {', '.join(sorted(missing))}"
                )
            st.stop()

        for c in ["Width", "Length", "Height"]:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        # ── Mode indicator ─────────────────────────────────────────────────
        mode_label = "Single-part · UI-driven handling" if is_single else "Multi-part · Excel-driven handling"
        box_short  = ("Catalogue auto-select" if use_catalogue
                      else f"Custom {custom_box_dim[0]:.0f}×{custom_box_dim[1]:.0f}×{custom_box_dim[2]:.0f} mm")
        dot_cls    = "green" if is_single else ""

        st.markdown(f"""
        <div class="mode-badge">
          <div class="mode-dot {dot_cls}"></div>
          <span class="mode-text">{mode_label} &nbsp;·&nbsp; {box_short}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="pill-row">
          <div class="pill"><div class="pill-label">File</div>
            <div class="pill-val" style="font-size:0.8rem">{uploaded_file.name}</div></div>
          <div class="pill"><div class="pill-label">Parts</div>
            <div class="pill-val">{len(df)}</div></div>
          <div class="pill"><div class="pill-label">Columns</div>
            <div class="pill-val">{len(df.columns)}</div></div>
          <div class="pill"><div class="pill-label">Box mode</div>
            <div class="pill-val" style="font-size:0.78rem">{"Catalogue" if use_catalogue else "Manual"}</div></div>
        </div>
        """, unsafe_allow_html=True)

        # ── 1e: Single-part handling rules (UI, not from file) ────────────
        # This entire block is HIDDEN for multi-part uploads.
        ui_handling = None
        if is_single:
            st.markdown("""
            <div class="config-panel accent">
              <div class="config-title">Handling Rules</div>
              <div class="config-sub">Single-part mode — select here (not read from file)</div>
            </div>
            """, unsafe_allow_html=True)

            hc1, hc2 = st.columns(2)
            with hc1:
                h_fragile  = st.selectbox("Fragile",  ["No", "Yes"], key="h_fragile")
                h_stacking = st.selectbox("Stacking", ["Yes", "No"], key="h_stacking")
            with hc2:
                h_nesting  = st.selectbox("Nesting",  ["No", "Yes"], key="h_nesting")
                h_nest_pct = st.number_input(
                    "Nesting %", min_value=0.0, max_value=100.0,
                    value=0.0, step=1.0, key="h_nest_pct",
                )

            ui_handling = {
                "Fragile":   h_fragile,
                "Stacking":  h_stacking,
                "Nesting":   h_nesting,
                "Nesting %": h_nest_pct,
            }

        # ── Store config and proceed ───────────────────────────────────────
        st.session_state.data.update({
            'parts_df':       df,
            'is_single':      is_single,
            'use_catalogue':  use_catalogue,
            'custom_box_dim': custom_box_dim,
            'ui_handling':    ui_handling,
        })
        st.session_state.mapping_confirmed = True

        if is_single:
            st.success("✓  Single part loaded. Handling rules taken from UI controls above.")
        else:
            st.success(f"✓  {len(df)} parts loaded. Handling rules will be read strictly from the file.")

        st.button("Run analysis →", on_click=next_step)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — RESULTS
# ─────────────────────────────────────────────────────────────────────────────
elif cur == 2:
    d              = st.session_state.data
    df             = d['parts_df']
    is_single      = d['is_single']
    use_catalogue  = d['use_catalogue']
    custom_box_dim = d['custom_box_dim']
    ui_handling    = d['ui_handling']   # None for multi-part

    results = []
    skipped = []

    for _, row in df.iterrows():
        # ── Route to the correct engine path ──────────────────────────────
        # ui_handling is non-None only in single-part mode.
        # multi-part always passes ui_handling=None → rules come from row.
        # No mixing is possible.
        if use_catalogue:
            best = catalogue_best_box(row, ui_handling=ui_handling)
        else:
            best = manual_box_fit(row, custom_box_dim, ui_handling=ui_handling)

        if best is None:
            skipped.append(str(row.get("Part Name", "?")))
            continue

        # Display values come from the same authoritative source
        fragile, stacking, nested, nest_pct = _resolve_handling(row, ui_handling)
        lifespan = (str(row.get("Lifespan", "—")).strip()
                    if not pd.isna(row.get("Lifespan", float("nan"))) else "—")

        results.append({
            "Part Name":    row["Part Name"],
            "Tier":         best.get("tier", "—"),
            "Best Box":     best["box_label"],
            "Parts / Box":  best["count"],
            "Orientation":  best["dims"],
            "Placement":    best["orientation"],
            "Utilization":  best["util"],
            "Unused (mm³)": int(best["unused"]),
            "Fragile":      fragile,
            "Stacking":     "Yes" if stacking else "No",
            "Nesting":      f"Yes ({nest_pct:.0f}%)" if nested else "No",
            "Lifespan":     lifespan,
        })

    res_df = pd.DataFrame(results)

    avg_util  = res_df["Utilization"].mean() if len(res_df) else 0
    best_part = res_df.loc[res_df["Utilization"].idxmax(), "Part Name"] if len(res_df) else "—"
    top_box   = res_df["Best Box"].value_counts().idxmax() if len(res_df) else "—"

    # Mode banner
    mode_label = "Single-part · UI-driven handling" if is_single else "Multi-part · Excel-driven handling"
    box_banner = ("Predefined Catalogue" if use_catalogue
                  else f"Custom Box  {custom_box_dim[0]:.0f}×{custom_box_dim[1]:.0f}×{custom_box_dim[2]:.0f} mm")
    dot_cls = "green" if is_single else ""

    st.markdown(f"""
    <div class="mode-badge">
      <div class="mode-dot {dot_cls}"></div>
      <span class="mode-text">{mode_label} &nbsp;·&nbsp; {box_banner}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sec-head">
      <span class="sec-num">02</span>
      <span class="sec-title">Results</span>
    </div>
    <hr class="sec-rule">
    """, unsafe_allow_html=True)

    if skipped:
        st.warning(f"⚠️  {len(skipped)} part(s) could not be fitted and were skipped: {', '.join(skipped)}")

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
        <div class="stat-label">{"Box Used" if not use_catalogue else "Top Box"}</div>
        <div class="stat-value" style="font-size:0.9rem;letter-spacing:0">{top_box}</div>
      </div>
      <div class="stat-cell">
        <div class="stat-label">Best Fit Part</div>
        <div class="stat-value" style="font-size:1.1rem;letter-spacing:0">{best_part}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Results table ──────────────────────────────────────────────────────
    tier_colors = {
        "Small": "#4a90d9", "Medium": "#e6a817",
        "Large": "#e63329", "Very Large": "#7b47c2", "Custom": "#555"
    }
    rows_html = ""
    for _, row in res_df.iterrows():
        u         = float(row["Utilization"])
        bar_color = "#2a9d5c" if u >= 60 else "#e63329"
        unused_v  = int(row["Unused (mm³)"])
        tier      = row.get("Tier", "—")
        tier_bg   = tier_colors.get(tier, "#aaa")

        rows_html += (
            f"<tr>"
            f"<td>{row['Part Name']}</td>"
            f"<td><span style='background:{tier_bg};color:#fff;padding:2px 8px;"
            f"font-size:0.6rem;letter-spacing:1px;text-transform:uppercase'>{tier}</span></td>"
            f"<td>{row['Best Box']}</td>"
            f"<td>{row['Parts / Box']}</td>"
            f"<td>{row['Orientation']}</td>"
            f"<td>{row['Placement']}</td>"
            f"<td>{u:.1f}%"
            f"<div style='background:#f0ece5;height:6px;width:100%;margin-top:4px;overflow:hidden'>"
            f"<div style='height:100%;width:{min(u,100):.1f}%;background:{bar_color}'></div></div></td>"
            f"<td>{unused_v:,}</td>"
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
      td {{ padding:0.85rem 1rem; border-bottom:1px solid #eee; color:#222; font-size:0.78rem; }}
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

    # ── Export ─────────────────────────────────────────────────────────────
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
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
    with c2:
        st.button("Start over", on_click=reset_process)
