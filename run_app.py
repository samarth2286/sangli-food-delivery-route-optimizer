"""
run_app.py
Launches the Sangli Food Delivery Route Optimizer in your default web browser
using a local HTTP server for maximum map tile and asset reliability.
"""

import os
import sys
import webbrowser
import threading
import http.server
import socketserver

PORT = 8000

def start_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    handler = http.server.SimpleHTTPRequestHandler
    # Suppress verbose log requests to keep console clean
    handler.log_message = lambda self, format, *args: None
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        httpd.serve_forever()

def main():
    print("=" * 65)
    print("  🛵 SANGLI FOOD DELIVERY ROUTE OPTIMIZER")
    print("=" * 65)
    print(f"Starting local server at: http://localhost:{PORT}")
    print("Features loaded:")
    print("  - 🗺️ Real Interactive Map of Sangli (Leaflet + Esri WorldStreetMap)")
    print("  - 🍽️ 31 Real Restaurants in Sangli with categories & ratings")
    print("  - 🏡 155 Residential Housing Societies & Colonies")
    print("  - ⚡ Dijkstra & A* Routing (Shortest Distance vs Fastest Time)")
    print("  - 🚦 Real-time Traffic & Monsoon Flood Hazard Avoidance")
    print("  - 💻 Exact Terminal Console Output Report visible on the website")
    print("  - 🛵 Real-time Animated Delivery Scooter Simulator")
    print("=" * 65)
    print("Press Ctrl+C in this terminal to stop the server.\n")

    # Start server in daemon thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Open browser to localhost
    webbrowser.open(f"http://localhost:{PORT}/index.html")

    # Keep main thread alive
    try:
        server_thread.join()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == '__main__':
    main()
