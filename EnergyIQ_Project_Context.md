# EnergyIQ — Smart Energy Consumption Optimizer
## Project Master Context Document

> **Purpose of this document:** This file is the single source of context for any AI assistant, developer, or teammate helping build EnergyIQ. Read it before proposing code or making architectural decisions. Keep the document updated as implementation choices change.

---

## 1. Project Overview

**Project name:** EnergyIQ — Smart Energy Consumption Optimizer  
**Hackathon:** HACKNOVA’26  
**Problem statement:** PS-1 — EnergyIQ: Smart Energy Consumption Optimizer  
**Project category:** Data analytics, machine learning, energy efficiency, dashboard/web application.

### One-line description

EnergyIQ analyzes building or household electricity-consumption data to reveal usage patterns, identify peak-demand periods and unusual readings, and provide practical, evidence-based energy-efficiency recommendations through an interactive dashboard.

### Short pitch

Buildings can collect large amounts of electricity-meter data, but raw readings do not automatically explain when consumption is unusually high, which patterns deserve investigation, or what actions could improve efficiency. EnergyIQ converts these readings into understandable insights and recommendations so facility managers can make better energy-management decisions.

### Important scope clarification

The initial prototype can work with uploaded CSV datasets or a supplied sample dataset. Physical smart-meter integration and continuous real-time monitoring are optional future extensions, not prerequisites for the first working prototype.

---

## 2. Problem Statement

Buildings, educational campuses, offices, and commercial facilities consume electricity throughout the day. Looking at raw readings alone makes it difficult to identify:

- When energy demand reaches its peak.
- Whether consumption is unusual compared with an appropriate historical baseline.
- Whether high overnight or low-occupancy-period consumption deserves investigation.
- Which recurring usage patterns may indicate an opportunity to improve efficiency.
- What practical action a facility manager should consider next.

### Target users

- Facility managers.
- Building administrators.
- College and university campuses.
- Commercial and office buildings.
- Energy-management teams.

### Project goal

Build a feasible, data-driven system that:
1. Analyzes historical or incoming energy-consumption readings.
2. Identifies trends and peak-demand intervals.
3. Flags unusual consumption patterns.
4. Generates recommendations supported by observed data.
5. Presents the results in a clear, interactive dashboard.

---

## 3. Core Features

The initial product should prioritize a small number of reliable, demonstrable features.

### Feature 1 — Dataset upload and preprocessing

**Purpose:** Allow a user to provide energy data for analysis.

Potential capabilities:
- Upload a CSV file.
- Preview the uploaded data.
- Identify available columns and data types.
- Parse timestamps and sort records chronologically.
- Handle missing or invalid readings transparently.
- Validate that the selected consumption column is numeric.
- Show understandable validation errors when required columns are absent.

**Expected output:** A validated dataset ready for analysis.

**Implementation note:** Dataset formats vary. Do not hard-code column names without checking the selected dataset. Provide a column-mapping step or configure the supported dataset format.

### Feature 2 — Consumption analytics

**Purpose:** Explain how energy usage changes over time.

Potential capabilities:
- Total and average consumption for the selected period.
- Minimum and maximum readings.
- Hourly, daily, or monthly aggregation, depending on data frequency.
- Time-series line charts.
- Comparison of selected time periods.
- Filters for date ranges and locations/buildings if those fields exist.

**Expected output:** Summary metrics and charts that help users understand consumption patterns.

### Feature 3 — Peak-load analysis

**Purpose:** Identify periods of high energy demand.

Potential capabilities:
- Find the highest-demand intervals.
- Rank the periods with the greatest consumption.
- Compare readings with a historical baseline.
- Highlight recurring high-demand times when the dataset has enough history.
- Show the date/time and measured consumption for each identified peak.

**Suggested first implementation:** Use aggregation, rolling statistics, percentiles, or a configurable threshold. Select the method based on the dataset and explain the rule used.

**Important:** A high reading is not automatically wasteful. It may reflect normal occupancy or equipment use. Use the term “peak demand” unless there is evidence that the energy was wasted.

### Feature 4 — Anomaly detection

**Purpose:** Flag readings or time intervals that differ from expected consumption patterns.

**Suggested machine-learning method:** Isolation Forest from scikit-learn.

Potential workflow:
1. Select relevant numerical features and, where appropriate, time-derived features.
2. Prepare the training data and handle invalid values.
3. Fit the model on suitable historical data.
4. score readings and flag potential anomalies.
5. Display the measured reading, anomaly score/flag, timestamp, and a plain-language explanation of why the record deserves attention.

