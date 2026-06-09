# Adaptive Systems Framework (ASF)

**ASF identifies why transformation programs miss their targets — and what to fix first.**

It measures organizational adaptation velocity: how fast you move from where you are today to where you need to be. When that velocity is insufficient to hit a target on time, ASF identifies the specific bottleneck causing the delay and recommends what to do about it in the next 90 days.

---

## The output ASF produces

Not a score. A decision.

> *"This AI transformation program is likely to miss its $4B savings target by $1.2B.
> The bottleneck is not AI capability or budget — it is workforce adoption.
> At current velocity, the program will reach $2.8B by 2030.
> Recommended action: adoption program targeting unadopted employees by Q3 2026.
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

## Live dashboards

Open in any browser — no install required.

| Dashboard | What it shows |
|---|---|
| [MNC 2030 Goals](https://hdannabo.github.io/adaptive-systems-framework/dashboard/mnc-2030-goals.html) | Will 49 top MNCs hit their 2030 targets? All objectives. Decision support for each company. |
| [Enterprise AI Benchmark](https://hdannabo.github.io/adaptive-systems-framework/dashboard/enterprise-benchmark.html) | NVIDIA, OpenAI, Anthropic, Microsoft, Scale AI, Palantir — adaptation velocity compared |
| [Manufacturing Benchmark](https://hdannabo.github.io/adaptive-systems-framework/dashboard/manufacturing-benchmark.html) | Toyota, Boeing, Foxconn, Siemens, BYD — global manufacturing adaptation |
| [Token Governance Scorer](https://hdannabo.github.io/adaptive-systems-framework/dashboard/token-governance.html) | Enter your AI program data → get governance score + P0/P1/P2 interventions |
| [Capability Realization Time](https://hdannabo.github.io/adaptive-systems-framework/dashboard/capability-realization-time.html) | How long to close the adaptation gap across 10 use cases |
| [Token Economics](https://hdannabo.github.io/adaptive-systems-framework/dashboard/token-economics.html) | 22 AI models scored on cost and context efficiency |

---

## Run locally

```bash
git clone https://github.com/hdannabo/adaptive-systems-framework.git
cd adaptive-systems-framework
pip install -r requirements.txt

# Score any system from a YAML file
python cli.py --file examples/att.yaml

# Analyze any document — annual report, postmortem, strategy doc
python asf_document_analyzer.py --file your_report.pdf

# Batch analyze all 100 cases
python asf_analyze.py --risk High
```

---

## Repository structure

```
adaptive-systems-framework/
│
├── methodology/                  ← Start here if you want to understand ASF
│   ├── what-is-asf.md           ← Plain English. For CEOs and executives.
│   ├── vs-other-frameworks.md   ← How ASF differs from Six Sigma, CMMI, BSC, 7S
│   ├── formulas.md              ← The math. For architects and engineers.
│   └── assumptions.md           ← Honest limitations. For everyone.
│
├── dashboard/                    ← Live tools. Open in browser.
│   ├── mnc-2030-goals.html
│   ├── enterprise-benchmark.html
│   ├── manufacturing-benchmark.html
│   ├── token-governance.html
│   └── capability-realization-time.html
│
├── src/asf/                      ← Working Python engine
│   ├── models.py
│   ├── scoring/engine.py
│   ├── scoring/crt_engine.py
│   └── recommendations/engine.py
│
├── docs/                         ← Documentation
│   ├── executive-getting-started.md
│   ├── current-state.md          ← Honest assessment of what works and what doesn't
│   └── acceptance-criteria.md
│
├── research/                     ← Dataset and case studies
│   ├── asf_100_cases.csv
│   └── mnc_2030_analysis.json
│
└── examples/                     ← Sample YAML inputs
    ├── att.yaml
    ├── toyota.yaml
    └── boeing.yaml
```

---

## Honest status

| Component | Status | Notes |
|---|---|---|
| Scoring engine | ✅ Working | Deterministic, tested, correct |
| CLI analyzer | ✅ Working | YAML input → full report |
| Dashboards | ✅ Live | GitHub Pages, all companies with multi-objective + decision support |
| Document analyzer | ✅ Working | LLM-based evidence extraction with cited quotes (v0.4) |
| Conformance agent | ✅ Working | Output validation against acceptance criteria |
| CRT engine | ✅ Working | Capability Realization Time estimates |

| REST API | 🔲 Planned | v0.4 — Azure Functions |

The company scores in the benchmarks are derived from public data by human analyst review, not automated extraction. This is documented in [docs/current-state.md](docs/current-state.md).

---

## Roadmap

| Version | Scope | Status |
|---|---|---|
| v0.3 | Scoring engine · Dashboards · CRT · 49-company benchmark | ✅ Done |
| v0.4 | Azure OpenAI evidence extraction with citations | ✅ Done |
| v0.5 | REST API · Web interface — no Python required | Planned |
| v1.0 | Upload any document · Get full ASF report automatically | Future |

---

## License & Copyright

Copyright © 2026 Hemanth Kumar Dannaboyina. All rights reserved.

For research attribution:
```
Dannaboyina, H.K. (2026). Adaptive Systems Framework (ASF).
https://github.com/hdannabo/adaptive-systems-framework
```

[hemanth1917@icloud.com](mailto:hemanth1917@icloud.com)
