import streamlit as st
import pandas as pd
import math
from itertools import permutations

def calculate_packing():
    st.set_page_config(page_title="Packaging Optimization Engine", layout="wide")
    
    st.title("📦 Supply Chain Packaging Optimization Engine")
    st.markdown("### 3D Box Packing & Orientation Analysis")

    # --- Sidebar Inputs ---
    st.sidebar.header("1. Part Dimensions (mm)")
    lp = st.sidebar.number_input("Part Length (Lp)", min_value=1.0, value=120.0)
    wp = st.sidebar.number_input("Part Width (Wp)", min_value=1.0, value=80.0)
    hp = st.sidebar.number_input("Part Height (Hp)", min_value=1.0, value=50.0)
    part_weight = st.sidebar.number_input("Part Weight (kg)", min_value=0.0, value=0.5)

    st.sidebar.header("2. Box Dimensions (mm)")
    lb = st.sidebar.number_input("Box Length (Lb)", min_value=1.0, value=400.0)
    wb = st.sidebar.number_input("Box Width (Wb)", min_value=1.0, value=300.0)
    hb = st.sidebar.number_input("Box Height (Hb)", min_value=1.0, value=250.0)
    max_weight = st.sidebar.number_input("Max Box Weight (kg)", min_value=0.0, value=20.0)

    st.sidebar.header("3. Constraints")
    clearance = st.sidebar.number_input("Clearance Tolerance (mm)", min_value=0.0, value=5.0)
    
    # --- Logic Engine ---
    
    # Effective box dimensions after clearance
    eff_lb = lb - clearance
    eff_wb = wb - clearance
    eff_hb = hb - clearance

    part_dims = [lp, wp, hp]
    # All 6 possible orientations (permutations)
    orientations = list(set(permutations(part_dims)))
    
    results = []

    for orientation in orientations:
        pl, pw, ph = orientation
        
        # Calculate parts per axis
        nx = math.floor(eff_lb / pl) if eff_lb >= pl else 0
        ny = math.floor(eff_wb / pw) if eff_wb >= pw else 0
        nz = math.floor(eff_hb / ph) if eff_hb >= ph else 0
        
        total_parts = nx * ny * nz
        
        # Weight constraint check
        total_weight = total_parts * part_weight
        if total_weight > max_weight and part_weight > 0:
            total_parts = math.floor(max_weight / part_weight)
            weight_limited = True
        else:
            weight_limited = False

        # Determine Direction Label
        # Logic: Which part dimension is aligned with Box Length?
        if pl == lp: direction = "Lengthwise"
        elif pl == wp: direction = "Breadthwise"
        else: direction = "Heightwise"

        # Volume Calculations
        box_vol = lb * wb * hb
        part_vol = lp * wp * hp
        utilized_vol = total_parts * part_vol
        utilization_pct = (utilized_vol / box_vol) * 100 if box_vol > 0 else 0

        results.append({
            "Orientation (L x W x H)": f"{pl} × {pw} × {ph}",
            "Direction": direction,
            "Parts": total_parts,
            "Layout": f"{nx} × {ny} × {nz}",
            "Utilization (%)": round(utilization_pct, 2),
            "Unused Vol (%)": round(100 - utilization_pct, 2),
            "Weight (kg)": round(total_parts * part_weight, 2),
            "Weight Limited": weight_limited
        })

    # Convert to Dataframe
    df = pd.DataFrame(results)
    df = df.sort_values(by="Parts", ascending=False).reset_index(drop=True)

    # --- Output Display ---
    if not df.empty and df.iloc[0]['Parts'] > 0:
        best = df.iloc[0]
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Best Orientation", best['Direction'])
        col2.metric("Max Parts", int(best['Parts']))
        col3.metric("Utilization", f"{best['Utilization (%)']}%")
        col4.metric("Fit Status", "FIT", delta_color="normal")

        st.success(f"✅ Optimization Complete: Found best layout using **{best['Direction']}** orientation.")

        # Detailed Summary
        with st.expander("View Full Analysis Details", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Packing Specifications:**")
                st.write(f"- Layout: {best['Layout']} (L×W×H pieces)")
                st.write(f"- Total Weight: {best['Weight (kg)']} kg / {max_weight} kg")
                if best['Weight Limited']:
                    st.warning("⚠️ Part count is limited by maximum box weight capacity.")
            with c2:
                st.write("**Volume Metrics:**")
                st.write(f"- Unused Volume: {best['Unused Vol (%)']}%")
                st.write(f"- Orientation: {best['Orientation (L x W x H)']} mm")

        # Comparison Table
        st.subheader("Orientation Comparison Matrix")
        st.dataframe(df, use_container_width=True)

    else:
        st.error("❌ NO FIT: Part dimensions exceed box dimensions or weight limits.")

    # --- Recommendations ---
    if not df.empty and df.iloc[0]['Utilization (%)'] < 70:
        st.info("💡 **Engine Recommendation:** Space utilization is below 70%. Consider reducing box size or changing part orientation to minimize shipping costs.")

if __name__ == "__main__":
    calculate_packing()
