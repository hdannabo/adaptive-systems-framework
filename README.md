# ASF — Adaptive Systems Framework

**ASF identifies why organizations fail to convert AI investment, capability, and information into measurable value.**

Upload a document. Score your AI program. Compare enterprises. ASF tells you where value is being lost and what to do about it.

---

## What it does

| Tool | What you get |
|---|---|
| **Token Governance Scorer** | Score your AI program 0–100. Primary bottleneck. P0/P1/P2 interventions. |
| **Document Analyzer** | Upload any doc — annual report, postmortem, strategy. ASF diagnoses it. |
| **Enterprise Benchmark** | NVIDIA, Meta, AT&T, Adobe, Datadog — scored from public data. |
| **Manufacturing Benchmark** | Toyota, Foxconn, Siemens, Boeing, BYD — global manufacturing adaptation. |
| **100-Case Dashboard** | 100 systems across 10 domains. Interactive. Open locally. |
| **Token Economics** | 22 AI models scored on cost efficiency, context efficiency, agent risk. |

---

## Run it in 30 seconds

```bash
git clone https://github.com/hdannabo/adaptive-systems-framework.git
cd adaptive-systems-framework
pip install pyyaml

# Score any system from a YAML file
python cli.py --file examples/att.yaml

# Analyze any document
python asf_document_analyzer.py --file your_report.pdf

# Batch analyze all 100 cases
python asf_analyze.py
```

---

## Open the dashboards

All dashboards are standalone HTML — open directly in any browser. No server needed.

| Dashboard | Location | What it shows |
|---|---|---|
| Token Governance Scorer | `dashboard/token-governance.html` | Score your AI program live |
| Enterprise AI Benchmark | `dashboard/enterprise-benchmark.html` | 5 companies, public data |
| Manufacturing Benchmark | `dashboard/manufacturing-benchmark.html` | Global manufacturing ASF |
| 100-Case Explorer | `research/asf-dashboard.html` | All 100 cases, filterable |
| Token Economics | `research/ai-token-economics/token-economics-dashboard.html` | 22 models scored |

---

## Dashboards

All dashboards open locally in any browser — no server needed.
GitHub Pages: **https://hdannabo.github.io/adaptive-systems-framework/**

| Dashboard | What it shows |
|---|---|
| [`dashboard/token-governance.html`](dashboard/token-governance.html) | Score your AI program — enter spend, users, adoption → governance score + P0/P1/P2 interventions |
| [`dashboard/enterprise-benchmark.html`](dashboard/enterprise-benchmark.html) | NVIDIA, Datadog, Adobe, AT&T, Meta — scored from public data |
| [`dashboard/manufacturing-benchmark.html`](dashboard/manufacturing-benchmark.html) | Toyota, Foxconn, Siemens, BYD, Boeing — global manufacturing adaptation |
| [`dashboard/token-economics.html`](dashboard/token-economics.html) | 22 AI models scored — click any model for full ASF token efficiency output |
| [`research/asf-dashboard.html`](research/asf-dashboard.html) | 100 cases across 10 domains — filterable by domain and risk band |

## The core finding

Across 100 analyzed systems — Toyota to Kodak, NVIDIA to Boeing, Netflix to AT&T:

> Organizations rarely fail because they don't know what to do.
> The real issue is the delay between recognizing a required change and operationalizing the response.

**The Kodak Theorem:** Recognition is not the bottleneck. Decision latency and execution friction are.

---

## The formula

```
Total Adaptation Latency =
    Observation Latency (how fast you detect change)
  + Decision Latency    (how fast you commit)
  + Execution Latency   (how fast you implement)
  + Feedback Delay      (how fast you see results)

Minus: Learning Velocity (how fast you improve)
```

---

## Repository structure

```
adaptive-systems-framework/
├── cli.py                          # Analyze any system from YAML
├── asf_document_analyzer.py        # Upload doc → ASF diagnosis
├── asf_analyze.py                  # Batch analyze 100 cases
├── src/asf/                        # Python scoring engine
├── dashboard/
│   ├── token-governance.html       # Score your AI program
│   ├── enterprise-benchmark.html   # Enterprise AI comparison
│   └── manufacturing-benchmark.html # Manufacturing comparison
├── docs/
│   ├── formulas.md                 # All ASF formulas
│   ├── theoretical-foundations.md  # MAPE, OODA, Senge, Ashby
│   ├── llm-adaptation.md           # ASF for LLMs
│   ├── deep-cases.md               # 10 deep case studies
│   └── vision.md                   # Universal adaptive systems model
├── research/
│   ├── asf-dashboard.html          # 100-case interactive dashboard
│   ├── asf_100_cases.csv           # Full dataset
│   └── ai-token-economics/         # Token pricing + efficiency scores
├── examples/
│   ├── att.yaml                    # HIGH risk — telecom
│   ├── toyota.yaml                 # LOW risk — benchmark
│   └── boeing.yaml                 # HIGH risk — governance failure
└── models/
    └── asf-model.yaml              # Canonical ASF schema
```

---

## Theoretical foundations

ASF is grounded in six established frameworks: Systems Thinking (Senge, Meadows, Forrester), OODA Loop (John Boyd), Cybernetics (Wiener, Ashby), MAPE-K (IBM Research), Adaptive Systems (Santa Fe Institute), and Learning Organizations (Peter Senge).

See [`docs/theoretical-foundations.md`](docs/theoretical-foundations.md)

---

## Roadmap

| Version | Scope | Status |
|---|---|---|
| v0.1 | Research, 100-case dataset | ✅ Done |
| v0.2 | Python engine, CLI, batch analyzer | ✅ Done |
| v0.3 | Document analyzer, governance scorer | ✅ Done |
| v0.4 | REST API + web interface | Planned |
| v1.0 | ASF Copilot — upload doc, get full report | Future |

---

## License & Copyright

Copyright © 2026 Hemanth Kumar Dannaboyina. All rights reserved.

Attribution for research use:
```
Dannaboyina, H.K. (2026). Adaptive Systems Framework (ASF).
GitHub: https://github.com/hdannabo/adaptive-systems-framework
```

[hemanth1917@icloud.com](mailto:hemanth1917@icloud.com) · AT&T · Procter & Gamble · Cisco · AZ-305 · AI-102 · CKA
