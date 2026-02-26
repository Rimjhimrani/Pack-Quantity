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
    pw, pl, ph = part_dim
    
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
            best_orient = orient

    part_volume = pw * pl * ph
    used_volume = best_count * part_volume
    box_volume = bw * bl * bh
    utilization = (used_volume / box_volume) * 100 if box_volume > 0 else 0
    
    return {
        "count": best_count,
        "orientation": f"{best_orient[0]}x{best_orient[1]}x{best_orient[2]}" if best_orient else "N/A",
        "used_vol": round(used_volume, 2),
        "unused_vol": round(box_volume - used_volume, 2),
        "util_pct": round(utilization, 2)
    }

# --- UI Layout ---
st.title("📦 AgiloPack – Step-Wise Process Flow")

# --- STEP 1: BOX SELECTION ---
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

# --- STEP 2: DATA UPLOAD & MAPPING ---
elif st.session_state.step == 2:
    st.header("Step 2: Upload & Map Part Data")
    uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
    
    if uploaded_file:
        if 'raw_df' not in st.session_state:
            if uploaded_file.name.endswith('.csv'):
                st.session_state.raw_df = pd.read_csv(uploaded_file)
            else:
                st.session_state.raw_df = pd.read_excel(uploaded_file)
        
        df = st.session_state.raw_df
        col_names = df.columns.tolist()
        
        st.info("Match your file columns to the required fields:")
        c1, c2, c3, c4 = st.columns(4)
        n_col = c1.selectbox("Part Name", col_names)
        w_col = c2.selectbox("Width", col_names)
        l_col = c3.selectbox("Length", col_names)
        h_col = c4.selectbox("Height", col_names)
        
        if st.button("Confirm & Map Columns ✅"):
            mapped_df = df[[n_col, w_col, l_col, h_col]].copy()
            mapped_df.columns = ['Part_Name', 'Width', 'Length', 'Height']
            for col in ['Width', 'Length', 'Height']:
                mapped_df[col] = pd.to_numeric(mapped_df[col], errors='coerce').fillna(0)
            
            st.session_state.data['parts_df'] = mapped_df
            st.session_state.mapping_confirmed = True
            st.success("Data Mapped Successfully!")

        if st.session_state.mapping_confirmed:
            st.dataframe(st.session_state.data['parts_df'].head())
            st.button("Next ➡️", on_click=next_step)

# --- STEP 3: NESTING ---
elif st.session_state.step == 3:
    st.header("Step 3: Nesting Configuration")
    is_nested = st.checkbox("Will parts be nested?")
    nest_pct = st.slider("Define Nesting Height Percentage (%)", 1, 100, 20) if is_nested else 0
    
    st.session_state.data['nested'] = is_nested
    st.session_state.data['nest_pct'] = nest_pct
    st.button("Next ➡️", on_click=next_step)

# --- STEP 4: RULES ---
elif st.session_state.step == 4:
    st.header("Step 4: Handling Rules")
    stacking = st.radio("Is stacking allowed?", ["Yes", "No"]) == "Yes"
    fragility = st.selectbox("Fragility Status:", ["Non-Fragile", "Fragile"])
    
    st.session_state.data['stacking'] = stacking
    st.session_state.data['fragility'] = fragility
    
    st.button("Generate Results 🚀", on_click=next_step)

# --- STEP 5: FINAL RESULTS & EXCEL DOWNLOAD ---
elif st.session_state.step == 5:
    st.header("Final Results & Space Utilization")
    
    if 'parts_df' not in st.session_state.data:
        st.error("Data missing. Please restart.")
        if st.button("Restart"): reset_process()
    else:
        box = st.session_state.data['box']
        df = st.session_state.data['parts_df']
        
        results = []
        for _, row in df.iterrows():
            res = calculate_fit(
                box, 
                (row['Width'], row['Length'], row['Height']), 
                st.session_state.data['nested'],
                st.session_state.data['nest_pct'],
                st.session_state.data['stacking'],
                st.session_state.data['fragility']
            )
            results.append({
                "Part Name": row['Part_Name'],
                "Box Size": f"{box[0]}x{box[1]}x{box[2]}",
                "Parts Per Box": res['count'],
                "Best Orientation": res['orientation'],
                "Used Volume": res['used_vol'],
                "Unused Volume": res['unused_vol'],
                "Utilization %": res['util_pct']
            })
        
        res_df = pd.DataFrame(results)
        st.dataframe(res_df, use_container_width=True)
        
        st.divider()
        st.subheader("Export Analysis")

        # --- EXCEL DOWNLOAD FIX ---
        def to_excel(df):
            output = io.BytesIO()
            # Using xlsxwriter engine is critical for .xlsx format
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='AgiloPack_Results')
                # Formatting (Optional: Autofit columns)
                worksheet = writer.sheets['AgiloPack_Results']
                for i, col in enumerate(df.columns):
                    column_len = max(df[col].astype(str).str.len().max(), len(col)) + 2
                    worksheet.set_column(i, i, column_len)
            return output.getvalue()

        # Generate the binary data
        excel_data = to_excel(res_df)

        st.download_button(
            label="Download as Excel (.xlsx) 📥",
            data=excel_data,
            file_name='AgiloPack_Analysis.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
        st.button("Start New Process 🔄", on_click=reset_process)
