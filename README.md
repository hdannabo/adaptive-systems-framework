# Adaptive Systems Framework (ASF)

**ASF identifies why transformation programs miss their targets — and what to fix first.**

It measures organizational adaptation velocity: how fast you move from where you are today to where you need to be. When that velocity is insufficient to hit a target on time, ASF identifies the specific bottleneck causing the delay and recommends what to do about it.

---

## The output ASF produces

Not a score. A decision.

> *"This AI transformation program is likely to miss its $4B savings target by $1.2B.
> The bottleneck is not AI capability or budget — it is workforce adoption.
> At current velocity, the program will reach $2.8B by 2030.
> Recommended action: mandatory adoption program targeting unadopted employees by Q3 2026.
> Every 10% adoption increase adds approximately $250M toward the target."*

---

## What makes ASF different

Every major framework measures something valuable:

- **Balanced Scorecard** — tracks performance outcomes
- **Six Sigma** — optimizes existing processes
- **CMMI** — assesses process maturity level
- **McKinsey 7S** — diagnoses organizational alignment

None answer: **"Given our current organizational speed, will we hit our target on time?"**

That is ASF's question. It is also the question that explains most transformation failures.

See [methodology/vs-other-frameworks.md](methodology/vs-other-frameworks.md) for the full comparison.

---

## Core model

```
Adaptation Gap = Required Capability − Current Capability

Adaptation Latency Score =
    (Observation Latency  × 0.15)   — how fast do you detect change?
  + (Decision Latency     × 0.25)   — how fast do you commit?
  + (Execution Latency    × 0.30)   — how fast do you implement?
  + (Feedback Delay       × 0.15)   — how fast do you see results?
  + (Dependency Index     × 0.15)   — how many manual steps block you?
  − (Learning Velocity    × 0.10)   — how fast do you improve?

Capability Realization Time (CRT):
  How many months to close the gap at current friction levels.
```

The dimension with the highest score is the primary bottleneck. Fixing it has the greatest impact on reaching the target on time.

---

## Quick start

```bash
git clone https://github.com/hdannabo/adaptive-systems-framework
cd adaptive-systems-framework
pip install -r requirements.txt

# Run a scored analysis from a YAML input
python cli.py --file examples/boeing.yaml

# Analyze a document (keyword mode, no credentials needed)
python asf_document_analyzer.py --file report.pdf --mode keyword

# Analyze a document (LLM mode — requires Azure OpenAI)
cp .env.example .env  # fill in your Azure credentials
python asf_document_analyzer.py --file annual_report.pdf

# Run all tests
python tests/test_evidence_extractor.py
```

---

## Repository structure

```
asf/
├── src/asf/                   # Python package — scoring engine, CRT, recommendations
│   ├── scoring/engine.py      # ALS formula (12 lines, deterministic)
│   ├── scoring/crt_engine.py  # CRT estimation
│   ├── recommendations/       # Intervention lookup by bottleneck
│   └── evidence/extractor.py  # LLM-based evidence extraction (v0.4)
│
├── cli.py                     # Command-line analysis tool
├── asf_document_analyzer.py   # Document → evidence → score pipeline
├── asf_conformance_agent.py   # Validate LLM outputs meet acceptance criteria
│
├── methodology/               # Theory: definitions, assumptions, limitations
│   ├── core.md                # Canonical model, formula, all definitions
│   ├── assumptions.md         # Honest limitations — read before using
│   ├── validation.md          # What evidence would refute ASF
│   └── vs-other-frameworks.md # Comparison to BSC, CMMI, 7S, DC theory
│
├── validation/                # Empirical validation program
│   ├── CASE_STUDY_001.md      # Boeing — ALS 3.70, Execution bottleneck
│   ├── CASE_STUDY_002.md      # LTM — ALS 2.05, Low risk
│   ├── CASE_STUDY_003.md      # AT&T — ALS 3.85, Execution + Dependency
│   ├── prediction_register.md # 13 timestamped predictions (June 2026)
│   ├── calibration_report.md  # CRT vs actual: 20 programs, -18.7% bias
│   └── external_validation_protocol.md  # IRR study design, ready to run
│
├── research/                  # Dataset and hypotheses
│   ├── asf_100_cases.csv      # 100-case dataset (single-analyst, v0.1)
│   ├── hypotheses.md          # Testable hypotheses, not conclusions
│   └── dataset-readme.md      # Dataset provenance and limitations
│
├── dashboard/                 # Live GitHub Pages dashboards
└── examples/                  # Sample YAML inputs (Boeing, AT&T, Toyota)
```

