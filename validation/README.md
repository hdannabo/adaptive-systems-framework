# ASF Validation Program

**Purpose:** Demonstrate the complete ASF chain — Document → Evidence → Score → Formula → Bottleneck → CRT → Recommendation — using real public-company examples.

**Status:** v0.2 — Three case studies + Inter-rater reliability + CRT calibration study.

---

## Validation Artifacts

| File | Description | Status |
|---|---|---|
| [CASE_STUDY_001.md](CASE_STUDY_001.md) | Boeing — ALS 3.70, CRT 70.7mo Critical | ✅ Complete |
| [CASE_STUDY_002.md](CASE_STUDY_002.md) | LTM — ALS 2.05, CRT 19.0mo High | ✅ Complete |
| [CASE_STUDY_003.md](CASE_STUDY_003.md) | AT&T — ALS 3.85, CRT 36.5mo Critical | ✅ Complete |
| [scoring_evidence.json](scoring_evidence.json) | Machine-readable evidence for all 3 companies | ✅ Complete |
| [inter_rater_reliability.md](inter_rater_reliability.md) | κ=0.739, 100% bottleneck agreement | ✅ v0.1 |
| [calibration_report.md](calibration_report.md) | CRT vs actual: 20 programs, T_base recalibration | ✅ v0.1 |
| [external_validation_protocol.md](external_validation_protocol.md) | External IRR study design — 3 analysts, 5 companies, full rubric | ✅ Ready |
| [prediction_register.md](prediction_register.md) | 13 timestamped predictions — Boeing, LTM, AT&T | ✅ v1.0 |
| [prediction_dashboard.html](prediction_dashboard.html) | Live prediction tracker with checkpoint calendar | ✅ v1.0 |
| [validation_metrics.py](validation_metrics.py) | Accuracy, calibration, lead time engine | ✅ v1.0 |
| [outcome_tracking_workflow.md](outcome_tracking_workflow.md) | P001 July 2026 checkpoint protocol | ✅ Ready |
| [annual_validation_report_template.md](annual_validation_report_template.md) | Annual review template | ✅ Ready |
| [crt_validation_results.csv](crt_validation_results.csv) | Raw data: all 20 programs predicted vs actual | ✅ Complete |

---

## CRT Calibration Summary (NEW)

20 historical transformation programs analyzed across 5 domains.

**Key finding:** CRT systematically underestimates by 18.7% on average. Technology domain is most underestimated (-43%). Telecom domain is most accurate (-2.8%).

**Recommended T_base corrections:**

| Domain | Current | Recommended | Evidence programs |
|---|---|---|---|
| Manufacturing | 6.0 | 7.8 | 5 programs |
| Telecom | 6.5 | 6.5 | 3 programs |
| Technology | 3.5 | 7.5 | 5 programs |
| Financial Services | 4.5 | 5.6 | 4 programs |
| Government | 7.0 | 7.7 | 3 programs |

**Status:** CRT moves from "unvalidated estimate" to "empirically grounded estimate with documented systematic bias." Apply 1.25× correction factor to all CRT outputs until T_base values are updated.

---

## Case Studies

| File | Company | ALS | Risk | Bottleneck | CRT |
|---|---|---|---|---|---|
| [CASE_STUDY_001.md](CASE_STUDY_001.md) | Boeing | 3.70 | High | Execution Latency | 70.7 months (Critical) |
| [CASE_STUDY_002.md](CASE_STUDY_002.md) | LTM (LTIMindtree) | 2.05 | Low | Execution Latency | 19.0 months (High) |
| [CASE_STUDY_003.md](CASE_STUDY_003.md) | AT&T | 3.85 | High | Execution Latency | 36.5 months (Critical) |

---

## Outcome Validation Schedule

| Company | Validation signal | Observable in | Status |
|---|---|---|---|
| Boeing | Production rate increase toward 25+ planes/month | Q3 2026 Boeing earnings | Pending |
| LTM | BFSI vertical returns to positive YoY growth | **Q1FY27 LTM earnings (July 2026)** | **PRIORITY** |
| AT&T | Mandatory adoption program announced | Q3 2026 AT&T earnings | Pending |

**LTM July 2026 is the first available outcome check (~July 22, 2026).** P001 is registered and timestamped. If BFSI returns to positive growth, this becomes the first confirmed ASF prediction and moves the framework from "promising" to "tested."

**To record the outcome when available:**
```bash
python validation/validation_metrics.py --update P001 Confirmed \
    "BFSI +X% YoY Q1FY27" 2026-07-22
```

---

## Inter-rater Reliability (v0.1)

- **κ = 0.739** (substantial agreement)
- 18/18 dimensions within ±1
- 100% bottleneck agreement on all 3 companies
- [See full results →](inter_rater_reliability.md)

**Limitation:** Analyst B is simulated (same system as Analyst A). Formal study requires external analyst.

---

## Validation Roadmap

| Stage | Status | Required evidence |
|---|---|---|
| 1 — Interesting | ✅ Complete | Case studies, evidence chains |
| 2 — Credible | 🔄 In progress | One confirmed prediction + external IRR study |
| 3 — Defensible | 📋 Planned | 3 confirmed predictions, κ>0.60 external |
| 4 — Trusted | 📋 Planned | Longitudinal outcome study, peer review |

---

## How to Verify Independently

Run the scoring engine against any case study's dimension scores:

```python
import sys
sys.path.insert(0, 'src')
from asf import analyze, AnalysisInput

inp = AnalysisInput(
    system_name="Boeing",
    domain="Aerospace Manufacturing",
    system_type="Enterprise",
    adaptation_scenario="Production rate recovery",
    input_event="FAA oversight; quality governance failures",
    adaptation_requirement="38 planes/month production rate",
    current_operating_state="18 planes/month",
    observation_latency=3, decision_latency=3, execution_latency=5,
    feedback_delay=4, learning_velocity=2, dependency_index=4,
)
report = analyze(inp)
print(f"ALS: {report.scores.adaptation_latency_score}")   # → 3.70
print(f"Risk: {report.scores.risk_band.value}")           # → High
print(f"Bottleneck: {report.bottleneck_dimension}")       # → Execution Latency
```

---

## Limitations

All scores based on publicly available information. Friction inputs are analyst-assigned, not measured. CRT T_base values are now empirically grounded (20 programs) but remain estimates — target is 50+ programs per domain for reliable calibration. Inter-rater reliability study is v0.1 simulation; formal external study is Priority 2.
