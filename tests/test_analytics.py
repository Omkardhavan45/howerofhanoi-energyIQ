"""
Unit Tests for EnergyIQ Analytics Engine
Tests preprocessing, column detection, summary metrics, peak load analysis,
anomaly detection, and recommendation generation.
"""

import unittest
import os
import pandas as pd
from backend.analytics import EnergyAnalyticsEngine

class TestEnergyAnalytics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.csv_path = "data/tetuan_city_power_consumption.csv"
        assert os.path.exists(cls.csv_path), f"Dataset not found at {cls.csv_path}"
        cls.raw_df = pd.read_csv(cls.csv_path)
        cls.engine = EnergyAnalyticsEngine(cls.raw_df)

    def test_column_detection(self):
        mapping = self.engine.column_map
        self.assertIn("DateTime", mapping["timestamp"])
        self.assertGreaterEqual(len(mapping["power_cols"]), 3)
        self.assertEqual(mapping["temperature"], "Temperature")
        self.assertEqual(mapping["humidity"], "Humidity")

    def test_kpi_computation(self):
        kpis = self.engine.compute_summary_kpis()
        self.assertGreater(kpis["total_energy_mwh"], 0)
        self.assertGreater(kpis["avg_power_kw"], 0)
        self.assertGreater(kpis["max_power_kw"], kpis["avg_power_kw"])
        self.assertGreater(kpis["energy_efficiency_score"], 0)
        self.assertIn("estimated_costs", kpis)

    def test_peak_detection(self):
        peaks = self.engine.detect_peaks(quantile=0.93)
        self.assertIsInstance(peaks, list)
        self.assertGreater(len(peaks), 0)
        top_peak = peaks[0]
        self.assertIn("peak_kw", top_peak)
        self.assertIn("duration_mins", top_peak)
        self.assertIn("severity_score", top_peak)
        self.assertGreaterEqual(top_peak["peak_kw"], top_peak["threshold_kw"])

    def test_anomaly_detection(self):
        anomalies = self.engine.detect_anomalies(sensitivity=3.0)
        self.assertIsInstance(anomalies, list)
        self.assertGreater(len(anomalies), 0)
        first_ano = anomalies[0]
        self.assertIn("measured_kw", first_ano)
        self.assertIn("anomaly_score", first_ano)
        self.assertIn("explanation", first_ano)

    def test_recommendation_generation(self):
        kpis = self.engine.compute_summary_kpis()
        peaks = self.engine.detect_peaks()
        anomalies = self.engine.detect_anomalies()
        recs = self.engine.generate_recommendations(kpis, peaks, anomalies)
        self.assertIsInstance(recs, list)
        self.assertGreaterEqual(len(recs), 3)
        for r in recs:
            self.assertIn("observation", r)
            self.assertIn("evidence", r)
            self.assertIn("suggested_action", r)

    def test_time_series_formatting(self):
        ts_data = self.engine.get_time_series_data(max_points=100)
        self.assertAlmostEqual(len(ts_data["timestamps"]), 100, delta=5)
        self.assertIn("Total", ts_data["series"])

if __name__ == "__main__":
    unittest.main()
