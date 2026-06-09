# ASF Engine Design — Modular Architecture

## Design Principle

ASF is a **modular pipeline**. Each stage takes structured input and produces structured output.
No stage depends on the implementation of another stage — only the interface contract.
This makes ASF usable as:
- A Python library (current)
- An Azure Function (v0.4)
- An AI agent reasoning framework
- A consulting methodology worksheet
- A strategy assessment model

---

## Engine Pipeline

```
┌─────────────────────────────────────────────────────┐
│                    ASF ENGINE                        │
│                                                     │
│  Input           Processing              Output     │
│  ────────        ──────────────          ───────    │
│  Strategic   →   Awareness          →    Gap        │
│  Goals           Detection               Score      │
│                                                     │
│  Current     →   Capability         →    Friction   │
│  State           Mapping                 Profile    │
│                                                     │
│  Evidence    →   Gap Analysis       →    CRT        │
│                                                     │
│  Constraints →   Friction Analysis  →    Bottleneck │
│                                                     │
│  Dependencies →  CRT Estimation     →    Actions    │
│                                                     │
│                  Recommendation     →    Summary    │
│                  Generation                         │
└─────────────────────────────────────────────────────┘
```

---

## Module 1 — Awareness Detection

**Purpose:** Determine whether the system has correctly identified what needs to change.

**Inputs:**
```python
class AwarenessInput:
    signal_type: str            # "market", "incident", "regulatory", "technology"
    signal_detected: bool       # Did the system receive the signal?
    signal_understood: bool     # Was the signal correctly interpreted?
    time_to_detection_days: float  # How long from signal emergence to detection?
    confidence: float           # 0.0–1.0 — how confident are we in this assessment?
```

**Outputs:**
```python
class AwarenessOutput:
    awareness_complete: bool
    awareness_score: float         # 0.0–1.0 (higher = more aware)
    observation_latency_score: int # 1–5 for ALS formula
    gap: str                       # Explanation of awareness gap if present
```

**Decision it supports:** Is this an awareness problem or an execution problem?
If awareness is incomplete, the intervention is measurement and signal detection.
If awareness is complete, the intervention is execution and governance.

---

## Module 2 — Capability Mapping

**Purpose:** Define the required state and measure the current state.

**Inputs:**
```python
class CapabilityInput:
    objective: str              # The stated goal in plain English
    required_capability: float  # Target state on 1–10 scale
    current_capability: float   # Current state on 1–10 scale
    target_date: str            # ISO date — when must the gap be closed?
    domain: str                 # "AI", "cloud", "manufacturing", "sustainability"...
    evidence: str               # What data supports these scores?
    confidence: float           # 0.0–1.0 — how reliable is this measurement?
```

**Outputs:**
```python
class CapabilityOutput:
    adaptation_gap: float          # G = required - current
    velocity_required: float       # Gap / months_remaining
    velocity_current: float        # Current measured rate of change (if known)
    velocity_sufficient: bool      # Is current velocity enough?
    days_to_deadline: int
    months_to_deadline: float
```

**Decision it supports:** Is the gap large enough to warrant concern? Is there time to close it?

---

## Module 3 — Friction Analysis

**Purpose:** Score the six ASF dimensions and identify the primary bottleneck.

**Inputs:**
```python
class FrictionInput:
    observation_latency: int  # 1–5 (1=fast, 5=slow)
    decision_latency: int     # 1–5
    execution_latency: int    # 1–5
    feedback_delay: int       # 1–5
    learning_velocity: int    # 1–5 (1=slow, 5=fast — INVERTED)
    dependency_index: int     # 1–5 (1=few, 5=many)
    evidence: dict            # {dimension: "evidence string"} for each dimension
```

**Outputs:**
```python
class FrictionOutput:
    adaptation_latency_score: float  # Weighted ALS
    risk_band: str                   # "Low" / "Medium" / "High"
    primary_bottleneck: str          # Dimension name
    primary_friction: str            # Friction category
    friction_profile: dict           # Full dimension breakdown
```

