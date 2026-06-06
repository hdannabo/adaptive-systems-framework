# ASF Formulas — v2.0

The following formulas operationalize ASF metrics into measurable quantities.
These are not scores. They are engineering-grade measurements.

---

## 1. Observation Latency (OL)

Time from when a signal becomes detectable to when the system registers it.

```
OL = T_detected − T_available

Where:
  T_detected  = timestamp when system logged the signal
  T_available = timestamp when signal was objectively present in data
```

**Examples:**
- Incident: time from first anomaly in telemetry to alert firing
- Market: time from competitor announcement to internal awareness
- Defect: time from first customer report to engineering ticket

**Target:** OL < 5 minutes for instrumented systems; < 24 hours for strategic signals

---

## 2. Decision Latency (DL)

Time from signal recognition to committed response decision.

```
DL = T_decided − T_recognized

Where:
  T_decided    = timestamp of approved, committed decision
  T_recognized = timestamp of documented signal recognition
```

**Decomposition:**
```
DL = Review Time + Approval Time + Escalation Time + Coordination Time
```

**Target:** DL < 1 sprint (2 weeks) for operational decisions; < 1 quarter for strategic

---

## 3. Execution Latency (EL)

Time from committed decision to operational implementation.

```
EL = T_operational − T_decided

Where:
  T_operational = timestamp when change is live and measurable
  T_decided     = timestamp of committed decision
```

**Decomposition:**
```
EL = Build Time + Test Time + Deployment Time + Validation Time
```

**Target:** EL < 1 week for platform teams with CI/CD; < 4 weeks for enterprise programs

---

## 4. Total Adaptation Latency (TAL)

The complete cycle from signal to operational change.

```
TAL = OL + DL + EL

TAL = (T_detected − T_available)
    + (T_decided  − T_recognized)
    + (T_operational − T_decided)

Simplified:
TAL = T_operational − T_available
```

This is the primary ASF engineering metric.

**Industry benchmarks (from 100-case dataset):**
| System Type | Median TAL | Best-in-class |
|---|---|---|
| AI-native platforms | 2–4 weeks | < 1 week |
| Cloud-native enterprises | 4–8 weeks | 2 weeks |
| Telecom operators | 8–26 weeks | 4 weeks |
| Legacy enterprises | 26–52 weeks | 8 weeks |
| Historical failures | > 52 weeks | N/A |

---

## 5. Feedback Delay (FD)

Time from execution to observable outcome measurement.

```
FD = T_measured − T_operational

Where:
  T_measured   = timestamp when outcome metric is available
  T_operational = timestamp when change went live
```

**Short FD:** real-time dashboards, automated testing, SLO monitoring
**Long FD:** annual reviews, lagging KPIs, manual reporting

---

## 6. Learning Velocity (LV)

Rate of improvement across successive adaptation cycles.

```
LV = (Performance_n − Performance_n-1) / TAL_n

Where:
  Performance_n   = outcome quality in cycle n
  Performance_n-1 = outcome quality in prior cycle
  TAL_n           = total adaptation latency of cycle n
```

Higher LV = system improves faster per unit of adaptation time.

**Proxy metrics when direct measurement unavailable:**
- Postmortem → runbook conversion rate
- Incident recurrence rate (lower = higher LV)
- Time-to-competency for new team members

---

## 7. Dependency Index (DI)

Degree of adaptation dependence on manual processes, approvals, and coordination.

```
DI = (Manual_steps + Approval_gates + Coordination_handoffs) / Total_steps

Range: 0.0 (fully automated) → 1.0 (fully manual)
```

**Example calculation:**
- 12-step deployment process
- 4 manual steps, 3 approval gates, 2 coordination handoffs
- DI = (4 + 3 + 2) / 12 = 0.75 — high dependency

---

## 8. Adaptation Latency Score (ALS)

Composite 0–100 score for cross-system comparison.

```
ALS = 100 − [
    (OL_norm × 0.15)
  + (DL_norm × 0.25)
  + (EL_norm × 0.30)
  + (FD_norm × 0.15)
  + (DI      × 0.15)
  − (LV_norm × 0.10)
] × 100

Where _norm = value normalized to [0,1] against domain benchmark
```

**Risk bands:**
| ALS | Band | Action |
|---|---|---|
| 80–100 | High adaptability | Maintain; share practices |
| 60–79 | Moderate adaptability | Targeted improvement |
| Below 60 | High adaptation risk | Systemic intervention |

---

## 9. LLM Adaptation Efficiency (LAE)

Measures how efficiently an LLM converts context and compute into useful outcomes.

```
LAE = (Task_success_rate × Outcome_quality) / (Token_cost × Latency)

Where:
  Task_success_rate = fraction of tasks completed correctly
  Outcome_quality   = human or automated quality score [0–1]
  Token_cost        = total tokens consumed (input + output)
  Latency           = wall-clock time to completion
```

**Context Efficiency:**
```
CE = Useful_information_extracted / Total_tokens_consumed
```

**Reasoning Efficiency:**
```
RE = Successful_tasks / Tokens_consumed
```

**Cost Efficiency:**
```
CoE = Business_value_generated / AI_spend
```

**Adaptation Efficiency (for long-context models):**
```
AE = Performance_gain / Additional_context_added

Ideal: AE > 1.0 (each additional context unit improves performance)
Degraded: AE < 1.0 (context rot — more context hurts performance)
```

---

## 10. Adaptation Funnel Loss (AFL)

Measures where adaptation value is lost in the pipeline.

```
AFL_stage = (Signals_in − Signals_out) / Signals_in

Total_AFL = 1 − (Signals_adapted / Signals_observed)
```

**Example from 100-case dataset average:**
```
100 signals observed
 80 correctly interpreted    → AFL = 0.20 (observation/interpretation loss)
 65 decisions made           → AFL = 0.19 (decision loss)
 40 executed                 → AFL = 0.38 (execution loss)  ← biggest gap
 25 measured                 → AFL = 0.38 (feedback loss)
 15 learned from             → AFL = 0.40 (learning loss)
 10 produced lasting change  → AFL = 0.33 (adaptation loss)

Total AFL = 0.90 — 90% of signals never produce lasting adaptation
```

The biggest loss is consistently at **execution** — not observation, not decision.
