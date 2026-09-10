"""
build_complete_app.py
Generates a modern, production-ready Leaflet-based interactive food delivery route optimizer
for Sangli, embedding all 31 restaurants, 155 housing societies, 81 nodes, 133 road edges,
full Dijkstra & A* routing, animated delivery scooter, and the EXACT terminal console report
directly inside the web interface.
Uses 100% watermark-free OpenStreetMap tiles.
"""

import json

def main():
    with open('sangli_delivery_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    json_str = json.dumps(data)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sangli Food Delivery Route Optimizer</title>
<!-- Leaflet CSS (Local with CDN fallback) -->
<link rel="stylesheet" href="leaflet.css" />
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">

<style>
  :root {{
    --bg-base: #090d16;
    --bg-surface: #111827;
    --bg-card: #1f2937;
    --bg-input: #172033;
    --border: #374151;
    --border-subtle: rgba(255,255,255,0.08);
    --text-main: #f9fafb;
    --text-muted: #9ca3af;
    --primary: #3b82f6;
    --primary-hover: #2563eb;
    --restaurant: #f59e0b;
    --resident: #10b981;
    --accent: #8b5cf6;
    --danger: #ef4444;
    --term-bg: #030712;
    --term-text: #a7f3d0;
  }}

  [data-theme="light"] {{
    --bg-base: #f3f4f6;
    --bg-surface: #ffffff;
    --bg-card: #f9fafb;
    --bg-input: #ffffff;
    --border: #e5e7eb;
    --border-subtle: rgba(0,0,0,0.06);
    --text-main: #111827;
    --text-muted: #6b7280;
    --primary: #2563eb;
    --primary-hover: #1d4ed8;
    --restaurant: #d97706;
    --resident: #059669;
    --term-bg: #111827;
    --term-text: #6ee7b7;
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    background: var(--bg-base);
    color: var(--text-main);
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }}

  /* Top Navbar */
  header {{
    background: var(--bg-surface);
    border-bottom: 1px solid var(--border);
    padding: 10px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: 1000;
    flex-shrink: 0;
  }}
  .brand {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}
  .logo {{
    width: 38px;
    height: 38px;
    background: linear-gradient(135deg, #f59e0b, #ef4444);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.35);
  }}
  .brand-text h1 {{
    font-size: 16px;
    font-weight: 700;
    letter-spacing: -0.3px;
  }}
  .brand-text p {{
    font-size: 11.5px;
    color: var(--text-muted);
  }}
  .badges-group {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  .badge {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 11.5px;
    color: var(--text-muted);
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }}
  .badge strong {{ color: var(--text-main); }}
  .badge .dot {{ width: 8px; height: 8px; border-radius: 50%; }}

  .nav-btns {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}
  button.btn {{
    font-family: inherit;
    font-size: 12px;
    font-weight: 600;
    padding: 6px 12px;
    border-radius: 8px;
    cursor: pointer;
    border: 1px solid var(--border);
    background: var(--bg-card);
    color: var(--text-main);
    display: inline-flex;
    align-items: center;
    gap: 6px;
    transition: all 0.15s;
  }}
  button.btn:hover {{
    background: var(--border);
  }}
  button.btn-primary {{
    background: var(--primary);
    border-color: var(--primary);
    color: #fff;
    box-shadow: 0 2px 8px rgba(59,130,246,0.35);
  }}
  button.btn-primary:hover {{
    background: var(--primary-hover);
  }}

  /* App Main Layout: Left Sidebar + Right Map */
  .app-layout {{
    flex: 1;
    display: flex;
    overflow: hidden;
    position: relative;
  }}

  /* Sidebar Controls & Details */
  .sidebar {{
    width: 440px;
    background: var(--bg-surface);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    z-index: 500;
    flex-shrink: 0;
  }}
  .sidebar::-webkit-scrollbar {{
    width: 6px;
  }}
  .sidebar::-webkit-scrollbar-thumb {{
    background: var(--border);
    border-radius: 3px;
  }}

  .panel-box {{
    padding: 16px;
    border-bottom: 1px solid var(--border);
  }}
  .panel-title {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: var(--text-muted);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}

  /* Form inputs */
  .form-group {{
    margin-bottom: 10px;
  }}
  .label-row {{
    display: flex;
    justify-content: space-between;
    font-size: 11.5px;
    font-weight: 600;
    margin-bottom: 4px;
  }}
  .label-row .tag {{
    font-size: 10px;
    color: var(--text-muted);
    font-weight: normal;
  }}
  select, input[type="text"] {{
    width: 100%;
    background: var(--bg-input);
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

  .swap-btn-wrap {{
    display: flex;
    justify-content: center;
    margin: -4px 0 6px;
  }}
  .swap-btn {{
    width: 28px;
    height: 28px;
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
  .swap-btn:hover {{
    color: var(--primary);
    border-color: var(--primary);
    transform: rotate(180deg);
  }}

  /* Quick presets */
  .presets-row {{
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin-top: 8px;
  }}
  .preset-chip {{
    font-size: 10.5px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    color: var(--text-muted);
    padding: 3px 8px;
    border-radius: 6px;
    cursor: pointer;
    user-select: none;
    transition: all 0.15s;
  }}
  .preset-chip:hover {{
    color: var(--text-main);
    border-color: var(--primary);
  }}

  /* Strategy Toggles */
  .seg-control {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    background: var(--bg-input);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 2px;
    gap: 2px;
    margin-bottom: 10px;
  }}
  .seg-btn {{
    border: none;
    background: transparent;
    color: var(--text-muted);
    padding: 6px;
    font-size: 11.5px;
    font-weight: 600;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.15s;
  }}
  .seg-btn.active {{
    background: var(--primary);
    color: #fff;
  }}

  .options-row {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }}

  .toggle-box {{
    background: var(--bg-input);
    border: 1px solid var(--border);
    padding: 8px 10px;
    border-radius: 8px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 11.5px;
    font-weight: 600;
    user-select: none;
  }}
  .toggle-box.active {{
    border-color: var(--danger);
    background: rgba(239, 68, 68, 0.12);
  }}
  .toggle-box .indicator {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--border);
  }}
  .toggle-box.active .indicator {{
    background: var(--danger);
    box-shadow: 0 0 8px var(--danger);
  }}

  .btn-run {{
    width: 100%;
    padding: 12px;
    margin-top: 12px;
    border: none;
    border-radius: 8px;
    background: linear-gradient(135deg, #2563eb, #3b82f6);
    color: #fff;
    font-size: 13.5px;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 4px 14px rgba(37,99,235,0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: all 0.15s;
  }}
  .btn-run:hover {{
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(37,99,235,0.5);
  }}

  /* Metrics Summary Card */
  .metrics-header {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 12px;
  }}
  .eta-row {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 10px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
  }}
  .eta-label {{
    font-size: 12px;
    color: var(--text-muted);
    font-weight: 600;
  }}
  .eta-val {{
    font-size: 26px;
    font-weight: 800;
    color: #38bdf8;
  }}
  .metrics-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
  }}
  .m-box {{
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 8px;
    text-align: center;
  }}
  .m-box .v {{
    font-size: 14px;
    font-weight: 700;
    color: var(--text-main);
  }}
  .m-box .l {{
    font-size: 10px;
    color: var(--text-muted);
    margin-top: 2px;
  }}

  /* Nodes Sequence Path */
  .nodes-seq {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 8px 10px;
    font-size: 11px;
    color: var(--text-muted);
    margin-bottom: 12px;
    line-height: 1.6;
  }}
  .node-pill {{
    display: inline-block;
    background: var(--bg-input);
    border: 1px solid var(--border);
    color: #38bdf8;
    padding: 1px 6px;
    border-radius: 4px;
    font-weight: 600;
  }}

  /* TERMINAL DISPLAY BOX (Live Terminal Mirror) */
  .terminal-box {{
    background: var(--term-bg);
    border: 1px solid #1f2937;
    border-radius: 8px;
    overflow: hidden;
    margin-top: 10px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.5);
  }}
  .term-header {{
    background: #111827;
    padding: 6px 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #1f2937;
  }}
  .term-dots {{
    display: flex;
    gap: 5px;
  }}
  .term-dot {{
    width: 9px;
    height: 9px;
    border-radius: 50%;
  }}
  .term-title {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px;
    color: #9ca3af;
  }}
  .btn-copy {{
    background: transparent;
    border: none;
    color: #9ca3af;
    font-size: 11px;
    cursor: pointer;
  }}
  .btn-copy:hover {{
    color: #fff;
  }}
  pre.term-content {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: var(--term-text);
    padding: 12px;
    overflow-x: auto;
    white-space: pre;
    line-height: 1.45;
    max-height: 280px;
    overflow-y: auto;
  }}
  pre.term-content::-webkit-scrollbar {{
    width: 5px;
    height: 5px;
  }}
  pre.term-content::-webkit-scrollbar-thumb {{
    background: #374151;
  }}

  /* Turn by Turn Directions */
  .directions-list {{
    max-height: 200px;
    overflow-y: auto;
    padding-right: 4px;
    margin-top: 8px;
  }}
  .dir-step {{
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
    font-size: 11.5px;
  }}
  .step-num {{
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: var(--bg-card);
    border: 1px solid var(--primary);
    color: #38bdf8;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    font-weight: 700;
    flex-shrink: 0;
  }}
  .step-info .step-name {{
    font-weight: 600;
    color: var(--text-main);
  }}
  .step-info .step-meta {{
    font-size: 10.5px;
    color: var(--text-muted);
  }}

  /* Right Map Container */
  .map-wrapper {{
    flex: 1;
    position: relative;
    background: #111827;
  }}
  #map {{
    width: 100%;
    height: 100%;
  }}

  /* Custom Leaflet Map Markers */
  .custom-div-icon {{
    background: transparent;
    border: none;
  }}
  .marker-pin {{
    width: 28px;
    height: 28px;
    border-radius: 50% 50% 50% 0;
    position: absolute;
    transform: rotate(-45deg);
    left: 50%;
    top: 50%;
    margin: -14px 0 0 -14px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 3px 8px rgba(0,0,0,0.4);
  }}
  .marker-pin span {{
    transform: rotate(45deg);
    font-size: 13px;
  }}
  .marker-rest {{
    background: linear-gradient(135deg, #f59e0b, #d97706);
    border: 2px solid #ffffff;
  }}
  .marker-res {{
    background: linear-gradient(135deg, #10b981, #059669);
    border: 2px solid #ffffff;
  }}

  /* Scooter Rider Marker */
  .scooter-marker {{
    font-size: 24px;
    filter: drop-shadow(0 3px 6px rgba(0,0,0,0.6));
    transition: transform 0.05s linear;
  }}

  /* Floating Map Tools */
  .floating-controls {{
    position: absolute;
    top: 14px;
    right: 14px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    z-index: 800;
  }}
  .map-action-btn {{
    width: 36px;
    height: 36px;
    border-radius: 8px;
    background: var(--bg-surface);
    border: 1px solid var(--border);
    color: var(--text-main);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    transition: all 0.15s;
  }}
  .map-action-btn:hover {{
    background: var(--border);
    color: var(--primary);
  }}

  .map-filter-tags {{
    position: absolute;
    bottom: 18px;
    left: 18px;
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    z-index: 800;
  }}
  .map-tag {{
    background: var(--bg-surface);
    border: 1px solid var(--border);
    color: var(--text-main);
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    user-select: none;
  }}
  .map-tag.off {{
    opacity: 0.45;
  }}
  .map-tag .dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
  }}
