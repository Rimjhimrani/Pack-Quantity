import streamlit as st
import pandas as pd
import math
from itertools import permutations

# --- CORE CALCULATION ENGINE ---
def optimize_packing(lp, wp, hp, part_weight, lb, wb, hb, max_box_weight, clearance):
    # Adjust box dimensions for clearance
    eff_lb, eff_wb, eff_hb = lb - clearance, wb - clearance, hb - clearance
    
    if any(d <= 0 for d in [eff_lb, eff_wb, eff_hb]):
        return None

    part_dims = [lp, wp, hp]
    orientations = list(set(permutations(part_dims)))
    
    best_result = None
    max_parts = -1

    for orientation in orientations:
        pl, pw, ph = orientation
        
        # Calculate max units per dimension
        nx = math.floor(eff_lb / pl) if eff_lb >= pl else 0
        ny = math.floor(eff_wb / pw) if eff_wb >= pw else 0
        nz = math.floor(eff_hb / ph) if eff_hb >= ph else 0
        
        total_parts = nx * ny * nz
        
        # Weight Constraint Check
        if part_weight > 0 and (total_parts * part_weight) > max_box_weight:
            total_parts = math.floor(max_box_weight / part_weight)
        
        # Volume Calculation
        box_vol = lb * wb * hb
        part_vol = lp * wp * hp
        utilization = ((total_parts * part_vol) / box_vol) * 100 if box_vol > 0 else 0

        # Determine Primary Direction
        if pl == lp: direction = "Lengthwise"
        elif pl == wp: direction = "Breadthwise"
        else: direction = "Heightwise"

        if total_parts > max_parts:
            max_parts = total_parts
            best_result = {
                "Best Direction": direction,
                "Orientation": f"{pl}x{pw}x{ph}",
                "Parts per Box": total_parts,
                "Layout (LxWxH)": f"{nx} x {ny} x {nz}",
                "Utilization %": round(utilization, 2),
                "Fit Status": "FIT" if total_parts > 0 else "NO FIT"
            }
            
    return best_result

# --- STREAMLIT UI ---
st.set_page_config(page_title="Multi-Part Packaging Engine", layout="wide")

st.title("📦 Multi-Part Packaging Optimization Engine")
st.markdown("Enter multiple part types below to calculate optimal box density for each.")

# --- SIDEBAR: GLOBAL BOX SETTINGS ---
st.sidebar.header("Global Box Dimensions")
lb = st.sidebar.number_input("Box Length (mm)", value=600.0)
wb = st.sidebar.number_input("Box Width (mm)", value=400.0)
hb = st.sidebar.number_input("Box Height (mm)", value=400.0)
max_box_weight = st.sidebar.number_input("Max Weight Capacity (kg)", value=25.0)
clearance = st.sidebar.number_input("Clearance Tolerance (mm)", value=5.0)

# --- MAIN: MULTI-PART INPUT ---
st.subheader("1. Define Part Manifest")
st.info("Edit the table below. Add rows for different part types.")

# Default data for the editor
default_parts = pd.DataFrame([
    {"Part ID": "P-001", "Length": 120.0, "Width": 80.0, "Height": 50.0, "Weight": 0.5},
    {"Part ID": "P-002", "Length": 200.0, "Width": 150.0, "Height": 100.0, "Weight": 2.0},
    {"Part ID": "P-003", "Length": 500.0, "Width": 300.0, "Height": 100.0, "Weight": 5.0},
])

# Interactive Data Editor
edited_df = st.data_editor(
    default_parts, 
    num_rows="dynamic", 
    use_container_width=True,
    column_config={
        "Part ID": st.column_config.TextColumn("Part ID", required=True),
        "Length": st.column_config.NumberColumn("L (mm)", min_value=1),
        "Width": st.column_config.NumberColumn("W (mm)", min_value=1),
        "Height": st.column_config.NumberColumn("H (mm)", min_value=1),
        "Weight": st.column_config.NumberColumn("Weight (kg)", min_value=0),
    }
)

# --- CALCULATION TRIGGER ---
if st.button("🚀 Run Batch Optimization"):
    results_list = []
    
    for index, row in edited_df.iterrows():
        res = optimize_packing(
            row['Length'], row['Width'], row['Height'], row['Weight'],
            lb, wb, hb, max_box_weight, clearance
        )
        
        if res:
            res['Part ID'] = row['Part ID']
            results_list.append(res)
        else:
            results_list.append({
                "Part ID": row['Part ID'], 
                "Fit Status": "ERROR/INVALID DIMS",
                "Parts per Box": 0
            })

    # --- DISPLAY RESULTS ---
    res_df = pd.DataFrame(results_list)
    
    # Reorder columns to put Part ID first
    cols = ['Part ID'] + [c for c in res_df.columns if c != 'Part ID']
    res_df = res_df[cols]

    st.subheader("2. Optimization Results")
    
    # Summary Metrics
    avg_util = res_df[res_df["Fit Status"] == "FIT"]["Utilization %"].mean()
    st.metric("Average Box Utilization", f"{round(avg_util, 2)}%" if not math.isnan(avg_util) else "0%")

    # Styled Result Table
    def color_status(val):
        color = 'green' if val == "FIT" else 'red'
        return f'color: {color}'

    st.dataframe(res_df.style.applymap(color_status, subset=['Fit Status']), use_container_width=True)

    # Export functionality
    csv = res_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Results as CSV", csv, "packing_results.csv", "text/csv")

    # Flag low efficiency
    low_eff = res_df[(res_df["Utilization %"] < 50) & (res_df["Fit Status"] == "FIT")]
    if not low_eff.empty:
        st.warning(f"⚠️ Warning: {len(low_eff)} part types have space utilization below 50%. Consider alternative packaging for these items.")