**Formula:**
```
ALS = (OL×0.15) + (DL×0.25) + (EL×0.30) + (FD×0.15) + (DI×0.15) − (LV×0.10)
```

---

## Module 4 — CRT Estimation

**Purpose:** Estimate how long it will take to close the adaptation gap.

**Inputs:**
```python
class CRTInput:
    adaptation_gap: float        # From Module 2
    governance_friction: float   # 0.0–1.0
    execution_friction: float    # 0.0–1.0
    dependency_risk: float       # 0.0–1.0
    learning_velocity: float     # 0.0–1.0
    evidence_confidence: float   # 0.0–1.0
    objective_integrity: float   # 0.0–1.0 (how clear and stable is the goal?)
    base_months_per_point: float # Domain-specific baseline
```

**Outputs:**
```python
class CRTOutput:
    crt_months: float
    crt_range_low: float   # Confidence interval lower bound
    crt_range_high: float  # Confidence interval upper bound
    crt_risk: str          # "Low" / "Medium" / "High" / "Critical"
    governance_readiness: float  # 0.0–1.0
    will_miss_deadline: bool     # If target date provided
    months_to_miss: float        # How far behind (negative = ahead)
```

**Formula:**
```
CRT = G × T_base × (1 + Gov×0.30 + Exec×0.40 + Dep×0.30) × (1 − LV×0.35)
```

---

## Module 5 — Recommendation Engine

**Purpose:** Generate prioritized interventions targeting the primary bottleneck.

**Inputs:**
- `FrictionOutput` from Module 3
- `CRTOutput` from Module 4
- `CapabilityOutput` from Module 2

**Outputs:**
```python
class RecommendationOutput:
    summary: str           # CEO-grade plain English — bottleneck-first, time estimate
    interventions: list    # P0/P1/P2 prioritized actions
    expected_impact: str   # What the P0 action achieves
    confidence: str        # High / Medium / Low
```

**CEO-grade summary format:**
```
"This [program type] is [at risk of / likely to] miss its target by [N] months 
 because [Dimension] is the critical bottleneck. 
 [Non-obvious insight about the constraint]. 
 [Urgency statement]."
```

---

## Interface Contract

All modules communicate through typed dataclasses. No module reaches into another module's internals.

```python
# Full pipeline call
from asf import analyze, AnalysisInput

result = analyze(AnalysisInput(
    system_name="Enterprise AI Program",
    ...
))

# Result contains all module outputs
result.scores           # FrictionOutput
result.summary          # CEO-grade statement
result.interventions    # Prioritized actions
result.bottleneck_dimension
result.primary_friction
```

---

## Modular Use Cases

### As a consulting methodology worksheet
Input the six dimension scores manually based on client interviews.
Output: bottleneck identification, CRT estimate, prioritized interventions.
No code required. Works in a spreadsheet.

### As an AI agent reasoning framework
Pass the engine a strategic document.
Agent extracts dimension scores with evidence.
Engine produces the analysis.
Agent presents the CEO summary.

### As an Azure Solution Accelerator
Document ingestion → Azure AI Foundry → structured dimension scores → ASF engine → output API.
Full production architecture in `docs/methodology/azure-architecture.md`.

### As a strategy assessment model
Run against 10–50 organizations in the same sector.
Sort by ALS score.
Identify which organizations are adapting fastest and why.
Produces a defensible peer benchmark.

---

## Domain Calibration

Different domains require different `base_months_per_point` values:

| Domain | Base months/point | Rationale |
|---|---|---|
| AI/Software | 2–4 | Fast iteration cycles |
| Cloud infrastructure | 3–6 | Moderate complexity |
| Enterprise transformation | 4–8 | Organizational friction high |
| Manufacturing | 6–12 | Physical constraints |
| Healthcare | 8–14 | Regulatory cycles |
| Government | 10–18 | Legislative and procurement constraints |
| Energy/Infrastructure | 15–30 | Physical build cycles, regulatory approvals |

These are initial estimates. Calibration against outcome data will refine them.
