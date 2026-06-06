# ASF Product Architecture — v0.1

## Overview

The Adaptive Systems Framework is built as a five-layer pipeline.
Each layer has a single responsibility. Data flows in one direction.
The feedback loop is handled externally — outputs feed back into new input events.

---

## Pipeline

```
┌─────────────────────────────────────────────────────┐
│                    Data Sources                     │
│  Annual Reports · Incident Data · AI Metrics        │
│  Operational KPIs · User Input                      │
└─────────────────────────┬───────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│            Adaptive Analysis Engine                 │
│  Observation · Decision · Execution                 │
│  Feedback · Learning · Dependency                   │
└─────────────────────────┬───────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│                  Scoring Engine                     │
│  Adaptation Score · Latency Score                   │
│  Friction Score · Risk Classification               │
└─────────────────────────┬───────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│             Recommendation Engine                   │
│  Root Cause Analysis · Suggested Interventions      │
│  Improvement Actions                                │
└─────────────────────────┬───────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│               Dashboard / API                       │
│  Visual Dashboard · REST API · Report Export        │
└─────────────────────────────────────────────────────┘
```

---

## Layer 1 — Data Sources

**Responsibility:** Ingest all inputs required for analysis.

| Source | Description | Format |
|---|---|---|
| Annual reports | Public filings, earnings calls, 10-K/10-Q | Text, PDF |
| Incident data | Post-mortems, SRE data, failure reports | Structured / text |
| AI metrics | Token spend, model usage, latency, cost | JSON / API |
| Operational KPIs | Deployment frequency, MTTR, cycle time | Structured |
| User input | Manual ASF diagnostic form | YAML / JSON |

**Key principle:** All inputs are normalized to the ASF model schema before entering the analysis engine.

---

## Layer 2 — Adaptive Analysis Engine

**Responsibility:** Score each of the six analysis dimensions independently.

| Analyzer | Metric Produced | What It Measures |
|---|---|---|
| Observation analysis | Observation Latency (1-5) | How quickly change is detected |
| Decision analysis | Decision Latency (1-5) | How long commitment takes |
| Execution analysis | Execution Latency (1-5) | How quickly decisions become reality |
| Feedback analysis | Feedback Delay (1-5) | How quickly outcomes are observable |
| Learning analysis | Learning Velocity (1-5) | How effectively feedback improves future behavior |
| Dependency analysis | Dependency Index (1-5) | Degree of manual/approval dependency |

Each analyzer produces a structured output that flows into the scoring engine.

---

## Layer 3 — Scoring Engine

**Responsibility:** Compute composite scores and classify risk.

### Scoring Formula

```
Adaptation Latency Score =
    (Observation Latency  × 0.15)
  + (Decision Latency     × 0.25)
  + (Execution Latency    × 0.30)
  + (Feedback Delay       × 0.15)
  + (Dependency Index     × 0.15)
  − (Learning Velocity    × 0.10)
```

### Risk Classification

| Score Range | Risk Band | Action |
|---|---|---|
| 1.0 – 2.4 | Low | Monitor; maintain current trajectory |
| 2.5 – 3.4 | Medium | Investigate; targeted interventions |
| 3.5 – 4.9 | High | Urgent; systemic intervention required |

### Additional Scores

- **Friction Score:** Weighted sum of active friction sources
- **Adaptation Score:** Inverse of Latency Score — measures adaptation capability

---

## Layer 4 — Recommendation Engine

**Responsibility:** Translate scores into actionable recommendations.

### Root Cause Analysis
Maps high scores on individual latency dimensions to likely friction sources.

| High Dimension | Most Likely Friction |
|---|---|
| Decision Latency | Governance delay, ownership ambiguity |
| Execution Latency | Manual dependency, legacy systems |
| Observation Latency | Data quality, tooling gaps |
| Feedback Delay | Missing observability, measurement gaps |
| Learning Velocity (low) | No postmortem culture, knowledge silos |
| Dependency Index | Manual approvals, coordination overhead |

### Intervention Priority
Recommendations are ranked P0 / P1 / P2 based on:
- Latency reduction potential
- Implementation effort
- Risk reduction impact

### Output Format
```yaml
recommendations:
  - priority: p0
    action: ""
    target_dimension: ""
    expected_latency_reduction_weeks: 0
    effort_estimate: ""
  - priority: p1
    ...
```

---

## Layer 5 — Dashboard / API

**Responsibility:** Surface results to humans and downstream systems.

### Visual Dashboard
- Domain-level latency heatmap
- Risk band distribution
- Layer-by-layer radar chart
- Case explorer with filtering
- Intervention tracker

### REST API

```
GET  /api/v1/cases                    # List all analyzed cases
GET  /api/v1/cases/{id}               # Get single case with full scores
POST /api/v1/analyze                  # Submit new system for analysis
GET  /api/v1/recommendations/{id}     # Get recommendations for a case
GET  /api/v1/domains                  # Domain-level aggregates
GET  /api/v1/scores/distribution      # Score distribution across dataset
```

### Report Export
- PDF: Executive summary with scores and top 3 interventions
- CSV: Full dataset export
- YAML: Machine-readable case output for downstream integration

---

## Data Flow Summary

```
Raw input
  → Normalized to ASF schema
  → Six-dimension analysis
  → Composite scoring + risk classification
  → Root cause mapping + intervention ranking
  → Dashboard / API / Report
  → Human reviews and acts
  → Outcome measured
  → Feeds back as new input event
```

---

## Token Cost Layer (AI-Assisted Analysis)

When the analysis engine uses LLM-assisted scoring (e.g. analyzing annual report text):

```
Input tokens:   Document ingestion + prompt
Analysis tokens: Per-dimension scoring
Output tokens:  Structured YAML score output
```

**Cost control principles:**
- Chunk documents; do not pass full 200-page annual reports in a single context
- Cache scoring results; re-analyze only on new data ingestion
- Use smaller models for structured extraction; larger models for root cause synthesis
- Track cost-per-case; flag cases where AI spend exceeds intervention value

This is the AI spend problem ASF solves for others — applied to itself.

---

## Implementation Roadmap

| Phase | Scope | Status |
|---|---|---|
| v0.1 | Manual YAML input, scoring formula, 100-case dataset | Done |
| v0.2 | Python scoring engine, CLI tool, report export | Next |
| v0.3 | REST API, LLM-assisted analysis engine | Planned |
| v0.4 | Visual dashboard, domain benchmarking | Planned |
| v1.0 | Full pipeline, multi-source ingestion, production API | Future |
