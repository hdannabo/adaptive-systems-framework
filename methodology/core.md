# ASF Methodology — Canonical Reference

**Version:** 0.4  
**Status:** Working draft — validated against 100-case dataset  
**Last updated:** June 2026

---

## Problem Statement

Organizations set transformation targets and miss them.

Not because the strategy was wrong. Not because the budget was insufficient.

**Because the organization could not move fast enough.**

The gap between recognizing that change is needed and actually delivering that change is the central problem ASF measures. Most frameworks measure outcomes. None measure the velocity of the adaptive process itself — whether the organization is moving fast enough to close the gap in time.

---

## Core Hypothesis

> Every system exists in a current state and attempts to move toward a required future state.
> Success depends not on the quality of the strategy but on the velocity of adaptation.
> The primary cause of transformation failure is not lack of awareness but insufficient adaptation velocity given existing friction.

This hypothesis is supported by:
- IBM MAPE-K (2003): autonomous systems require closed-loop adaptation cycles
- John Boyd's OODA Loop: decision velocity determines competitive outcome
- Peter Senge's Fifth Discipline: learning organizations outadapt non-learning ones
- Donella Meadows: delays in feedback loops are the primary cause of system failure
- ASF 100-case dataset: 73% of failures had recognized the need for change before failing

---

## Canonical Model

```
Current State
     ↓
Awareness Cycle
  [How fast does the system detect that change is needed?]
     ↓
Adaptation Gap
  [How large is the gap between current and required capability?]
     ↓
Capability Acquisition
  [What must be built, learned, or changed to close the gap?]
     ↓
Execution Friction
  [What is slowing the capability acquisition process?]
     ↓
Capability Realization Time (CRT)
  [Given the gap and the friction, how long will it take?]
     ↓
Outcome
  [Did the system reach the required state before the deadline?]
```

Every ASF concept maps into this model. Concepts that do not map are not in ASF.

---

## Definitions

### Awareness
The state in which a system has received, processed, and correctly interpreted a signal requiring adaptation.

Awareness is the precondition for adaptation. A system cannot adapt to a change it has not detected.

**Awareness Cycle** = the complete loop from signal emergence to confirmed organizational awareness.

**What slows the Awareness Cycle:**
- Fragmented data — signals exist but are not connected
- Lagging indicators — signals arrive after the window for response has narrowed
- Organizational filters — signals are suppressed by hierarchy or incentive misalignment

---

### Adaptation Gap (G)

```
G = C_required − C_current

Where:
  C_required = capability score required to achieve stated objective  (1–10 scale)
  C_current  = current measured capability score                      (1–10 scale)
  G ≥ 0      (minimum zero — exceeding requirements is G = 0)
```

The Adaptation Gap is the distance the system must travel. It does not tell you how fast you can travel it — that is CRT.

---

### Capability

The measurable ability of a system to perform a defined function at a defined quality level. Capability is domain-specific and requires a defined benchmark.

**Capability Acquisition** = the process of closing the Adaptation Gap through learning, investment, hiring, automation, or structural change.

---

### Adaptation Velocity (V)

```
V_actual = ΔC / Δt     (current measured rate of capability change)
V_required = G / T      (velocity needed to close gap by target date)

If V_actual < V_required → objective will be missed
If V_actual ≥ V_required → objective is achievable
```

Velocity is the key diagnostic. Not current state. Not gap size. Whether the velocity is sufficient.

---

### Execution Friction

The forces that slow Capability Acquisition. Four categories:

| Category | Examples | Primary effect |
|---|---|---|
| Technical | Legacy systems, integration complexity, data quality | Slows execution |
| Organizational | Approval layers, ownership ambiguity, silos | Slows decisions |
| Human | Risk aversion, change fatigue, skill gaps | Slows adoption |
| Governance | Compliance reviews, audit requirements, regulatory cycles | Slows all stages |

---

### Adaptation Latency Score (ALS)

The ASF scoring model operationalizes six dimensions of friction:

```
ALS = (Observation Latency  × 0.15)
    + (Decision Latency     × 0.25)
    + (Execution Latency    × 0.30)
    + (Feedback Delay       × 0.15)
    + (Dependency Index     × 0.15)
    − (Learning Velocity    × 0.10)

Scale: 1.0 (fastest possible) → 5.0 (slowest possible)
```

**Why these weights:**
- Execution Latency (0.30): Most common primary bottleneck in the 100-case dataset
- Decision Latency (0.25): Second most common; governance delay frequently precedes execution delay
- Observation, Feedback, Dependency (0.15 each): Supporting dimensions; rarely the sole bottleneck
- Learning Velocity (−0.10): Accelerator that reduces effective friction over time

