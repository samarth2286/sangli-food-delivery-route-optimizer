"""
prepare_network.py
Consolidates Sangli road network, 31 restaurants, and 155 residential housing societies.
Links all locations to nearest network nodes and generates unified data files.
Incorporates real urban arterial connectors to ensure shortest and most direct city paths.
"""

import json
import math
import re
import pandas as pd

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0088
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def main():
    # 1. Load base network data from network_map.html
    with open('network_map.html', 'r', encoding='utf-8') as f:
        html_text = f.read()

    m = re.search(r'const DATA = (\{.*?\});', html_text)
    if not m:
        raise ValueError("Could not find DATA in network_map.html")

    base_data = json.loads(m.group(1))
    nodes = base_data['nodes']
    edges = list(base_data['edges'])

    # Add realistic urban nodes for Sangliwadi North and 100 Feet Road
    extra_nodes = [
        {
            "id": "sangliwadi_north",
            "name": "Sangliwadi Main Chowk",
            "lat": 16.858,
            "lon": 74.552,
            "x": 74.552 * math.cos(math.radians(16.858)),
            "y": 16.858,
            "type": "junction",
            "role": "structure",
            "area": "Sangliwadi",
            "deg": 3,
            "label": True
        },
        {
            "id": "hundred_ft_dmart",
            "name": "100 Feet Road D-Mart Chowk",
            "lat": 16.848,
            "lon": 74.576,
            "x": 74.576 * math.cos(math.radians(16.848)),
            "y": 16.848,
            "type": "junction",
            "role": "structure",
            "area": "Sangli",
            "deg": 4,
            "label": True
        }
    ]

    existing_node_ids = {n['id'] for n in nodes}
    for en in extra_nodes:
        if en['id'] not in existing_node_ids:
            nodes.append(en)

    # Real-world direct road connections
    primary_connectors = [
        {"u": "balaji_nagar", "v": "kupwad_junction", "km": 5.14, "type": "arterial", "kmph": 40.0, "name": "Sangli-Kupwad Road"},
        {"u": "civil_hospital", "v": "kupwad_link", "km": 4.55, "type": "arterial", "kmph": 40.0, "name": "100 Feet Road Extension"},
        {"u": "shivaji_nagar", "v": "vishrambag_chowk", "km": 2.42, "type": "arterial", "kmph": 40.0, "name": "100 Feet Road"},
        {"u": "sangli_south_jn", "v": "smr_north", "km": 1.85, "type": "arterial", "kmph": 40.0, "name": "100 Feet Road (West)"},
        {"u": "shivaji_nagar", "v": "vishrambag_res", "km": 2.05, "type": "main", "kmph": 30.0, "name": "Old Dhamani Road"},
        {"u": "sangli_st_stand", "v": "market_yard", "km": 1.22, "type": "main", "kmph": 30.0, "name": "Market Yard Direct Road"},
        {"u": "smr_north", "v": "kupwad_link", "km": 3.55, "type": "arterial", "kmph": 40.0, "name": "Kupwad-Miraj Link"},
        {"u": "sangliwadi", "v": "ashta_road", "km": 3.35, "type": "main", "kmph": 35.0, "name": "Sangliwadi-Ashta Road"},
        {"u": "kupwad_junction", "v": "kupwad_midc", "km": 3.25, "type": "main", "kmph": 35.0, "name": "Kupwad MIDC Main Road"},
        {"u": "ganapati_mandir", "v": "sangliwadi", "km": 1.25, "type": "bridge", "kmph": 25.0, "name": "Irwin Bridge Approach"},
        {"u": "sangliwadi_north", "v": "sangliwadi", "km": 2.45, "type": "main", "kmph": 30.0, "name": "Sangliwadi Main Road"},
        {"u": "sangliwadi_north", "v": "irwin_bridge", "km": 1.75, "type": "bridge", "kmph": 25.0, "name": "Irwin Bridge North Approach"},
        {"u": "hundred_ft_dmart", "v": "shivaji_nagar", "km": 0.23, "type": "local", "kmph": 20.0, "name": "100 Feet Road"},
        {"u": "hundred_ft_dmart", "v": "smr_north", "km": 1.05, "type": "arterial", "kmph": 40.0, "name": "100 Feet Road"},
        {"u": "hundred_ft_dmart", "v": "sangli_south_jn", "km": 0.85, "type": "main", "kmph": 30.0, "name": "100 Feet Road"}
    ]

    # Add new connectors avoiding duplicates
    existing_edge_pairs = {(e['u'], e['v']) for e in edges} | {(e['v'], e['u']) for e in edges}
    for c in primary_connectors:
        if (c['u'], c['v']) not in existing_edge_pairs:
            edges.append(c)
            existing_edge_pairs.add((c['u'], c['v']))
            existing_edge_pairs.add((c['v'], c['u']))

    node_map = {n['id']: n for n in nodes}
    print(f"Total network nodes: {len(nodes)}, edges: {len(edges)}")

    # 2. Process 31 restaurants
    rest_df = pd.read_csv('restaurants_final (1).csv')
    restaurants = []
    for _, row in rest_df.iterrows():
        r_lat = float(row['latitude'])
        r_lon = float(row['longitude'])
        
        # Calculate closest node dynamically
        best_node = None
        best_dist = float('inf')
        for n in nodes:
            d = haversine_km(r_lat, r_lon, n['lat'], n['lon'])
            if d < best_dist:
                best_dist = d
                best_node = n['id']

        r_dict = {
            'id': f"R_{row['restaurant_id']}",
            'code': str(row['restaurant_id']),
            'name': str(row['restaurant_name']),
            'address': str(row['address']),
            'lat': r_lat,
            'lon': r_lon,
            'category': str(row['category']),
            'rating': float(row['rating']),
            'reviews': int(row['review_count']),
            'nearest_node': best_node,
            'distance_to_node_km': round(best_dist, 3)
        }
        restaurants.append(r_dict)

    print(f"Processed {len(restaurants)} restaurants.")

    # 3. Process 155 residents / housing societies
    res_df = pd.read_csv('residents.csv')
    residents = []
    for _, row in res_df.iterrows():
        lat = float(row['latitude'])
        lon = float(row['longitude'])
        
        best_node = None
        best_dist = float('inf')
        for n in nodes:
            d = haversine_km(lat, lon, n['lat'], n['lon'])
            if d < best_dist:
                best_dist = d
                best_node = n['id']

        res_dict = {
            'id': f"H_{row['id']}",
            'num_id': int(row['id']),
            'name': str(row['name']),
            'locality': str(row['locality']),
            'city_zone': str(row['city_zone']),
            'lat': lat,
            'lon': lon,
            'type': str(row['type']),
            'nearest_node': best_node,
            'distance_to_node_km': round(best_dist, 3)
        }
        residents.append(res_dict)

    print(f"Processed {len(residents)} residents/housing societies.")

    # Coordinate bounds
    all_lats = [n['lat'] for n in nodes] + [r['lat'] for r in restaurants] + [h['lat'] for h in residents]
    all_lons = [n['lon'] for n in nodes] + [r['lon'] for r in restaurants] + [h['lon'] for h in residents]

    bounds = {
        'min_lat': min(all_lats),
        'max_lat': max(all_lats),
        'min_lon': min(all_lons),
        'max_lon': max(all_lons)
    }

    unified = {
        'bounds': bounds,
        'nodes': nodes,
        'edges': edges,
        'restaurants': restaurants,
        'residents': residents
    }

    with open('sangli_delivery_data.json', 'w', encoding='utf-8') as f:
        json.dump(unified, f, indent=2)

    pd.DataFrame(residents).to_csv('residents_enriched.csv', index=False)
    pd.DataFrame(restaurants).to_csv('restaurants_enriched.csv', index=False)

    edges_df = pd.DataFrame(edges)
    edges_df['travel_time_mins'] = (edges_df['km'] / edges_df['kmph']) * 60
    edges_df.to_csv('edges_clean.csv', index=False)

    print("Data preparation complete! Real urban connectors integrated successfully.")

if __name__ == '__main__':
    main()