---

## Live dashboards

Open in any browser — no install required.

| Dashboard | What it shows |
|---|---|
| [MNC 2030 Goals](https://hdannabo.github.io/adaptive-systems-framework/dashboard/mnc-2030-goals.html) | Will 49 top MNCs hit their 2030 targets? |
| [Enterprise AI Benchmark](https://hdannabo.github.io/adaptive-systems-framework/dashboard/enterprise-benchmark.html) | NVIDIA, OpenAI, Microsoft, Palantir — adaptation velocity |
| [Manufacturing Benchmark](https://hdannabo.github.io/adaptive-systems-framework/dashboard/manufacturing-benchmark.html) | Toyota, Boeing, Siemens, BYD |
| [LTM Validation](https://hdannabo.github.io/adaptive-systems-framework/dashboard/ltm-validation.html) | Full traceable case study — evidence → score → CRT |
| [Prediction Register](https://hdannabo.github.io/adaptive-systems-framework/dashboard/prediction-register.html) | 13 live predictions with checkpoint calendar |
| [CRT Explorer](https://hdannabo.github.io/adaptive-systems-framework/dashboard/capability-realization-time.html) | Capability Realization Time calculator |

---

## What is validated and what is not

ASF is a working research methodology. The table below is honest about status.

| Component | Status | Evidence |
|---|---|---|
| ALS formula | ✅ Deterministic, verified | Engine tests pass; formula reproducible by hand |
| Bottleneck identification | ✅ Preliminary | Simulated IRR κ = 0.739, 100% bottleneck agreement on 3 companies |
| CRT model | ⚠️ Calibrated, not validated | 20 programs tested; -18.7% systematic underestimation documented; revised T_base values published |
| Scoring rubric | ⚠️ Preliminary | External IRR study designed and ready; not yet run with human analysts |
| Dimension weights | ❌ Unvalidated | Derived from single-analyst 100-case dataset; no regression analysis run |
| Recommendations | ❌ Generic | Hardcoded lookup table; company-specific recommendations require analyst judgment |
| Predictions | ⏳ Pending | 13 registered June 2026; first check July 2026 (LTM Q1FY27 earnings) |

See [methodology/assumptions.md](methodology/assumptions.md) for the complete limitations statement.

---

## Validation program

The `validation/` folder contains a structured research program:

1. **Three case studies** — Boeing, LTM, AT&T — with complete evidence chains
2. **CRT calibration** — 20 historical programs, documented -18.7% underestimation bias
3. **Inter-rater reliability** — simulated κ = 0.739; external study protocol ready
4. **Prediction register** — 13 timestamped predictions before outcomes are available
5. **Outcome tracking** — first resolvable checkpoint July 22, 2026 (LTM BFSI)

The prediction register is the most important artifact. A framework is not validated because analysts agree. It is validated when its predictions are confirmed or falsified by observable events.

---

## Theoretical grounding

ASF operationalizes concepts from six established research traditions:

- **Systems Thinking** — Meadows, Senge, Forrester: feedback loop delays cause system failure
- **OODA Loop** — Boyd (1986): decision velocity determines competitive outcome
- **Dynamic Capabilities** — Teece, Pisano, Shuen (1997): sensing/seizing/reconfiguring as microfoundations
- **Time-Based Competition** — Stalk (1988): time compression as competitive advantage
- **MAPE-K** — IBM (2003): autonomous systems require closed-loop adaptation cycles
- **Complex Adaptive Systems** — Santa Fe Institute: emergence and adaptation in complex environments

See [docs/theoretical-foundations.md](docs/theoretical-foundations.md) for the full grounding.

---

## License

MIT License — see [LICENSE](LICENSE).

Use ASF freely for research, consulting, and internal transformation work.
If you use ASF in published research, please cite the repository and the validation case studies.

---

## Contributing

The highest-value contribution right now is not code. It is validation.

1. **Run the external IRR study** — recruit two analysts, follow [validation/external_validation_protocol.md](validation/external_validation_protocol.md)
2. **Check LTM Q1FY27 earnings** — July 22, 2026 — follow [validation/outcome_tracking_workflow.md](validation/outcome_tracking_workflow.md)
3. **Add a case study** — use [validation/CASE_STUDY_001.md](validation/CASE_STUDY_001.md) as the template

The framework's credibility grows with each confirmed prediction and each inter-rater study. Those are the contributions that matter most right now.