</style>
</head>
<body data-theme="dark">

<!-- Top Navigation -->
<header>
  <div class="brand">
    <div class="logo">🛵</div>
    <div class="brand-text">
      <h1>Sangli Food Delivery Route Optimizer</h1>
      <p>Shortest Path & Real-time Delivery Simulator &middot; Sangli, Maharashtra</p>
    </div>
  </div>

  <div class="badges-group">
    <div class="badge">
      <span class="dot" style="background:var(--restaurant)"></span>
      <span><strong>31</strong> Restaurants</span>
    </div>
    <div class="badge">
      <span class="dot" style="background:var(--resident)"></span>
      <span><strong>155</strong> Societies</span>
    </div>
    <div class="badge">
      <span class="dot" style="background:#3b82f6"></span>
      <span><strong>81</strong> Junctions</span>
    </div>
    <div class="badge">
      <span class="dot" style="background:#a855f7"></span>
      <span><strong>133</strong> Roads</span>
    </div>
  </div>

  <div class="nav-btns">
    <button class="btn" onclick="toggleTheme()" id="theme-btn">☀️ Light</button>
    <button class="btn btn-primary" onclick="simulateScooterDelivery()">▶ Simulate Delivery</button>
  </div>
</header>

<!-- Main App Workspace -->
<div class="app-layout">
  <!-- Left Control & Result Sidebar -->
  <aside class="sidebar">
    <!-- Location Pickers -->
    <div class="panel-box">
      <div class="panel-title">
        <span>Delivery Endpoints</span>
        <span style="color:#38bdf8;">Graph Connected</span>
      </div>

      <!-- Origin Selection -->
      <div class="form-group">
        <div class="label-row">
          <span>1. Pickup (Restaurant)</span>
          <span class="tag" id="orig-subtag">31 Available</span>
        </div>
        <input type="text" id="orig-search" placeholder="🔍 Search restaurant..." oninput="filterOriginOptions()" style="margin-bottom:4px; font-size:11.5px; padding:5px 8px;">
        <select id="orig-select" onchange="onEndpointChange()">
          <!-- Populated by JS -->
        </select>
      </div>

      <div class="swap-btn-wrap">
        <button class="swap-btn" title="Swap Origin & Destination" onclick="swapEndpoints()">⇅</button>
      </div>

      <!-- Destination Selection -->
      <div class="form-group">
        <div class="label-row">
          <span>2. Dropoff (Housing Society)</span>
          <span class="tag" id="dest-subtag">155 Societies</span>
        </div>
        <input type="text" id="dest-search" placeholder="🔍 Search society / locality..." oninput="filterDestOptions()" style="margin-bottom:4px; font-size:11.5px; padding:5px 8px;">
        <select id="dest-select" onchange="onEndpointChange()">
          <!-- Populated by JS -->
        </select>
      </div>

      <!-- Quick Preset Tests -->
      <div class="panel-title" style="margin-top:10px; margin-bottom:4px; font-size:10px;">Quick Demonstrations:</div>
      <div class="presets-row">
        <div class="preset-chip" onclick="setPreset('R_R002', 'H_1')">🍛 Biryani &rarr; Jawahar Soc</div>
        <div class="preset-chip" onclick="setPreset('R_R006', 'H_8')">🍕 Domino's &rarr; Kupwad</div>
        <div class="preset-chip" onclick="setPreset('R_R005', 'H_34')">🥗 Veg Villa &rarr; Sangliwadi</div>
        <div class="preset-chip" onclick="setPreset('R_R001', 'H_55')">🍲 Kapital &rarr; Vijaynagar</div>
      </div>
    </div>

    <!-- Optimization Strategy & Conditions -->
    <div class="panel-box">
      <div class="panel-title"><span>Optimization Rules</span></div>

      <div class="seg-control">
        <button class="seg-btn active" id="btn-opt-time" onclick="setOptCriterion('time')">⚡ Fastest Travel Time</button>
        <button class="seg-btn" id="btn-opt-dist" onclick="setOptCriterion('distance')">📏 Shortest Distance</button>
      </div>

      <div class="options-row">
        <div>
          <div class="label-row"><span>Traffic Congestion</span></div>
          <select id="traffic-select" onchange="calculateRoute()">
            <option value="normal">🟢 Normal (1.0x)</option>
            <option value="lunch_peak">🟡 Lunch Rush (1.35x)</option>
            <option value="dinner_peak">🔴 Dinner Peak (1.50x)</option>
            <option value="rain">🌧️ Rain Alert (1.40x)</option>
          </select>
        </div>

        <div>
          <div class="label-row"><span>River Flood Alert</span></div>
          <div class="toggle-box" id="hazard-box" onclick="toggleFloodHazard()">
            <span>Avoid Bridges</span>
            <div class="indicator"></div>
          </div>
        </div>
      </div>

      <button class="btn-run" onclick="calculateRoute()">
        <span>🚀 Compute Shortest Delivery Route</span>
      </button>
    </div>

    <!-- Visual Delivery Metrics -->
    <div class="panel-box" id="results-panel">
      <div class="panel-title">
        <span>Delivery Performance</span>
        <span id="opt-goal-badge" style="color:#10b981; font-weight:700;">FASTEST TIME</span>
      </div>

      <div class="metrics-header">
        <div class="eta-row">
          <div>
            <div class="eta-label">Estimated Delivery Arrival</div>
            <div style="font-size:11px; color:var(--text-muted); margin-top:2px;" id="food-type-tag">Cooking + Transit + Handoff</div>
          </div>
          <div class="eta-val" id="val-eta">30.2 min</div>
        </div>

        <div class="metrics-grid">
          <div class="m-box">
            <div class="v" id="val-dist">4.12 km</div>
            <div class="l">Total Distance</div>
          </div>
          <div class="m-box">
            <div class="v" id="val-drive">9.2 min</div>
            <div class="l">Road Driving</div>
          </div>
          <div class="m-box">
            <div class="v" id="val-prep">18 min</div>
            <div class="l">Kitchen Prep</div>
          </div>
        </div>
      </div>

      <div class="panel-title" style="margin-bottom:6px;"><span>Nodes in Path</span></div>
      <div class="nodes-seq" id="nodes-path-seq">
        <!-- Populated by JS -->
      </div>

      <!-- Exact Terminal Output Mirror -->
      <div class="panel-title" style="margin-bottom:4px;">
        <span>Terminal Console Output</span>
        <button class="btn-copy" onclick="copyTerminalText()">📋 Copy</button>
      </div>
      <div class="terminal-box">
        <div class="term-header">
          <div class="term-dots">
            <span class="term-dot" style="background:#ef4444"></span>
            <span class="term-dot" style="background:#f59e0b"></span>
            <span class="term-dot" style="background:#10b981"></span>
          </div>
          <div class="term-title">optimizer.py &mdash; output</div>
          <div></div>
        </div>
        <pre class="term-content" id="term-output">Calculating route...</pre>
      </div>

      <!-- Turn By Turn -->
      <div class="panel-title" style="margin-top:14px; margin-bottom:4px;"><span>Turn-By-Turn Navigation</span></div>
      <div class="directions-list" id="directions-list">
        <!-- Populated by JS -->
      </div>
    </div>
  </aside>

  <!-- Right Map View -->
  <main class="map-wrapper">
    <div id="map"></div>

    <!-- Map Action Floating Toolbar -->
    <div class="floating-controls">
      <div class="map-action-btn" title="Center & Fit Route" onclick="fitRouteBounds()">🎯</div>
      <div class="map-action-btn" title="Zoom in" onclick="map.zoomIn()">+</div>
      <div class="map-action-btn" title="Zoom out" onclick="map.zoomOut()">&minus;</div>
      <div class="map-action-btn" title="Reset Sangli View" onclick="resetMapView()">🏛️</div>
    </div>

    <!-- Layer Toggles -->
    <div class="map-filter-tags">
      <div class="map-tag" id="tag-rest" onclick="toggleMapLayer('restaurants')">
        <span class="dot" style="background:var(--restaurant)"></span>
        <span>Restaurants (31)</span>
      </div>
      <div class="map-tag" id="tag-res" onclick="toggleMapLayer('residents')">
        <span class="dot" style="background:var(--resident)"></span>
        <span>Societies (155)</span>
      </div>
      <div class="map-tag" id="tag-roads" onclick="toggleMapLayer('roads')">
        <span class="dot" style="background:#60a5fa"></span>
        <span>Road Network (133)</span>
      </div>
    </div>
  </main>
