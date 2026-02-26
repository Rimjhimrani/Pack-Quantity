import streamlit as st
import pandas as pd
import itertools
import io

# --- Page Configuration ---
st.set_page_config(page_title="AgiloPack - Space Utilization", layout="wide", page_icon="📦")

# --- CSS Styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

/* ===== GLOBAL ===== */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* White text only for dark background Streamlit native elements */
.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stMarkdownContainer"] li,
.stApp [data-testid="stMarkdownContainer"] strong,
.stApp [data-testid="stWidgetLabel"] p,

.stApp [data-baseweb="radio"] span,
.stApp [data-baseweb="checkbox"] span {
    color: #ffffff !important;
}

.stApp {
    background: linear-gradient(135deg, #0f1923 0%, #1a2a3a 50%, #0f1923 100%);
    min-height: 100vh;
}

/* ===== HEADER ===== */
.main-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    background: linear-gradient(90deg, #f5a623, #f7c46e, #f5a623);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s linear infinite;
    margin-bottom: 0.2rem;
}

.main-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    color: #ffffff;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

@keyframes shimmer {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}

/* ===== 3D BOX ANIMATION ===== */
.box-scene-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 1.5rem 0;
}

.box-scene {
    width: 120px;
    height: 120px;
    perspective: 400px;
}

.box-3d {
    width: 100%;
    height: 100%;
    position: relative;
    transform-style: preserve-3d;
    animation: rotatebox 6s ease-in-out infinite;
}

@keyframes rotatebox {
    0%   { transform: rotateX(-20deg) rotateY(0deg); }
    50%  { transform: rotateX(-20deg) rotateY(180deg); }
    100% { transform: rotateX(-20deg) rotateY(360deg); }
}

.box-face {
    position: absolute;
    width: 80px;
    height: 80px;
    border: 2px solid rgba(245,166,35,0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    backface-visibility: visible;
}

.face-front  { background: rgba(245,166,35,0.18); transform: translateZ(40px); left:20px; top:20px; }
.face-back   { background: rgba(245,166,35,0.10); transform: rotateY(180deg) translateZ(40px); left:20px; top:20px; }
.face-left   { background: rgba(200,130,20,0.13); transform: rotateY(-90deg) translateZ(40px); left:20px; top:20px; }
.face-right  { background: rgba(200,130,20,0.13); transform: rotateY(90deg) translateZ(40px); left:20px; top:20px; }
.face-top    { background: rgba(245,200,80,0.20); transform: rotateX(90deg) translateZ(40px); left:20px; top:20px; }
.face-bottom { background: rgba(180,110,10,0.10); transform: rotateX(-90deg) translateZ(40px); left:20px; top:20px; }

/* ===== STEP INDICATOR ===== */
.step-bar {
    display: flex;
    justify-content: center;
    gap: 0;
    margin: 1.5rem auto 2rem auto;
    max-width: 600px;
}

.step-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
    position: relative;
}

.step-item:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 18px;
    left: 50%;
    width: 100%;
    height: 2px;
    background: rgba(255,255,255,0.1);
    z-index: 0;
}

.step-circle {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 0.9rem;
    border: 2px solid rgba(255,255,255,0.3);
    background: #1a2a3a;
    color: #ffffff;
    z-index: 1;
    position: relative;
}

.step-circle.active {
    background: #f5a623;
    border-color: #f5a623;
    color: #0f1923;
    box-shadow: 0 0 16px rgba(245,166,35,0.5);
}

.step-circle.done {
    background: #2a7a4a;
    border-color: #3aaa6a;
    color: #fff;
}

.step-label {
    font-size: 0.65rem;
    color: #ffffff;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 1px;
    text-align: center;
}

