# ASF Dataset — 100 Cases (v0.1 Illustrative)

This dataset applies the ASF universal model to 100 systems across 10 domains.

**Status:** v0.1 illustrative — built from public information, research, and structured inference.
Not proprietary data. Intended as a research baseline for pattern validation.

---

## Coverage

| Domain | Cases | Avg Latency Score | High Risk | Low Risk |
|---|---|---|---|---|
| AI Systems | 10 | 2.53 | 0 | 7 |
| Data & Cloud Platforms | 10 | 2.64 | 0 | 4 |
| Manufacturing & Industrial | 10 | 2.92 | 1 | 2 |
| Retail & Consumer | 10 | 2.91 | 0 | 1 |
| Finance & Healthcare | 10 | 3.08 | 0 | 2 |
| Entertainment & Media | 10 | 3.15 | 1 | 1 |
| Logistics & Transport | 10 | 3.21 | 1 | 1 |
| Telecom & Networks | 10 | 3.58 | 1 | 0 |
| Human / Social / Natural Systems | 10 | 3.62 | 1 | 0 |
| Historical Adaptive Systems | 10 | 4.26 | 9 | 1 |

**Overall mean latency score: 3.19 / 5.0**

---

## Schema

Each case contains 20 fields:

| Field | Description |
|---|---|
| Case ID | Unique identifier |
| System Name | Organization or system |
| Domain | One of 10 domain categories |
| System Type | e.g. AI Lab, Enterprise, Nation-State |
| Adaptation Scenario | What change the system needed to make |
| Input Event / Trigger | What forced the adaptation |
| Adaptation Requirement | What the system needed to develop |
| Current Operating State | Maturity at time of trigger |
| Observation Latency (1-5) | Speed of signal detection |
| Decision Latency (1-5) | Speed of committing to response |
| Execution Latency (1-5) | Speed of implementation |
| Feedback Delay (1-5) | Speed of observing outcomes |
| Learning Velocity (1-5) | Rate of improvement across cycles |
| Dependency Index (1-5) | Degree of manual/approval/coordination dependency |
| Primary Friction | Dominant friction source |
| Control Layer Needed | Yes/No/Partial |
| Intervention Hypothesis | Recommended action |
| Adaptation Latency Score | Composite score (weighted average) |
| Risk Band | Low / Medium / High |
| Dataset Status | Version and data provenance |

---

## Scoring Model

```
Adaptation Latency Score =
    (Observation Latency × 0.15)
  + (Decision Latency    × 0.25)
  + (Execution Latency   × 0.30)
  + (Feedback Delay      × 0.15)
  + (Dependency Index    × 0.15)
  — (Learning Velocity   × 0.10)  ← reduces score (accelerator)
```

Scale: 1.0 (fastest) → 5.0 (slowest / most at risk)

---

## Key Findings from v0.1 Data

### Fastest Adapters (score < 2.0)
| System | Score | Why Fast |
|---|---|---|
| Toyota | 1.20 | Lean culture = built-in friction reduction |
| CAST AI | 1.60 | Born automated; minimal human dependency |
| Singapore Airlines | 1.95 | Operational discipline + feedback loops |
| Amazon Retail | 1.95 | Data infrastructure enables fast decisions |
| Netflix | 1.95 | Platform rebuild complete; low residual friction |

### Slowest Adapters (score > 4.0)
| System | Score | Primary Friction |
|---|---|---|
| Sears | 4.85 | Legacy operating model |
| Coral Reef Ecosystem | 4.75 | Environmental stress exceeds adaptation capacity |
| Kodak | 4.70 | Revenue protection inertia |
| Blockbuster | 4.70 | Business model inertia |
| Nokia Mobile | 4.50 | Platform transition + decision delay |

### Domain Patterns
- **AI Systems** show the lowest average latency (2.53) — new organizations, minimal legacy
- **Historical cases** show the highest (4.26) — confirming the framework's core hypothesis
- **Telecom** (3.58) and **Human/Social** (3.62) are the hardest active domains
- **Decision Latency** is the strongest individual predictor of high risk across all domains
- **Learning Velocity** is the strongest differentiator between fast and slow adapters

### Hypothesis Validation (preliminary)
- **H4 confirmed:** All 9 high-risk historical cases show evidence of recognition before failure
- **H3 supported:** Dependency Index correlates with Risk Band across domains
- **H6 supported:** Organizational friction dominates in telecom and historical cases
- **H2 supported:** Low-latency systems (Toyota, Netflix, Amazon) all show high learning velocity

---

## Files

- `asf_100_cases.csv` — flat CSV, all 100 cases
- `adaptive_systems_framework_100_cases.xlsx` — Excel workbook with formatting

---

## Next Steps

1. Validate scores against primary sources where available
2. Add 50 additional cases (target: government, healthcare, climate)
3. Build regression model to identify which friction categories most predict high risk
4. Publish v0.2 with expanded methodology notes