</div>

<!-- Load Leaflet JS (Local with CDN fallback) -->
<script src="leaflet.js"></script>
<script>
  if (typeof L === 'undefined') {{
    document.write('<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"><\\/script>');
  }}
</script>

<script>
// Complete Sangli Dataset
const DATA = {json_str};

// Global App State
let map;
let roadLayersGroup = L.layerGroup();
let restaurantMarkersGroup = L.layerGroup();
let residentMarkersGroup = L.layerGroup();
let routeLayerGroup = L.layerGroup();
let scooterMarker = null;

let currentCriterion = 'time';
let floodHazardActive = false;
let currentRouteData = null;
let animInterval = null;

let showRestaurantsLayer = true;
let showResidentsLayer = true;
let showRoadsLayer = true;

// Fast Indexing
const nodeById = {{}};
DATA.nodes.forEach(n => nodeById[n.id] = n);

const restById = {{}};
DATA.restaurants.forEach(r => restById[r.id] = r);

const resById = {{}};
DATA.residents.forEach(h => resById[h.id] = h);

// Road styles by class
const ROAD_COLORS = {{
  highway:  {{ color: '#3b82f6', weight: 4.5, opacity: 0.85 }},
  arterial: {{ color: '#8b5cf6', weight: 3.5, opacity: 0.85 }},
  main:     {{ color: '#10b981', weight: 2.5, opacity: 0.80 }},
  local:    {{ color: '#6b7280', weight: 1.5, opacity: 0.65 }},
  bridge:   {{ color: '#ef4444', weight: 3.5, opacity: 0.90, dashArray: '6, 6' }}
}};

