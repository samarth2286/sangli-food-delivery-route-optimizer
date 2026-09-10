# 🛵 Sangli Food Delivery Route Optimizer

An intelligent graph-based delivery route optimization system designed for **Sangli, Maharashtra**. Features real-time shortest path calculation (Dijkstra and A*), realistic road network modeling with speed profiles, traffic congestion simulation, river flood avoidance, and an interactive Leaflet-powered web dashboard.

---

## 🌟 Key Features

- **🗺️ Real Interactive Map of Sangli**: Integrated with Leaflet.js and OpenStreetMap (100% watermark-free), displaying real streets, bridges, and landmarks.
- **🍽️ 31 Real Restaurants**: Geocoded restaurants across Sangli with cuisine types, ratings, and reviews.
- **🏡 155 Residential Housing Societies**: Covers colonies, apartments, and townships across Sangli, Vishrambag, Kupwad, Miraj, Madhavnagar, Sangliwadi, Haripur, and Budhgaon.
- **🛣️ Connected Road Network**: 81 junctions and 133 road segments with realistic road classifications:
  - Highway: 60 km/h
  - Arterial: 40 km/h
  - Main Roads: 30 km/h
  - Bridges: 25 km/h
  - Local Streets: 20 km/h
- **⚡ Dual Optimization Modes**:
  - **Fastest Travel Time (mins)**: Calculates optimal path factoring in speed limits.
  - **Shortest Distance (km)**: Minimizes physical driving distance.
- **🚦 Real-Time Traffic & Monsoon Simulation**:
  - Normal (1.0x), Lunch Peak (1.35x), Dinner Peak (1.50x), Rain Alert (1.40x).
  - River Flood Hazard mode dynamically diverts routes away from Krishna River bridges (Irwin Bridge and South Bridge).
- **⏱️ Comprehensive Order ETA Calculator**:
  \[
  \text{Total Delivery ETA} = \text{Kitchen Cooking Time} + \text{Pickup Access} + \text{Road Transit} + \text{Doorstep Handoff}
  \]
- **💻 Live Terminal Console Mirror**: Directly displays the full terminal output report on the web dashboard with a single-click copy button.
- **🛵 Animated Scooter Delivery Simulator**: Watch the delivery rider travel along the optimal route in real time.

---

## 📂 Project Structure

```
route-optimizer/
├── index.html                 # Main interactive web dashboard
├── route_optimizer.html       # Web application mirror
├── run_app.py                 # Local server launcher (opens browser)
├── optimizer.py               # Core Python optimization engine (CLI & API)
├── test_optimizer.py          # Automated test suite (7 unit tests)
├── prepare_network.py         # Network data preparation & connector script
├── sangli_delivery_data.json  # Consolidated graph and entity dataset
├── residents.csv              # 155 housing societies & colonies
├── restaurants_final (1).csv  # 31 Sangli restaurants dataset
├── edges_clean.csv            # Clean road segment definitions
├── leaflet.js                 # Local Leaflet map engine (offline-ready)
├── leaflet.css                # Local Leaflet stylesheet
└── README.md                  # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Launch the Web Application
Run the launcher script to start a local server and automatically open the map in your default browser:
```powershell
python run_app.py
```
Or simply double-click `index.html`.

### 2. Run Route Optimization via Python CLI
You can also calculate the optimal route programmatically:
```powershell
# Shortest distance from Pride Kitchen's Biryani to Jawahar Housing Society
python optimizer.py --origin R_R002 --dest H_1 --criterion distance

# Fastest time under dinner rush traffic
python optimizer.py --origin R_R006 --dest H_21 --traffic dinner_peak

# Route with River Flood avoidance (avoids Krishna river bridges)
python optimizer.py --origin R_R005 --dest H_34 --flood
```

### 3. Run Automated Tests
```powershell
python test_optimizer.py
```

---

## 📊 Sample Route Output

```text
=================================================================
  SANGLI FOOD DELIVERY ROUTE OPTIMIZATION RESULT
=================================================================
Origin (Pickup):      Pride Kitchen's Hyderabadi Biryani Sangli (Restaurant)
  Category & Rating:  Biryani restaurant | Rating: 4.8 stars
Destination (Drop):   Jawahar Cooperative Housing Society (Vishrambag)
Optimization Goal:    TIME (Traffic: normal)
-----------------------------------------------------------------
Total Physical Distance:    4.12 km
Road Driving Travel Time:   9.2 minutes
Kitchen Preparation Time:   18 minutes
Doorstep Handoff:           3.0 minutes
TOTAL ESTIMATED ETA:        30.2 minutes
-----------------------------------------------------------------
Nodes in Path (5): shivaji_nagar -> smr_north -> smr_mid -> dhamani_road -> rest_dhamani
=================================================================
```

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Leaflet.js, OpenStreetMap
- **Backend / Engine**: Python 3, NetworkX, Pandas, NumPy
- **Algorithms**: Dijkstra's Shortest Path, A* Search, Haversine Geodesic Distance
