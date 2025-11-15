import pickle
import pandas as pd
from collections import defaultdict

try:
    from lanes import ENTRY_ZONES, EXIT_ZONES
except ImportError:
    print("Error: Could not find lanes.py.")
    exit()

def get_zone(point, zones_dict):
    x, y = point
    for zone_name, (x1, y1, x2, y2) in zones_dict.items():
        if x1 > x2 or y1 > y2:
            print(f"ERROR in zone '{zone_name}': {zone_name}: Coords are invalid. x1 > x2 or y1 > y2.")
            print("fix your lanes.py file.")
            exit()
            
        if x1 <= x <= x2 and y1 <= y <= y2:
            return zone_name
    return None

TURN_LOGIC = {
    "entry_north": {
        "exit_south": "Straight",
        "exit_west": "Right Turn",
        "exit_north": "U-Turn"
    },
    "entry_south": {
        "exit_north": "Straight",
        "exit_east": "Right Turn",
        "exit_south": "U-Turn"
    },
    "entry_east": {
        "exit_west": "Straight",
        "exit_south": "Right Turn",
        "exit_east": "U-Turn"
    },
    "entry_west": {
        "exit_east": "Straight",
        "exit_north": "Right Turn",
        "exit_west": "U-Turn"
    }
}

def analyze():
    try:
        with open("trajectories.pkl", "rb") as f:
            trajectories = pickle.load(f)
    except FileNotFoundError:
        print("Error: trajectories.pkl not found.")
        print("Please run your tracking_deepsort.py script first.")
        return
        
    print(f"Loaded {len(trajectories)} unique vehicle tracks.")

    final_counts = defaultdict(int)

    for track_id, path in trajectories.items():
        if len(path) < 2:
            continue
            
        start_point = path[0]
        end_point = path[-1]
        
        start_zone = get_zone(start_point, ENTRY_ZONES)
        end_zone = get_zone(end_point, EXIT_ZONES)
        
        if start_zone and end_zone:
            if start_zone in TURN_LOGIC and end_zone in TURN_LOGIC[start_zone]:
                
                direction = TURN_LOGIC[start_zone][end_zone]
                
                vehicle_class = 'vehicle'
                
                key = (start_zone, direction, vehicle_class)
                final_counts[key] += 1

    output_data = []
    for (lane, direction, vehicle), count in final_counts.items():
        output_data.append({
            "Entry Lane": lane,
            "Direction": direction,
            "Vehicle Type": vehicle,
            "Count": count
        })

    if output_data:
        df = pd.DataFrame(output_data)
        
        excel_filename = "traffic_analysis_report2.xlsx"
        df.to_excel(excel_filename, index=False, sheet_name="TrafficFlow")
        
        print(f"\nsaved report to '{excel_filename}' ---")
        print("\nFinal Counts:")
        print(df)
   

if __name__ == "__main__":
    analyze()