**Risk bands:**
```
ALS < 2.5  → Low risk    — adapting at or above required velocity
ALS 2.5–3.5 → Medium risk — at risk; targeted intervention needed
ALS > 3.5  → High risk   — likely to miss target; executive action required
```

---

### Capability Realization Time (CRT)

```
CRT = G × T_base × F_mult × L_accel

Where:
  G       = Adaptation Gap
  T_base  = domain-specific baseline months per capability point
  
  F_mult  = 1 + (F_gov × 0.30) + (F_exec × 0.40) + (F_dep × 0.30)
  
  L_accel = 1 − (LV × 0.35)
```

CRT answers: **"Given the gap and the friction, how long will it actually take?"**

**Risk classification:**
```
CRT < 6 months   → Low      — achievable within planning cycle
CRT 6–18 months  → Medium   — sustained effort required
CRT 18–36 months → High     — multi-year investment; milestone tracking essential
CRT > 36 months  → Critical — fundamental intervention required
```

---

## Inputs Required

| Input | Type | Source | Confidence |
|---|---|---|---|
| System name | String | User | High |
| Strategic objective | String | Annual report / strategy doc | High |
| Required capability score | 1–10 | Analyst assessment | Medium |
| Current capability score | 1–10 | Analyst assessment / document | Medium |
| Observation Latency | 1–5 | Operational measurement / analyst | Medium |
| Decision Latency | 1–5 | Process audit / analyst | Medium |
| Execution Latency | 1–5 | Delivery metrics / analyst | Medium |
| Feedback Delay | 1–5 | Observability assessment / analyst | Medium |
| Learning Velocity | 1–5 | Retrospective quality / analyst | Low–Medium |
| Dependency Index | 1–5 | Process mapping / analyst | Medium |
| Governance friction | 0–1 | Compliance overhead assessment | Medium |
| Evidence confidence | 0–1 | Analyst judgment | Self-reported |

---

## Outputs

| Output | Description | Executive use |
|---|---|---|
| Adaptation Gap (G) | Distance from current to required capability | Scope of change |
| ALS | Friction score across six dimensions | Overall velocity assessment |
| Risk Band | Low / Medium / High | Risk communication |
| Primary Bottleneck | Which dimension is causing the most delay | Where to intervene |
| Primary Friction | What kind of friction dominates | What type of intervention |
| CRT | Estimated months to close gap | Schedule and timeline |
| CEO Summary | Plain-English decision-support statement | Executive briefing |
| Interventions | P0/P1/P2 ranked actions | Prioritized roadmap |

---

## Confidence Levels

Every ASF output carries a confidence level based on evidence quality:

| Level | Meaning | Typical source |
|---|---|---|
| High | Score directly supported by quantitative primary data | Financial filings, operational metrics, primary research |
| Medium | Score inferred from qualitative public disclosure | Annual reports, press releases, earnings calls |
| Low | Score estimated from indirect signals | Industry analysis, peer comparison, inference |

**Confidence affects CRT range:**
- High confidence → ±15% confidence interval
- Medium confidence → ±25% confidence interval
- Low confidence → ±40% confidence interval

---

## Assumptions

1. **Six dimensions are sufficient** — The 100-case dataset supports these six as the primary friction sources. Domains with regulatory-dominant constraints may require additional governance dimension weighting.

2. **Weights are validated on current dataset** — Weights reflect patterns across 100 cases. Not yet validated against longitudinal outcome data.

3. **1–5 scale is ordinal, not interval** — A score of 4 is worse than 2, but not necessarily twice as slow.

4. **Dimensions are treated as independent** — In practice, Decision Latency and Execution Latency correlate. This correlation is not currently modeled.

5. **Current velocity continues** — CRT assumes current adaptation rate continues. Leadership changes, new investment, or major interventions can shift this.

6. **Public data is sufficient** — Company analyses based on public disclosure may understate internal execution problems that are not disclosed.

---

## Limitations

- ASF does not predict outcomes; it estimates velocity relative to target
- ASF does not replace expert judgment; it structures and quantifies it
- ASF does not provide investment, legal, or financial advice
- Scores derived from public data carry inherent disclosure bias
- Framework has not been peer-reviewed or academically validated
- Longitudinal validation study not yet completed

---

## What Would Make ASF More Credible

1. **Automated evidence-based scoring** — LLM reads documents, assigns scores with cited evidence (v0.4)
2. **Longitudinal outcome study** — Compare 2023 ASF scores to 2025 actual outcomes
3. **Inter-rater reliability** — Second analyst scores same organizations independently
4. **Peer review** — Submit to management science or information systems journal
5. **Practitioner validation** — Executives confirm or deny the bottleneck identification