**Alternative/simple baseline:** Compare readings against a rolling mean and standard deviation, or a suitable time-of-day baseline.

**Important limitations:**
- An anomaly is a signal to investigate, not proof of energy waste or equipment failure.
- A model can flag legitimate events as unusual.
- Evaluation is easier when known anomalies or labelled test data are available.
- Compare readings with appropriate time periods where possible; weekday and nighttime patterns may differ from daytime or weekend patterns.

### Feature 5 — Recommendation engine

**Purpose:** Convert analytics into practical next steps.

**Recommended initial approach:** Use a transparent rule-based engine. Recommendations should be generated from actual calculated results, not invented by a language model.

Example rules:
- If overnight usage is substantially above the building's normal overnight baseline, recommend checking equipment schedules and expected overnight operations.
- If a repeated peak occurs during a particular interval, recommend reviewing equipment scheduling and demand-management options.
- If usage is consistently elevated compared with comparable periods, recommend investigating the relevant equipment, occupancy, or operating conditions.

Each recommendation should include:
- **Observation:** What the data shows.
- **Evidence:** The relevant timestamp, value, baseline, or comparison.
- **Suggested action:** What the user could investigate or change.
- **Confidence/limitation:** What is known and what remains uncertain.

**Do not claim exact savings** unless the project calculates them using a stated electricity tariff and defensible assumptions. Do not claim a root cause unless the available data supports it.

### Feature 6 — Interactive dashboard

The dashboard should make the analysis easy to understand.

Suggested sections:
- Total consumption and average consumption cards.
- Peak-demand summary.
- Anomaly count and alert list.
- Consumption-over-time chart.
- Peak-period chart or table.
- Anomaly table with timestamp, measured value, and explanation.
- Recommendations panel.
- Dataset/date filters.
- Upload and analysis status.

Use consistent units and labels. Show the units actually present or derived from the selected dataset.

### Optional future feature — Conversational AI assistant

A natural-language assistant could answer questions such as:
- “When was consumption highest?”
- “Which readings were flagged as unusual?”
- “Why was last night's usage flagged?”
- “What should we investigate first?”

If implemented, it should retrieve computed results from EnergyIQ's analytics layer and explain those results. It must not fabricate readings, causes, or savings. An LLM API integration is optional and should not delay the core working prototype.

### Optional future features

Only add these after the core pipeline works:
- Forecasting future demand.
- Comparisons across multiple buildings.
- Real-time smart-meter integration.
- Role-based accounts and persistent history.
- Conversational AI.
- Cost and carbon-impact estimates, with explicit assumptions and suitable tariff/emissions data.

---

## 4. Suggested Technology Stack

The following is a **recommended stack, not a claim that the team has already implemented it**. Confirm the team's actual choices before generating project code.

| Layer | Suggested technology | Purpose |
|---|---|---|
| Frontend | React | Interactive web application and dashboard |
| Frontend styling | CSS or Tailwind CSS | Responsive layout and reusable UI styling |
| Charts | Plotly.js or a React-compatible chart library | Consumption charts and anomaly visualizations |
| Backend API | Python with FastAPI | Accept uploads, run analysis, and return results |
| Data processing | Pandas, NumPy | CSV handling, cleaning, aggregation, feature preparation |
| Machine learning | scikit-learn | Isolation Forest and model evaluation |
| Initial data storage | Uploaded CSV / in-memory processing | Keep the first prototype simple |
| Optional persistent storage | SQLite or PostgreSQL | Store datasets, analysis history, or user settings if required |
| Version control | Git and GitHub | Collaboration, source control, and submission repository |
| Deployment | A suitable frontend and Python-backend hosting service | Publish the demo if time and access permit |

### Stack selection principles

- Avoid adding a database before there is a clear need for persistent storage.
- Avoid a complex cloud architecture for a small hackathon prototype.
- Keep model and analytics logic in Python, separate from UI components.
- Keep API responses structured and predictable.
- Pin compatible package versions in a requirements file and document how to run the project.

---

## 5. End-to-End Workflow

### User workflow

1. The user opens the EnergyIQ dashboard.
2. The user uploads a supported CSV file or selects a sample dataset.
3. The application previews the data and validates its columns.
4. The user confirms the timestamp and consumption columns, if mapping is required.
5. The backend cleans and prepares the data.
6. The analytics engine calculates consumption summaries and trends.
7. Peak-load logic identifies high-demand intervals.
8. The anomaly detector flags unusual readings.
9. The recommendation engine generates data-supported suggestions.
10. The dashboard displays charts, alerts, findings, and recommended actions.
11. The user investigates the evidence and decides what action to take.

