"""
build_web_app.py
Generates route_optimizer.html and index.html embedding the complete Sangli delivery dataset,
interactive SVG map, Dijkstra routing engine, animated delivery simulator, and real-time metrics.
"""

import json

def generate_html():
    with open('sangli_delivery_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    json_str = json.dumps(data)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sangli Food Delivery Route Optimizer</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg-base: #0f172a;
    --bg-surface: #1e293b;
    --bg-card: #273549;
    --bg-hover: #334155;
    --border: #334155;
    --border-light: rgba(255,255,255,0.1);
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --primary: #3b82f6;
    --primary-glow: rgba(59,130,246,0.5);
    --restaurant: #f59e0b;
    --restaurant-glow: rgba(245,158,11,0.6);
    --resident: #10b981;
    --resident-glow: rgba(16,185,129,0.6);
    --accent: #ec4899;
    --road-highway: #60a5fa;
    --road-arterial: #818cf8;
    --road-main: #34d399;
    --road-local: #475569;
    --road-bridge: #f43f5e;
  }}

  [data-theme="light"] {{
    --bg-base: #f8fafc;
    --bg-surface: #ffffff;
    --bg-card: #f1f5f9;
    --bg-hover: #e2e8f0;
    --border: #cbd5e1;
    --border-light: rgba(0,0,0,0.08);
    --text-main: #0f172a;
    --text-muted: #64748b;
    --primary: #2563eb;
    --primary-glow: rgba(37,99,235,0.4);
    --restaurant: #d97706;
    --restaurant-glow: rgba(217,119,6,0.4);
    --resident: #059669;
    --resident-glow: rgba(5,150,105,0.4);
    --road-highway: #2563eb;
    --road-arterial: #6366f1;
    --road-main: #059669;
    --road-local: #94a3b8;
    --road-bridge: #e11d48;
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    background: var(--bg-base);
    color: var(--text-main);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}

  /* Top Navigation Bar */
  header {{
    background: var(--bg-surface);
    border-bottom: 1px solid var(--border);
    padding: 10px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: 30;
    flex-shrink: 0;
  }}
  .brand {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .logo-badge {{
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, var(--restaurant), #ef4444);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
  }}
  .brand h1 {{
    font-size: 17px;
    font-weight: 700;
    letter-spacing: -0.3px;
  }}
  .brand p {{
    font-size: 11.5px;
    color: var(--text-muted);
  }}
  .stats-bar {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}
  .stat-pill {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    color: var(--text-muted);
  }}
  .stat-pill strong {{
    color: var(--text-main);
  }}
  .stat-pill .dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
  }}
  .header-actions {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  button.btn {{
    font-family: inherit;
    font-size: 12.5px;
    font-weight: 600;
    background: var(--bg-card);
    color: var(--text-main);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 6px 12px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: all 0.15s ease;
  }}
  button.btn:hover {{
    background: var(--bg-hover);
    border-color: var(--primary);
  }}
  button.btn-primary {{
    background: var(--primary);
    color: #ffffff;
    border-color: var(--primary);
  }}
  button.btn-primary:hover {{
    filter: brightness(1.1);
  }}

  /* Main Workspace Layout */
  .workspace {{
    display: flex;
    flex: 1;
    overflow: hidden;
    position: relative;
  }}

  /* Sidebar Controls Panel */
  .sidebar {{
    width: 390px;
    background: var(--bg-surface);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    z-index: 20;
    overflow-y: auto;
    flex-shrink: 0;
  }}
  .sidebar-section {{
    padding: 16px;
    border-bottom: 1px solid var(--border);
  }}
  .sidebar-section:last-child {{
    border-bottom: none;
  }}
  .sec-title {{
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-muted);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}
  .sec-title span.badge {{
    font-size: 10px;
    background: var(--bg-card);
    padding: 2px 6px;
    border-radius: 4px;
    color: var(--primary);
  }}

  /* Form Elements */
  .field-group {{
    margin-bottom: 12px;
  }}
  .field-label {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 5px;
  }}
  .field-label .hint {{
    font-size: 11px;
    color: var(--text-muted);
    font-weight: 400;
  }}
  select, input[type="text"] {{
    width: 100%;
    background: var(--bg-card);
    border: 1px solid var(--border);
    color: var(--text-main);
    padding: 8px 10px;
    border-radius: 8px;
    font-family: inherit;
    font-size: 12.5px;
    outline: none;
    transition: border-color 0.15s;
  }}
  select:focus, input[type="text"]:focus {{
    border-color: var(--primary);
  }}
  .swap-row {{
    display: flex;
    justify-content: center;
    margin: -4px 0 8px;
  }}
  .btn-swap {{
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--bg-card);
    border: 1px solid var(--border);
    color: var(--text-muted);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.15s;
  }}
  .btn-swap:hover {{
    color: var(--primary);
    border-color: var(--primary);
    transform: rotate(180deg);
  }}

  /* Mode Chips & Toggles */
  .segmented-control {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 3px;
    gap: 3px;
  }}
  .segmented-btn {{
    font-size: 11.5px;
    font-weight: 600;
    padding: 6px;
    border-radius: 6px;
    border: none;
    background: transparent;
    color: var(--text-muted);
    cursor: pointer;
    text-align: center;
    transition: all 0.15s;
  }}
  .segmented-btn.active {{
    background: var(--primary);
    color: #ffffff;
    box-shadow: 0 2px 6px var(--primary-glow);
  }}

  .options-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin-top: 10px;
  }}
  .toggle-card {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    padding: 8px 10px;
    border-radius: 8px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: all 0.15s;
    user-select: none;
  }}
  .toggle-card:hover {{
    border-color: var(--border-light);
  }}
  .toggle-card.active {{
    border-color: var(--primary);
    background: rgba(59,130,246,0.1);
  }}
  .toggle-card.hazard.active {{
    border-color: var(--road-bridge);
    background: rgba(244,63,94,0.1);
  }}
  .toggle-card span {{
    font-size: 11.5px;
    font-weight: 600;
  }}
  .status-indicator {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--border);
  }}
  .toggle-card.active .status-indicator {{
    background: var(--primary);
    box-shadow: 0 0 8px var(--primary);
  }}
  .toggle-card.hazard.active .status-indicator {{
    background: var(--road-bridge);
    box-shadow: 0 0 8px var(--road-bridge);
  }}

  /* Calculate Route Action */
  .btn-calculate {{
    width: 100%;
    padding: 12px;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.3px;
    border-radius: 10px;
    background: linear-gradient(135deg, #2563eb, #3b82f6);
    color: #ffffff;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    box-shadow: 0 4px 14px var(--primary-glow);
    transition: all 0.15s;
  }}
  .btn-calculate:hover {{
    transform: translateY(-1px);
    box-shadow: 0 6px 18px var(--primary-glow);
  }}
  .btn-calculate:active {{
    transform: translateY(0);
  }}

  /* Results Card */
  .results-card {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px;
    margin-top: 14px;
    display: none;
  }}
  .results-card.show {{
    display: block;
    animation: fadeIn 0.25s ease;
  }}
  @keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(6px); }}
    to {{ opacity: 1; transform: translateY(0); }}
  }}
  .metrics-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 12px;
  }}
  .metric-item {{
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px;
  }}
  .metric-item .val {{
    font-size: 18px;
    font-weight: 800;
    color: var(--text-main);
  }}
  .metric-item .lbl {{
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 2px;
  }}
  .metric-item.highlight {{
    border-color: var(--primary);
    background: rgba(59,130,246,0.08);
  }}
  .metric-item.highlight .val {{
    color: var(--primary);
  }}

  .progress-breakdown {{
    margin: 10px 0;
  }}
  .bar-segments {{
    height: 6px;
    border-radius: 3px;
    overflow: hidden;
    display: flex;
    background: var(--bg-surface);
  }}
  .bar-seg {{
    height: 100%;
  }}
  .bar-legend {{
    display: flex;
    justify-content: space-between;
    font-size: 10.5px;
    color: var(--text-muted);
    margin-top: 5px;
  }}

  /* Step by Step Timeline */
  .timeline {{
    max-height: 220px;
    overflow-y: auto;
    margin-top: 10px;
    padding-right: 4px;
  }}
  .timeline-step {{
    display: flex;
    gap: 10px;
    position: relative;
    padding-bottom: 12px;
  }}
  .timeline-step:last-child {{
    padding-bottom: 0;
  }}
  .timeline-step::before {{
    content: '';
    position: absolute;
    left: 9px;
    top: 18px;
    bottom: 0;
    width: 2px;
    background: var(--border);
  }}
  .timeline-step:last-child::before {{
    display: none;
  }}
  .step-icon {{
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: var(--bg-surface);
    border: 2px solid var(--primary);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 9px;
    font-weight: 700;
    flex-shrink: 0;
    z-index: 1;
  }}
  .step-content {{
    flex: 1;
  }}
  .step-title {{
    font-size: 11.5px;
    font-weight: 600;
    line-height: 1.3;
  }}
  .step-desc {{
    font-size: 10.5px;
    color: var(--text-muted);
    margin-top: 2px;
  }}

  /* Map View Area */
  .map-container {{
    flex: 1;
    position: relative;
    background: var(--bg-base);
    overflow: hidden;
  }}
  #map-svg {{
    width: 100%;
    height: 100%;
    cursor: grab;
    user-select: none;
    display: block;
  }}
  #map-svg.dragging {{
    cursor: grabbing;
  }}

  /* Map Controls Overlay */
  .map-toolbar {{
    position: absolute;
    top: 16px;
    right: 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    z-index: 10;
  }}
  .tool-btn {{
    width: 36px;
    height: 36px;
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text-main);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transition: all 0.15s;
  }}
  .tool-btn:hover {{
    background: var(--bg-hover);
    border-color: var(--primary);
  }}

  .layer-chips {{
    position: absolute;
    bottom: 16px;
    left: 16px;
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    z-index: 10;
  }}
  .layer-chip {{
    background: var(--bg-surface);
    border: 1px solid var(--border);
    padding: 6px 10px;
    border-radius: 20px;
    font-size: 11.5px;
    font-weight: 600;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    user-select: none;
    transition: all 0.15s;
  }}
  .layer-chip.off {{
    opacity: 0.45;
  }}
  .layer-chip .dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
  }}

  /* Map Legend */
  .map-legend {{
    position: absolute;
    bottom: 16px;
    right: 16px;
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 10px 14px;
    display: flex;
    gap: 14px;
    font-size: 11.5px;
    color: var(--text-muted);
    box-shadow: 0 4px 14px rgba(0,0,0,0.2);
    z-index: 10;
  }}
  .legend-item {{
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .legend-color {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
  }}

  /* Tooltip */
  #tooltip {{
    position: fixed;
    pointer-events: none;
    opacity: 0;
    background: var(--bg-surface);
    color: var(--text-main);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 12px;
    line-height: 1.45;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    z-index: 100;
    max-width: 280px;
    transition: opacity 0.1s ease;
  }}
  #tooltip h4 {{
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 2px;
  }}
  #tooltip .subtag {{
    color: var(--text-muted);
    font-size: 11px;
    margin-bottom: 4px;
  }}
  #tooltip .tip-detail {{
    font-size: 11px;
    color: var(--text-main);
  }}

  /* SVG Graphics Styling */
  .road-path {{
    fill: none;
    stroke-linecap: round;
    transition: stroke-width 0.15s;
  }}
  .road-path:hover {{
    stroke: #ffffff;
  }}
  .route-glow {{
    fill: none;
    stroke: var(--primary);
    stroke-linecap: round;
    stroke-linejoin: round;
    opacity: 0.35;
    filter: drop-shadow(0 0 8px var(--primary));
  }}
  .route-active {{
    fill: none;
    stroke: #38bdf8;
    stroke-linecap: round;
    stroke-linejoin: round;
    stroke-dasharray: 8 4;
    animation: dashRoute 1s linear infinite;
  }}
  @keyframes dashRoute {{
    to {{ stroke-dashoffset: -12; }}
  }}
  .connector-line {{
    fill: none;
    stroke: #e2e8f0;
    stroke-dasharray: 3 3;
    opacity: 0.75;
  }}
  .node-circle {{
    cursor: pointer;
    transition: transform 0.15s;
  }}
  .node-circle:hover {{
    filter: brightness(1.3);
  }}
  .restaurant-pin {{
    cursor: pointer;
    transition: transform 0.15s;
  }}
  .resident-pin {{
    cursor: pointer;
    transition: transform 0.15s;
  }}
  .pulse-pin {{
    animation: pulseMarker 1.5s infinite;
  }}
  @keyframes pulseMarker {{
    0% {{ r: 6; opacity: 1; }}
    50% {{ r: 11; opacity: 0.4; }}
    100% {{ r: 6; opacity: 1; }}
  }}

  /* Delivery Scooter Animation */
  #delivery-rider {{
    filter: drop-shadow(0 2px 6px rgba(0,0,0,0.5));
    transition: transform 0.05s linear;
  }}
