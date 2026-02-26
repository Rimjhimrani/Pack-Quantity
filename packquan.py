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
    bw, bl, bh = box_dim
    # Indices: 0=Width, 1=Length, 2=Height
    p_dims = [part_dim[0], part_dim[1], part_dim[2]]
    labels = ["Width", "Length", "Height"]
    
    # We permute the indices (0,1,2) to keep track of which dim is which
    orient_indices = list(itertools.permutations([0, 1, 2]))
    
    best_count = 0
    best_info = {}

    for indices in orient_indices:
        # Map the permuted indices to actual values
        ow, ol, oh = p_dims[indices[0]], p_dims[indices[1]], p_dims[indices[2]]
        
        # Fragility Rule: If fragile, original Height (index 2) must stay as oh
        if fragile == "Fragile" and indices[2] != 2:
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
            # Find what is along the box length (ol)
            placed_along_length = labels[indices[1]]
            placed_along_width = labels[indices[0]]
            
            best_info = {
                "count": best_count,
                "dims": f"{ow} x {ol} x {oh}",
                "description": f"Part's {placed_along_length} along Box Length",
                "ow": ow, "ol": ol, "oh": oh
            }

    if not best_info:
        return None

    # Utilization
    part_vol = p_dims[0] * p_dims[1] * p_dims[2]
    box_vol = bw * bl * bh
    used_vol = best_count * part_vol
    
    best_info["util"] = round((used_vol / box_vol) * 100, 2)
    best_info["unused_vol"] = round(box_vol - used_vol, 2)
    return best_info

# --- UI Layout ---
st.title("📦 AgiloPack – Step-Wise Process Flow")

# --- STEP 1: BOX ---
if st.session_state.step == 1:
    st.header("Step 1: Select Box Size")
    box_type = st.radio("Choose Source:", ["Predefined Options", "Enter Custom Dimensions"])
    if box_type == "Predefined Options":
        option = st.selectbox("Standard Boxes:", ["Small (20x20x20)", "Medium (40x40x40)", "Large (60x60x60)"])
        dims = {"Small (20x20x20)": (20,20,20), "Medium (40x40x40)": (40,40,40), "Large (60x60x60)": (60,60,60)}
        st.session_state.data['box'] = dims[option]
    else:
        c1, c2, c3 = st.columns(3)
        bw = c1.number_input("Box Width", min_value=1.0, value=50.0)
        bl = c2.number_input("Box Length", min_value=1.0, value=50.0)
        bh = c3.number_input("Box Height", min_value=1.0, value=50.0)
        st.session_state.data['box'] = (bw, bl, bh)
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
        n_col = c1.selectbox("Part Name", col_names)
        w_col = c2.selectbox("Width", col_names)
        l_col = c3.selectbox("Length", col_names)
        h_col = c4.selectbox("Height", col_names)
        
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
    st.session_state.data['nested'] = is_nested
    st.session_state.data['nest_pct'] = nest_pct
    st.button("Next ➡️", on_click=next_step)

# --- STEP 4: HANDLING ---
elif st.session_state.step == 4:
    st.header("Step 4: Handling Rules")
    stacking = st.radio("Is stacking allowed?", ["Yes", "No"]) == "Yes"
    fragility = st.selectbox("Fragility Status:", ["Non-Fragile", "Fragile"])
    st.session_state.data['stacking'] = stacking
    st.session_state.data['fragility'] = fragility
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
                "Best Orientation (WxLxH)": res['dims'],
                "Placement Logic": res['description'],
                "Utilization %": res['util'],
                "Unused Volume": res['unused_vol']
            })

    res_df = pd.DataFrame(results)
    st.dataframe(res_df, use_container_width=True)

    # Excel Download Logic
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        res_df.to_excel(writer, index=False, sheet_name='Pack_Analysis')
    
    st.download_button(
        label="Download as Excel (.xlsx) 📥",
        data=output.getvalue(),
        file_name='AgiloPack_Analysis.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
    st.button("Start New Process 🔄", on_click=reset_process)
