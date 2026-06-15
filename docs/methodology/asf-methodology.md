# ASF Methodology — Capability Realization Intelligence System

> Note: This document is the battery-sector adaptation of ASF using EFS. The canonical ASF methodology is documented in [`methodology/core.md`](./core.md).

> **Technical reference document.** This covers the CRT formula, Execution Friction Score (EFS), Confidence Interval model, evidence scoring protocol, and the 10-dimension capability assessment. This is how ASF produces its outputs — not marketing language, not black-box results.

---

## 1. What ASF Is Actually Measuring

ASF measures **Capability Realization Time (CRT)**: the estimated number of months between a company's current organizational capability and the capability required to deliver a declared strategic objective.

CRT is not a financial metric. It is not a strategy score. It is a time-to-capability estimate — grounded in operational evidence, adjusted for execution friction and dependency risk, and expressed with explicit confidence intervals.

The central ASF question is:

> *"If this organization starts closing its capability gap today, how many months until it has the capability its strategy requires — and what is currently slowing that process down?"*

---

## 2. The CRT Formula

```
CRT = gap × T_base × F_m × (1 / L_a) × CI_adj
```

| Variable | Name | Definition |
|----------|------|------------|
| `gap` | Capability Gap Score | Distance from current to required capability (0–1 scale from 10-dimension model) |
| `T_base` | Base Realization Time | Industry-calibrated base months per unit of capability gap |
| `F_m` | Friction Multiplier | Execution friction score converted to a time multiplier (≥1.0) |
| `L_a` | Learning Accelerator | Rate at which capability is being developed (0.5–1.5) |
| `CI_adj` | Confidence Adjustment | Widens or narrows output range based on evidence quality |

### T_base by Industry

| Sector | T_base (months/unit) |
|--------|----------------------|
| Manufacturing / Aerospace | 7.8 |
| Technology | 7.5 |
| Government / Public Sector | 7.7 |
| Healthcare | 7.0 |
| Telecom | 6.5 |
| Financial Services | 5.6 |
| Default | 6.5 |

Battery and advanced manufacturing companies are classified under **Manufacturing/Aerospace** (T_base 7.8), reflecting the higher complexity of physical process scale-up versus software-only transitions.

---

## 3. Execution Friction Score (EFS)

The EFS replaces the earlier ALS (Adaptation Level Score) designation in external documentation.

```
EFS = (obs × 0.20) + (dec × 0.25) + (exec × 0.30) + (fdb × 0.15) + (lv × 0.10)
```

| Component | Weight | Measures |
|-----------|--------|----------|
| `obs` | 20% | Observation capability — does the organization have real-time signal visibility? |
| `dec` | 25% | Decision speed — how quickly does leadership convert signals to decisions? |
| `exec` | 30% | Execution velocity — rate at which decisions become operational outcomes |
| `fdb` | 15% | Feedback quality — how well does the organization learn from execution outcomes? |
| `lv` | 10% | Capability Development Rate — pace at which new organizational capabilities are built |

**Note on dependency and EFS:** Dependency load is assessed separately through Dimension 6 of the 10-dimension capability model (see Section 5). Dependency is captured there as a risk magnitude score (Critical / High / Medium / Low). EFS captures internal execution friction only — what the organization controls. This separation prevents the same variable from influencing both the capability gap score (Dimension 6) and the friction multiplier.

Each component is scored 0–10 based on evidence. Weights sum to 1.0. EFS range: 0–10. Higher EFS = lower friction = lower CRT.

The EFS feeds the Friction Multiplier:

```
F_m = 2.0 − (EFS / 10)
```

At EFS = 10 (no friction): F_m = 1.0 (no time penalty)  
At EFS = 5 (moderate friction): F_m = 1.5 (50% additional time)  
At EFS = 0 (maximum friction): F_m = 2.0 (CRT doubles)

---

## 4. Confidence Interval Model

```
CI = 0.30 + (1 − dq) × 0.20
```

Where `dq` is the data quality score (0–1) assigned based on the evidence mix available:

| Evidence State | `dq` value | CI (formula) | CI (applied) |
|----------------|------------|--------------|--------------|
| Public data only — NSE filings, credit reports, press | 0.50 | ±40% | ±30–40% |
| Internal programme data — 90-day engagement | 0.75 | ±35% | ±20–25% |
| Full internal data — MES, yield, workflow, leadership logs | 0.90 | ±32% | ±15–20% |

**How CI is applied in practice:** The formula provides a floor. The analyst applies the CI after reviewing how many NOT DISCLOSED items affect material programme KPIs. If a programme has key unknowns (e.g., yield rates undisclosed for a manufacturing programme), the applied CI is at the wider end of the range. If public data is unusually rich (NSE-listed company with annual CARE/ICRA reviews plus investor days), it may be at the narrower end.

Battery sector CI examples (June 2026):