</style>
</head>
<body data-theme="dark">

<header>
  <div class="brand">
    <div class="logo-badge">🛵</div>
    <div>
      <h1>Sangli Food Delivery Route Optimizer</h1>
      <p>Shortest Distance & Travel Time Optimization Engine &middot; Sangli-Miraj-Kupwad</p>
    </div>
  </div>

  <div class="stats-bar">
    <div class="stat-pill">
      <span class="dot" style="background:var(--restaurant)"></span>
      <span><strong>31</strong> Restaurants</span>
    </div>
    <div class="stat-pill">
      <span class="dot" style="background:var(--resident)"></span>
      <span><strong>155</strong> Housing Societies</span>
    </div>
    <div class="stat-pill">
      <span class="dot" style="background:var(--road-highway)"></span>
      <span><strong>118</strong> Road Segments</span>
    </div>
  </div>

  <div class="header-actions">
    <button class="btn" id="btn-theme" onclick="toggleTheme()">☀️ Light Mode</button>
    <button class="btn btn-primary" onclick="simulateDelivery()">▶ Simulate Delivery</button>
  </div>
</header>

<div class="workspace">
  <!-- Controls & Directions Sidebar -->
  <aside class="sidebar">
    <div class="sidebar-section">
      <div class="sec-title">
        <span>Delivery Locations</span>
        <span class="badge">Dijkstra Ready</span>
      </div>

      <!-- Origin Selection (Restaurant or Resident) -->
      <div class="field-group">
        <div class="field-label">
          <span>1. Origin / Pickup Point</span>
          <span class="hint" id="origin-type-label">Restaurant</span>
        </div>
        <select id="origin-select" onchange="onSelectionChange()">
          <!-- Populated by JS -->
        </select>
      </div>

      <div class="swap-row">
        <button class="btn-swap" title="Swap Origin and Destination" onclick="swapLocations()">⇄</button>
      </div>

      <!-- Destination Selection (Housing Society) -->
      <div class="field-group">
        <div class="field-label">
          <span>2. Destination / Dropoff</span>
          <span class="hint">Housing Society</span>
        </div>
        <select id="dest-select" onchange="onSelectionChange()">
          <!-- Populated by JS -->
        </select>
      </div>
    </div>

    <!-- Optimization Preferences -->
    <div class="sidebar-section">
      <div class="sec-title">
        <span>Optimization Strategy</span>
      </div>

      <div class="segmented-control">
        <button class="segmented-btn active" id="btn-opt-time" onclick="setCriterion('time')">⚡ Fastest Travel Time</button>
        <button class="segmented-btn" id="btn-opt-dist" onclick="setCriterion('distance')">📏 Shortest Distance</button>
      </div>

      <div class="options-grid">
        <div class="field-group" style="margin-bottom:0">
          <div class="field-label"><span>Traffic Condition</span></div>
          <select id="traffic-select" onchange="calculateRoute()">
            <option value="normal">🟢 Normal Traffic (1.0x)</option>
            <option value="lunch_peak">🟡 Lunch Rush (1.35x)</option>
            <option value="dinner_peak">🔴 Dinner Peak (1.50x)</option>
            <option value="rain">🌧️ Monsoon Rain (1.40x)</option>
          </select>
        </div>

        <div class="field-group" style="margin-bottom:0">
          <div class="field-label"><span>River Flood Alert</span></div>
          <div class="toggle-card hazard" id="hazard-toggle" onclick="toggleHazard()">
            <span>Avoid Bridges</span>
            <div class="status-indicator"></div>
          </div>
        </div>
      </div>

      <div style="margin-top:14px">
        <button class="btn-calculate" onclick="calculateRoute()">
          <span>🔍 Compute Shortest Delivery Route</span>
        </button>
      </div>
    </div>

    <!-- Route Results & Metrics -->
    <div class="sidebar-section">
      <div class="sec-title">
        <span>Delivery Metrics</span>
        <span class="badge" id="route-status">Ready</span>
      </div>

      <div class="results-card show" id="results-card">
        <div class="metrics-grid">
          <div class="metric-item">
            <div class="val" id="metric-dist">0.0 km</div>
            <div class="lbl">Physical Distance</div>
          </div>
          <div class="metric-item">
            <div class="val" id="metric-travel">0.0 min</div>
            <div class="lbl">Road Travel Time</div>
          </div>
          <div class="metric-item">
            <div class="val" id="metric-prep">0 min</div>
            <div class="lbl">Kitchen Prep Time</div>
          </div>
          <div class="metric-item highlight">
            <div class="val" id="metric-eta">0.0 min</div>
            <div class="lbl">Total Delivery ETA</div>
          </div>
        </div>

        <div class="progress-breakdown">
          <div class="bar-segments" id="road-bars">
            <div class="bar-seg" style="width:60%; background:var(--road-arterial);"></div>
            <div class="bar-seg" style="width:25%; background:var(--road-main);"></div>
            <div class="bar-seg" style="width:15%; background:var(--road-local);"></div>
          </div>
          <div class="bar-legend">
            <span>Road Breakdown</span>
            <span id="speed-stat">Avg 32 km/h</span>
          </div>
        </div>

        <div class="sec-title" style="margin-top:14px; margin-bottom:8px">
          <span>Turn-By-Turn Navigation</span>
        </div>
        <div class="timeline" id="timeline">
          <!-- Populated by JS -->
        </div>
      </div>
    </div>
  </aside>

  <!-- Interactive SVG Map Canvas -->
  <main class="map-container">
    <svg id="map-svg"></svg>

    <!-- Map Zoom & Reset Tools -->
    <div class="map-toolbar">
      <button class="tool-btn" onclick="zoomIn()" title="Zoom In">+</button>
      <button class="tool-btn" onclick="zoomOut()" title="Zoom Out">&minus;</button>
      <button class="tool-btn" onclick="resetZoom()" title="Reset View">&#x21bb;</button>
    </div>

    <!-- Filter Visibility Chips -->
    <div class="layer-chips">
      <div class="layer-chip" id="chip-rest" onclick="toggleLayer('restaurants')">
        <span class="dot" style="background:var(--restaurant)"></span>
        <span>Restaurants (31)</span>
      </div>
      <div class="layer-chip" id="chip-res" onclick="toggleLayer('residents')">
        <span class="dot" style="background:var(--resident)"></span>
        <span>Societies (155)</span>
      </div>
      <div class="layer-chip" id="chip-roads" onclick="toggleLayer('roads')">
        <span class="dot" style="background:var(--road-arterial)"></span>
        <span>Roads</span>
      </div>
      <div class="layer-chip" id="chip-labels" onclick="toggleLayer('labels')">
        <span class="dot" style="background:#cbd5e1"></span>
        <span>Labels</span>
      </div>
    </div>

    <!-- Map Legend -->
    <div class="map-legend">
      <div class="legend-item">
        <span class="legend-color" style="background:var(--restaurant)"></span>
        <span>Pickup</span>
      </div>
      <div class="legend-item">
        <span class="legend-color" style="background:var(--resident)"></span>
        <span>Dropoff</span>
      </div>
      <div class="legend-item">
        <span class="legend-color" style="background:var(--road-highway)"></span>
        <span>Highway</span>
      </div>
      <div class="legend-item">
        <span class="legend-color" style="background:var(--road-arterial)"></span>
        <span>Arterial</span>
      </div>
      <div class="legend-item">
        <span class="legend-color" style="background:var(--road-main)"></span>
        <span>Main</span>
      </div>
      <div class="legend-item">
        <span class="legend-color" style="background:var(--road-bridge); border:1px dashed white;"></span>
        <span>Bridge</span>
      </div>
    </div>
  </main>
