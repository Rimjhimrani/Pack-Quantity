import streamlit as st
import pandas as pd
import itertools
import io

# --- Page Configuration ---
st.set_page_config(page_title="AgiloPack - Space Utilization", layout="wide")

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
    # Unpacking box dimensions (Length, Width, Height)
    bl, bw, bh = box_dim
    # Original indices for parts: 0: Width, 1: Length, 2: Height
    p_dims = [part_dim[0], part_dim[1], part_dim[2]]
    # Mapping for placement logic
    labels = {0: "Breadthwise", 1: "Lengthwise", 2: "Heightwise"}
    
    orient_indices = list(itertools.permutations([0, 1, 2]))
    best_count = 0
    best_info = None

    for idx in orient_indices:
        # ow: width, ol: length, oh: vertical height in box
        ow, ol, oh = p_dims[idx[0]], p_dims[idx[1]], p_dims[idx[2]]
        
        # Fragility Rule: If fragile, must be "Heightwise" (index 2 must be the vertical dimension)
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

# --- UI Layout ---
st.title("📦 AgiloPack – Step-Wise Process Flow")

# --- STEP 1: BOX ---
if st.session_state.step == 1:
    st.header("Step 1: Select Box Size")
    box_type = st.radio("Choose Source:", ["Predefined Options", "Enter Custom Dimensions"])
    
    # Updated Predefined Boxes from the Table
    PREDEFINED_BOXES = {
        "Option A (120x80x80)": (120, 80, 80),
        "Option B (200x180x120)": (200, 180, 120),
        "Option C (360x360x100)": (360, 360, 100),
        "Option D (400x300x220)": (400, 300, 220),
        "Option E (600x500x400)": (600, 500, 400),
        "Option F (850x400x250)": (850, 400, 250),
        "Option G (1200x1000x250)": (1200, 1000, 250),
        "Option H (1500x1200x1000)": (1500, 1200, 1000),
        "Option i (1500x1200x1000)": (1500, 1200, 1000),
    }

    if box_type == "Predefined Options":
        option = st.selectbox("Standard Boxes (Length x Width x Height):", list(PREDEFINED_BOXES.keys()))
        st.session_state.data['box'] = PREDEFINED_BOXES[option]
    else:
        c1, c2, c3 = st.columns(3)
        # Order aligned with the table: Length, Width, Height
        st.session_state.data['box'] = (
            c1.number_input("Box Length", min_value=1.0, value=50.0),
            c2.number_input("Box Width", min_value=1.0, value=50.0),
            c3.number_input("Box Height", min_value=1.0, value=50.0)
        )
    st.button("Next ➡️", on_click=next_step)

# --- STEP 2: DATA MAPPING ---
elif st.session_state.step == 2:
    st.header("Step 2: Upload & Map Part Data")
    uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
    if uploaded_file:
        if 'raw_df' not in st.session_state:
            st.session_state.raw_df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        
        col_names = st.session_state.raw_df.columns.tolist()
        c1, c2, c3, c4 = st.columns(4)
        n_col, w_col, l_col, h_col = c1.selectbox("Part Name", col_names), c2.selectbox("Width", col_names), c3.selectbox("Length", col_names), c4.selectbox("Height", col_names)
        
        if st.button("Confirm Mapping ✅"):
            mapped_df = st.session_state.raw_df[[n_col, w_col, l_col, h_col]].copy()
            mapped_df.columns = ['Part_Name', 'Width', 'Length', 'Height']
            for col in ['Width', 'Length', 'Height']:
                mapped_df[col] = pd.to_numeric(mapped_df[col], errors='coerce').fillna(0)
            st.session_state.data['parts_df'] = mapped_df
            st.session_state.mapping_confirmed = True
        
        if st.session_state.mapping_confirmed:
            st.success("Mapping Confirmed")
            st.button("Next ➡️", on_click=next_step)

# --- STEP 3: NESTING ---
elif st.session_state.step == 3:
    st.header("Step 3: Nesting Configuration")
    is_nested = st.checkbox("Will parts be nested?")
    nest_pct = st.slider("Define Nesting Height Percentage (%)", 1, 100, 20) if is_nested else 0
    st.session_state.data.update({'nested': is_nested, 'nest_pct': nest_pct})
    st.button("Next ➡️", on_click=next_step)

# --- STEP 4: HANDLING ---
elif st.session_state.step == 4:
    st.header("Step 4: Handling Rules")
    stacking = st.radio("Is stacking allowed?", ["Yes", "No"]) == "Yes"
    fragility = st.selectbox("Fragility Status:", ["Non-Fragile", "Fragile"])
    st.session_state.data.update({'stacking': stacking, 'fragility': fragility})
    st.button("Generate Results 🚀", on_click=next_step)

# --- STEP 5: RESULTS & EXCEL ---
elif st.session_state.step == 5:
    st.header("Final Results & Space Utilization")
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
                "Placement Orientation": res['orientation_label'],
                "Utilization %": res['util'],
                "Unused Vol": res['unused_vol']
            })

    res_df = pd.DataFrame(results)
    st.dataframe(res_df, use_container_width=True)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        res_df.to_excel(writer, index=False, sheet_name='AgiloPack_Results')
    
    st.download_button(
        label="Download as Excel (.xlsx) 📥",
        data=output.getvalue(),
        file_name='AgiloPack_Analysis.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
    st.button("Start New Process 🔄", on_click=reset_process)