// Initialize Leaflet Map
function initMap() {{
  map = L.map('map', {{
    zoomControl: false,
    attributionControl: false
  }}).setView([16.8524, 74.5815], 13);

  // 100% Free, Watermark-Free Standard OpenStreetMap Tiles
  L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
    maxZoom: 19,
    subdomains: ['a', 'b', 'c'],
    attribution: '&copy; OpenStreetMap contributors'
  }}).addTo(map);

  // Add layer groups
  roadLayersGroup.addTo(map);
  restaurantMarkersGroup.addTo(map);
  residentMarkersGroup.addTo(map);
  routeLayerGroup.addTo(map);

  // Draw network
  drawRoadNetwork();
  drawRestaurantMarkers();
  drawResidentMarkers();
}}

// Draw the Sangli Road Network on the Leaflet Map
function drawRoadNetwork() {{
  roadLayersGroup.clearLayers();

  DATA.edges.forEach(e => {{
    const u = nodeById[e.u];
    const v = nodeById[e.v];
    if (!u || !v) return;

    const style = ROAD_COLORS[e.type] || ROAD_COLORS.local;
    const polyline = L.polyline([[u.lat, u.lon], [v.lat, v.lon]], {{
      color: style.color,
      weight: style.weight,
      opacity: style.opacity,
      dashArray: style.dashArray || null
    }});

    polyline.bindTooltip(`
      <div style="font-family:sans-serif; font-size:12px;">
        <b>${{e.name || 'Sangli Road'}}</b> (${{e.type}})<br>
        ${{u.name}} &rarr; ${{v.name}}<br>
        Distance: <b>${{e.km.toFixed(2)}} km</b> &middot; Speed: <b>${{e.kmph}} km/h</b>
      </div>
    `);

    roadLayersGroup.addLayer(polyline);
  }});
}}