</div>

<!-- Floating Tooltip -->
<div id="tooltip"></div>

<script>
// Embedded Complete Sangli Delivery Network Data
const SANGLI_DATA = {json_str};

// State Variables
let currentCriterion = 'time';
let floodHazardActive = false;
let showRestaurants = true;
let showResidents = true;
let showRoads = true;
let showLabels = false;

let view = {{ x: 0, y: 0, k: 1 }};
let isDragging = false;
let dragStart = [0, 0];
let currentRoute = null;
let animTimer = null;

// Road Class Styling
const ROAD_STYLES = {{
  highway:  {{ w: 3.8, color: 'var(--road-highway)', dash: '' }},
  arterial: {{ w: 2.8, color: 'var(--road-arterial)', dash: '' }},
  main:     {{ w: 2.0, color: 'var(--road-main)', dash: '' }},
  local:    {{ w: 1.2, color: 'var(--road-local)', dash: '' }},
  bridge:   {{ w: 2.8, color: 'var(--road-bridge)', dash: '6 4' }}
}};

// Index data by ID
const nodeById = {{}};
SANGLI_DATA.nodes.forEach(n => nodeById[n.id] = n);

const restById = {{}};
SANGLI_DATA.restaurants.forEach(r => restById[r.id] = r);

const resById = {{}};
SANGLI_DATA.residents.forEach(h => resById[h.id] = h);

