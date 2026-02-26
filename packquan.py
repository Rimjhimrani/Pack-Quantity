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
    """
    Evaluates all 6 orientations and returns the best fit.
    """
    bw, bl, bh = box_dim
    pw, pl, ph = part_dim
    
    # Generate all 6 possible orientations (L x W x H)
    orientations = list(set(itertools.permutations([pw, pl, ph])))
    
    best_count = 0
    best_orient = None
    
    for orient in orientations:
        ow, ol, oh = orient
        
        # Fragility Rule: If fragile, maybe only specific orientations are valid.
        # Here we assume fragile parts cannot be rotated onto their side (Height must stay H)
        if fragile == "Fragile" and oh != ph:
            continue
            
        # 1. Calculate how many fit on the floor (Grid)
        cols = bw // ow
        rows = bl // ol
        per_layer = cols * rows
        
        if per_layer == 0:
            continue
            
        # 2. Calculate Vertical Fitting (Stacking/Nesting)
        if not stacking:
            # If stacking is not allowed, only 1 layer is possible
            total_parts = per_layer
        else:
            if nested:
                # Nesting Formula: First part is 100% height, others are 'nest_pct'%
                # Total H = oh + (n-1) * (oh * nest_pct/100) <= bh
                increment = oh * (nest_pct / 100)
                if increment == 0: # Avoid div by zero
                    layers = 1000000 
                else:
                    layers = 1 + int((bh - oh) // increment)
                total_parts = per_layer * max(1, layers)
            else:
                # Standard Stacking
                layers = bh // oh
                total_parts = per_layer * layers
                
        if total_parts > best_count:
            best_count = int(total_parts)
            best_orient = orient

    # Utilization Stats
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
        option = st.selectbox("Standard Boxes (W x L x H):", ["Small (20x20x20)", "Medium (40x40x40)", "Large (60x60x60)"])
        dims = {"Small (20x20x20)": (20,20,20), "Medium (40x40x40)": (40,40,40), "Large (60x60x60)": (60,60,60)}
        st.session_state.data['box'] = dims[option]
    else:
        c1, c2, c3 = st.columns(3)
        bw = c1.number_input("Width", min_value=1.0, value=50.0)
        bl = c2.number_input("Length", min_value=1.0, value=50.0)
        bh = c3.number_input("Height", min_value=1.0, value=50.0)
        st.session_state.data['box'] = (bw, bl, bh)
    
    st.button("Next ➡️", on_click=next_step)

# --- Step 2: Part Data Upload ---
elif st.session_state.step == 2:
    st.header("Step 2: Upload Part Data")
    st.info("Upload a CSV/Excel with columns: Part_Name, Width, Length, Height")
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])
    
    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.write("Preview of Uploaded Data:")
        st.dataframe(df.head())
        st.session_state.data['parts_df'] = df
        st.button("Next ➡️", on_click=next_step)

# --- Step 3 & 4: Nesting Logic ---
elif st.session_state.step == 3:
    st.header("Step 3: Nesting Configuration")
    is_nested = st.checkbox("Will parts be nested?")
    nest_pct = 0
    if is_nested:
        nest_pct = st.slider("Define Nesting Height Percentage (%)", 1, 100, 20)
    
    st.session_state.data['nested'] = is_nested
    st.session_state.data['nest_pct'] = nest_pct
    st.button("Next ➡️", on_click=next_step)

# --- Step 5 & 6: Stacking & Fragility ---
elif st.session_state.step == 4:
    st.header("Step 4: Handling Rules")
    stacking = st.radio("Is stacking allowed?", ["Yes", "No"]) == "Yes"
    fragility = st.selectbox("Fragility Status:", ["Non-Fragile", "Fragile"])
    
    st.session_state.data['stacking'] = stacking
    st.session_state.data['fragility'] = fragility
    
    if st.button("Generate Results 🚀"):
        next_step()

# --- Final Results Display ---
elif st.session_state.step == 5:
    st.header("Final Results & Space Utilization")
    
    box = st.session_state.data['box']
    df = st.session_state.data['parts_df']
    results = []
    
    for index, row in df.iterrows():
        part_dim = (row['Width'], row['Length'], row['Height'])
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
            "Best Orientation (W,L,H)": str(res['orientation']),
            "Used Vol": res['used_vol'],
            "Unused Vol": res['unused_vol'],
            "Utilization (%)": res['util_pct']
        })
    
    res_df = pd.DataFrame(results)
    st.success("Analysis Complete!")
    st.dataframe(res_df)
    
    # Visual metrics for the first part as a summary
    if not res_df.empty:
        m1, m2, m3 = st.columns(3)
        m1.metric("Avg. Utilization", f"{res_df['Utilization (%)'].mean():.1f}%")
        m2.metric("Best Fit Count", f"{res_df['Parts Per Box'].max()} units")
        m3.metric("Total Rows Processed", len(res_df))

    st.button("Start New Process 🔄", on_click=reset_process)