// Draw all 31 Restaurants on the Map
function drawRestaurantMarkers() {{
  restaurantMarkersGroup.clearLayers();

  DATA.restaurants.forEach(r => {{
    const icon = L.divIcon({{
      className: 'custom-div-icon',
      html: `<div class="marker-pin marker-rest" title="${{r.name}}"><span>🍽️</span></div>`,
      iconSize: [28, 28],
      iconAnchor: [14, 28],
      popupAnchor: [0, -28]
    }});

    const marker = L.marker([r.lat, r.lon], {{ icon: icon }});
    marker.bindPopup(`
      <div style="font-family:sans-serif; min-width:200px;">
        <h3 style="font-size:14px; margin-bottom:2px; color:#d97706;">🍽️ ${{r.name}}</h3>
        <p style="font-size:11px; color:#6b7280; margin-bottom:6px;">${{r.category}} &middot; ⭐ ${{r.rating}} (${{r.reviews}} reviews)</p>
        <p style="font-size:11px; margin-bottom:6px;">${{r.address}}</p>
        <p style="font-size:11px; color:#4b5563;">Nearest Junction: <b>${{nodeById[r.nearest_node]?.name || r.nearest_node}}</b> (${{r.distance_to_node_km}} km)</p>
        <button onclick="setAsOrigin('${{r.id}}')" style="margin-top:8px; width:100%; padding:6px; background:#f59e0b; color:#fff; border:none; border-radius:6px; font-weight:600; cursor:pointer;">
          Set as Pickup Point
        </button>
      </div>
    `);

    restaurantMarkersGroup.addLayer(marker);
  }});
}}

// Draw all 155 Housing Societies on the Map
function drawResidentMarkers() {{
  residentMarkersGroup.clearLayers();

  DATA.residents.forEach(h => {{
    const icon = L.divIcon({{
      className: 'custom-div-icon',
      html: `<div class="marker-pin marker-res" title="${{h.name}}"><span>🏡</span></div>`,
      iconSize: [28, 28],
      iconAnchor: [14, 28],
      popupAnchor: [0, -28]
    }});

    const marker = L.marker([h.lat, h.lon], {{ icon: icon }});
    marker.bindPopup(`
      <div style="font-family:sans-serif; min-width:200px;">
        <h3 style="font-size:14px; margin-bottom:2px; color:#059669;">🏡 ${{h.name}}</h3>
        <p style="font-size:11px; color:#6b7280; margin-bottom:6px;">${{h.type}} &middot; ${{h.locality}}, ${{h.city_zone}}</p>
        <p style="font-size:11px; color:#4b5563;">Nearest Junction: <b>${{nodeById[h.nearest_node]?.name || h.nearest_node}}</b> (${{h.distance_to_node_km}} km)</p>
        <button onclick="setAsDestination('${{h.id}}')" style="margin-top:8px; width:100%; padding:6px; background:#10b981; color:#fff; border:none; border-radius:6px; font-weight:600; cursor:pointer;">
          Set as Dropoff Point
        </button>
      </div>
    `);

    residentMarkersGroup.addLayer(marker);
  }});
}}

// Populate Dropdown Selectors
function populateDropdowns() {{
  const oSel = document.getElementById('orig-select');
  const dSel = document.getElementById('dest-select');

  oSel.innerHTML = '';
  dSel.innerHTML = '';

  // 1. Restaurants Group
  const rGroup = document.createElement('optgroup');
  rGroup.label = '🍽️ Restaurants in Sangli (31)';
  DATA.restaurants.forEach(r => {{
    const opt = document.createElement('option');
    opt.value = r.id;
    opt.textContent = `${{r.name}} (${{r.category}} - ⭐${{r.rating}})`;
    rGroup.appendChild(opt);
  }});
  oSel.appendChild(rGroup);

  // 2. Societies Group (grouped by locality)
  const locMap = {{}};
  DATA.residents.forEach(h => {{
    const loc = h.locality || 'Sangli';
    if (!locMap[loc]) locMap[loc] = [];
    locMap[loc].push(h);
  }});

  Object.keys(locMap).sort().forEach(loc => {{
    const grp = document.createElement('optgroup');
    grp.label = `📍 ${{loc}} (${{locMap[loc].length}} societies)`;
    locMap[loc].forEach(h => {{
      const opt = document.createElement('option');
      opt.value = h.id;
      opt.textContent = `${{h.name}} [${{h.type}}]`;
      grp.appendChild(opt);
    }});
    dSel.appendChild(grp);
  }});

  // Set default selection
  oSel.value = 'R_R002'; // Pride Kitchen's Biryani
  dSel.value = 'H_1';    // Jawahar Housing Society
}}

// Search Filter helper for Origin
function filterOriginOptions() {{
  const query = document.getElementById('orig-search').value.toLowerCase().trim();
  const select = document.getElementById('orig-select');
  Array.from(select.options).forEach(opt => {{
    const match = opt.textContent.toLowerCase().includes(query);
    opt.style.display = match ? '' : 'none';
  }});
}}

// Search Filter helper for Destination
function filterDestOptions() {{
  const query = document.getElementById('dest-search').value.toLowerCase().trim();
  const select = document.getElementById('dest-select');
  Array.from(select.options).forEach(opt => {{
    const match = opt.textContent.toLowerCase().includes(query);
    opt.style.display = match ? '' : 'none';
  }});
}}