// Map projection configuration
const W = 1400, H = 850, PAD = 60;
const svg = document.getElementById('map-svg');
const tooltip = document.getElementById('tooltip');

function projectCoordinates() {{
  const b = SANGLI_DATA.bounds;
  const sx = (W - PAD * 2) / (b.max_lon - b.min_lon);
  const sy = (H - PAD * 2) / (b.max_lat - b.min_lat);
  const s = Math.min(sx, sy);
  
  const ox = PAD + ((W - PAD * 2) - (b.max_lon - b.min_lon) * s) / 2;
  const oy = PAD + ((H - PAD * 2) - (b.max_lat - b.min_lat) * s) / 2;

  // Project base nodes
  SANGLI_DATA.nodes.forEach(n => {{
    n.px = ox + (n.lon - b.min_lon) * s;
    n.py = H - (oy + (n.lat - b.min_lat) * s);
  }});

  // Project restaurants
  SANGLI_DATA.restaurants.forEach(r => {{
    r.px = ox + (r.lon - b.min_lon) * s;
    r.py = H - (oy + (r.lat - b.min_lat) * s);
  }});

  // Project residents
  SANGLI_DATA.residents.forEach(h => {{
    h.px = ox + (h.lon - b.min_lon) * s;
    h.py = H - (oy + (h.lat - b.min_lat) * s);
  }});
}}

// Initialize Dropdowns
function populateDropdowns() {{
  const origSel = document.getElementById('origin-select');
  const destSel = document.getElementById('dest-select');

  origSel.innerHTML = '';
  destSel.innerHTML = '';

  // 1. Group restaurants for origin
  const restGroup = document.createElement('optgroup');
  restGroup.label = '🍽️ Restaurants in Sangli (31)';
  SANGLI_DATA.restaurants.forEach(r => {{
    const opt = document.createElement('option');
    opt.value = r.id;
    opt.textContent = `${{r.name}} (${{r.rating}}★ - ${{r.category}})`;
    restGroup.appendChild(opt);
  }});
  origSel.appendChild(restGroup);

  // Group residents by locality for destination
  const localities = {{}};
  SANGLI_DATA.residents.forEach(h => {{
    const loc = h.locality || 'Sangli';
    if (!localities[loc]) localities[loc] = [];
    localities[loc].push(h);
  }});

  Object.keys(localities).sort().forEach(loc => {{
    const grp = document.createElement('optgroup');
    grp.label = `📍 ${{loc}} (${{localities[loc].length}} societies)`;
    localities[loc].forEach(h => {{
      const opt = document.createElement('option');
      opt.value = h.id;
      opt.textContent = `${{h.name}} [${{h.type}}]`;
      grp.appendChild(opt);
    }});
    destSel.appendChild(grp);
  }});

  // Also add residents to origin options in case peer-to-peer routing is desired
  const origResGroup = document.createElement('optgroup');
  origResGroup.label = '🏡 Residential Societies (Peer-to-Peer / Errand)';
  SANGLI_DATA.residents.slice(0, 30).forEach(h => {{
    const opt = document.createElement('option');
    opt.value = h.id;
    opt.textContent = `${{h.name}} (${{h.locality}})`;
    origResGroup.appendChild(opt);
  }});
  origSel.appendChild(origResGroup);

  // Set default selection
  origSel.value = 'R_R002'; // Pride Kitchen's Hyderabadi Biryani
  destSel.value = 'H_1';    // Jawahar Housing Society
}}

