# Adaptive Systems Framework (ASF)

**ASF measures the gap between what a system can do today and what it needs to do — then tells you how long it will take to close that gap.**

> *Adaptation Gap = Required Capability − Current Capability*

Used by platform engineers, AI governance teams, and enterprise architects to diagnose why AI programs, cloud migrations, and operational systems fail to deliver value on time.

---

## What problem does ASF solve?

Organizations spend billions on AI, cloud, and digital transformation — and miss their targets. The gap is rarely strategy. It is almost always execution friction: manual dependencies, governance delays, legacy systems, and weak feedback loops that slow adaptation to a pace that cannot close the gap in time.

ASF makes that friction visible, measurable, and actionable.

---

## Core formula

```
Adaptation Latency Score =
    (Observation Latency  × 0.15)   how fast do you detect change?
  + (Decision Latency     × 0.25)   how fast do you commit?
  + (Execution Latency    × 0.30)   how fast do you implement?
  + (Feedback Delay       × 0.15)   how fast do you see results?
  + (Dependency Index     × 0.15)   how many manual steps block you?
  − (Learning Velocity    × 0.10)   how fast do you improve?

Scale: 1.0 (fastest) → 5.0 (slowest)
Risk:  < 2.5 = Low · 2.5–3.5 = Medium · > 3.5 = High
```

**Capability Realization Time (CRT)** — derived metric:
```
CRT = f(Adaptation Gap, Governance Friction, Execution Friction, Learning Velocity)
```
CRT estimates how many months it will take to close the adaptation gap given current friction levels.

---

## Available tools

| Tool | What it does |
|---|---|
| `cli.py` | Analyze any system from a YAML file — scored in seconds |
| `asf_analyze.py` | Batch analyze all 100 cases from the dataset |
| `asf_document_analyzer.py` | Upload any document — ASF extracts adaptation signals |
| `asf_conformance_agent.py` | Validate any LLM output against acceptance criteria |

---

## Live dashboards

All dashboards are live on GitHub Pages — open in any browser, no install needed.

