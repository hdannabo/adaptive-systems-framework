# ASF Validation Program

**Purpose:** Demonstrate the complete ASF chain — Document → Evidence → Score → Formula → Bottleneck → CRT → Recommendation — using real public-company examples.

**Status:** v0.1 — Three case studies, all evidence from public sources.

---

## What These Case Studies Prove

Each case study demonstrates that:

1. **Every score is traceable.** Each of the six dimension scores maps to a specific public document, a specific quote or metric, and a one-sentence reasoning statement. No score is asserted without evidence.

2. **The formula is deterministic.** Given the six scores, the ALS and risk band are computed by `src/asf/scoring/engine.py` without analyst judgment. The formula output is verified against the engine in each case.

3. **The bottleneck follows from the scores.** The primary bottleneck is the highest-scoring dimension. It is not subjectively chosen — it is the mathematical result of the scoring.

4. **The recommendation follows from the bottleneck.** The P0 intervention addresses the bottleneck dimension specifically, not the company generally.

5. **The outcome can be validated.** Each case study identifies specific, observable signals in future public disclosures that would confirm or refute the ASF bottleneck identification.

---

## Case Studies

| File | Company | ALS | Risk | Bottleneck | CRT |
|---|---|---|---|---|---|
| [CASE_STUDY_001.md](CASE_STUDY_001.md) | Boeing | 3.70 | High | Execution Latency | 70.7 months (Critical) |
| [CASE_STUDY_002.md](CASE_STUDY_002.md) | LTM (LTIMindtree) | 2.05 | Low | Execution Latency | 19.0 months (High) |
| [CASE_STUDY_003.md](CASE_STUDY_003.md) | AT&T | 3.85 | High | Execution Latency | 36.5 months (Critical) |

---

## Evidence File

`scoring_evidence.json` contains the complete structured scoring data for all three companies:
- Six dimension scores per company
- Evidence citation per dimension
- Source document per dimension
- Confidence level per dimension
- CRT inputs and output
- Formula verification string

This file is the machine-readable version of the case study documents.

---

## How to Verify Independently

Run the scoring engine against any case study's dimension scores:

```python
import sys
sys.path.insert(0, 'src')
from asf import analyze, AnalysisInput

# Boeing example
inp = AnalysisInput(
    system_name="Boeing",
    domain="Aerospace Manufacturing",
    system_type="Enterprise",
    adaptation_scenario="Production rate recovery",
    input_event="FAA oversight; quality governance failures",
    adaptation_requirement="38 planes/month production rate",
    current_operating_state="18 planes/month",
    observation_latency=3,
    decision_latency=3,
    execution_latency=5,
    feedback_delay=4,
    learning_velocity=2,
    dependency_index=4,
)
report = analyze(inp)
print(f"ALS: {report.scores.adaptation_latency_score}")   # → 3.70
print(f"Risk: {report.scores.risk_band.value}")           # → High
print(f"Bottleneck: {report.bottleneck_dimension}")       # → Execution Latency
```

The formula can also be verified by hand:
```
(3×0.15) + (3×0.25) + (5×0.30) + (4×0.15) + (4×0.15) − (2×0.10)
= 0.45 + 0.75 + 1.50 + 0.60 + 0.60 − 0.20
= 3.70
```

---

## Outcome Validation Schedule

These case studies become validated when observable signals appear in future public disclosures:

| Company | Validation signal | Observable in | Status |
|---|---|---|---|
| Boeing | Production rate increase toward 25+ planes/month | Q3 2026 Boeing earnings | Pending |
| Boeing | CEO commentary confirming quality feedback cycle as constraint | Next earnings or annual report | Pending |
| LTM | BFSI vertical returns to positive YoY growth | Q1FY27 LTM earnings (July 2026) | Pending |
| LTM | BlueVerse outcome contract count disclosed and growing | Any LTM earnings/Investor Day | Pending |
| AT&T | Mandatory adoption program announced | Q3 2026 AT&T earnings | Pending |
| AT&T | AI savings acceleration toward $2B/year | Q4 2026 AT&T earnings | Pending |

---

## Confidence Levels Explained

**High confidence** means the input evidence is quantitative, primary, and within the last 12 months. Boeing's production rate (18 planes/month), LTM's revenue (+6% YoY), and AT&T's savings ($1B of $4B) are all High confidence inputs.

**Medium confidence** means the input is inferred from qualitative language in an official disclosure. Boeing's observation latency score (3/5) is Medium confidence because the monthly review cycle is described in process terms, not measured in hours.

**Low confidence** is not present in these three case studies. It would indicate that a score was assigned without any direct public evidence.

---

## Limitations

These case studies do not predict outcomes. They estimate adaptation velocity relative to stated targets. The following assumptions are explicitly noted:

1. The six dimension weights (0.15, 0.25, 0.30, 0.15, 0.15, −0.10) are derived from the 100-case ASF dataset, not from regression analysis against outcome data. The weights represent the best current estimate.

2. CRT base_months_per_capability_point values (Boeing: 8.0, LTM: 4.0, AT&T: 5.0) are domain estimates, not empirically validated calibration values.

3. The AT&T decision latency score (4/5) involves inference — the absence of a publicly announced mandatory adoption program is interpreted as decision delay. An internal program may exist without public disclosure.

4. Public company disclosures reflect what companies choose to share. Internal operational reality may differ from public communication.

ASF scores and CRT estimates are analytical tools for decision support, not audited measurements.