// Draw Entire Map
let gRoot, gRoads, gRoute, gNodes, gResidents, gRestaurants, gLabels, gScooter;

function drawMap() {{
  svg.innerHTML = '';
  svg.setAttribute('viewBox', `0 0 ${{W}} ${{H}}`);

  gRoot = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  gRoot.setAttribute('transform', `translate(${{view.x}} ${{view.y}}) scale(${{view.k}})`);
  svg.appendChild(gRoot);

  gRoads = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  gRoute = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  gNodes = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  gResidents = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  gRestaurants = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  gLabels = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  gScooter = document.createElementNS('http://www.w3.org/2000/svg', 'g');

  gRoot.appendChild(gRoads);
  gRoot.appendChild(gRoute);
  gRoot.appendChild(gNodes);
  gRoot.appendChild(gResidents);
  gRoot.appendChild(gRestaurants);
  gRoot.appendChild(gLabels);
  gRoot.appendChild(gScooter);

  const s = 1 / view.k;

  // 1. Draw Road Segments
  if (showRoads) {{
    SANGLI_DATA.edges.forEach(e => {{
      const u = nodeById[e.u], v = nodeById[e.v];
      if (!u || !v) return;
      const st = ROAD_STYLES[e.type] || ROAD_STYLES.local;
      const ln = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      ln.setAttribute('class', 'road-path');
      ln.setAttribute('x1', u.px); ln.setAttribute('y1', u.py);
      ln.setAttribute('x2', v.px); ln.setAttribute('y2', v.py);
      ln.setAttribute('stroke', st.color);
      ln.setAttribute('stroke-width', (st.w * 0.9) * s);
      if (st.dash) ln.setAttribute('stroke-dasharray', st.dash);

      ln.addEventListener('mousemove', ev => showTip(ev, `
        <h4>${{e.name || 'Sangli Road'}}</h4>
        <div class="subtag">${{u.name}} &rarr; ${{v.name}}</div>
        <div class="tip-detail">Length: <b>${{e.km.toFixed(2)}} km</b> &middot; Class: <b>${{e.type}}</b> &middot; Speed: <b>${{e.kmph}} km/h</b></div>
      `));
      ln.addEventListener('mouseleave', hideTip);
      gRoads.appendChild(ln);
    }});
  }}

  // 2. Draw Junction Nodes
  SANGLI_DATA.nodes.forEach(n => {{
    const c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    c.setAttribute('class', 'node-circle');
    c.setAttribute('cx', n.px); c.setAttribute('cy', n.py);
    c.setAttribute('r', 2.8 * s);
    c.setAttribute('fill', '#64748b');
    c.setAttribute('stroke', 'var(--bg-surface)');
    c.setAttribute('stroke-width', 1.2 * s);

    c.addEventListener('mousemove', ev => showTip(ev, `
      <h4>${{n.name}}</h4>
      <div class="subtag">${{n.type}} &middot; ${{n.area}}</div>
      <div class="tip-detail">Degree: ${{n.deg}} roads &middot; Coords: ${{n.lat.toFixed(4)}}, ${{n.lon.toFixed(4)}}</div>
    `));
    c.addEventListener('mouseleave', hideTip);
    gNodes.appendChild(c);
  }});

  // 3. Draw 155 Residents / Housing Societies
  if (showResidents) {{
    SANGLI_DATA.residents.forEach(h => {{
      const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      g.setAttribute('class', 'resident-pin');

      const c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      c.setAttribute('cx', h.px); c.setAttribute('cy', h.py);
      c.setAttribute('r', 3.8 * s);
      c.setAttribute('fill', 'var(--resident)');
      c.setAttribute('stroke', '#ffffff');
      c.setAttribute('stroke-width', 1.2 * s);
      g.appendChild(c);

      // Hit area
      const hit = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      hit.setAttribute('cx', h.px); hit.setAttribute('cy', h.py);
      hit.setAttribute('r', 9 * s);
      hit.setAttribute('fill', 'transparent');
      g.appendChild(hit);

      g.addEventListener('mousemove', ev => showTip(ev, `
        <h4 style="color:var(--resident)">🏡 ${{h.name}}</h4>
        <div class="subtag">${{h.type}} &middot; ${{h.locality}}, ${{h.city_zone}}</div>
        <div class="tip-detail">Nearest Junction: <b>${{nodeById[h.nearest_node]?.name || h.nearest_node}}</b> (${{h.distance_to_node_km}} km)</div>
        <div style="margin-top:4px; font-size:10.5px; color:var(--primary);">👉 Click to set as Destination</div>
      `));
      g.addEventListener('mouseleave', hideTip);
      g.addEventListener('click', () => setAsDestination(h.id));
      gResidents.appendChild(g);
    }});
  }}

  // 4. Draw 31 Restaurants
  if (showRestaurants) {{
    SANGLI_DATA.restaurants.forEach(r => {{
      const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      g.setAttribute('class', 'restaurant-pin');

      const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      const rw = 9 * s, rh = 9 * s;
      rect.setAttribute('x', r.px - rw / 2); rect.setAttribute('y', r.py - rh / 2);
      rect.setAttribute('width', rw); rect.setAttribute('height', rh);
      rect.setAttribute('rx', 2 * s);
      rect.setAttribute('fill', 'var(--restaurant)');
      rect.setAttribute('stroke', '#ffffff');
      rect.setAttribute('stroke-width', 1.4 * s);
      g.appendChild(rect);

      // Hit area
      const hit = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      hit.setAttribute('cx', r.px); hit.setAttribute('cy', r.py);
      hit.setAttribute('r', 10 * s);
      hit.setAttribute('fill', 'transparent');
      g.appendChild(hit);

      g.addEventListener('mousemove', ev => showTip(ev, `
        <h4 style="color:var(--restaurant)">🍽️ ${{r.name}}</h4>
        <div class="subtag">${{r.category}} &middot; ⭐ ${{r.rating}} (${{r.reviews}} reviews)</div>
        <div class="tip-detail">${{r.address}}</div>
        <div class="tip-detail" style="margin-top:2px;">Nearest Junction: <b>${{nodeById[r.nearest_node]?.name || r.nearest_node}}</b> (${{r.distance_to_node_km}} km)</div>
        <div style="margin-top:4px; font-size:10.5px; color:var(--primary);">👉 Click to set as Origin</div>
      `));
      g.addEventListener('mouseleave', hideTip);
      g.addEventListener('click', () => setAsOrigin(r.id));
      gRestaurants.appendChild(g);
    }});
  }}

  // 5. Draw Key Labels
  if (showLabels) {{
    SANGLI_DATA.nodes.filter(n => n.label).forEach(n => {{
      const t = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      t.setAttribute('x', n.px + 7 * s);
      t.setAttribute('y', n.py - 4 * s);
      t.setAttribute('font-size', (8.5 * s) + 'px');
      t.setAttribute('font-weight', '600');
      t.setAttribute('fill', 'var(--text-main)');
      t.setAttribute('stroke', 'var(--bg-base)');
      t.setAttribute('stroke-width', (2.5 * s) + 'px');
      t.setAttribute('paint-order', 'stroke');
      t.textContent = n.name;
      gLabels.appendChild(t);
    }});
  }}

  // Redraw active route if present
  if (currentRoute) {{
    renderRoute(currentRoute);
  }}
}}

