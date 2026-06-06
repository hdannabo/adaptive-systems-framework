# ASF Formulas

This document defines all quantitative formulas in the Adaptive Systems Framework. These are the mathematical core of ASF — turning qualitative observations into measurable, comparable scores.

---

## Core Formula: Adaptation Latency Score

The primary ASF metric. Measures how slowly a system adapts relative to its maximum capability.

```
Adaptation Latency Score =
    (Observation Latency  × 0.15)
  + (Decision Latency     × 0.25)
  + (Execution Latency    × 0.30)
  + (Feedback Delay       × 0.15)
  + (Dependency Index     × 0.15)
  − (Learning Velocity    × 0.10)
```

**Scale:** 1.0 (fastest) → 5.0 (slowest)

**Weight rationale:**
- Execution carries the highest weight (0.30) — the most common bottleneck across all 100 cases
- Decision carries the second-highest weight (0.25) — governance failure is the dominant failure mode in historical cases
- Learning Velocity subtracts from the score — it is the primary accelerator

---

## Observation Latency Formula

```
Observation Latency (weeks) =
    Detection Date − Signal Emergence Date

Where:
  Signal Emergence Date = date the trigger event became observable
  Detection Date        = date the system acknowledged the signal
```

**Scoring guide:**
| Weeks to Detect | Score |
|---|---|
| < 1 week | 1 |
| 1–2 weeks | 2 |
| 2–4 weeks | 3 |
| 1–3 months | 4 |
| > 3 months | 5 |

---

## Decision Latency Formula

```
Decision Latency (weeks) =
    Commitment Date − Detection Date

Where:
  Detection Date   = date the signal was acknowledged
  Commitment Date  = date a course of action was formally approved
```

**Approval overhead multiplier:**
```
Adjusted Decision Latency =
    Base Decision Latency × (1 + (Approval Gates × 0.15))
```

Each additional approval gate adds ~15% to decision latency based on empirical observation across the 100-case dataset.

---

## Execution Latency Formula

```
Execution Latency (weeks) =
    Operational Date − Commitment Date

Where:
  Commitment Date  = date the decision was made
  Operational Date = date the change was live and measurable
```

**Manual dependency multiplier:**
```
Adjusted Execution Latency =
    Base Execution Latency × (1 + (Manual Steps / Total Steps) × 0.5)
```

---

## Total Adaptation Latency Formula

```
Total Adaptation Latency =
    Observation Latency
  + Decision Latency
  + Execution Latency
  + Feedback Delay

Units: weeks

Adaptation Gap =
    Total Adaptation Latency − Target Latency
```

---

## Learning Velocity Formula

```
Learning Velocity =
    Improvements Implemented / Time Period
  × Recurrence Prevention Rate

Where:
  Improvements Implemented    = process changes, automations, runbook updates
  Time Period                 = quarter or year
  Recurrence Prevention Rate  = 1 − (Repeated Incidents / Total Incidents)
```

**Scoring guide:**
| Characteristics | Score |
|---|---|
| No postmortems, incidents repeat | 1 |
| Postmortems exist, rarely actioned | 2 |
| Some improvements implemented | 3 |
| Systematic improvement program | 4 |
| Kaizen culture, improvements compound | 5 |

---

## Dependency Index Formula

```
Dependency Index =
    (Manual Steps / Total Steps) × 0.40
  + (Approval Gates / Optimal Gates) × 0.35
  + (External Blockers / Total Blockers) × 0.25
```

**Scoring guide:**
| Profile | Score |
|---|---|
| Fully automated, policy-as-code | 1 |
| Mostly automated, few manual steps | 2 |
| Mix of manual and automated | 3 |
| Mostly manual, some automation | 4 |
| Fully manual, many approval gates | 5 |

---

## Friction Score Formula

```
Friction Score =
    (Max Single Dimension Score × 0.50)
  + (Average of All Dimensions  × 0.50)

Where dimensions =
    Observation Latency, Decision Latency, Execution Latency,
    Feedback Delay, Dependency Index
```

The Friction Score amplifies the single worst bottleneck — consistent with the Theory of Constraints (Goldratt): the system is limited by its weakest link.

---

## Adaptation Capability Formula