| Company | Evidence State | Not Disclosed Items | Applied CI | Rationale |
|---------|---------------|---------------------|------------|-----------|
| HBL Engineering | Public data | 2 (Ni-Cad utilization basis; TMS plans) | ±25% | Unusually rich public record: CARE, NSE, RDSO notices, investor comms |
| Exide EESL | Public data | 3 (yield rates; production specs; SVOLT terms) | ±30% | Material yield data not public; two delays with no technical explanation |
| Amara Raja | Public data | 4 (yield; sequencing decision; off-take; programme schedule) | ±35% | Dual-factory complexity, new leadership, limited cell production history |

**Important:** Internal engagement data replaces NOT DISCLOSED items with operational data, typically reducing applied CI by 50–60%.

---

## 5. Ten-Dimension Capability Assessment

Every company assessed receives a score (0–10) across ten capability dimensions. Each score must be backed by at least one HIGH or MEDIUM confidence evidence item.

| # | Dimension | What Is Being Measured |
|---|-----------|------------------------|
| 1 | Strategic Clarity | Specificity, measurability, and time-boundedness of declared objective |
| 2 | Capability Creation Mechanism | Existence and quality of structured process to build new organizational capabilities |
| 3 | Technology Transition Readiness | Ability to absorb and operationalize new technology at the required pace |
| 4 | Manufacturing Readiness | Physical infrastructure, workforce, process, and quality systems in place |
| 5 | Execution Velocity | Rate at which planned activities are completed against commitment |
| 6 | Dependency Risk | Exposure to external blockers across 6 dependency dimensions |
| 7 | Execution Friction (EFS) | Combined score from EFS formula above |
| 8 | Evidence Confidence | Quality of data supporting the overall assessment |
| 9 | Talent Readiness | Availability of human capability matching the strategic objective requirements |
| 10 | Data and System Maturity | Quality, availability, and integration of operational data and supporting systems |

---

## 6. Dependency Risk — Six Dimensions

Dependency risk is assessed across six dimensions that capture the major categories of external blockers:

| Dimension | Definition |
|-----------|------------|
| Data Dependency | Reliance on data that is not yet available, integrated, or visible to management |
| Process Dependency | Critical processes that depend on partner, regulator, or third-party approval rather than internal control |
| Workforce Dependency | Talent categories that are scarce, partner-supplied, or require long build cycles |
| Vendor/System Dependency | Technology, equipment, or service provider relationships that control programme pace |
| Governance Dependency | Regulatory, compliance, or approval processes that are outside operational control |
| Technology Dependency | Underlying technology platforms, partnerships, or know-how not owned by the organization |

Each dimension is rated: Critical / High / Medium / Low based on evidence.

---

## 7. Evidence Scoring Protocol

All evidence is classified at point of collection:

| Rating | Definition | Example |
|--------|------------|---------|
| HIGH | Directly documented in a primary source — no inference required | NSE filing with exact capex figure; RDSO certification notice; ICRA rating rationale |
| MEDIUM | Reasonably inferred from documented data — inference step required | Utilization rate inferred from capacity and production volume; talent gap inferred from programme scope |
| NOT DISCLOSED | Material information not available in public domain | Cell yield rates; commercial terms of OEM agreements; internal programme timeline |

NOT DISCLOSED items are recorded but receive no score contribution. The presence of NOT DISCLOSED evidence on material programme KPIs is itself a risk signal.

---

## 8. Prediction Register Protocol

ASF issues timestamped, falsifiable predictions — not directional outlooks. Each prediction follows a structured format:

```
ID:         [Company-###]
Issued:     [Date]
Statement:  [Specific, falsifiable claim with timeframe]
Trigger:    [Observable event that would confirm or refute this prediction]
Validate:   [Date when prediction should be checked against outcomes]
Confidence: [HIGH / MEDIUM]
```

Predictions are published in [`validation/prediction-register-core.md`](../../validation/prediction-register-core.md) and [`validation/prediction-register-battery.md`](../../validation/prediction-register-battery.md) and are not modified after issuance. Validation outcomes are recorded against each prediction as they become available.

This creates a public accountability mechanism that differentiates ASF from analysis that does not commit to verifiable claims.

---

## 9. Methodology Limitations — Explicit Disclosure

ASF is a structured analytical framework, not a validated predictive model. The following limitations apply:

1. **CRT estimates are calibrated from industry heuristics**, not from a dataset of validated prior predictions. Battery sector calibration data grows with each engagement.

2. **EFS component weights are theoretically derived**, not empirically fitted. The weighting (execution 30%, decision 25%, etc.) reflects analytical judgement, not regression analysis.

3. **Public-data analysis is inherently limited.** Yield rates, process capability metrics, internal programme timelines, and leadership decision quality cannot be assessed from public disclosures. NOT DISCLOSED evidence items are not placeholders — they represent genuine analytical limitations.

4. **CRT estimates cannot account for events ASF has not observed.** New technology breakthroughs, policy changes, M&A, or market shifts that change the capability landscape will not be reflected in a point-in-time assessment.

5. **The battery sector represents a single sector application.** Cross-sector calibration data does not yet exist. Sector-specific T_base values are preliminary.

These limitations are disclosed because analytical credibility requires them. Internal engagement data materially improves precision on items 1–3.

---

*ASF Methodology v1.0 · June 2026 · Battery Sector Application*  
*Technical queries: github.com/hdannabo/adaptive-systems-framework*
