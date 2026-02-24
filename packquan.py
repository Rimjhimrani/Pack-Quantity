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

    def get_best_orientation(self, pl, pw, ph, rem_l, rem_w, rem_h):
        """Finds the best orientation of a part to fit into a remaining space."""
        orientations = list(set(permutations([pl, pw, ph])))
        valid = []
        for o in orientations:
            if o[0] <= rem_l and o[1] <= rem_w and o[2] <= rem_h:
                # Priority: Height efficiency (keep height low)
                valid.append(o)
        
        if not valid:
            return None
        # Return orientation that minimizes height used
        return sorted(valid, key=lambda x: x[2])[0]

    def calculate_packing(self, parts_list):
        """
        Heuristic: Mixed Bin Packing.
        Sorts parts by volume and attempts to fill boxes sequentially.
        """
        # Prepare Master Manifest (Flattening quantity into individual items)
        manifest = []
        for p in parts_list:
            for _ in range(int(p['Qty'])):
                manifest.append({
                    'id': p['Part ID'],
                    'dims': (p['L'], p['W'], p['H']),
                    'weight': p['Weight'],
                    'vol': p['L'] * p['W'] * p['H']
                })

        # Sort manifest by volume descending (Largest First)
        manifest.sort(key=lambda x: x['vol'], reverse=True)

        boxes = []
        while len(manifest) > 0:
            current_box_parts = []
            rem_vol = self.box_vol
            rem_weight = self.box_max_w
            
            # Simple 3D volume-based greedy heuristic with dimension checking
            idx = 0
            while idx < len(manifest):
                item = manifest[idx]
                
                # Preliminary checks
                if item['vol'] <= rem_vol and item['weight'] <= rem_weight:
                    # Check if at least one orientation fits in the box shell
                    if self.get_best_orientation(*item['dims'], self.box_l, self.box_w, self.box_h):
                        current_box_parts.append(item)
                        rem_vol -= item['vol']
                        rem_weight -= item['weight']
                        manifest.pop(idx) # Remove from manifest
                    else:
                        idx += 1
                else:
                    idx += 1
            
            if not current_box_parts: # Item too big for box
                break
                
            boxes.append(current_box_parts)

        return boxes, manifest

# --- STREAMLIT UI ---
st.set_page_config(page_title="3D Multi-SKU Packing Engine", layout="wide")

st.title("📦 Multi-SKU Packaging & Bin-Packing Engine")
st.markdown("Optimize the packing of **mixed part types** into standard shipping containers.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Global Box Dimensions")
    lb = st.number_input("Box Length (mm)", value=600.0)
    wb = st.number_input("Box Width (mm)", value=400.0)
    hb = st.number_input("Box Height (mm)", value=400.0)
    max_box_weight = st.number_input("Max Weight (kg)", value=25.0)
    clearance = st.number_input("Clearance (mm)", value=5.0)
    st.divider()
    st.write("**Packing Strategy:** First-Fit Decreasing (FFD) 3D Heuristic")

# --- PART INPUT ---
st.subheader("1. Part Manifest (Multi-SKU)")
default_data = pd.DataFrame([
    {"Part ID": "SKU-A", "L": 150, "W": 100, "H": 80, "Weight": 1.2, "Qty": 20},
    {"Part ID": "SKU-B", "L": 300, "W": 200, "H": 150, "Weight": 4.5, "Qty": 5},
    {"Part ID": "SKU-C", "L": 100, "W": 100, "H": 50, "Weight": 0.5, "Qty": 50},
])

edited_df = st.data_editor(default_data, num_rows="dynamic", use_container_width=True)

if st.button("🚀 Run Multi-SKU Optimization"):
    parts_list = edited_df.to_dict('records')
    engine = PackagingEngine(lb, wb, hb, max_box_weight, clearance)
    
    packed_boxes, remaining_items = engine.calculate_packing(parts_list)
    
    # --- OUTPUTS ---
    st.divider()
    col1, col2, col3 = st.columns(3)
    
    total_items_requested = edited_df['Qty'].sum()
    total_items_packed = sum(len(b) for b in packed_boxes)
    
    with col1:
        st.metric("Total Boxes Required", len(packed_boxes))
    with col2:
        utilization = sum([sum(p['vol'] for p in box) for box in packed_boxes]) / (len(packed_boxes) * engine.box_vol) if packed_boxes else 0
        st.metric("Avg. Space Utilization", f"{round(utilization*100, 2)}%")
    with col3:
        fit_status = "FIT" if len(remaining_items) == 0 else "PARTIAL"
        st.metric("Fit Status", fit_status)

    if remaining_items:
        st.error(f"⚠️ {len(remaining_items)} items could not fit in the box dimensions provided.")

    # --- BOX BREAKDOWN ---
    st.subheader("2. Detailed Packing Plan (Box by Box)")
    
    for i, box in enumerate(packed_boxes):
        with st.expander(f"📦 Box {i+1} Details", expanded=(i==0)):
            box_df = pd.DataFrame(box)
            summary = box_df.groupby('id').size().reset_index(name='Qty Packed')
            
            c1, c2 = st.columns([1, 2])
            with c1:
                st.write("**Contents:**")
                st.table(summary)
            with c2:
                box_weight = box_df['weight'].sum()
                box_vol_used = box_df['vol'].sum()
                st.write(f"**Box Statistics:**")
                st.write(f"- Weight: {round(box_weight, 2)} kg / {max_box_weight} kg")
                st.write(f"- Vol Utilization: {round((box_vol_used / engine.box_vol)*100, 2)}%")
                
                # Progress bars for visual feedback
                st.progress(min(box_weight/max_box_weight, 1.0), text="Weight Capacity")
                st.progress(min(box_vol_used/engine.box_vol, 1.0), text="Volume Capacity")

    # --- CSV EXPORT ---
    # Create a manifest for the warehouse
    manifest_data = []
    for i, box in enumerate(packed_boxes):
        box_df = pd.DataFrame(box)
        summary = box_df.groupby('id').size().reset_index(name='Qty')
        summary['Box_Number'] = i + 1
        manifest_data.append(summary)
    
    if manifest_data:
        final_manifest = pd.concat(manifest_data)
        csv = final_manifest.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Packing Manifest", csv, "packing_manifest.csv", "text/csv")