### Data-processing pipeline

```text
CSV / sample energy dataset
          |
          v
File validation and column mapping
          |
          v
Preprocessing
- Parse timestamps
- Sort chronologically
- Validate numeric readings
- Handle missing/invalid data
          |
          v
Feature engineering
- Time-of-day / day-of-week features, if useful
- Aggregated consumption intervals
- Appropriate historical baselines
          |
          +------------------------+
          |                        |
          v                        v
Consumption analytics       Peak-load analysis
          |                        |
          +------------+-----------+
                       |
                       v
               Anomaly detection
          (statistical baseline / Isolation Forest)
                       |
                       v
             Evidence-based insights
                       |
                       v
            Rule-based recommendations
                       |
                       v
                 Backend API
                       |
                       v
              React dashboard
                       |
                       v
        Facility manager reviews and acts
```

Peak detection and anomaly detection are distinct: a peak may be normal, while an anomaly is a reading that deviates from an appropriate expected pattern. They can overlap, but should not be treated as the same result.

---

## 6. Suggested System Architecture

```text
+-------------------------------------+
|           React Frontend            |
|                                     |
| Upload / Filters / Charts / Alerts   |
| Metrics / Recommendations            |
+------------------+------------------+
                   |
                   | HTTP requests (JSON / file upload)
                   v
+-------------------------------------+
|          FastAPI Backend            |
|                                     |
| Upload and validation endpoints      |
| Analysis endpoints                   |
| Results and recommendation endpoints |
+------------------+------------------+
                   |
                   v
+-------------------------------------+
|         Analytics Service           |
|                                     |
| Pandas / NumPy preprocessing          |
| Consumption aggregation             |
| Peak-load detection                 |
| Isolation Forest / statistical rules|
| Recommendation rules                |
+------------------+------------------+
                   |
                   v
+-------------------------------------+
|       Dataset / Results Layer       |
|                                     |
| CSV input and processed results      |
| Optional persistent database         |
+-------------------------------------+
```

### Example API design

These are suggested endpoints; names can change to match the final implementation.

- `GET /health` — Check whether the backend is running.
- `POST /api/analyze` — Upload a dataset and run analysis.
- `GET /api/results/{analysis_id}` — Retrieve saved results, if analysis IDs and persistence are implemented.
- `GET /api/recommendations/{analysis_id}` — Retrieve recommendations for an analysis, if this endpoint is implemented.

For an initial prototype, the analysis endpoint may return the results directly. Do not build endpoints that the application does not need.

### Example response structure

```json
{
  "summary": {
    "total_consumption": null,
    "average_consumption": null,
    "peak_period_count": null,
    "anomaly_count": null
  },
  "peaks": [],
  "anomalies": [],
  "recommendations": []
}
```

The `null` values and empty arrays are placeholders for computed results, not actual measurements. Define the exact response schema after choosing the dataset and analysis functions.

---

## 7. Dataset Options

The PS-1 problem statement identifies these public dataset options:

### Option A — UCI Appliances Energy Prediction
URL: https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction

Contains appliance energy-consumption measurements and environmental features such as temperature and humidity. Useful for exploring consumption patterns and possible relationships with environmental conditions.

### Option B — UCI Individual Household Electric Power Consumption
URL: https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption

Contains household electricity measurements, including active power, voltage, current intensity, and sub-metering values. Useful for time-series analysis and anomaly detection.

### Option C — UCI Power Consumption of Tetouan City
URL: https://archive.ics.uci.edu/dataset/849/power+consumption+of+tetouan+city

Contains consumption measurements from three distribution networks. Useful for peak-demand analysis and comparisons between networks.

### Dataset selection guidance

Choose one dataset for the initial prototype rather than attempting to support every format immediately.

- Choose Appliances Energy Prediction if environmental features are important to your planned analysis.
- Choose Tetouan City if demand patterns and peak-load identification are the primary focus.
- Choose Individual Household Electric Power Consumption if you want detailed household electrical measurements.

Before implementing the pipeline:
1. Inspect the dataset's actual column names, units, timestamp format, frequency, and missing values.
2. Select the main consumption variable.
3. Decide how to aggregate the readings.
4. Decide how to establish normal usage and evaluate anomalies.
5. Document any transformations and assumptions.

