"""
Tetuan City Power Consumption Dataset Generator
Generates high-fidelity 10-minute interval telemetry matching the UCI Tetouan City dataset specification.
Includes authentic diurnal load curves, solar cycles, weather variations, and labelled anomaly events.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

def generate_tetuan_dataset(output_path="data/tetuan_city_power_consumption.csv", days=90):
    np.random.seed(42)
    start_date = datetime(2017, 1, 1, 0, 0, 0)
    intervals = days * 24 * 6  # 10-min intervals
    
    timestamps = [start_date + timedelta(minutes=10 * i) for i in range(intervals)]
    
    # Time features
    hours = np.array([ts.hour + ts.minute / 60.0 for ts in timestamps])
    day_of_week = np.array([ts.weekday() for ts in timestamps])
    is_weekend = np.isin(day_of_week, [5, 6]).astype(float)
    day_of_year = np.array([ts.timetuple().tm_yday for ts in timestamps])
    
    # 1. Temperature: seasonal trend + diurnal cycle + noise
    seasonal_temp = 12.0 + 8.0 * (day_of_year / days)  # gradual warming
    diurnal_temp = 6.0 * np.sin((hours - 9) * np.pi / 12)  # min at 6am, max at 3pm
    temp_noise = np.random.normal(0, 0.8, intervals)
    temperature = np.round(np.clip(seasonal_temp + diurnal_temp + temp_noise, 4.0, 38.0), 2)
    
    # 2. Humidity: inverse of temperature + weather front variations
    base_humidity = 75.0 - 5.0 * (day_of_year / days)
    diurnal_humidity = -15.0 * np.sin((hours - 9) * np.pi / 12)
    hum_noise = np.random.normal(0, 2.5, intervals)
    humidity = np.round(np.clip(base_humidity + diurnal_humidity + hum_noise, 20.0, 95.0), 2)
    
    # 3. Wind Speed (km/h)
    wind_base = 2.0 + 1.5 * np.sin(hours * np.pi / 12)
    wind_noise = np.random.exponential(1.0, intervals)
    wind_speed = np.round(np.clip(wind_base + wind_noise, 0.1, 8.5), 2)
    
    # 4. Solar Radiation / Diffuse flows (W/m2)
    # Sun elevation approx from 07:00 to 19:00
    solar_elevation = np.maximum(0, np.sin((hours - 7) * np.pi / 12))
    solar_mask = (hours >= 7.0) & (hours <= 19.0)
    gen_diffuse = np.zeros(intervals)
    diffuse = np.zeros(intervals)
    
    cloud_cover = np.random.uniform(0.7, 1.1, intervals)
    gen_diffuse[solar_mask] = 850.0 * solar_elevation[solar_mask] * cloud_cover[solar_mask] + np.random.normal(0, 15, np.sum(solar_mask))
    diffuse[solar_mask] = 550.0 * solar_elevation[solar_mask] * cloud_cover[solar_mask] + np.random.normal(0, 10, np.sum(solar_mask))
    
    gen_diffuse = np.round(np.clip(gen_diffuse, 0.0, 1100.0), 2)
    diffuse = np.round(np.clip(diffuse, 0.0, 850.0), 2)
    
    # 5. Zone 1 Power Consumption (Quads - Commercial/Residential Hub)
    # Peak in evening 18:00 - 22:00, baseload 14,000 - 18,000 kW
    z1_base = 16000.0
    z1_diurnal = 14000.0 * np.exp(-((hours - 20.5) ** 2) / 10) + 6000.0 * np.exp(-((hours - 13.0) ** 2) / 12)
    z1_weekend_effect = -1500.0 * is_weekend
    z1_temp_effect = 250.0 * np.maximum(0, temperature - 22.0)  # AC cooling load
    z1_noise = np.random.normal(0, 600, intervals)
    z1_power = z1_base + z1_diurnal + z1_weekend_effect + z1_temp_effect + z1_noise
    
    # 6. Zone 2 Power Consumption (Smir - Tourism/Coastal Zone)
    z2_base = 11000.0
    z2_diurnal = 9000.0 * np.exp(-((hours - 21.0) ** 2) / 12) + 4000.0 * np.exp(-((hours - 14.0) ** 2) / 14)
    z2_weekend_effect = 1500.0 * is_weekend  # Higher on weekends due to tourism
    z2_temp_effect = 180.0 * np.maximum(0, temperature - 22.0)
    z2_noise = np.random.normal(0, 450, intervals)
    z2_power = z2_base + z2_diurnal + z2_weekend_effect + z2_temp_effect + z2_noise
    
    # 7. Zone 3 Power Consumption (Boussafou - Mixed Light Industrial & Commercial)
    z3_base = 9000.0
    # Industrial shift: peaks during workday 09:00 - 17:00, drops sharply on weekends
    workday_curve = 12000.0 * ((hours >= 8.5) & (hours <= 17.5)).astype(float) * (1.0 - 0.7 * is_weekend)
    z3_noise = np.random.normal(0, 500, intervals)
    z3_power = z3_base + workday_curve + z3_noise
    
    # --- INJECT REALISTIC ANOMALIES FOR EVALUATION & INVESTIGATION ---
    # Anomaly 1: Nighttime industrial compressor runaway in Zone 3 (Day 12, 01:00 - 04:30)
    mask_a1 = (day_of_year == 12) & (hours >= 1.0) & (hours <= 4.5)
    z3_power[mask_a1] += 11500.0
    
    # Anomaly 2: Extreme heatwave peak surge in Zone 1 (Day 35, 19:00 - 21:30)
    mask_a2 = (day_of_year == 35) & (hours >= 19.0) & (hours <= 21.5)
    z1_power[mask_a2] += 14000.0
    
    # Anomaly 3: Sudden substation feeder drop / partial outage in Zone 2 (Day 52, 14:00 - 15:30)
    mask_a3 = (day_of_year == 52) & (hours >= 14.0) & (hours <= 15.5)
    z2_power[mask_a3] = np.maximum(2500.0, z2_power[mask_a3] * 0.25)
    
    # Anomaly 4: Weekend unauthorized operation in Zone 3 (Day 70, Sunday 10:00 - 16:00)
    mask_a4 = (day_of_year == 70) & (hours >= 10.0) & (hours <= 16.0)
    z3_power[mask_a4] += 9500.0
    
    # Anomaly 5: Sensor calibration drift spike in Zone 1 (Day 82, 03:20)
    idx_a5 = np.where((day_of_year == 82) & (hours >= 3.3) & (hours <= 3.6))[0]
    if len(idx_a5) > 0:
        z1_power[idx_a5] += 18000.0

    # Format outputs
    df = pd.DataFrame({
        "DateTime": [ts.strftime("%m/%d/%Y %H:%M") for ts in timestamps],
        "Temperature": temperature,
        "Humidity": humidity,
        "Wind Speed": wind_speed,
        "general diffuse flows": gen_diffuse,
        "diffuse flows": diffuse,
        "Zone 1 Power Consumption": np.round(np.clip(z1_power, 8000.0, 58000.0), 2),
        "Zone 2 Power Consumption": np.round(np.clip(z2_power, 4000.0, 42000.0), 2),
        "Zone 3 Power Consumption": np.round(np.clip(z3_power, 4000.0, 38000.0), 2),
    })
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} rows to {output_path}")
    print(df.head(3))
    return df

if __name__ == "__main__":
    generate_tetuan_dataset()
