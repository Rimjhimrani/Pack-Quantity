import streamlit as st
import pandas as pd
import itertools

# --- Page Configuration ---
st.set_page_config(page_title="AgiloPack - Space Utilization", layout="wide")

# --- Initialize Session State ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'data' not in st.session_state:
    st.session_state.data = {}

def next_step():
    st.session_state.step += 1

def reset_process():
    st.session_state.step = 1
    st.session_state.data = {}

# --- Calculation Engine ---
def calculate_fit(box_dim, part_dim, nested, nest_pct, stacking, fragile):
    bw, bl, bh = box_dim
    pw, pl, ph = part_dim
    
    # Generate orientations
    orientations = list(set(itertools.permutations([pw, pl, ph])))
    best_count = 0
    best_orient = None
    
    for orient in orientations:
        ow, ol, oh = orient
        if fragile == "Fragile" and oh != ph:
            continue
            
        cols = bw // ow
        rows = bl // ol
        per_layer = cols * rows
        
        if per_layer == 0: continue
            
        if not stacking:
            total_parts = per_layer
        else:
            if nested:
                increment = oh * (nest_pct / 100)
                layers = 1 + int((bh - oh) // increment) if increment > 0 else 1
                total_parts = per_layer * max(1, layers)
            else:
                layers = bh // oh
                total_parts = per_layer * layers
                
        if total_parts > best_count:
            best_count = int(total_parts)
            best_orient = orient

    part_volume = pw * pl * ph
    used_volume = best_count * part_volume
    box_volume = bw * bl * bh
    utilization = (used_volume / box_volume) * 100 if box_volume > 0 else 0
    
    return {
        "count": best_count,
        "orientation": best_orient,
        "used_vol": used_volume,
        "unused_vol": box_volume - used_volume,
        "util_pct": round(utilization, 2)
    }

# --- UI Layout ---
st.title("📦 AgiloPack – Step-Wise Process Flow")

# --- Step 1: Box Dimensions ---
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

# --- Step 2: Part Data Upload & Column Mapping ---
elif st.session_state.step == 2:
    st.header("Step 2: Upload Part Data")
    uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        
        st.write("### Map Your Columns")
        st.info("Match the required fields to your file columns to avoid errors.")
        
        col_names = df.columns.tolist()
        
        c1, c2, c3, c4 = st.columns(4)
        name_col = c1.selectbox("Part Name Column", col_names)
        w_col = c2.selectbox("Width Column", col_names)
        l_col = c3.selectbox("Length Column", col_names)
        h_col = c4.selectbox("Height Column", col_names)
        
        # Clean up the dataframe to only use selected columns and rename them
        final_df = df[[name_col, w_col, l_col, h_col]].copy()
        final_df.columns = ['Part_Name', 'Width', 'Length', 'Height']
        
        st.session_state.data['parts_df'] = final_df
        st.success("Columns mapped successfully!")
        st.dataframe(final_df.head())
        
        st.button("Next ➡️", on_click=next_step)

# --- Step 3: Nesting Logic ---
elif st.session_state.step == 3:
    st.header("Step 3: Nesting Configuration")
    is_nested = st.checkbox("Will parts be nested?")
    nest_pct = 0
    if is_nested:
        nest_pct = st.slider("Define Nesting Height Percentage (%)", 1, 100, 20)
    
    st.session_state.data['nested'] = is_nested
    st.session_state.data['nest_pct'] = nest_pct
    st.button("Next ➡️", on_click=next_step)

# --- Step 4: Handling Rules ---
elif st.session_state.step == 4:
    st.header("Step 4: Handling Rules")
    stacking = st.radio("Is stacking allowed?", ["Yes", "No"]) == "Yes"
    fragility = st.selectbox("Fragility Status:", ["Non-Fragile", "Fragile"])
    
    st.session_state.data['stacking'] = stacking
    st.session_state.data['fragility'] = fragility
    
    if st.button("Generate Results 🚀"):
        next_step()

# --- Step 5: Final Results ---
elif st.session_state.step == 5:
    st.header("Final Results & Space Utilization")
    
    box = st.session_state.data['box']
    df = st.session_state.data['parts_df']
    results = []
    
    # Using the standardized names from Step 2
    for _, row in df.iterrows():
        part_dim = (float(row['Width']), float(row['Length']), float(row['Height']))
        res = calculate_fit(
            box, 
            part_dim, 
            st.session_state.data['nested'],
            st.session_state.data['nest_pct'],
            st.session_state.data['stacking'],
            st.session_state.data['fragility']
        )
        results.append({
            "Part Name": row['Part_Name'],
            "Parts Per Box": res['count'],
            "Orientation (W,L,H)": str(res['orientation']),
            "Used Vol": res['used_vol'],
            "Utilization (%)": res['util_pct']
        })
    
    res_df = pd.DataFrame(results)
    st.dataframe(res_df, use_container_width=True)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Avg. Utilization", f"{res_df['Utilization (%)'].mean():.1f}%")
    m2.metric("Total Box Volume", f"{box[0]*box[1]*box[2]:,}")
    m3.metric("Total Parts Analyzed", len(res_df))

    st.button("Start New Process 🔄", on_click=reset_process)