| Dashboard | URL | What it shows |
|---|---|---|
| MNC 2030 Goals | [mnc-2030-goals](https://hdannabo.github.io/adaptive-systems-framework/dashboard/mnc-2030-goals.html) | Will 49 top MNCs hit their 2030 targets? |
| Enterprise AI Benchmark | [enterprise-benchmark](https://hdannabo.github.io/adaptive-systems-framework/dashboard/enterprise-benchmark.html) | NVIDIA, AT&T, Meta, Adobe, Datadog |
| Manufacturing Benchmark | [manufacturing-benchmark](https://hdannabo.github.io/adaptive-systems-framework/dashboard/manufacturing-benchmark.html) | Toyota, Boeing, Foxconn, Siemens, BYD |
| Token Governance Scorer | [token-governance](https://hdannabo.github.io/adaptive-systems-framework/dashboard/token-governance.html) | Score your AI program — enter spend → get governance score |
| Token Economics | [token-economics](https://hdannabo.github.io/adaptive-systems-framework/dashboard/token-economics.html) | 22 AI models scored on cost and context efficiency |
| Capability Realization Time | [capability-realization-time](https://hdannabo.github.io/adaptive-systems-framework/dashboard/capability-realization-time.html) | Estimate how long it takes to close the adaptation gap |
| 100-Case Explorer | [asf-dashboard](https://hdannabo.github.io/adaptive-systems-framework/research/asf-dashboard.html) | 100 systems across 10 domains, filterable |

---

## Run locally in 30 seconds

```bash
git clone https://github.com/hdannabo/adaptive-systems-framework.git
cd adaptive-systems-framework
pip install -r requirements.txt

# Analyze a system from YAML
python cli.py --file examples/att.yaml

# Analyze any document
python asf_document_analyzer.py --file your_report.pdf

# Batch analyze all 100 cases
python asf_analyze.py

# Filter by risk or domain
python asf_analyze.py --risk High
python asf_analyze.py --domain "Telecom & Networks"

# Validate an output against acceptance criteria
python asf_conformance_agent.py --demo
```

---

## Repository structure

```
adaptive-systems-framework/
├── cli.py                            # Score any system from YAML
├── asf_analyze.py                    # Batch analyze 100 cases
├── asf_document_analyzer.py          # Document → ASF analysis
├── asf_conformance_agent.py          # Output conformance validation
├── src/asf/
│   ├── models.py                     # Core data models
│   ├── analyzer.py                   # Analysis pipeline
│   ├── scoring/engine.py             # Deterministic scoring
│   ├── scoring/crt_engine.py         # Capability Realization Time
│   └── recommendations/engine.py    # Intervention generation
├── dashboard/
│   ├── mnc-2030-goals.html           # 49 MNCs vs 2030 targets
│   ├── enterprise-benchmark.html     # Enterprise AI benchmark
│   ├── manufacturing-benchmark.html  # Global manufacturing
│   ├── token-governance.html         # AI governance scorer
│   ├── token-economics.html          # Token efficiency scoring
│   └── capability-realization-time.html  # CRT dashboard
├── docs/
│   ├── capability-realization-time.md    # CRT methodology
│   ├── formulas.md                   # All ASF formulas
│   ├── acceptance-criteria.md        # Product acceptance criteria
│   ├── current-state.md              # Honest status assessment
│   └── global-governance-validation.md  # NIST/EU/ISO/OECD alignment
├── research/
│   ├── asf_100_cases.csv             # 100-case dataset
│   ├── mnc_2030_analysis.json        # 49 MNC analysis results
│   └── global-llm-adoption.md        # 20+ country LLM data
└── examples/
    ├── att.yaml                      # HIGH risk — telecom
    ├── toyota.yaml                   # LOW risk — benchmark
    ├── boeing.yaml                   # HIGH risk — manufacturing
    └── crt_examples.yaml             # CRT use case examples
```

---

## Current status

| Component | Status | Notes |
|---|---|---|
| Scoring engine | ✅ Production | Deterministic, tested, correct |
| CLI analyzer | ✅ Working | YAML → scored report |
| Batch analyzer | ✅ Working | 100 cases, filterable |
| Document analyzer | ⚠️ Partial | Signal detection; LLM reasoning planned for v0.4 |
| Conformance agent | ✅ Working | ALIGNED / DRIFTING / VIOLATED |
| Dashboards | ✅ Live | GitHub Pages, no install |
| CRT engine | ✅ v0.3 | Capability Realization Time scoring |
| REST API | 🔲 Planned | Azure Functions — v0.4 |
| LLM document reasoning | 🔲 Planned | Azure OpenAI integration — v0.4 |

---

## Roadmap

| Version | Scope | Status |
|---|---|---|
| v0.1 | Research framework, 100-case dataset | ✅ Done |
| v0.2 | Python scoring engine, CLI | ✅ Done |
| v0.3 | Document analyzer, conformance agent, CRT, dashboards | ✅ Done |
| v0.4 | Azure OpenAI document reasoning, REST API | Planned |
| v1.0 | ASF Copilot — upload document, get full report | Future |

---

## Governance alignment

ASF satisfies requirements across major AI governance frameworks:

| Framework | Region | Alignment |
|---|---|---|
| NIST AI Risk Management Framework | USA | Strong — all four functions covered |
| EU AI Act | Europe | Good — risk classification, documentation, monitoring |
| ISO/IEC 42001 | International | Strong — all 10 clauses |
| Australia NAIC | Australia | Good |
| India MeitY Guidelines | India | Good |
| OECD AI Principles | 42 countries | Strong |

See [`docs/global-governance-validation.md`](docs/global-governance-validation.md)

---

## License & Copyright

Copyright © 2026 Hemanth Kumar Dannaboyina. All rights reserved.

For research attribution:
```
Dannaboyina, H.K. (2026). Adaptive Systems Framework (ASF).
https://github.com/hdannabo/adaptive-systems-framework
```

[hemanth1917@icloud.com](mailto:hemanth1917@icloud.com)
