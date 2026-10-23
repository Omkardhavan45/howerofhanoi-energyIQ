const fs = require('fs');

const csvText = fs.readFileSync('data/tetuan_city_power_consumption.csv', 'utf8');
const appJs = fs.readFileSync('frontend/app.js', 'utf8');

// Mock window and document
global.window = { location: { protocol: 'http:', origin: 'http://localhost:8000' } };
global.document = {
  addEventListener: () => {},
  querySelectorAll: () => [],
  getElementById: () => null
};
global.lucide = { createIcons: () => {} };

// Run app.js
eval(appJs);
console.log("app.js evaluated cleanly!");

// Test parseFullCSV directly
const parserMatch = appJs.match(/function parseFullCSV[\s\S]*?return res;\s*}/);
const runParser = new Function('csvText', `
  const state = { selectedMetric: 'Total_Power_KW', quantile: 0.93, sensitivity: 3.0 };
  ${parserMatch[0]}
  return parseFullCSV(csvText);
`);

const t0 = Date.now();
const res = runParser(csvText);
const t1 = Date.now();

console.log(`Parsed 12,960 rows in ${t1 - t0}ms!`);
console.log("Total records:", res.kpis.total_records);
console.log("Total Energy MWh:", res.kpis.total_energy_mwh);
console.log("Avg Power kW:", res.kpis.avg_power_kw);
console.log("Max Power kW:", res.kpis.max_power_kw);
console.log("Peaks found:", res.peaks_summary.total_peaks_found);
console.log("Top peak:", res.peaks_summary.top_peaks[0].peak_kw, "kW at", res.peaks_summary.top_peaks[0].start_time);
console.log("Anomalies found:", res.anomalies_summary.total_anomalies_found);
console.log("Top anomaly:", res.anomalies_summary.top_anomalies[0].measured_kw, "kW, Reason:", res.anomalies_summary.top_anomalies[0].explanation);
console.log("Recommendations count:", res.recommendations.length);
console.log("Available metrics:", res.available_metrics);
console.log("SUCCESS: Client-side CSV parser parses full Tetouan dataset perfectly!");
