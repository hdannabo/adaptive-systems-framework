# ASF Product Architecture

## Overview

ASF is built as a five-layer pipeline. Each layer has a single responsibility.

```
Data Sources
    ↓
Adaptive Analysis Engine
    ↓
Scoring Engine
    ↓
Recommendation Engine
    ↓
Dashboard / API
```

## Layer 1 — Data Sources

| Source | Format | Notes |
|---|---|---|
| Annual reports | PDF, text | Public filings, earnings calls |
| Incident data | Structured | Post-mortems, SRE reports |
| AI metrics | JSON / API | Token spend, latency, cost |
| Operational KPIs | Structured | DORA metrics, deployment frequency |
| User input | YAML / JSON | Manual diagnostic form |

## Layer 2 — Adaptive Analysis Engine

Six analyzers run in parallel, one per ASF dimension:

| Analyzer | Metric | Weight |
|---|---|---|
| Observation | Observation Latency | 0.15 |
| Decision | Decision Latency | 0.25 |
| Execution | Execution Latency | 0.30 |
| Feedback | Feedback Delay | 0.15 |
| Learning | Learning Velocity | −0.10 (accelerator) |
| Dependency | Dependency Index | 0.15 |

## Layer 3 — Scoring Engine

```python
ALS = (OL × 0.15) + (DL × 0.25) + (EL × 0.30)
    + (FD × 0.15) + (DI × 0.15) − (LV × 0.10)

Risk bands:
  ALS < 2.5  → Low
  ALS < 3.5  → Medium
  ALS >= 3.5 → High
```

## Layer 4 — Recommendation Engine

Maps bottleneck dimension to friction type to prioritized interventions.

| Bottleneck | Friction | P0 Intervention |
|---|---|---|
| Execution Latency | Manual dependency | Automate top 3 manual handoffs |
| Decision Latency | Governance delay | Replace CAB gates with policy-as-code |
| Feedback Delay | Missing observability | Zero blind spots — full telemetry |
| Observation Latency | Data / tooling gap | Instrument observability pipelines |
| Dependency Index | Manual approvals | Map and eliminate critical path dependencies |

## Layer 5 — Dashboard / API

- `dashboard/token-governance.html` — interactive governance scorer
- `dashboard/enterprise-benchmark.html` — 5-company benchmark
- `dashboard/manufacturing-benchmark.html` — global manufacturing
- `dashboard/token-economics.html` — 22-model token efficiency
- `research/asf-dashboard.html` — 100-case explorer

REST API (v0.4, planned):
```
POST /api/v1/analyze/document
POST /api/v1/analyze/form
GET  /api/v1/cases
GET  /api/v1/health
```

## Source Code Structure

```
src/asf/
├── models.py              # AnalysisInput, LayerScores, ASFReport
├── analyzer.py            # Main pipeline — wires all engines
├── scoring/engine.py      # Deterministic scoring computation
└── recommendations/engine.py  # Bottleneck → intervention mapping
```
