"""
EnergyIQ — Application Launcher
Starts the FastAPI analytics backend on http://localhost:8000 and opens the interactive dashboard.
"""

import sys
import os
import time
import webbrowser
import uvicorn

def main():
    print("=" * 60)
    print("   EnergyIQ — Smart Energy Consumption Optimizer")
    print("   HACKNOVA’26 Prototype (PS-1)")
    print("   Light Theme Interactive GUI & Analytics Engine")
    print("=" * 60)
    
    port = 8000
    host = "127.0.0.1"
    url = f"http://{host}:{port}/"
    
    print(f"\n[+] Starting FastAPI backend on {url}...")
    print(f"[+] Loaded Dataset: data/tetuan_city_power_consumption.csv")
    print(f"[+] Launching interactive web GUI in your default browser...\n")
    
    # Open browser after a brief delay
    def open_browser():
        time.sleep(1.2)
        try:
            webbrowser.open(url)
        except Exception:
            pass

    import threading
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run uvicorn server
    uvicorn.run("backend.main:app", host=host, port=port, reload=False, log_level="info")

if __name__ == "__main__":
    main()