A public dataset does not necessarily contain building names, occupancy, equipment state, or labelled waste events. Do not assume these fields exist.

---

## 8. Recommendation Logic Examples

Use transparent rules first. Thresholds must be tuned to the selected dataset and should not be presented as universal values.

| Detected pattern | Evidence to show | Possible recommendation |
|---|---|---|
| Overnight usage above its usual baseline | Current overnight usage compared with similar historical nights | Check equipment schedules and whether overnight operation was expected |
| Repeated high-demand interval | Dates, times, and consumption values of recurring peaks | Review operating schedules and possible demand-management options |
| Unusual consumption spike | Timestamp, measured value, expected baseline, anomaly score/flag | Investigate the event and check for unusual equipment or operating conditions |
| Consistently elevated consumption | Trend compared with comparable days or periods | Review available equipment, occupancy, and operational context |

Recommendations should be conditional on evidence. For example, without occupancy data, the application cannot reliably conclude that a room was empty.

---

## 9. Testing and Evaluation

A hackathon-quality solution should show evidence that its analysis is useful and reasonably reliable.

### Functional tests

- Valid CSV upload works.
- Invalid file types and missing required columns produce helpful errors.
- Timestamps and numeric values are parsed correctly.
- Missing values are handled consistently.
- Charts match the processed dataset.
- Peak intervals match the chosen peak-detection rule.
- Anomaly flags can be traced to individual readings.
- Recommendations refer to actual calculated findings.
- The interface handles empty results and failed analysis gracefully.

### Model evaluation

For anomaly detection:
- Use labelled anomalies if available.
- If labels are unavailable, create carefully documented synthetic test cases or perform a reviewed sample-based assessment.
- Report precision, recall, and F1-score only when a suitable labelled evaluation set exists.
- If using synthetic cases, explicitly say that the evaluation is synthetic and does not prove real-world accuracy.

For peak detection:
- Compare results against a documented threshold or reference calculation.
- Verify that peak timestamps and values are correct.
- Explain the definition of “peak” used.

### Impact evaluation

Possible measures:
- Processing time for a dataset of a stated size.
- Number and proportion of flagged readings.
- Anomaly detection metrics on a labelled test set.
- Agreement between peak detection and a documented reference rule.
- Estimated cost implications using an explicit tariff and assumptions.

Do not claim that the application has reduced real electricity consumption unless an actual before-and-after measurement supports that conclusion.

---

## 10. Feasibility, Risks, and Mitigations

| Risk | Mitigation |
|---|---|
| Different datasets use different column names | Add column mapping or dataset-specific configuration |
| Missing or invalid readings | Validate input and document cleaning decisions |
| False anomaly alerts | Use suitable baselines, tune the model, and present alerts as items to investigate |
| Legitimate peak classified as waste | Separate peak detection from anomaly detection and avoid unsupported claims |
| Recommendations are too generic | Attach each recommendation to a specific measured pattern |
| LLM invents explanations | Base explanations on computed results and constrain claims to available evidence |
| No live smart-meter access | Use historical CSV data for the first demo |
| Demo or deployment fails | Keep a local working version and a prepared sample dataset |

---

## 11. Implementation Plan

Build the smallest complete working version before adding advanced features.

### Phase 1 — Data and baseline analytics
- Select one dataset.
- Inspect and clean the data.
- Implement consumption summaries and charts.
- Implement peak-load detection.
- Validate the results with simple test cases.

### Phase 2 — Anomaly detection
- Establish a statistical baseline.
- Implement Isolation Forest if appropriate for the selected features.
- Compare its flags with the baseline and test cases.
- Display the timestamp, reading, and reason for review.

### Phase 3 — Recommendations
- Write rule-based recommendations for the supported patterns.
- Link every recommendation to calculated evidence.
- Add caveats when the data cannot identify a cause or quantify savings.

### Phase 4 — Web application
- Build the React dashboard.
- Implement the FastAPI endpoints required by the UI.
- Connect file upload, analytics results, charts, alerts, and recommendations.
- Add clear loading, success, and error states.

### Phase 5 — Testing and hackathon preparation
- Test the full upload-to-results flow.
- Check charts and metrics against the source data.
- Prepare a sample CSV and reliable demo path.
- Record genuine screenshots of the working product.
- Prepare a short backup demo if possible.
- Document the actual stack, model choices, test results, and limitations.

