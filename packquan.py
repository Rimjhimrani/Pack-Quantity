import streamlit as st
import pandas as pd
import math
from itertools import permutations

# --- CORE CALCULATION ENGINE ---
def optimize_packing(lp, wp, hp, part_weight, lb, wb, hb, max_box_weight, clearance, total_qty):
    # Adjust box dimensions for clearance
    eff_lb, eff_wb, eff_hb = lb - clearance, wb - clearance, hb - clearance
    
    if any(d <= 0 for d in [eff_lb, eff_wb, eff_hb]):
        return None

    part_dims = [lp, wp, hp]
    orientations = list(set(permutations(part_dims)))
    
    best_orientation_result = None
    max_parts_per_box = -1

    for orientation in orientations:
        pl, pw, ph = orientation
        
        # Calculate max units per dimension
        nx = math.floor(eff_lb / pl) if eff_lb >= pl else 0
        ny = math.floor(eff_wb / pw) if eff_wb >= pw else 0
        nz = math.floor(eff_hb / ph) if eff_hb >= ph else 0
        
        total_fit = nx * ny * nz
        
        # Weight Constraint Check
        if part_weight > 0 and (total_fit * part_weight) > max_box_weight:
            total_fit = math.floor(max_box_weight / part_weight)
        
        if total_fit > max_parts_per_box:
            max_parts_per_box = total_fit
            
            # Volume Calculation for one full box
            box_vol = lb * wb * hb
            part_vol = lp * wp * hp
            utilization = ((total_fit * part_vol) / box_vol) * 100 if box_vol > 0 else 0

            # Determine Primary Direction
            if pl == lp: direction = "Lengthwise"
            elif pl == wp: direction = "Breadthwise"
            else: direction = "Heightwise"

            best_orientation_result = {
                "Direction": direction,
                "Orientation": f"{pl}x{pw}x{ph}",
                "Parts_Per_Box": total_fit,
                "Layout": f"{nx}x{ny}x{nz}",
                "Utilization_Pct": round(utilization, 2)
            }
            
    # --- Logistics Calculations ---
    if max_parts_per_box > 0:
        total_boxes = math.ceil(total_qty / max_parts_per_box)
        full_boxes = math.floor(total_qty / max_parts_per_box)
        remainder = total_qty % max_parts_per_box
        
        return {
            **best_orientation_result,
            "Total Qty": total_qty,
            "Boxes Needed": total_boxes,
            "Full Boxes": full_boxes,
            "Last Box Qty": remainder if remainder > 0 else max_parts_per_box,
            "Status": "FIT"
        }
    else:
        return {"Status": "NO FIT", "Total Qty": total_qty, "Boxes Needed": 0}

# --- STREAMLIT UI ---
st.set_page_config(page_title="Supply Chain Box Calculator", layout="wide")

st.title("📦 Logistics & Packaging Optimization Engine")
st.markdown("Calculate optimal packing and **Total Box Count** for multiple part types.")

# --- SIDEBAR: GLOBAL BOX SETTINGS ---
with st.sidebar:
    st.header("Standard Box Specs")
    lb = st.number_input("Box Length (mm)", value=600.0)
    wb = st.number_input("Box Width (mm)", value=400.0)
    hb = st.number_input("Box Height (mm)", value=400.0)
    max_box_weight = st.number_input("Max Weight Cap (kg)", value=20.0)
    clearance = st.number_input("Clearance (mm)", value=5.0)
    st.divider()
    st.info("The engine assumes all parts of one type are packed together.")

# --- MAIN: MULTI-PART INPUT ---
st.subheader("1. Part Inventory & Requirements")

# Default data for the editor including Quantity
default_parts = pd.DataFrame([
    {"Part ID": "P-101", "L": 120.0, "W": 80.0, "H": 50.0, "Weight": 0.4, "Qty": 500},
    {"Part ID": "P-102", "L": 250.0, "W": 200.0, "H": 100.0, "Weight": 1.5, "Qty": 120},
    {"Part ID": "P-103", "L": 400.0, "W": 300.0, "H": 200.0, "Weight": 8.0, "Qty": 45},
])

edited_df = st.data_editor(
    default_parts, 
    num_rows="dynamic", 
    use_container_width=True,
    column_config={
        "Part ID": st.column_config.TextColumn("Part ID", required=True),
        "L": st.column_config.NumberColumn("L (mm)"),
        "W": st.column_config.NumberColumn("W (mm)"),
        "H": st.column_config.NumberColumn("H (mm)"),
        "Weight": st.column_config.NumberColumn("Wt (kg)"),
        "Qty": st.column_config.NumberColumn("Total Qty", min_value=1),
    }
)

# --- CALCULATION TRIGGER ---
if st.button("🚀 Calculate Logistics Plan"):
    results_list = []
    
    for _, row in edited_df.iterrows():
        res = optimize_packing(
            row['L'], row['W'], row['H'], row['Weight'],
            lb, wb, hb, max_box_weight, clearance, row['Qty']
        )
        
        res['Part ID'] = row['Part ID']
        results_list.append(res)

    # Convert to Dataframe
    res_df = pd.DataFrame(results_list)

    # Organize Columns for the user
    display_cols = [
        'Part ID', 'Status', 'Total Qty', 'Parts_Per_Box', 
        'Boxes Needed', 'Full Boxes', 'Last Box Qty', 
        'Direction', 'Layout', 'Utilization_Pct'
    ]
    res_df = res_df[display_cols]

    # --- DISPLAY RESULTS ---
    st.subheader("2. Logistics Plan Summary")
    
    # KPIs
    total_boxes_all = res_df['Boxes Needed'].sum()
    st.metric("Total Shipping Boxes Required", int(total_boxes_all))

    # Color Styling
    def style_status(val):
        color = '#d4edda' if val == "FIT" else '#f8d7da'
        return f'background-color: {color}'

    st.dataframe(
        res_df.style.applymap(style_status, subset=['Status']), 
        use_container_width=True
    )

    # --- ADVANCED INSIGHTS ---
    st.subheader("3. Efficiency Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart of box distribution
        import plotly.express as px
        fig = px.pie(res_df, names='Part ID', values='Boxes Needed', title="Box Requirement by Part")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Warning for "Underfilled" boxes
        underfilled = res_df[res_df['Last Box Qty'] / res_df['Parts_Per_Box'] < 0.3]
        if not underfilled.empty:
            st.warning("⚠️ **Low Fill Warning:** The following parts have a 'Last Box' that is less than 30% full. Consider merging these or using a smaller secondary box.")
            st.write(underfilled[['Part ID', 'Last Box Qty', 'Parts_Per_Box']])

    # Export
    csv = res_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Shipping Manifest (CSV)", csv, "shipping_plan.csv", "text/csv")
