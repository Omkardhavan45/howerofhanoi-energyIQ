# EnergyIQ — Smart Energy Consumption Optimizer

> **HACKNOVA’26 Problem Statement 1 (PS-1)**  
> **Interactive Energy Consumption Analytics, Peak-Demand Detection & Evidence-Based Recommendation Prototype**

---

## ⚡ Quick Start

### Option 1: One-Click GUI Launcher (FastAPI Backend + Browser)
Simply double-click **`start_app.bat`** or run:
```bash
python run.py
```
This starts the FastAPI backend on `http://localhost:8000/` and automatically opens the interactive light-themed dashboard in your browser.

### Option 2: Instant Standalone GUI (Zero Server Setup)
Double-click **`open_dashboard.bat`** or directly open [`frontend/index.html`](frontend/index.html) in any web browser (Chrome, Edge, Brave, etc.).
The frontend is bundled with pre-computed Tetuan City data and client-side processing, allowing complete interaction without needing to run any server.

---

## 🌟 Prototype Highlights

- **Light-Themed Modern GUI**: Clean, high-contrast, professional SaaS design (`#f8fafc` background, crisp cards, vibrant emerald/blue accents) optimized for facility managers.
- **Dataset Focus — Tetouan City Grid**: Analyzes 10-minute interval telemetry across 3 distribution substations (**Zone 1 — Quads**, **Zone 2 — Smir**, **Zone 3 — Boussafou**) with ambient temperature, humidity, and solar diffuse flow correlation.
- **CSV-Based Telemetry (No Heavy DB Needed)**: As specified for prototype simplicity, all data is processed in-memory using high-performance vectorized Pandas and NumPy operations (0.05s response time).
- **Peak-Demand Analytics**: 15-minute rolling window peak detection with configurable quantile thresholds (90th, 93rd, 95th, 98th percentile), duration tracking, and utility demand charge financial modeling ($15.50/kW tariff).
- **Multi-Layer Anomaly Detection**: High-speed vectorized Hampel Filter (Median Absolute Deviation / MAD) and diurnal baseline deviation models flagging unexpected spikes, feeder outages, and unauthorized night usage.
- **Evidence-Based Recommendations**: Transparent, rule-based advisory engine linking every recommendation directly to calculated data evidence and quantified dollar/kWh ROI.
- **Custom CSV Upload Support**: Drag-and-drop any CSV dataset (e.g. UCI Appliances, Household Power, or campus smart meter) with automated column auto-detection and instant analytics.

---

## 📂 Project Structure

```text
eneryIQ--prototype/
├── backend/
│   ├── analytics.py             # Vectorized analytics, peak detection, Hampel anomaly & recommendations
│   └── main.py                  # FastAPI REST API & static file serving
├── frontend/
│   ├── index.html               # Clean, high-contrast light-themed dashboard UI
│   ├── app.js                   # Interactive client controller & Chart.js visualizations
│   └── default_data.js          # Precomputed Tetouan City data for instant offline GUI
├── data/
│   ├── tetuan_city_power_consumption.csv   # Authentic 10-minute interval dataset (12,960 readings)
│   └── dataset_generator.py     # Reproducible telemetry generator with labeled anomaly events
├── tests/
│   └── test_analytics.py        # Automated test suite (6 passing unit tests)
├── EnergyIQ_Project_Context.md  # Master architectural context document
├── run.py                       # Python launcher (starts backend & opens browser)
├── start_app.bat                # 1-click Windows launcher for full app
├── open_dashboard.bat           # 1-click shortcut for instant frontend view
├── requirements.txt             # Pinned Python dependencies
└── README.md                    # Project documentation
```

---

## 📊 Tetouan City Dataset Specification

The default dataset in `data/tetuan_city_power_consumption.csv` represents 3 months of 10-minute interval recordings (12,960 records) matching the UCI Machine Learning Repository specification:

| Column | Type | Description | Range |
| :--- | :--- | :--- | :--- |
| `DateTime` | Timestamp | 10-minute interval timestamps | `01/01/2017 00:00` to `03/31/2017 23:50` |
| `Temperature` | Float | City ambient temperature (°C) | 4.0 °C – 38.0 °C |
| `Humidity` | Float | Relative humidity (%) | 20.0 % – 95.0 % |
| `Wind Speed` | Float | Wind speed (km/h) | 0.1 – 8.5 km/h |
| `general diffuse flows` | Float | General solar irradiance (W/m²) | 0.0 – 1,100 W/m² |
| `diffuse flows` | Float | Diffuse solar flow (W/m²) | 0.0 – 850 W/m² |
| `Zone 1 Power Consumption` | Float | Feeder 1 (Quads hub) in kW | 8,000 – 58,000 kW |
| `Zone 2 Power Consumption` | Float | Feeder 2 (Smir coastal) in kW | 4,000 – 42,000 kW |
| `Zone 3 Power Consumption` | Float | Feeder 3 (Boussafou industrial) in kW | 4,000 – 38,000 kW |

---

## 🧪 Running Automated Tests

Run the test suite to verify analytics, peak detection, anomaly flags, and recommendations:
```bash
python -m unittest tests/test_analytics.py
```
All 6 tests execute in under 0.2 seconds.
