import streamlit as st
import pandas as pd
import math
from itertools import permutations
import io

class PackagingEngine:
    def __init__(self, lb, wb, hb, max_w, clearance):
        self.box_l = lb - clearance
        self.box_w = wb - clearance
        self.box_h = hb - clearance
        self.box_max_w = max_w
        self.box_vol = self.box_l * self.box_w * self.box_h

    def get_max_parts_single_sku(self, pl, pw, ph, p_weight):
        """Calculates how many of a SINGLE SKU fit in one box."""
        orientations = list(set(permutations([pl, pw, ph])))
        best_fit = 0
        best_layout = ""
        best_ori = ""

        for o in orientations:
            nx = math.floor(self.box_l / o[0]) if self.box_l >= o[0] else 0
            ny = math.floor(self.box_w / o[1]) if self.box_w >= o[1] else 0
            nz = math.floor(self.box_h / o[2]) if self.box_h >= o[2] else 0
            
            total = nx * ny * nz
            # Weight cap
            if p_weight > 0 and (total * p_weight) > self.box_max_w:
                total = math.floor(self.box_max_w / p_weight)
            
            if total > best_fit:
                best_fit = total
                best_layout = f"{nx}x{ny}x{nz}"
                best_ori = f"{o[0]}x{o[1]}x{o[2]}"
        
        return best_fit, best_layout, best_ori

    def run_mixed_packing(self, parts_list):
        """Heuristic for mixing different SKUs in boxes (Consolidated)."""
        manifest = []
        for p in parts_list:
            for _ in range(int(p['Qty'])):
                manifest.append({
                    'Part ID': p['Part ID'], 
                    'dims': (p['L'], p['W'], p['H']),
                    'Weight': p['Weight'], 
                    'vol': p['L'] * p['W'] * p['H']
                })
        # Sort by volume descending (Largest first)
        manifest.sort(key=lambda x: x['vol'], reverse=True)

        boxes = []
        while manifest:
            current_box = []
            rem_vol = self.box_vol
            rem_weight = self.box_max_w
            idx = 0
            while idx < len(manifest):
                item = manifest[idx]
                can_fit = any(o[0]<=self.box_l and o[1]<=self.box_w and o[2]<=self.box_h 
                              for o in permutations(item['dims']))
                
                if can_fit and item['vol'] <= rem_vol and item['Weight'] <= rem_weight:
                    current_box.append(item)
                    rem_vol -= item['vol']
                    rem_weight -= item['Weight']
                    manifest.pop(idx)
                else:
                    idx += 1
            if not current_box: break 
            boxes.append(current_box)
        return boxes

# --- UI SETUP ---
st.set_page_config(page_title="Supply Chain Packing Engine", layout="wide")
st.title("📦 Packaging Optimization Engine")

# --- SIDEBAR: CONFIGURATION ---
with st.sidebar:
    st.header("1. Target Box Dimensions")
    lb = st.number_input("Box Length (mm)", value=600.0)
    wb = st.number_input("Box Width (mm)", value=400.0)
    hb = st.number_input("Box Height (mm)", value=400.0)
    max_box_weight = st.number_input("Max Weight Cap (kg)", value=25.0)
    clearance = st.number_input("Clearance Tolerance (mm)", value=5.0)
    
    st.divider()
    st.header("2. Packing Strategy")
    packing_mode = st.radio(
        "Choose Mode:",
        ["Individual (Pure Cartons)", "Mixed (Consolidated Cartons)"],
        help="Individual: One SKU type per box. Mixed: Multiple SKUs combined to save space."
    )

# --- MAIN: FILE UPLOAD ---
st.subheader("Step 1: Upload Part Data")
uploaded_file = st.file_uploader("Upload CSV or Excel (Headers: Part ID, L, W, H, Weight, Qty)", type=['csv', 'xlsx'])

# Provide a sample template for the user
sample_data = "Part ID,L,W,H,Weight,Qty\nSKU-001,200,150,100,1.5,50\nSKU-002,100,100,50,0.5,100"
st.download_button("📥 Download Sample Template", sample_data, "template.csv", "text/csv")

if uploaded_file:
    # Load Data
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.write("### Data Preview", df.head())
    
    if st.button("🚀 Run Packaging Optimization"):
        engine = PackagingEngine(lb, wb, hb, max_box_weight, clearance)
        parts_list = df.to_dict('records')
        
        # --- EXECUTION ---
        if packing_mode == "Individual (Pure Cartons)":
            st.subheader("Optimization Results: Individual SKU Packing")
            results = []
            for p in parts_list:
                fit_per_box, layout, ori = engine.get_max_parts_single_sku(p['L'], p['W'], p['H'], p['Weight'])
                
                if fit_per_box > 0:
                    total_boxes = math.ceil(p['Qty'] / fit_per_box)
                    vol_util = ((p['L']*p['W']*p['H']*fit_per_box) / engine.box_vol) * 100
                    results.append({
                        "Part ID": p['Part ID'],
                        "Fit per Box": fit_per_box,
                        "Total Boxes": total_boxes,
                        "Layout": layout,
                        "Orientation": ori,
                        "Utilization %": round(vol_util, 2),
                        "Status": "FIT"
                    })
                else:
                    results.append({"Part ID": p['Part ID'], "Status": "OVERSIZE", "Total Boxes": 0})
            
            res_df = pd.DataFrame(results)
            st.dataframe(res_df, use_container_width=True)
            
            st.metric("Total Shipping Boxes Required", int(res_df["Total Boxes"].sum()))
            
            # Export
            csv = res_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Result", csv, "individual_packing.csv", "text/csv")

        else:
            # MIXED PACKING MODE
            st.subheader("Optimization Results: Mixed SKU Packing")
            packed_boxes = engine.run_mixed_packing(parts_list)
            
            st.metric("Total Consolidated Boxes Required", len(packed_boxes))
            
            # Detailed breakdown per box
            export_rows = []
            for i, box in enumerate(packed_boxes):
                with st.expander(f"📦 Box {i+1} Details"):
                    box_df = pd.DataFrame(box)
                    summary = box_df.groupby('Part ID').size().reset_index(name='Qty Packed')
                    
                    c1, c2 = st.columns(2)
                    c1.write("**Packing List:**")
                    c1.table(summary)
                    
                    wt = box_df['Weight'].sum()
                    vol_u = (box_df['vol'].sum() / engine.box_vol) * 100
                    c2.metric("Box Weight", f"{round(wt, 2)} kg")
                    c2.metric("Box Utilization", f"{round(vol_u, 1)}%")
                    c2.progress(min(wt/max_box_weight, 1.0))
                    
                    # Prepare for export
                    summary['Box_ID'] = i + 1
                    export_rows.append(summary)
            
            if export_rows:
                final_export = pd.concat(export_rows)
                csv = final_export.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Packing Manifest", csv, "mixed_manifest.csv", "text/csv")

else:
    st.info("Waiting for file upload to begin optimization.")