// Dijkstra Algorithm on client-side
function dijkstra(startId, endId, criterion, trafficMult, floodHazard) {{
  const adj = {{}};
  SANGLI_DATA.nodes.forEach(n => adj[n.id] = []);

  const floodBridges = new Set([
    'irwin_bridge_sangliwadi', 'sangliwadi_irwin_bridge',
    'south_bridge_sangliwadi_east', 'sangliwadi_east_south_bridge'
  ]);

  SANGLI_DATA.edges.forEach(e => {{
    let weight = (criterion === 'time')
      ? (e.km / (e.kmph / trafficMult)) * 60.0
      : e.km;

    const edgeKey1 = `${{e.u}}_${{e.v}}`;
    const edgeKey2 = `${{e.v}}_${{e.u}}`;
    if (floodHazard && (floodBridges.has(edgeKey1) || floodBridges.has(edgeKey2) || e.type === 'bridge')) {{
      weight *= 1000.0;
    }}

    adj[e.u].push({{ to: e.v, weight: weight, km: e.km, kmph: e.kmph / trafficMult, type: e.type, name: e.name }});
    adj[e.v].push({{ to: e.u, weight: weight, km: e.km, kmph: e.kmph / trafficMult, type: e.type, name: e.name }});
  }});

  const dist = {{}};
  const prev = {{}};
  const edgeUsed = {{}};
  const q = new Set();

  SANGLI_DATA.nodes.forEach(n => {{
    dist[n.id] = Infinity;
    prev[n.id] = null;
    edgeUsed[n.id] = null;
    q.add(n.id);
  }});

  dist[startId] = 0;

  while (q.size > 0) {{
    let u = null;
    let minD = Infinity;
    q.forEach(node => {{
      if (dist[node] < minD) {{
        minD = dist[node];
        u = node;
      }}
    }});

    if (u === null || dist[u] === Infinity || u === endId) break;
    q.delete(u);

    adj[u].forEach(edge => {{
      const v = edge.to;
      if (q.has(v)) {{
        const alt = dist[u] + edge.weight;
        if (alt < dist[v]) {{
          dist[v] = alt;
          prev[v] = u;
          edgeUsed[v] = edge;
        }}
      }}
    }});
  }}

  if (dist[endId] === Infinity) return null;

  const path = [];
  const segments = [];
  let curr = endId;
  while (curr !== null) {{
    path.unshift(curr);
    if (prev[curr]) {{
      segments.unshift(edgeUsed[curr]);
    }}
    curr = prev[curr];
  }}

  return {{ path, segments }};
}}

// Calculate Complete Route
function calculateRoute() {{
  const origId = document.getElementById('origin-select').value;
  const destId = document.getElementById('dest-select').value;
  const trafficKey = document.getElementById('traffic-select').value;

  const trafficMults = {{
    normal: 1.0,
    lunch_peak: 1.35,
    dinner_peak: 1.50,
    rain: 1.40
  }};
  const tMult = trafficMults[trafficKey] || 1.0;

  const orig = restById[origId] || resById[origId] || nodeById[origId];
  const dest = resById[destId] || restById[destId] || nodeById[destId];

  if (!orig || !dest) return;

  const startNode = orig.nearest_node || orig.id;
  const endNode = dest.nearest_node || dest.id;

  let netPath = [startNode];
  let segments = [];

  if (startNode !== endNode) {{
    const res = dijkstra(startNode, endNode, currentCriterion, tMult, floodHazardActive);
    if (!res) {{
      alert('No accessible route found with current constraints (e.g. bridge flood closures).');
      return;
    }}
    netPath = res.path;
    segments = res.segments;
  }}

  // Distance and Driving Time Calculation
  let networkKm = 0;
  let networkTime = 0;
  const roadClassKm = {{ highway: 0, arterial: 0, main: 0, local: 0, bridge: 0 }};

  segments.forEach(s => {{
    networkKm += s.km;
    const segTime = (s.km / s.kmph) * 60;
    networkTime += segTime;
    roadClassKm[s.type] = (roadClassKm[s.type] || 0) + s.km;
  }});

  // Pickup leg (Origin to nearest start node)
  const pickupDist = orig.distance_to_node_km || 0;
  const pickupTime = (pickupDist / (18 / tMult)) * 60;

  // Dropoff leg (end node to Destination)
  const dropoffDist = dest.distance_to_node_km || 0;
  const dropoffTime = (dropoffDist / (18 / tMult)) * 60;

  const totalKm = pickupDist + networkKm + dropoffDist;
  const totalDrivingMins = pickupTime + networkTime + dropoffTime;

  // Kitchen preparation time
  let prepMins = 0;
  if (orig.category) {{
    const cat = orig.category.toLowerCase();
    if (cat.includes('biryani')) prepMins = 18;
    else if (cat.includes('pizza')) prepMins = 16;
    else if (cat.includes('south') || cat.includes('cafe')) prepMins = 10;
    else if (cat.includes('veg') || cat.includes('thali')) prepMins = 12;
    else prepMins = 15;
  }}

  const handoffMins = 3.0;
  const totalEtaMins = prepMins + totalDrivingMins + handoffMins;

  currentRoute = {{
    origin: orig,
    destination: dest,
    path: netPath,
    segments: segments,
    pickupDist,
    pickupTime,
    dropoffDist,
    dropoffTime,
    networkKm,
    totalKm,
    drivingMins: totalDrivingMins,
    prepMins,
    totalEtaMins,
    roadClassKm
  }};

  updateResultsUI(currentRoute);
  renderRoute(currentRoute);
}}