```
Adaptation Capability = 6.0 − Adaptation Latency Score

Range: 1.0 (minimum capability) to 5.0 (maximum capability)
```

This is the inverse of latency — how capable of adaptation the system actually is.

---

## Adaptation Debt Formula

```
Adaptation Debt =
    Σ (Friction Score × Weeks Unresolved)

Units: friction-weeks

Interpretation:
  < 10  = manageable
  10–25 = significant — intervention warranted
  > 25  = critical — systemic intervention required
```

Adaptation Debt compounds. A friction score of 4 unresolved for 10 weeks = 40 friction-weeks. The longer it goes unaddressed, the harder it becomes to reduce.

---

## LLM Adaptation Efficiency Formula

```
LLM Adaptation Efficiency =
    (Task Accuracy           × 0.30)
  + (Context Utilization     × 0.20)
  + (Retrieval Precision     × 0.20)
  + (Reasoning Depth         × 0.15)
  + (Feedback Responsiveness × 0.15)

Scale: 0–100
```

---

## Effective Context Utilization Formula

```
Effective Context Utilization =
    Useful Output Tokens / Total Input Tokens Consumed

Where:
  Useful Output Tokens = tokens contributing to task completion
  Total Input Tokens   = full prompt + context + retrieval payload
```

**Benchmark targets:**
| ECU | Assessment |
|---|---|
| > 0.40 | High efficiency |
| 0.20–0.40 | Acceptable |
| < 0.20 | Context waste — optimize prompt or retrieval |

---

## Context Rot Detection Formula

```
Context Rot Score =
    1 − (Performance at 80% context / Performance at 20% context)

Where Performance = task accuracy at given context fill level

Interpretation:
  < 0.05 = negligible degradation
  0.05–0.15 = moderate — monitor
  0.15–0.30 = significant — redesign context strategy
  > 0.30 = severe — context window is a liability
```

---

## Agent Efficiency Formula

```
Agent Efficiency Ratio =
    Task Value / Total Token Cost

Where:
  Task Value   = business outcome score (0–10)
  Token Cost   = total tokens consumed × cost per token

Loop Overhead =
    (Agent Tokens − Baseline Tokens) / Baseline Tokens

Cost Per Adaptation =
    Total Agent Cost / Number of Successful Adaptations
```

---

## Platform Engineering Adaptation Score

```
Platform Adaptation Score =
    (Deployment Frequency    × 0.25)
  + (MTTR Efficiency         × 0.25)
  + (Automation Coverage     × 0.20)
  + (Change Success Rate     × 0.20)
  + (Upgrade Cycle Speed     × 0.10)

Where each dimension is normalized to 1–5 scale.
```

---

## Manufacturing Adaptation Score

```
Manufacturing Adaptation Score =
    (Defect Detection Speed  × 0.25)
  + (Root Cause Cycle Time   × 0.25)
  + (Kaizen Velocity         × 0.20)
  + (First Pass Yield        × 0.20)
  + (Supplier Adaptation     × 0.10)
```

---

## Enterprise AI ROI Formula

```
AI Value Realization Score =
    (Adoption Velocity       × 0.30)
  + (Value Realization Speed × 0.25)
  + (ROI Efficiency          × 0.25)
  + (Cost Predictability     × 0.20)

ROI Efficiency =
    Measured Business Value / Total AI Spend

Value Realization Lag =
    First Value Date − Deployment Date  (weeks)
```

---

## Summary

| Formula | Application | Primary Signal |
|---|---|---|
| Adaptation Latency Score | All domains | Overall adaptation speed |
| Total Adaptation Latency | All domains | Calendar time from recognition to operation |
| Adaptation Debt | All domains | Cost of unresolved friction |
| LLM Adaptation Efficiency | AI systems | Value per token |
| Effective Context Utilization | AI systems | Context efficiency |
| Context Rot Score | AI systems | Window degradation |
| Agent Efficiency Ratio | AI agents | Value per dollar |
| Platform Adaptation Score | Platform engineering | Delivery velocity |
| Manufacturing Adaptation Score | Manufacturing | Quality loop speed |
| Enterprise AI ROI Score | Enterprise | AI investment efficiency |

All formulas share the same principle:

> **Measure the delay between stimulus and adapted response. Identify the friction causing that delay. Reduce it.**
