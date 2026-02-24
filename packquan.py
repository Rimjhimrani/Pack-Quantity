import streamlit as st
import pandas as pd
import math
from itertools import permutations

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
        """Heuristic for mixing different SKUs in boxes."""
        manifest = []
        for p in parts_list:
            for _ in range(int(p['Qty'])):
                manifest.append({
                    'id': p['Part ID'], 'dims': (p['L'], p['W'], p['H']),
                    'weight': p['Weight'], 'vol': p['L'] * p['W'] * p['H']
                })
        manifest.sort(key=lambda x: x['vol'], reverse=True)

        boxes = []
        while manifest:
            current_box = []
            rem_vol = self.box_vol
            rem_weight = self.box_max_w
            idx = 0
            while idx < len(manifest):
                item = manifest[idx]
                # Check if item fits dimensions, volume, and weight
                can_fit = any(o[0]<=self.box_l and o[1]<=self.box_w and o[2]<=self.box_h 
                              for o in permutations(item['dims']))
                
                if can_fit and item['vol'] <= rem_vol and item['weight'] <= rem_weight:
                    current_box.append(item)
                    rem_vol -= item['vol']
                    rem_weight -= item['weight']
                    manifest.pop(idx)
                else:
                    idx += 1
            if not current_box: break # Item too big
            boxes.append(current_box)
        return boxes

# --- STREAMLIT UI ---
st.set_page_config(page_title="Pro Pack Optimizer", layout="wide")

st.title("📦 Advanced Supply Chain Packaging Engine")

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("1. Box Configuration")
    lb = st.number_input("Box Length (mm)", value=600.0)
    wb = st.number_input("Box Width (mm)", value=400.0)
    hb = st.number_input("Box Height (mm)", value=400.0)
    max_box_weight = st.number_input("Weight Limit (kg)", value=20.0)
    clearance = st.number_input("Clearance (mm)", value=5.0)
    
    st.divider()
    st.header("2. Optimization Strategy")
    packing_mode = st.radio(
        "Select Packing Mode:",
        ["Individual (Pure Cartons)", "Mixed (Consolidated Cartons)"],
        help="Individual: One SKU per box. Mixed: Multiple SKUs allowed per box."
    )

# --- INPUT DATA ---
st.subheader("Part Manifest")
default_data = pd.DataFrame([
    {"Part ID": "SKU-001", "L": 200, "W": 150, "H": 100, "Weight": 1.5, "Qty": 20},
    {"Part ID": "SKU-002", "L": 100, "W": 100, "H": 50, "Weight": 0.5, "Qty": 50}
])
edited_df = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)

if st.button("🚀 Execute Packing Analysis"):
    engine = PackagingEngine(lb, wb, hb, max_box_weight, clearance)
    parts_list = edited_df.to_dict('records')

    if packing_mode == "Individual (Pure Cartons)":
        st.subheader("Results: Individual SKU Packing")
        results = []
        for p in parts_list:
            fit_per_box, layout, ori = engine.get_max_parts_single_sku(p['L'], p['W'], p['H'], p['Weight'])
            
            if fit_per_box > 0:
                boxes_needed = math.ceil(p['Qty'] / fit_per_box)
                util = ((p['L']*p['W']*p['H']*fit_per_box)/(engine.box_vol))*100
                results.append({
                    "Part ID": p['Part ID'],
                    "Units/Box": fit_per_box,
                    "Total Boxes": boxes_needed,
                    "Layout": layout,
                    "Orientation": ori,
                    "Space Util %": round(util, 2),
                    "Status": "FIT"
                })
            else:
                results.append({"Part ID": p['Part ID'], "Status": "OVERSIZE", "Total Boxes": 0})
        
        res_df = pd.DataFrame(results)
        st.dataframe(res_df, use_container_width=True)
        st.metric("Total Boxes Required", int(res_df["Total Boxes"].sum()))

    else:
        # MIXED PACKING MODE
        st.subheader("Results: Mixed SKU Packing")
        packed_boxes = engine.run_mixed_packing(parts_list)
        
        col1, col2 = st.columns(2)
        col1.metric("Total Boxes Required", len(packed_boxes))
        
        for i, box in enumerate(packed_boxes):
            with st.expander(f"📦 Box {i+1} Contents", expanded=(i==0)):
                box_df = pd.DataFrame(box)
                summary = box_df.groupby('id').size().reset_index(name='Qty')
                
                c1, c2 = st.columns(2)
                c1.write("**Inventory:**")
                c1.table(summary)
                
                used_w = box_df['weight'].sum()
                used_v = box_df['vol'].sum()
                c2.write("**Box Metrics:**")
                c2.write(f"Weight: {round(used_w,1)} / {max_box_weight} kg")
                c2.write(f"Volume: {round((used_v/engine.box_vol)*100,1)}% utilized")
                c2.progress(min(used_w/max_box_weight, 1.0))