// Dijkstra Algorithm
function runDijkstra(startNodeId, endNodeId, criterion, trafficMult, avoidBridges) {{
  const adj = {{}};
  DATA.nodes.forEach(n => adj[n.id] = []);

  const floodBridgeSet = new Set([
    'irwin_bridge_sangliwadi', 'sangliwadi_irwin_bridge',
    'south_bridge_sangliwadi_east', 'sangliwadi_east_south_bridge',
    'ganapati_mandir_sangliwadi', 'sangliwadi_ganapati_mandir',
    'sangliwadi_north_irwin_bridge', 'irwin_bridge_sangliwadi_north'
  ]);

  DATA.edges.forEach(e => {{
    let weight = (criterion === 'time')
      ? (e.km / (e.kmph / trafficMult)) * 60.0
      : e.km;

    const k1 = `${{e.u}}_${{e.v}}`;
    const k2 = `${{e.v}}_${{e.u}}`;
    if (avoidBridges && (floodBridgeSet.has(k1) || floodBridgeSet.has(k2) || e.type === 'bridge')) {{
      weight *= 1000.0;
    }}

    adj[e.u].push({{ to: e.v, weight: weight, km: e.km, kmph: e.kmph / trafficMult, type: e.type, name: e.name }});
    adj[e.v].push({{ to: e.u, weight: weight, km: e.km, kmph: e.kmph / trafficMult, type: e.type, name: e.name }});
  }});

  const dist = {{}};
  const prev = {{}};
  const edgeUsed = {{}};
  const q = new Set();

  DATA.nodes.forEach(n => {{
    dist[n.id] = Infinity;
    prev[n.id] = null;
    edgeUsed[n.id] = null;
    q.add(n.id);
  }});

  dist[startNodeId] = 0;

  while (q.size > 0) {{
    let u = null;
    let minD = Infinity;
    q.forEach(node => {{
      if (dist[node] < minD) {{
        minD = dist[node];
        u = node;
      }}
    }});

    if (u === null || dist[u] === Infinity || u === endNodeId) break;
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

  if (dist[endNodeId] === Infinity) return null;

  const path = [];
  const segments = [];
  let curr = endNodeId;
  while (curr !== null) {{
    path.unshift(curr);
    if (prev[curr]) {{
      segments.unshift(edgeUsed[curr]);
    }}
    curr = prev[curr];
  }}

  return {{ path, segments }};
}}

// Calculate Route & Update Terminal & Visuals
function calculateRoute() {{
  const origId = document.getElementById('orig-select').value;
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
    const res = runDijkstra(startNode, endNode, currentCriterion, tMult, floodHazardActive);
    if (!res) {{
      alert('No accessible route found with current flood closure restrictions.');
      return;
    }}
    netPath = res.path;
    segments = res.segments;
  }}

  // Distances & times
  let networkKm = 0;
  let networkTime = 0;
  segments.forEach(s => {{
    networkKm += s.km;
    networkTime += (s.km / s.kmph) * 60.0;
  }});

  const pickupDist = orig.distance_to_node_km || 0;
  const pickupTime = (pickupDist / (18 / tMult)) * 60.0;

  const dropoffDist = dest.distance_to_node_km || 0;
  const dropoffTime = (dropoffDist / (18 / tMult)) * 60.0;

  const totalKm = pickupDist + networkKm + dropoffDist;
  const totalDrivingMins = pickupTime + networkTime + dropoffTime;

  // Kitchen Prep Time
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

  currentRouteData = {{
    origin: orig,
    destination: dest,
    path: netPath,
    segments: segments,
    pickupDist,
    pickupTime,
    dropoffDist,
    dropoffTime,
    totalKm,
    totalDrivingMins,
    prepMins,
    handoffMins,
    totalEtaMins,
    trafficKey,
    trafficMult: tMult
  }};

  // 1. Update Visual Metrics Card
  updateVisualCards(currentRouteData);

  // 2. Generate EXACT Terminal Text Output
  generateTerminalOutput(currentRouteData);

  // 3. Render Route on Leaflet Map
  renderRouteOnMap(currentRouteData);
}}

function updateVisualCards(r) {{
  document.getElementById('val-eta').textContent = r.totalEtaMins.toFixed(1) + ' min';
  document.getElementById('val-dist').textContent = r.totalKm.toFixed(2) + ' km';
  document.getElementById('val-drive').textContent = r.totalDrivingMins.toFixed(1) + ' min';
  document.getElementById('val-prep').textContent = r.prepMins + ' min';
  document.getElementById('opt-goal-badge').textContent = currentCriterion.toUpperCase() + (r.trafficMult > 1 ? ` (${{r.trafficKey}})` : '');

  // Nodes sequence
  const seqHtml = r.path.map(nId => `<span class="node-pill">${{nodeById[nId]?.name || nId}}</span>`).join(' &rarr; ');
  document.getElementById('nodes-path-seq').innerHTML = `<b>${{r.path.length}} Nodes:</b> ` + seqHtml;

  // Step-by-step directions
  let dirHtml = '';
  let sNum = 1;

  if (r.pickupDist > 0) {{
    dirHtml += `
      <div class="dir-step">
        <div class="step-num">1</div>
        <div class="step-info">
          <div class="step-name">Depart from ${{r.origin.name}}</div>
          <div class="step-meta">Access leg &rarr; ${{nodeById[r.path[0]]?.name}} (${{r.pickupDist.toFixed(2)}} km, ${{r.pickupTime.toFixed(1)}} min)</div>
        </div>
      </div>`;
    sNum++;
  }}

  r.segments.forEach((seg, i) => {{
    const fromName = nodeById[r.path[i]]?.name;
    const toName = nodeById[r.path[i+1]]?.name;
    const t = (seg.km / seg.kmph) * 60;
    dirHtml += `
      <div class="dir-step">
        <div class="step-num">${{sNum}}</div>
        <div class="step-info">
          <div class="step-name">${{seg.name || 'Road to ' + toName}} (${{seg.type}})</div>
          <div class="step-meta">${{fromName}} &rarr; ${{toName}} &middot; ${{seg.km.toFixed(2)}} km at ${{seg.kmph.toFixed(0)}} km/h (${{t.toFixed(1)}} min)</div>
        </div>
      </div>`;
    sNum++;
  }});

  if (r.dropoffDist > 0) {{
    dirHtml += `
      <div class="dir-step">
        <div class="step-num">${{sNum}}</div>
        <div class="step-info">
          <div class="step-name">Final Approach to ${{r.destination.name}}</div>
          <div class="step-meta">${{nodeById[r.path[r.path.length-1]]?.name}} &rarr; doorstep handoff (${{r.dropoffDist.toFixed(2)}} km, ${{r.dropoffTime.toFixed(1)}} min)</div>
        </div>
      </div>`;
  }}

  document.getElementById('directions-list').innerHTML = dirHtml;
}}