---

## 12. User Interface Plan

Suggested dashboard layout:

```text
+---------------------------------------------------------------+
| EnergyIQ                           Date Filter | Upload Dataset|
+---------------------------------------------------------------+
| Total Consumption | Average Usage | Peak Periods | Anomalies  |
+---------------------------------------------------------------+
|                                                               |
|               Consumption Trend Over Time                     |
|                                                               |
+--------------------------------+------------------------------+
| Peak-Demand Periods             | Anomaly Alerts               |
|                                |                              |
+--------------------------------+------------------------------+
| Evidence-Based Recommendations                                |
| - Observation                                                   |
| - Evidence / comparison                                         |
| - Suggested action                                              |
+---------------------------------------------------------------+
```

This is a layout concept, not a screenshot of an already implemented product. Adapt the UI to the selected dataset and screen size.

---

## 13. Hackathon Presentation Requirements

The provided HACKNOVA’26 presentation template has a maximum of 10 slides, including the title and Thank You slides. Delete the template's separate instruction slide before submission.

Suggested slide mapping:

1. **Title and team information** — EnergyIQ, PS-1, team details, repository/demo links.
2. **Problem statement and existing challenges** — Raw data, hidden patterns, target users.
3. **Proposed solution** — Product overview and core features.
4. **Technical approach and workflow** — Data processing, peak detection, anomaly detection, recommendations.
5. **System architecture** — Frontend, backend, analytics, and data flow.
6. **Technology stack and implementation** — Actual libraries, models, dataset, and deployment.
7. **Prototype and key features** — Genuine screenshots and actual outputs.
8. **Feasibility, impact, and benefits** — Target users, risks, limitations, measured results.
9. **Extra slide** — Innovation, validation, or future scope; prioritize real evidence.
10. **Thank You / Q&A** — Closing statement and demo link.

Keep the presentation concise. Demonstrate a complete working pipeline instead of claiming many unfinished features.

---

## 14. Current Decisions and Items to Confirm

The following items have not been confirmed in the project context and should be decided by the team:

- [ ] Final dataset.
- [ ] Final frontend framework and styling library.
- [ ] Final backend framework.
- [ ] Whether the team will use Isolation Forest, a statistical baseline, or both.
- [ ] Final peak-detection definition.
- [ ] Required dataset columns and units.
- [ ] Whether a database is needed.
- [ ] Whether conversational AI will be included in the hackathon build.
- [ ] Deployment platform.
- [ ] Team name, members, GitHub URL, and demo URL.
- [ ] Actual testing results and evaluation metrics.

**Recommended default plan:** Start with one CSV dataset, React, FastAPI, Pandas, scikit-learn, and Plotly. Implement consumption analytics, peak detection, anomaly flags, evidence-based rules, and the dashboard. Add optional features only after the end-to-end pipeline works.

---

## 15. Instructions for Any AI Assistant Helping With EnergyIQ

When this document is pasted into a new AI conversation, follow these rules:

1. Treat this document as the project's main context.
2. Do not ask the user to repeat information already stated here.
3. First identify which decisions are confirmed and which remain open.
4. Do not claim a feature, model, test result, deployment, or metric is implemented unless the user confirms it or the code/evidence demonstrates it.
5. Prefer a simple, maintainable solution that can be completed during a hackathon.
6. Keep the frontend, API, data processing, anomaly detection, and recommendation logic modular.
7. Inspect the actual dataset schema before writing dataset-specific code.
8. Provide complete, runnable code for requested files, with file paths and setup/run commands.
9. Explain required environment variables and dependencies without exposing secrets.
10. Handle malformed input, missing values, empty results, and errors.
11. Make recommendations traceable to calculated evidence.
12. Do not fabricate energy savings, anomaly accuracy, causes, or real-world impact.
13. When changing the architecture or stack, explain the reason and update this context document.
14. When debugging, ask for the relevant code, error, or project structure only if it is not already available.
15. Prioritize a complete end-to-end prototype over unnecessary complexity.

### First task for a new AI assistant

Help the team turn this plan into a working EnergyIQ prototype. Start by confirming the selected dataset and current project files, then implement the smallest complete end-to-end flow: CSV input → validation/preprocessing → consumption and peak analytics → anomaly detection → evidence-based recommendations → dashboard. Keep optional features out of the critical path until this works.

---

**Document status:** Project specification and implementation guide. The technology stack and several features above are proposals until the team confirms or implements them. Update this file as the project evolves.
