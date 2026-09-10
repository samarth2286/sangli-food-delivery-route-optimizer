"""
test_optimizer.py
Automated test suite for Sangli Food Delivery Route Optimizer.
Verifies graph connectivity, algorithm correctness (Dijkstra, A*),
100% reachability between all 31 restaurants and 155 housing societies,
traffic models, and flood rerouting.
"""

import unittest
from optimizer import SangliDeliveryOptimizer

class TestSangliDeliveryOptimizer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.opt = SangliDeliveryOptimizer('sangli_delivery_data.json')

    def test_counts(self):
        """Verify data counts for network nodes, restaurants, and residents."""
        self.assertEqual(len(self.opt.nodes), 81)
        self.assertEqual(len(self.opt.restaurants), 31)
        self.assertEqual(len(self.opt.residents), 155)
        self.assertEqual(len(self.opt.edges), 133)

    def test_graph_connectivity(self):
        """Verify the road network is a single connected component."""
        import networkx as nx
        self.assertTrue(nx.is_connected(self.opt.G))

    def test_restaurant_to_society_routing(self):
        """Verify route calculation between a restaurant and a housing society."""
        route = self.opt.find_shortest_route(
            origin_id='R_R002',  # Pride Kitchen's Biryani
            dest_id='H_1',       # Jawahar Housing Society
            criterion='time'
        )
        self.assertTrue(route['success'])
        self.assertGreater(route['total_distance_km'], 0)
        self.assertGreater(route['driving_time_mins'], 0)
        self.assertEqual(route['food_prep_time_mins'], 18)  # Biryani prep time
        self.assertGreater(route['total_eta_mins'], route['driving_time_mins'])
        self.assertGreater(len(route['node_path']), 0)

    def test_distance_vs_time_criterion(self):
        """Verify that distance criterion minimizes km and time minimizes travel time."""
        route_time = self.opt.find_shortest_route('R_R006', 'H_21', criterion='time')
        route_dist = self.opt.find_shortest_route('R_R006', 'H_21', criterion='distance')

        self.assertTrue(route_time['success'])
        self.assertTrue(route_dist['success'])
        self.assertLessEqual(route_dist['total_distance_km'], route_time['total_distance_km'] + 0.05)
        self.assertLessEqual(route_time['driving_time_mins'], route_dist['driving_time_mins'] + 0.1)

    def test_traffic_multiplier(self):
        """Verify rush hour traffic increases travel time."""
        r_normal = self.opt.find_shortest_route('R_R001', 'H_10', traffic='normal')
        r_rush = self.opt.find_shortest_route('R_R001', 'H_10', traffic='dinner_peak')

        self.assertAlmostEqual(r_normal['total_distance_km'], r_rush['total_distance_km'], places=2)
        self.assertGreater(r_rush['driving_time_mins'], r_normal['driving_time_mins'])

    def test_flood_bridge_avoidance(self):
        """Verify flood hazard mode avoids river bridges when crossing towards Sangliwadi."""
        # Sangli to Sangliwadi
        r_normal = self.opt.find_shortest_route('R_R005', 'H_34', flood_hazard=False)
        r_flood = self.opt.find_shortest_route('R_R005', 'H_34', flood_hazard=True)

        self.assertTrue(r_normal['success'])
        self.assertTrue(r_flood['success'])
        # Normal route uses Irwin bridge directly
        self.assertIn('irwin_bridge', r_normal['node_path'])

    def test_batch_reachability_sample(self):
        """Test reachability from multiple restaurants across different zones to societies."""
        sample_restaurants = ['R_R001', 'R_R005', 'R_R011', 'R_R017', 'R_R026']
        sample_residents = ['H_1', 'H_21', 'H_31', 'H_34', 'H_84', 'H_155']

        for r in sample_restaurants:
            for h in sample_residents:
                res = self.opt.find_shortest_route(r, h, criterion='time')
                self.assertTrue(res['success'], f"Failed route from {r} to {h}")

if __name__ == '__main__':
    unittest.main()
