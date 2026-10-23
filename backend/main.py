"""
EnergyIQ — FastAPI Backend Server
Serves REST API endpoints for energy analytics, peak detection, anomaly detection,
rule-based recommendations, and hosts the interactive GUI.
"""

import os
import io
import pandas as pd
from typing import Optional
from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from backend.analytics import EnergyAnalyticsEngine

app = FastAPI(
    title="EnergyIQ API",
    description="Smart Energy Consumption Optimizer API for Tetuan City and custom datasets",
    version="1.0.0"
)

# Enable CORS for local development and cross-origin frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load default Tetuan dataset into memory on startup
DEFAULT_CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "tetuan_city_power_consumption.csv")
default_engine = None

if os.path.exists(DEFAULT_CSV_PATH):
    try:
        print(f"Loading default dataset from {DEFAULT_CSV_PATH}...")
        raw_df = pd.read_csv(DEFAULT_CSV_PATH)
        default_engine = EnergyAnalyticsEngine(raw_df)
        print("Default dataset loaded successfully!")
    except Exception as e:
        print(f"Warning: Failed to load default dataset: {e}")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "EnergyIQ Smart Energy Optimizer",
        "version": "1.0.0",
        "default_dataset_loaded": default_engine is not None
    }

@app.get("/api/dataset/info")
def get_dataset_info():
    if not default_engine:
        raise HTTPException(status_code=404, detail="Default dataset not loaded")
    return {
        "dataset_name": "Tetuan City Power Consumption",
        "description": "10-minute interval power telemetry across 3 distribution substations (Quads, Smir, Boussafou) with weather features.",
        "columns": list(default_engine.processed_df.columns),
        "column_mapping": default_engine.column_map,
        "total_records": len(default_engine.processed_df)
    }

@app.get("/api/analyze/default")
def analyze_default_dataset(
    selected_metric: Optional[str] = Query(None, description="Column to analyze (e.g. Zone 1 Power Consumption, Total_Power_KW)"),
    peak_quantile: float = Query(0.93, ge=0.50, le=0.99, description="Quantile threshold for peak detection"),
    anomaly_sensitivity: float = Query(3.0, ge=1.5, le=6.0, description="Hampel filter sensitivity threshold"),
    max_chart_points: int = Query(400, ge=50, le=2000, description="Chart downsampling resolution")
):
    if not default_engine:
        raise HTTPException(status_code=404, detail="Default dataset not found on server")
        
    kpis = default_engine.compute_summary_kpis(selected_metric)
    peaks = default_engine.detect_peaks(selected_metric, quantile=peak_quantile)
    anomalies = default_engine.detect_anomalies(selected_metric, sensitivity=anomaly_sensitivity)
    recommendations = default_engine.generate_recommendations(kpis, peaks, anomalies)
    time_series = default_engine.get_time_series_data(selected_metric, max_points=max_chart_points)
    load_profile = default_engine.get_hourly_load_profile(selected_metric)
    
    return {
        "kpis": kpis,
        "peaks_summary": {
            "total_peaks_found": len(peaks),
            "peak_threshold_kw": peaks[0]["threshold_kw"] if peaks else 0,
            "top_peaks": peaks[:15]
        },
        "anomalies_summary": {
            "total_anomalies_found": len(anomalies),
            "critical_count": sum(1 for a in anomalies if a["severity"] == "Critical"),
            "high_count": sum(1 for a in anomalies if a["severity"] == "High"),
            "top_anomalies": anomalies[:25]
        },
        "recommendations": recommendations,
        "time_series": time_series,
        "load_profile": load_profile,
        "available_metrics": ["Total_Power_KW"] + default_engine.column_map.get("power_cols", [])
    }

class UploadPayload(BaseModel):
    csv_text: str
    filename: Optional[str] = "uploaded_data.csv"
    selected_metric: Optional[str] = None
    peak_quantile: Optional[float] = 0.93
    anomaly_sensitivity: Optional[float] = 3.0
    max_chart_points: Optional[int] = 400

@app.post("/api/analyze/upload")
async def analyze_uploaded_csv(payload: UploadPayload):
    try:
        if not payload.csv_text or not payload.csv_text.strip():
            raise HTTPException(status_code=400, detail="Uploaded CSV text is empty.")
            
        df = pd.read_csv(io.StringIO(payload.csv_text))
        if len(df) == 0:
            raise HTTPException(status_code=400, detail="Uploaded CSV file has no records.")
            
        custom_engine = EnergyAnalyticsEngine(df)
        
        kpis = custom_engine.compute_summary_kpis(payload.selected_metric)
        peaks = custom_engine.detect_peaks(payload.selected_metric, quantile=payload.peak_quantile or 0.93)
        anomalies = custom_engine.detect_anomalies(payload.selected_metric, sensitivity=payload.anomaly_sensitivity or 3.0)
        recommendations = custom_engine.generate_recommendations(kpis, peaks, anomalies)
        time_series = custom_engine.get_time_series_data(payload.selected_metric, max_points=payload.max_chart_points or 400)
        load_profile = custom_engine.get_hourly_load_profile(payload.selected_metric)
        
        return {
            "filename": payload.filename,
            "kpis": kpis,
            "peaks_summary": {
                "total_peaks_found": len(peaks),
                "peak_threshold_kw": peaks[0]["threshold_kw"] if peaks else 0,
                "top_peaks": peaks[:15]
            },
            "anomalies_summary": {
                "total_anomalies_found": len(anomalies),
                "critical_count": sum(1 for a in anomalies if a["severity"] == "Critical"),
                "high_count": sum(1 for a in anomalies if a["severity"] == "High"),
                "top_anomalies": anomalies[:25]
            },
            "recommendations": recommendations,
            "time_series": time_series,
            "load_profile": load_profile,
            "available_metrics": ["Total_Power_KW"] + custom_engine.column_map.get("power_cols", [])
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error analyzing uploaded file: {str(e)}")

# Mount data and frontend directories for static serving
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

if os.path.exists(DATA_DIR):
    app.mount("/data", StaticFiles(directory=DATA_DIR), name="data")

if os.path.exists(FRONTEND_DIR):
    # Mount frontend at root so index.html, app.js, default_data.js are served directly
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