function updateResultsUI(r) {{
  document.getElementById('metric-dist').textContent = r.totalKm.toFixed(2) + ' km';
  document.getElementById('metric-travel').textContent = r.drivingMins.toFixed(1) + ' min';
  document.getElementById('metric-prep').textContent = r.prepMins + ' min';
  document.getElementById('metric-eta').textContent = r.totalEtaMins.toFixed(1) + ' min';

  const avgKmph = r.drivingMins > 0 ? (r.totalKm / (r.drivingMins / 60)) : 0;
  document.getElementById('speed-stat').textContent = `Avg ${{avgKmph.toFixed(1)}} km/h`;

  // Road breakdown bar
  const totalRoad = r.networkKm || 1;
  const artP = ((r.roadClassKm.arterial + r.roadClassKm.highway) / totalRoad * 100).toFixed(0);
  const mainP = (r.roadClassKm.main / totalRoad * 100).toFixed(0);
  const localP = (r.roadClassKm.local / totalRoad * 100).toFixed(0);

  document.getElementById('road-bars').innerHTML = `
    <div class="bar-seg" style="width:${{artP}}%; background:var(--road-arterial);" title="Arterial/Highway: ${{artP}}%"></div>
    <div class="bar-seg" style="width:${{mainP}}%; background:var(--road-main);" title="Main Roads: ${{mainP}}%"></div>
    <div class="bar-seg" style="width:${{localP}}%; background:var(--road-local);" title="Local Roads: ${{localP}}%"></div>
  `;

  // Navigation Steps
  let html = '';
  let stepNum = 1;

  if (r.pickupDist > 0) {{
    html += `
      <div class="timeline-step">
        <div class="step-icon">1</div>
        <div class="step-content">
          <div class="step-title">Pickup from ${{r.origin.name}}</div>
          <div class="step-desc">Depart origin &rarr; connect to ${{nodeById[r.path[0]]?.name}} (${{r.pickupDist.toFixed(2)}} km, ${{r.pickupTime.toFixed(1)}} min)</div>
        </div>
      </div>`;
    stepNum++;
  }}

  r.segments.forEach((seg, i) => {{
    const uName = nodeById[r.path[i]]?.name;
    const vName = nodeById[r.path[i+1]]?.name;
    const time = (seg.km / seg.kmph) * 60;
    html += `
      <div class="timeline-step">
        <div class="step-icon">${{stepNum}}</div>
        <div class="step-content">
          <div class="step-title">${{seg.name || 'Road to ' + vName}}</div>
          <div class="step-desc">${{uName}} &rarr; ${{vName}} &middot; ${{seg.km.toFixed(2)}} km at ${{seg.kmph.toFixed(0)}} km/h (${{time.toFixed(1)}} min)</div>
        </div>
      </div>`;
    stepNum++;
  }});

  if (r.dropoffDist > 0) {{
    html += `
      <div class="timeline-step">
        <div class="step-icon">${{stepNum}}</div>
        <div class="step-content">
          <div class="step-title">Final approach to ${{r.destination.name}}</div>
          <div class="step-desc">${{nodeById[r.path[r.path.length-1]]?.name}} &rarr; doorstep handoff (${{r.dropoffDist.toFixed(2)}} km, ${{r.dropoffTime.toFixed(1)}} min)</div>
        </div>
      </div>`;
  }}

  document.getElementById('timeline').innerHTML = html;
}}

// Visual Route Highlight on SVG Map
function renderRoute(r) {{
  gRoute.innerHTML = '';
  const s = 1 / view.k;

  const points = [];

  // Start point
  points.push({{ px: r.origin.px, py: r.origin.py }});

  // Network path
  r.path.forEach(nId => {{
    const n = nodeById[nId];
    if (n) points.push({{ px: n.px, py: n.py }});
  }});

  // End point
  points.push({{ px: r.destination.px, py: r.destination.py }});

  // 1. Draw connecting polyline
  const dStr = points.map((pt, i) => (i === 0 ? 'M' : 'L') + `${{pt.px}},${{pt.py}}`).join(' ');

  // Glow line
  const glow = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  glow.setAttribute('d', dStr);
  glow.setAttribute('class', 'route-glow');
  glow.setAttribute('stroke-width', 10 * s);
  gRoute.appendChild(glow);

  // Active dashed animated route
  const active = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  active.setAttribute('d', dStr);
  active.setAttribute('class', 'route-active');
  active.setAttribute('stroke-width', 3.5 * s);
  gRoute.appendChild(active);

  // Start marker (Origin)
  const startCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
  startCircle.setAttribute('cx', r.origin.px);
  startCircle.setAttribute('cy', r.origin.py);
  startCircle.setAttribute('r', 7 * s);
  startCircle.setAttribute('fill', 'var(--restaurant)');
  startCircle.setAttribute('stroke', '#ffffff');
  startCircle.setAttribute('stroke-width', 2.5 * s);
  startCircle.setAttribute('class', 'pulse-pin');
  gRoute.appendChild(startCircle);

  // End marker (Destination)
  const endCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
  endCircle.setAttribute('cx', r.destination.px);
  endCircle.setAttribute('cy', r.destination.py);
  endCircle.setAttribute('r', 7 * s);
  endCircle.setAttribute('fill', 'var(--resident)');
  endCircle.setAttribute('stroke', '#ffffff');
  endCircle.setAttribute('stroke-width', 2.5 * s);
  endCircle.setAttribute('class', 'pulse-pin');
  gRoute.appendChild(endCircle);
}}