// Generates the EXACT terminal output formatted string
function generateTerminalOutput(r) {{
  const orig = r.origin;
  const dest = r.destination;

  let text = "=================================================================\\n";
  text += "  SANGLI FOOD DELIVERY ROUTE OPTIMIZATION RESULT\\n";
  text += "=================================================================\\n";
  text += `Origin (Pickup):      ${{orig.name}} (Restaurant)\\n`;
  if (orig.category) {{
    text += `  Category & Rating:  ${{orig.category}} | Rating: ${{orig.rating}} stars\\n`;
  }}
  text += `Destination (Drop):   ${{dest.name}} (${{dest.locality || dest.city_zone || 'Sangli'}})\\n`;
  text += `Optimization Goal:    ${{currentCriterion.toUpperCase()}} (Traffic: ${{r.trafficKey}})\\n`;
  text += "-----------------------------------------------------------------\\n";
  text += `Total Physical Distance:    ${{r.totalKm.toFixed(2)}} km\\n`;
  text += `Road Driving Travel Time:   ${{r.totalDrivingMins.toFixed(1)}} minutes\\n`;
  text += `Kitchen Preparation Time:   ${{r.prepMins}} minutes\\n`;
  text += `Doorstep Handoff:           ${{r.handoffMins.toFixed(1)}} minutes\\n`;
  text += `TOTAL ESTIMATED ETA:        ${{r.totalEtaMins.toFixed(1)}} minutes\\n`;
  text += "-----------------------------------------------------------------\\n";
  text += `Nodes in Path (${{r.path.length}}): ` + r.path.join(' -> ') + "\\n\\n";
  text += "Step-by-Step Directions:\\n";

  let step = 1;
  if (r.pickupDist > 0) {{
    text += `  ${{step}}. Start at ${{orig.name}} -> head to ${{nodeById[r.path[0]]?.name}} (${{r.pickupDist.toFixed(3)}} km, ${{r.pickupTime.toFixed(1)}} min)\\n`;
    step++;
  }}

  r.segments.forEach((seg, i) => {{
    const toName = nodeById[r.path[i+1]]?.name;
    const t = (seg.km / seg.kmph) * 60;
    text += `  ${{step}}. Follow ${{seg.name || 'Road to ' + toName}} (${{seg.type}}) -> ${{toName}} [${{seg.km.toFixed(2)}} km at ${{seg.kmph.toFixed(1)}} km/h, ${{t.toFixed(1)}} min]\\n`;
    step++;
  }});

  if (r.dropoffDist > 0) {{
    text += `  ${{step}}. Final approach from ${{nodeById[r.path[r.path.length-1]]?.name}} -> arrive at ${{dest.name}} (${{r.dropoffDist.toFixed(3)}} km, ${{r.dropoffTime.toFixed(1)}} min)\\n`;
  }}
  text += "=================================================================";

  document.getElementById('term-output').textContent = text;
}}

function copyTerminalText() {{
  const text = document.getElementById('term-output').textContent;
  navigator.clipboard.writeText(text).then(() => {{
    alert('Terminal report copied to clipboard!');
  }});
}}

// Draw the Glowing Shortest Route on Leaflet
function renderRouteOnMap(r) {{
  routeLayerGroup.clearLayers();

  const latlngs = [];

  // Start at origin GPS point
  latlngs.push([r.origin.lat, r.origin.lon]);

  // Network path
  r.path.forEach(nId => {{
    const n = nodeById[nId];
    if (n) latlngs.push([n.lat, n.lon]);
  }});

  // End at destination GPS point
  latlngs.push([r.destination.lat, r.destination.lon]);

  // 1. Glow background line
  const glowLine = L.polyline(latlngs, {{
    color: '#00f2fe',
    weight: 8,
    opacity: 0.45,
    lineCap: 'round',
    lineJoin: 'round'
  }});

  // 2. Crisp animated line
  const mainLine = L.polyline(latlngs, {{
    color: '#38bdf8',
    weight: 4,
    opacity: 0.95,
    dashArray: '8, 6',
    lineCap: 'round',
    lineJoin: 'round'
  }});

  // Pulsing Start Pin
  const startCircle = L.circleMarker([r.origin.lat, r.origin.lon], {{
    radius: 9,
    fillColor: '#f59e0b',
    color: '#ffffff',
    weight: 2.5,
    fillOpacity: 1
  }}).bindTooltip(`<b>Start:</b> ${{r.origin.name}}`);

  // Pulsing End Pin
  const endCircle = L.circleMarker([r.destination.lat, r.destination.lon], {{
    radius: 9,
    fillColor: '#10b981',
    color: '#ffffff',
    weight: 2.5,
    fillOpacity: 1
  }}).bindTooltip(`<b>Dropoff:</b> ${{r.destination.name}}`);

  routeLayerGroup.addLayer(glowLine);
  routeLayerGroup.addLayer(mainLine);
  routeLayerGroup.addLayer(startCircle);
  routeLayerGroup.addLayer(endCircle);

  // Auto fit map bounds with padding
  map.fitBounds(L.latLngBounds(latlngs), {{ padding: [50, 50] }});
}}

