"""
optimizer.py
Food Delivery Route Optimization Engine for Sangli, Maharashtra.
Calculates shortest distance and fastest travel time between any restaurant,
housing society/resident, or road junction using Dijkstra and A* algorithms.
"""

import json
import math
import argparse
import networkx as nx

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0088
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

class SangliDeliveryOptimizer:
    def __init__(self, data_path='sangli_delivery_data.json'):
        with open(data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.nodes = {n['id']: n for n in self.data['nodes']}
        self.edges = self.data['edges']
        self.restaurants = {r['id']: r for r in self.data['restaurants']}
        self.residents = {h['id']: h for h in self.data['residents']}

        # Quick lookup dictionaries by name/code
        self.all_entities = {}
        for r_id, r in self.restaurants.items():
            self.all_entities[r_id] = {
                'id': r_id,
                'name': r['name'],
                'type': 'restaurant',
                'category': r['category'],
                'rating': r['rating'],
                'lat': r['lat'],
                'lon': r['lon'],
                'nearest_node': r['nearest_node'],
                'dist_to_node': r['distance_to_node_km']
            }
        for h_id, h in self.residents.items():
            self.all_entities[h_id] = {
                'id': h_id,
                'name': h['name'],
                'type': 'resident',
                'locality': h['locality'],
                'city_zone': h['city_zone'],
                'lat': h['lat'],
                'lon': h['lon'],
                'nearest_node': h['nearest_node'],
                'dist_to_node': h['distance_to_node_km']
            }
        for n_id, n in self.nodes.items():
            self.all_entities[n_id] = {
                'id': n_id,
                'name': n['name'],
                'type': 'node',
                'area': n['area'],
                'lat': n['lat'],
                'lon': n['lon'],
                'nearest_node': n_id,
                'dist_to_node': 0.0
            }

        self._build_graph()

    def _build_graph(self):
        """Build NetworkX graph from road edges."""
        self.G = nx.Graph()
        for n_id, node in self.nodes.items():
            self.G.add_node(n_id, **node)

        for edge in self.edges:
            u, v = edge['u'], edge['v']
            km = float(edge['km'])
            kmph = float(edge['kmph'])
            rtype = edge['type']
            name = edge.get('name', '')
            time_mins = (km / kmph) * 60.0

            self.G.add_edge(u, v, km=km, kmph=kmph, type=rtype, name=name, time_mins=time_mins)

    def get_prep_time(self, category):
        """Estimated kitchen cooking/prep time based on food category."""
        cat = category.lower()
        if 'biryani' in cat:
            return 18
        elif 'pizza' in cat or 'italian' in cat:
            return 16
        elif 'south indian' in cat or 'cafe' in cat:
            return 10
        elif 'pure veg' in cat or 'thali' in cat:
            return 12
        elif 'north indian' in cat or 'marathi' in cat:
            return 15
        return 14

    def heuristic_time(self, u, v):
        """A* admissible heuristic for travel time in minutes."""
        n1 = self.nodes[u]
        n2 = self.nodes[v]
        dist_km = haversine_km(n1['lat'], n1['lon'], n2['lat'], n2['lon'])
        max_speed = 60.0  # Highway speed
        return (dist_km / max_speed) * 60.0

    def heuristic_dist(self, u, v):
        """A* admissible heuristic for distance in km."""
        n1 = self.nodes[u]
        n2 = self.nodes[v]
        return haversine_km(n1['lat'], n1['lon'], n2['lat'], n2['lon'])

    def find_shortest_route(self, origin_id, dest_id, criterion='time', traffic='normal', flood_hazard=False):
        """
        Find optimal delivery route between ANY origin and destination.
        
        Args:
            origin_id (str): Restaurant ID (e.g. 'R_R001'), Resident ID (e.g. 'H_1'), or Node ID.
            dest_id (str): Restaurant, Resident, or Node ID.
            criterion (str): 'time' (fastest delivery) or 'distance' (shortest km).
            traffic (str): 'normal' (1.0x), 'lunch_peak' (1.35x), 'dinner_peak' (1.5x), 'rain' (1.4x).
            flood_hazard (bool): If True, blocks or heavily penalizes Krishna River bridges (Irwin & South Bridge).
            
        Returns:
            dict: Route summary with distance, travel time, prep time, total ETA, and step-by-step turns.
        """
        if origin_id not in self.all_entities:
            raise KeyError(f"Origin ID '{origin_id}' not found.")
        if dest_id not in self.all_entities:
            raise KeyError(f"Destination ID '{dest_id}' not found.")

        orig = self.all_entities[origin_id]
        dest = self.all_entities[dest_id]

        start_node = orig['nearest_node']
        end_node = dest['nearest_node']

        # Traffic multiplier
        traffic_multipliers = {
            'normal': 1.0,
            'lunch_peak': 1.35,
            'dinner_peak': 1.50,
            'rain': 1.40
        }
        t_mult = traffic_multipliers.get(traffic, 1.0)

        # Create temporary working graph with current traffic and flood penalties
        G_work = self.G.copy()
        flood_bridges = {('irwin_bridge', 'sangliwadi'), ('sangliwadi', 'irwin_bridge'),
                         ('south_bridge', 'sangliwadi_east'), ('sangliwadi_east', 'south_bridge')}

        for u, v, data in G_work.edges(data=True):
            is_bridge = (u, v) in flood_bridges or (v, u) in flood_bridges or data.get('type') == 'bridge'
            
            # Apply traffic multiplier to time
            data['adjusted_time'] = data['time_mins'] * t_mult
            data['adjusted_km'] = data['km']

            if flood_hazard and is_bridge:
                # River flood: bridges are submerged or impassable
                data['adjusted_time'] = data['time_mins'] * 1000.0
                data['adjusted_km'] = data['km'] * 1000.0

        weight_key = 'adjusted_time' if criterion == 'time' else 'adjusted_km'

        # Compute path on road network
        if start_node == end_node:
            node_path = [start_node]
            network_dist_km = 0.0
            network_time_mins = 0.0
            turn_segments = []
        else:
            try:
                node_path = nx.dijkstra_path(G_work, start_node, end_node, weight=weight_key)
            except nx.NetworkXNoPath:
                return {
                    'success': False,
                    'message': f"No connected route found between {orig['name']} and {dest['name']}."
                }

            # Calculate network distance and time
            network_dist_km = 0.0
            network_time_mins = 0.0
            turn_segments = []

            for i in range(len(node_path) - 1):
                u = node_path[i]
                v = node_path[i + 1]
                edge_data = G_work[u][v]
                seg_km = edge_data['km']
                seg_speed = edge_data['kmph'] / t_mult
                seg_time = (seg_km / seg_speed) * 60.0

                network_dist_km += seg_km
                network_time_mins += seg_time

                turn_segments.append({
                    'from_node': u,
                    'from_name': self.nodes[u]['name'],
                    'to_node': v,
                    'to_name': self.nodes[v]['name'],
                    'road_name': edge_data['name'] or f"Road from {self.nodes[u]['name']} to {self.nodes[v]['name']}",
                    'road_type': edge_data['type'],
                    'distance_km': round(seg_km, 3),
                    'speed_kmph': round(seg_speed, 1),
                    'time_mins': round(seg_time, 2)
                })

        # First leg: Origin to start_node
        pickup_access_speed = 18.0 / t_mult
        pickup_dist_km = orig['dist_to_node']
        pickup_time_mins = (pickup_dist_km / pickup_access_speed) * 60.0 if pickup_dist_km > 0 else 0.0

        # Last leg: end_node to Destination
        dropoff_access_speed = 18.0 / t_mult
        dropoff_dist_km = dest['dist_to_node']
        dropoff_time_mins = (dropoff_dist_km / dropoff_access_speed) * 60.0 if dropoff_dist_km > 0 else 0.0

        # Total driving stats
        total_distance_km = round(pickup_dist_km + network_dist_km + dropoff_dist_km, 3)
        total_driving_time_mins = round(pickup_time_mins + network_time_mins + dropoff_time_mins, 2)

        # Kitchen preparation & doorstep handoff
        if orig['type'] == 'restaurant':
            prep_time_mins = self.get_prep_time(orig.get('category', ''))
        else:
            prep_time_mins = 0

        handoff_time_mins = 3.0  # customer handoff & building entry

        # Total order delivery time (ETA)
        total_eta_mins = round(prep_time_mins + total_driving_time_mins + handoff_time_mins, 1)

        # Road classification distribution
        road_types = {}
        for seg in turn_segments:
            rtype = seg['road_type']
            road_types[rtype] = road_types.get(rtype, 0.0) + seg['distance_km']

        return {
            'success': True,
            'origin': orig,
            'destination': dest,
            'criterion': criterion,
            'traffic_condition': traffic,
            'traffic_multiplier': t_mult,
            'flood_avoidance_active': flood_hazard,
            'node_path': node_path,
            'pickup_leg': {
                'from': orig['name'],
                'to': self.nodes[start_node]['name'],
                'distance_km': round(pickup_dist_km, 3),
                'time_mins': round(pickup_time_mins, 2)
            },
            'dropoff_leg': {
                'from': self.nodes[end_node]['name'],
                'to': dest['name'],
                'distance_km': round(dropoff_dist_km, 3),
                'time_mins': round(dropoff_time_mins, 2)
            },
            'turn_segments': turn_segments,
            'total_distance_km': total_distance_km,
            'driving_time_mins': total_driving_time_mins,
            'food_prep_time_mins': prep_time_mins,
            'handoff_time_mins': handoff_time_mins,
            'total_eta_mins': total_eta_mins,
            'road_type_distribution': {k: round(v, 2) for k, v in road_types.items()}
        }

    def print_route_summary(self, result):
        """Prints formatted summary of the route."""
        if not result.get('success'):
            print("Route Error:", result.get('message'))
            return

        print("\n" + "=" * 65)
        print("  SANGLI FOOD DELIVERY ROUTE OPTIMIZATION RESULT")
        print("=" * 65)
        orig = result['origin']
        dest = result['destination']
        print(f"Origin (Pickup):      {orig['name']} ({orig['type'].capitalize()})")
        if orig.get('category'):
            print(f"  Category & Rating:  {orig['category']} | Rating: {orig['rating']} stars")
        print(f"Destination (Drop):   {dest['name']} ({dest.get('locality', dest.get('area', ''))})")
        print(f"Optimization Goal:    {result['criterion'].upper()} (Traffic: {result['traffic_condition']})")
        print("-" * 65)
        print(f"Total Physical Distance:    {result['total_distance_km']:.2f} km")
        print(f"Road Driving Travel Time:   {result['driving_time_mins']:.1f} minutes")
        print(f"Kitchen Preparation Time:   {result['food_prep_time_mins']} minutes")
        print(f"Doorstep Handoff:           {result['handoff_time_mins']} minutes")
        print(f"TOTAL ESTIMATED ETA:        {result['total_eta_mins']:.1f} minutes")
        print("-" * 65)
        print(f"Nodes in Path ({len(result['node_path'])}): " + " -> ".join(result['node_path']))
        print("\nStep-by-Step Directions:")
        if result['pickup_leg']['distance_km'] > 0:
            print(f"  1. Start at {result['pickup_leg']['from']} -> head to {result['pickup_leg']['to']} ({result['pickup_leg']['distance_km']} km, {result['pickup_leg']['time_mins']:.1f} min)")

        step = 2
        for seg in result['turn_segments']:
            print(f"  {step}. Follow {seg['road_name']} ({seg['road_type']}) -> {seg['to_name']} [{seg['distance_km']} km at {seg['speed_kmph']} km/h, {seg['time_mins']:.1f} min]")
            step += 1

        if result['dropoff_leg']['distance_km'] > 0:
            print(f"  {step}. Final approach from {result['dropoff_leg']['from']} -> arrive at {result['dropoff_leg']['to']} ({result['dropoff_leg']['distance_km']} km, {result['dropoff_leg']['time_mins']:.1f} min)")

        print("=" * 65 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Sangli Food Delivery Route Optimizer")
    parser.add_argument('--origin', type=str, default='R_R002', help="Origin ID, e.g., R_R002 (Pride Kitchen's Biryani)")
    parser.add_argument('--dest', type=str, default='H_1', help="Destination ID, e.g., H_1 (Jawahar Housing Society)")
    parser.add_argument('--criterion', choices=['time', 'distance'], default='time', help="Optimization criterion")
    parser.add_argument('--traffic', choices=['normal', 'lunch_peak', 'dinner_peak', 'rain'], default='normal')
    parser.add_argument('--flood', action='store_true', help="Avoid flood hazard river bridges")

    args = parser.parse_args()
    opt = SangliDeliveryOptimizer()
    result = opt.find_shortest_route(args.origin, args.dest, criterion=args.criterion, traffic=args.traffic, flood_hazard=args.flood)
    opt.print_route_summary(result)

if __name__ == '__main__':
    main()