.step-label.active { color: #f5a623; font-weight: 600; }
.step-label.done   { color: #3aaa6a; }

/* ===== CARD ===== */
.ui-card {
    background: linear-gradient(135deg, rgba(26,42,58,0.95), rgba(20,32,45,0.95));
    border: 1px solid rgba(245,166,35,0.15);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
    margin-bottom: 1.5rem;
}

.card-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.6rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    color: #f5a623;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
    display: flex;
    align-items: center;
    gap: 10px;
}

.card-desc {
    color: #ffffff;
    font-size: 0.88rem;
    margin-bottom: 1.5rem;
}

/* ===== BADGES ===== */
.badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 50px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.badge-gold    { background: rgba(245,166,35,0.15); color: #f5a623; border: 1px solid rgba(245,166,35,0.3); }
.badge-green   { background: rgba(58,170,106,0.15); color: #3aaa6a; border: 1px solid rgba(58,170,106,0.3); }
.badge-blue    { background: rgba(60,120,200,0.15); color: #6aaaf5; border: 1px solid rgba(60,120,200,0.3); }

/* ===== BOX SIZE CARDS ===== */
.box-option-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
    gap: 12px;
    margin-top: 1rem;
}

.box-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 14px 16px;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}

.box-card:hover {
    border-color: rgba(245,166,35,0.4);
    background: rgba(245,166,35,0.05);
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(245,166,35,0.1);
}

.box-card.selected {
    border-color: #f5a623;
    background: rgba(245,166,35,0.08);
}

.box-card-label { color: #f5a623; font-weight: 600; font-size: 0.85rem; margin-bottom: 4px; }
.box-card-dims  { color: #ffffff; font-size: 0.78rem; }

/* ===== INFO STRIP ===== */
.info-strip {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin: 1rem 0;
}

.info-pill {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 0.82rem;
    color: #ffffff;
}

.info-pill span { color: #f5a623; font-weight: 600; }

/* ===== STREAMLIT OVERRIDES ===== */
.stButton > button {
    background: linear-gradient(135deg, #f5a623, #e8920a) !important;
    color: #0f1923 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    padding: 0.5rem 2rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 16px rgba(245,166,35,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px rgba(245,166,35,0.45) !important;
}

/* Reset button style */
.stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.06) !important;
    color: #ffffff !important;
    box-shadow: none !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}

div[data-testid="stSelectbox"] > div > div,
div[data-testid="stNumberInput"] input,
div[data-testid="stSlider"] {
    background: rgba(255,255,255,0.04) !important;
    border-color: rgba(255,255,255,0.12) !important;
    color: #e0eaf5 !important;
    border-radius: 8px !important;
}

label, .stRadio label, .stCheckbox label {
    color: #ffffff !important;
    font-size: 0.9rem !important;
}

/* Keep dropdown option text readable on light dropdown bg */
[data-baseweb="select"] [data-testid="stSelectboxVirtualDropdown"] * {
    color: #1a1a1a !important;
}

.stSuccess { 
    background: rgba(58,170,106,0.1) !important; 
    border: 1px solid rgba(58,170,106,0.3) !important;
    border-radius: 8px !important;
    color: #3aaa6a !important;
}

/* Dataframe */
.stDataFrame {
    border: 1px solid rgba(245,166,35,0.2) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* Divider */
.divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 1.5rem 0;
}

/* File uploader has light background - keep text dark */
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] button,
[data-testid="stFileUploader"] small {
    color: #1a1a1a !important;
}

/* Upload area */
[data-testid="stFileUploader"] {
    border: 2px dashed rgba(245,166,35,0.3) !important;
    border-radius: 12px !important;
    background: rgba(245,166,35,0.02) !important;
    padding: 1rem !important;
}

/* Progress stat */
.stat-row {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    margin-top: 1rem;
}
.stat-box {
    flex: 1;
    min-width: 120px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 14px 16px;
    text-align: center;
}
.stat-val { font-family: 'Rajdhani',sans-serif; font-size: 1.8rem; font-weight:700; color: #f5a623; }
.stat-key { font-size: 0.72rem; color: #ffffff; text-transform: uppercase; letter-spacing:1px; margin-top: 2px; }

/* Download button */
[data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, #2a7a4a, #1d5c37) !important;
    color: #fff !important;
    box-shadow: 0 4px 16px rgba(42,122,74,0.35) !important;
}
</style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'data' not in st.session_state:
    st.session_state.data = {}
if 'mapping_confirmed' not in st.session_state:
    st.session_state.mapping_confirmed = False

def next_step():
    st.session_state.step += 1

def reset_process():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- Calculation Engine ---
def calculate_fit(box_dim, part_dim, nested, nest_pct, stacking, fragile):
    bl, bw, bh = box_dim
    p_dims = [part_dim[0], part_dim[1], part_dim[2]]
    labels = {0: "Breadthwise", 1: "Lengthwise", 2: "Heightwise"}
    orient_indices = list(itertools.permutations([0, 1, 2]))
    best_count = 0
    best_info = None

    for idx in orient_indices:
        ow, ol, oh = p_dims[idx[0]], p_dims[idx[1]], p_dims[idx[2]]
        if fragile == "Fragile" and idx[2] != 2:
            continue
        cols = bw // ow
        rows = bl // ol
        per_layer = cols * rows
        if per_layer <= 0: continue
        if not stacking:
            total_parts = per_layer
        else:
            if nested:
                increment = oh * (nest_pct / 100)
                layers = 1 + int((bh - oh) // increment) if (bh >= oh and increment > 0) else 1
                total_parts = per_layer * max(1, layers)
            else:
                layers = bh // oh
                total_parts = per_layer * layers
        if total_parts > best_count:
            best_count = int(total_parts)
            best_info = {
                "count": best_count,
                "dims": f"{ow}x{ol}x{oh}",
                "orientation_label": labels[idx[2]],
                "used_vol": round(best_count * (p_dims[0] * p_dims[1] * p_dims[2]), 2)
            }

    if not best_info: return None
    box_vol = bw * bl * bh
    best_info["util"] = round((best_info["used_vol"] / box_vol) * 100, 2)
    best_info["unused_vol"] = round(box_vol - best_info["used_vol"], 2)
    return best_info

# --- 3D Box Animation HTML ---
def render_3d_box(size_label=""):
    return f"""
    <div class="box-scene-wrapper">
      <div class="box-scene">
        <div class="box-3d">
          <div class="box-face face-front">📦</div>
          <div class="box-face face-back"></div>
          <div class="box-face face-left"></div>
          <div class="box-face face-right"></div>
          <div class="box-face face-top"></div>
          <div class="box-face face-bottom"></div>
        </div>
      </div>
    </div>
    """

# --- Step Progress Bar ---
def render_steps(current):
    step_info = [
        ("1", "Box"),
        ("2", "Data"),
        ("3", "Nesting"),
        ("4", "Handling"),
        ("5", "Results"),
    ]
    html = '<div class="step-bar">'
    for i, (num, label) in enumerate(step_info, 1):
        if i < current:
            circle_cls = "done"
            label_cls = "done"
            num_display = "✓"
        elif i == current:
            circle_cls = "active"
            label_cls = "active"
            num_display = num
        else:
            circle_cls = ""
            label_cls = ""
            num_display = num
        html += f"""
        <div class="step-item">
          <div class="step-circle {circle_cls}">{num_display}</div>
          <div class="step-label {label_cls}">{label}</div>
        </div>"""
    html += '</div>'
    return html

# ===== HEADER =====
st.markdown('<div class="main-title">📦 AgiloPack</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Intelligent Box Space Utilization Tool</div>', unsafe_allow_html=True)
st.markdown(render_steps(st.session_state.step), unsafe_allow_html=True)

# ===== STEP 1: BOX =====
if st.session_state.step == 1:
    st.markdown(render_3d_box(), unsafe_allow_html=True)
    st.markdown("""
    <div class="ui-card">
        <div class="card-title">🗃️ Step 1 — Select Box Size</div>
        <div class="card-desc">Choose a standard shipping box or enter your own custom dimensions (L × W × H in mm).</div>
    </div>
    """, unsafe_allow_html=True)

    PREDEFINED_BOXES = {
        "Option A — 120×80×80":   (120, 80, 80),
        "Option B — 200×180×120": (200, 180, 120),
        "Option C — 360×360×100": (360, 360, 100),
        "Option D — 400×300×220": (400, 300, 220),
        "Option E — 600×500×400": (600, 500, 400),
        "Option F — 850×400×250": (850, 400, 250),
        "Option G — 1200×1000×250": (1200, 1000, 250),
        "Option H — 1500×1200×1000": (1500, 1200, 1000),
    }

    box_type = st.radio("Choose Input Type:", ["📋 Predefined Standard Boxes", "✏️ Custom Dimensions"], horizontal=True)

    if box_type == "📋 Predefined Standard Boxes":
        option = st.selectbox("Select a Standard Box (L × W × H in mm):", list(PREDEFINED_BOXES.keys()))
        dims = PREDEFINED_BOXES[option]
        st.session_state.data['box'] = dims
        st.markdown(f"""
        <div class="info-strip">
          <div class="info-pill">Length: <span>{dims[0]} mm</span></div>
          <div class="info-pill">Width: <span>{dims[1]} mm</span></div>
          <div class="info-pill">Height: <span>{dims[2]} mm</span></div>
          <div class="info-pill">Volume: <span>{dims[0]*dims[1]*dims[2]:,} mm³</span></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        c1, c2, c3 = st.columns(3)
        l = c1.number_input("📏 Length (mm)", min_value=1.0, value=50.0)
        w = c2.number_input("📐 Width (mm)", min_value=1.0, value=50.0)
        h = c3.number_input("📦 Height (mm)", min_value=1.0, value=50.0)
        st.session_state.data['box'] = (l, w, h)
        st.markdown(f"""
        <div class="info-strip">
          <div class="info-pill">Volume: <span>{l*w*h:,.0f} mm³</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.button("Next ➡️", on_click=next_step)

# ===== STEP 2: DATA MAPPING =====
elif st.session_state.step == 2:
    st.markdown("""
    <div class="ui-card">
        <div class="card-title">📂 Step 2 — Upload & Map Part Data</div>
        <div class="card-desc">Upload a CSV or Excel file containing your parts list. Then map columns to the correct dimensions.</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Drop your file here or click to browse", type=["csv", "xlsx"])

    if uploaded_file:
        if 'raw_df' not in st.session_state:
            st.session_state.raw_df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

        st.markdown(f"""
        <div class="info-strip">
          <div class="info-pill">File: <span>{uploaded_file.name}</span></div>
          <div class="info-pill">Rows: <span>{len(st.session_state.raw_df)}</span></div>
          <div class="info-pill">Columns: <span>{len(st.session_state.raw_df.columns)}</span></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("**Map Your Columns:**")
        col_names = st.session_state.raw_df.columns.tolist()
        c1, c2, c3, c4 = st.columns(4)
        n_col = c1.selectbox("🏷️ Part Name", col_names)
        w_col = c2.selectbox("↔️ Width", col_names)
        l_col = c3.selectbox("↕️ Length", col_names)
        h_col = c4.selectbox("⬆️ Height", col_names)

        if st.button("Confirm Mapping ✅"):
            mapped_df = st.session_state.raw_df[[n_col, w_col, l_col, h_col]].copy()
            mapped_df.columns = ['Part_Name', 'Width', 'Length', 'Height']
            for col in ['Width', 'Length', 'Height']:
                mapped_df[col] = pd.to_numeric(mapped_df[col], errors='coerce').fillna(0)
            st.session_state.data['parts_df'] = mapped_df
            st.session_state.mapping_confirmed = True

        if st.session_state.mapping_confirmed:
            st.success(f"✅ Mapping confirmed! {len(st.session_state.data['parts_df'])} parts ready for analysis.")
            st.button("Next ➡️", on_click=next_step)

# ===== STEP 3: NESTING =====
elif st.session_state.step == 3:
    st.markdown("""
    <div class="ui-card">
        <div class="card-title">🔗 Step 3 — Nesting Configuration</div>
        <div class="card-desc">Nesting allows parts to be placed inside each other (like stacking cups). Enable this if your parts support it.</div>
    </div>
    """, unsafe_allow_html=True)

    is_nested = st.checkbox("✅ Parts can be nested into each other")

    if is_nested:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**How deep does one part sit inside another?**")
        nest_pct = st.slider("Nesting Depth (% of part height)", 1, 100, 20,
                             help="20% means each additional nested part only adds 20% of its height to the stack.")
        st.markdown(f"""
        <div class="info-strip">
          <div class="info-pill">Nesting Depth: <span>{nest_pct}%</span></div>
          <div class="info-pill">Space Saved per Part: <span>{100 - nest_pct}%</span></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        nest_pct = 0

    st.session_state.data.update({'nested': is_nested, 'nest_pct': nest_pct})
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("Next ➡️", on_click=next_step)

# ===== STEP 4: HANDLING =====
elif st.session_state.step == 4:
    st.markdown("""
    <div class="ui-card">
        <div class="card-title">🛡️ Step 4 — Handling Rules</div>
        <div class="card-desc">Define how parts should be packed. Fragile parts stay upright; non-stackable parts occupy a single layer.</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Stacking**")
        stacking_opt = st.radio("Can parts be stacked on top of each other?", ["Yes ✅", "No ❌"])
        stacking = (stacking_opt == "Yes ✅")
    with c2:
        st.markdown("**Fragility**")
        fragility = st.selectbox("Part Fragility:", ["Non-Fragile 💪", "Fragile ⚠️"])
        fragility = "Fragile" if "Fragile ⚠️" in fragility else "Non-Fragile"

    st.markdown(f"""
    <div class="info-strip">
      <div class="info-pill">Stacking: <span>{"Allowed" if stacking else "Not Allowed"}</span></div>
      <div class="info-pill">Fragility: <span>{fragility}</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.session_state.data.update({'stacking': stacking, 'fragility': fragility})
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("Generate Results 🚀", on_click=next_step)

# ===== STEP 5: RESULTS =====
elif st.session_state.step == 5:
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
                "Parts Per Box": res['count'],
                "Best Orientation": res['dims'],
                "Placement": res['orientation_label'],
                "Utilization %": res['util'],
                "Unused Vol (mm³)": res['unused_vol']
            })

    res_df = pd.DataFrame(results)

    # Summary stats
    avg_util = res_df["Utilization %"].mean() if len(res_df) > 0 else 0
    total_parts = res_df["Parts Per Box"].sum() if len(res_df) > 0 else 0
    box_vol = box[0] * box[1] * box[2]

    st.markdown(f"""
    <div class="ui-card">
        <div class="card-title">✅ Results — Space Utilization</div>
        <div class="card-desc">Analysis complete for {len(res_df)} part(s) in the selected box.</div>
        <div class="stat-row">
          <div class="stat-box"><div class="stat-val">{len(res_df)}</div><div class="stat-key">Parts Analyzed</div></div>
          <div class="stat-box"><div class="stat-val">{avg_util:.1f}%</div><div class="stat-key">Avg Utilization</div></div>
          <div class="stat-box"><div class="stat-val">{box_vol:,}</div><div class="stat-key">Box Vol (mm³)</div></div>
          <div class="stat-box"><div class="stat-val">{box[0]}×{box[1]}×{box[2]}</div><div class="stat-key">Box Dims</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(render_3d_box(), unsafe_allow_html=True)

    st.dataframe(res_df, use_container_width=True)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        res_df.to_excel(writer, index=False, sheet_name='AgiloPack_Results')

    c1, c2 = st.columns([2, 1])
    with c1:
        st.download_button(
            label="📥 Download Excel Report",
            data=output.getvalue(),
            file_name='AgiloPack_Analysis.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    with c2:
        st.button("🔄 Start New Process", on_click=reset_process)
