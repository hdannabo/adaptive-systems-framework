# Capability Realization Time (CRT)

## What CRT is

CRT is a derived ASF metric.

**ASF finds the Adaptation Gap. CRT estimates how long it may take to close it.**

```
Adaptation Gap = Required Capability Score − Current Capability Score
```

The adaptation gap tells you how far a system is from where it needs to be.
CRT tells you how long it will take to get there — given current friction levels.

---

## Why CRT matters

Organizations set targets. They rarely estimate how long it will take to reach them
given the friction they are carrying. The result: missed deadlines, budget overruns,
and stakeholder disappointment.

CRT makes the time cost of friction visible before it becomes a missed target.

---

## The formula

```
CRT = Gap × Base Time × Friction Multiplier × Learning Accelerator

Where:
  Gap                = Required Capability − Current Capability
  Base Time          = domain-specific baseline months per capability point
  Friction Multiplier = 1 + (Governance Friction × 0.30)
                          + (Execution Friction  × 0.40)
                          + (Dependency Risk     × 0.30)
  Learning Accelerator = 1 − (Learning Velocity × 0.35)
```

Execution friction carries the highest weight (0.40) because it is the
dominant delay source across all domains in the ASF 100-case dataset.

---

## Risk classification

| CRT | Risk Level | Interpretation |
|---|---|---|
| < 6 months | Low | Achievable within a standard planning cycle |
| 6–18 months | Medium | Requires sustained effort over 1–2 planning cycles |
| 18–36 months | High | Multi-year investment; milestone tracking essential |
| > 36 months | Critical | Fundamental intervention required; current friction rate too high |

---

## Inputs

| Input | Scale | Description |
|---|---|---|
| required_capability_score | 1.0–10.0 | Target capability level |
| current_capability_score | 1.0–10.0 | Current capability level |
| governance_friction | 0.0–1.0 | Approval overhead, policy delays |
| execution_friction | 0.0–1.0 | Manual steps, legacy systems, integration complexity |
| dependency_risk | 0.0–1.0 | External blockers, coordination overhead |
| learning_velocity | 0.0–1.0 | How fast the system improves per cycle |
| evidence_confidence | 0.0–1.0 | Reliability of input data |
| objective_integrity_score | 0.0–1.0 | How well-defined and stable the goal is |
| base_realization_time_months | months | Domain baseline per capability point |

---

## Outputs

| Output | Description |
|---|---|
| adaptation_gap | Gap between required and current capability |
| crt_months | Estimated months to close the gap |
| crt_years | CRT in years |
| crt_range_low_months | Lower bound of confidence interval |
| crt_range_high_months | Upper bound of confidence interval |
| crt_risk_level | Low / Medium / High / Critical |
| primary_bottleneck | Dominant friction source |
| governance_readiness_score | 0–1 governance quality score |
| evidence_confidence_score | 0–1 input reliability score |
| plain_english_explanation | Non-technical explanation of results |

---

## Governance alignment

| Framework | CRT Alignment |
|---|---|
| NIST AI RMF — MANAGE | Prioritize risk responses based on gap and friction |
| EU AI Act — Article 9 | Risk management documentation with time estimates |
| ISO 42001 — Clause 6 | Planning: quantify risks with realization timelines |
| COBIT EDM02 | Ensure benefits delivery with time-bounded estimates |
| ITIL 4 — Continual Improvement | Track progress toward capability targets |

---

## Usage

```python
from src.asf.scoring.crt_engine import CRTInput, calculate_crt

inp = CRTInput(
    system_name="Enterprise AI Program",
    use_case="AI-driven operations",
    required_capability_score=8.0,
    current_capability_score=3.5,
    governance_friction=0.65,
    execution_friction=0.70,
    dependency_risk=0.55,
    learning_velocity=0.45,
    evidence_confidence=0.80,
    objective_integrity_score=0.75,
    base_realization_time_months=4.0,
)

result = calculate_crt(inp)
print(result.crt_months)            # e.g. 28.4
print(result.crt_risk_level)        # High
print(result.plain_english_explanation)
```

---

## Relationship to ASF

CRT does not replace ASF. It extends it.

ASF diagnoses **why** a system is not adapting fast enough.
CRT estimates **how long** it will take to close the gap at current friction levels.

Together:
- ASF → Adaptation Gap + Bottleneck + Intervention
- CRT → Time to close gap + Confidence range + Governance readiness