// Delivery Scooter Animation
function simulateDelivery() {{
  if (!currentRoute) calculateRoute();
  if (!currentRoute) return;

  if (animTimer) clearInterval(animTimer);
  gScooter.innerHTML = '';

  const s = 1 / view.k;

  const points = [];
  points.push({{ px: currentRoute.origin.px, py: currentRoute.origin.py }});
  currentRoute.path.forEach(nId => {{
    const n = nodeById[nId];
    if (n) points.push({{ px: n.px, py: n.py }});
  }});
  points.push({{ px: currentRoute.destination.px, py: currentRoute.destination.py }});

  // Calculate segment lengths
  const segLens = [];
  let totalLen = 0;
  for (let i = 0; i < points.length - 1; i++) {{
    const dx = points[i+1].px - points[i].px;
    const dy = points[i+1].py - points[i].py;
    const dist = Math.sqrt(dx * dx + dy * dy);
    segLens.push(dist);
    totalLen += dist;
  }}

  // Scooter marker
  const scooter = document.createElementNS('http://www.w3.org/2000/svg', 'text');
  scooter.setAttribute('id', 'delivery-rider');
  scooter.setAttribute('text-anchor', 'middle');
  scooter.setAttribute('dominant-baseline', 'central');
  scooter.style.fontSize = (18 * s) + 'px';
  scooter.textContent = '🛵';
  gScooter.appendChild(scooter);

  let progress = 0;
  const stepFrac = 0.005;

  animTimer = setInterval(() => {{
    progress += stepFrac;
    if (progress >= 1) {{
      progress = 1;
      clearInterval(animTimer);
    }}

    const targetDist = progress * totalLen;
    let curDist = 0;
    let pos = points[0];

    for (let i = 0; i < segLens.length; i++) {{
      if (curDist + segLens[i] >= targetDist) {{
        const rem = targetDist - curDist;
        const frac = rem / segLens[i];
        pos = {{
          px: points[i].px + (points[i+1].px - points[i].px) * frac,
          py: points[i].py + (points[i+1].py - points[i].py) * frac
        }};
        break;
      }}
      curDist += segLens[i];
    }}

    scooter.setAttribute('x', pos.px);
    scooter.setAttribute('y', pos.py);
  }}, 25);
}}

// User Interaction Helpers
function setAsOrigin(id) {{
  document.getElementById('origin-select').value = id;
  calculateRoute();
}}

function setAsDestination(id) {{
  document.getElementById('dest-select').value = id;
  calculateRoute();
}}

function swapLocations() {{
  const oSel = document.getElementById('origin-select');
  const dSel = document.getElementById('dest-select');
  const temp = oSel.value;
  oSel.value = dSel.value;
  dSel.value = temp;
  calculateRoute();
}}

function setCriterion(c) {{
  currentCriterion = c;
  document.getElementById('btn-opt-time').classList.toggle('active', c === 'time');
  document.getElementById('btn-opt-dist').classList.toggle('active', c === 'distance');
  calculateRoute();
}}

function toggleHazard() {{
  floodHazardActive = !floodHazardActive;
  document.getElementById('hazard-toggle').classList.toggle('active', floodHazardActive);
  calculateRoute();
}}

function toggleLayer(layer) {{
  if (layer === 'restaurants') {{
    showRestaurants = !showRestaurants;
    document.getElementById('chip-rest').classList.toggle('off', !showRestaurants);
  }} else if (layer === 'residents') {{
    showResidents = !showResidents;
    document.getElementById('chip-res').classList.toggle('off', !showResidents);
  }} else if (layer === 'roads') {{
    showRoads = !showRoads;
    document.getElementById('chip-roads').classList.toggle('off', !showRoads);
  }} else if (layer === 'labels') {{
    showLabels = !showLabels;
    document.getElementById('chip-labels').classList.toggle('off', !showLabels);
  }}
  drawMap();
}}

function toggleTheme() {{
  const isDark = document.body.getAttribute('data-theme') === 'dark';
  document.body.setAttribute('data-theme', isDark ? 'light' : 'dark');
  document.getElementById('btn-theme').textContent = isDark ? '🌙 Dark Mode' : '☀️ Light Mode';
}}

function onSelectionChange() {{
  calculateRoute();
}}

// Tooltip display
function showTip(ev, html) {{
  tooltip.innerHTML = html;
  tooltip.style.opacity = 1;
  const rect = tooltip.getBoundingClientRect();
  let x = ev.clientX + 14;
  let y = ev.clientY + 14;
  if (x + rect.width > window.innerWidth - 10) x = ev.clientX - rect.width - 14;
  if (y + rect.height > window.innerHeight - 10) y = ev.clientY - rect.height - 14;
  tooltip.style.left = x + 'px';
  tooltip.style.top = y + 'px';
}}
function hideTip() {{ tooltip.style.opacity = 0; }}

// Pan & Zoom handlers
svg.addEventListener('pointerdown', e => {{
  isDragging = true;
  dragStart = [e.clientX, e.clientY];
  svg.classList.add('dragging');
  svg.setPointerCapture(e.pointerId);
}});

svg.addEventListener('pointermove', e => {{
  if (!isDragging) return;
  const sc = W / svg.getBoundingClientRect().width;
  view.x += (e.clientX - dragStart[0]) * sc;
  view.y += (e.clientY - dragStart[1]) * sc;
  dragStart = [e.clientX, e.clientY];
  gRoot.setAttribute('transform', `translate(${{view.x}} ${{view.y}}) scale(${{view.k}})`);
}});

svg.addEventListener('pointerup', e => {{
  isDragging = false;
  svg.classList.remove('dragging');
}});

svg.addEventListener('wheel', e => {{
  e.preventDefault();
  const box = svg.getBoundingClientRect();
  const sc = W / box.width;
  const mx = (e.clientX - box.left) * sc;
  const my = (e.clientY - box.top) * sc;
  const factor = e.deltaY < 0 ? 1.15 : 1 / 1.15;
  const newK = Math.min(12, Math.max(0.6, view.k * factor));
  view.x = mx - (mx - view.x) * (newK / view.k);
  view.y = my - (my - view.y) * (newK / view.k);
  view.k = newK;
  drawMap();
}}, {{ passive: false }});

function zoomIn() {{
  view.k = Math.min(12, view.k * 1.25);
  drawMap();
}}

function zoomOut() {{
  view.k = Math.max(0.6, view.k / 1.25);
  drawMap();
}}

function resetZoom() {{
  view = {{ x: 0, y: 0, k: 1 }};
  drawMap();
}}

// Initialize Application
projectCoordinates();
populateDropdowns();
drawMap();
calculateRoute();

window.addEventListener('resize', () => drawMap());
</script>
</body>
</html>
"""

    with open('route_optimizer.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Successfully built route_optimizer.html and index.html!")

if __name__ == '__main__':
    generate_html()