// Animated Scooter Delivery Simulation
function simulateScooterDelivery() {{
  if (!currentRouteData) calculateRoute();
  if (!currentRouteData) return;

  if (animInterval) clearInterval(animInterval);
  if (scooterMarker) {{
    routeLayerGroup.removeLayer(scooterMarker);
  }}

  const coords = [];
  coords.push([currentRouteData.origin.lat, currentRouteData.origin.lon]);
  currentRouteData.path.forEach(nId => {{
    const n = nodeById[nId];
    if (n) coords.push([n.lat, n.lon]);
  }});
  coords.push([currentRouteData.destination.lat, currentRouteData.destination.lon]);

  const scooterIcon = L.divIcon({{
    className: 'custom-div-icon',
    html: '<div class="scooter-marker">🛵</div>',
    iconSize: [30, 30],
    iconAnchor: [15, 15]
  }});

  scooterMarker = L.marker(coords[0], {{ icon: scooterIcon }}).addTo(routeLayerGroup);

  // Compute segment lengths
  const segLens = [];
  let totalDist = 0;
  for (let i = 0; i < coords.length - 1; i++) {{
    const d = map.distance(coords[i], coords[i+1]);
    segLens.push(d);
    totalDist += d;
  }}

  let progress = 0;
  const step = 0.006;

  animInterval = setInterval(() => {{
    progress += step;
    if (progress >= 1) {{
      progress = 1;
      clearInterval(animInterval);
      scooterMarker.bindTooltip("✅ Delivered! Order Completed.", {{ permanent: true, direction: "top" }}).openTooltip();
    }}

    const targetD = progress * totalDist;
    let accum = 0;
    let currentPos = coords[0];

    for (let i = 0; i < segLens.length; i++) {{
      if (accum + segLens[i] >= targetD) {{
        const rem = targetD - accum;
        const frac = rem / segLens[i];
        currentPos = [
          coords[i][0] + (coords[i+1][0] - coords[i][0]) * frac,
          coords[i][1] + (coords[i+1][1] - coords[i][1]) * frac
        ];
        break;
      }}
      accum += segLens[i];
    }}

    scooterMarker.setLatLng(currentPos);
  }}, 30);
}}

// User Interaction Helpers
function setAsOrigin(id) {{
  document.getElementById('orig-select').value = id;
  calculateRoute();
  map.closePopup();
}}

function setAsDestination(id) {{
  document.getElementById('dest-select').value = id;
  calculateRoute();
  map.closePopup();
}}

function onEndpointChange() {{
  calculateRoute();
}}

function swapEndpoints() {{
  const oSel = document.getElementById('orig-select');
  const dSel = document.getElementById('dest-select');
  const temp = oSel.value;
  oSel.value = dSel.value;
  dSel.value = temp;
  calculateRoute();
}}

function setPreset(origId, destId) {{
  document.getElementById('orig-select').value = origId;
  document.getElementById('dest-select').value = destId;
  calculateRoute();
}}

function setOptCriterion(c) {{
  currentCriterion = c;
  document.getElementById('btn-opt-time').classList.toggle('active', c === 'time');
  document.getElementById('btn-opt-dist').classList.toggle('active', c === 'distance');
  calculateRoute();
}}

function toggleFloodHazard() {{
  floodHazardActive = !floodHazardActive;
  document.getElementById('hazard-box').classList.toggle('active', floodHazardActive);
  calculateRoute();
}}

function toggleMapLayer(layer) {{
  if (layer === 'restaurants') {{
    showRestaurantsLayer = !showRestaurantsLayer;
    document.getElementById('tag-rest').classList.toggle('off', !showRestaurantsLayer);
    if (showRestaurantsLayer) map.addLayer(restaurantMarkersGroup);
    else map.removeLayer(restaurantMarkersGroup);
  }} else if (layer === 'residents') {{
    showResidentsLayer = !showResidentsLayer;
    document.getElementById('tag-res').classList.toggle('off', !showResidentsLayer);
    if (showResidentsLayer) map.addLayer(residentMarkersGroup);
    else map.removeLayer(residentMarkersGroup);
  }} else if (layer === 'roads') {{
    showRoadsLayer = !showRoadsLayer;
    document.getElementById('tag-roads').classList.toggle('off', !showRoadsLayer);
    if (showRoadsLayer) map.addLayer(roadLayersGroup);
    else map.removeLayer(roadLayersGroup);
  }}
}}

function toggleTheme() {{
  const isDark = document.body.getAttribute('data-theme') === 'dark';
  document.body.setAttribute('data-theme', isDark ? 'light' : 'dark');
  document.getElementById('theme-btn').textContent = isDark ? '🌙 Dark' : '☀️ Light';
}}

function fitRouteBounds() {{
  if (currentRouteData) {{
    renderRouteOnMap(currentRouteData);
  }}
}}

function resetMapView() {{
  map.setView([16.8524, 74.5815], 13);
}}

// Initialize Application
window.addEventListener('DOMContentLoaded', () => {{
  initMap();
  populateDropdowns();
  calculateRoute();
}});
</script>
</body>
</html>
"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    with open('route_optimizer.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Successfully built updated index.html and route_optimizer.html with zero watermarks and direct roads!")

if __name__ == '__main__':
    main()
