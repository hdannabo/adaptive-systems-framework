# Adaptive Systems Framework (ASF)

> **Why do some systems adapt faster than others when exposed to the same information?**

ASF is a systems-engineering and AI-era research framework for measuring, diagnosing, and accelerating adaptation in organizations, AI systems, and operational platforms.

Built by a Forward-Deployed AI Infrastructure & Platform Engineer with 7+ years designing and operating production systems at Fortune 500 scale — AT&T, Procter & Gamble, Cisco.

---

## Core Hypothesis

> Systems succeed when their rate of adaptation exceeds the rate of environmental change.

---

## The Core Finding

Across 100 analyzed systems — Toyota to Kodak, Netflix to Boeing, OpenAI to AT&T:

> Organizations rarely fail because they don't know what to do.
> The real issue is the delay between recognizing a required change and operationalizing the response.

**The Kodak Theorem:** Recognition is not the bottleneck. Decision latency and execution friction are.

---

## Theoretical Foundations

ASF is grounded in six established frameworks:

| Framework | Key Contributors | What ASF Takes |
|---|---|---|
| Systems Thinking | Forrester, Meadows, Senge | Feedback loops, delays, learning velocity |
| OODA Loop | John Boyd | Tempo as the primary competitive variable |
| Cybernetics | Wiener, Ashby | Law of Requisite Variety, feedback control |
| MAPE-K | IBM Research (Kephart & Chess) | Monitor-Analyze-Plan-Execute architecture |
| Adaptive Systems | Santa Fe Institute | Emergence, fitness landscapes |
| Learning Organizations | Peter Senge | Learning velocity as organizational capability |

---

## Engineering Formulas

ASF produces measurable quantities, not just scores.

```
Total Adaptation Latency (TAL):
  TAL = Observation Latency + Decision Latency + Execution Latency
      = T_operational − T_available

Adaptation Latency Score (ALS, 0–100):
  ALS = 100 − [(OL×0.15) + (DL×0.25) + (EL×0.30) + (FD×0.15) + (DI×0.15) − (LV×0.10)] × 100

LLM Adaptation Efficiency (LAE):
  LAE = (Task_success_rate × Outcome_quality) / (Token_cost × Latency)

Adaptation Funnel Loss (AFL):
  AFL = 1 − (Signals_adapted / Signals_observed)
```

See [`docs/formulas.md`](docs/formulas.md) for the complete formula reference.

---

## ASF for LLMs

One of ASF's strongest current applications: measuring LLM efficiency in production.

**The three LLM problems ASF addresses:**
1. Token cost explosion — organizations can't track AI ROI
2. Context window degradation — more context ≠ better results
3. Agent cost vs agent value — agentic workflows burn tokens without proportional value

**Key metrics:**
- Context Efficiency: `CE = Useful_information / Total_tokens`
- Cost Efficiency: `CoE = Business_value / AI_spend`
- Adaptation Efficiency: `AE = Performance_gain / Additional_context` (< 1.0 = context rot)

See [`docs/llm-adaptation.md`](docs/llm-adaptation.md) for full analysis.

---

## Quickstart

```bash
git clone https://github.com/hdannabo/adaptive-systems-framework.git
cd adaptive-systems-framework
pip install pyyaml

# Analyze a single system
python cli.py --file examples/att.yaml

# Upload ANY document — annual report, postmortem, strategy doc
python asf_document_analyzer.py --file report.pdf
python asf_document_analyzer.py --file postmortem.txt --org "AT&T"
python asf_document_analyzer.py --file strategy.docx --export output.json

# Batch analyze all 100 cases
python asf_analyze.py
python asf_analyze.py --domain "Telecom & Networks"
python asf_analyze.py --risk High --top 10
```

---

## Repository Structure

```
adaptive-systems-framework/
├── cli.py                          # Single-system analyzer
├── asf_analyze.py                  # Batch analyzer — all 100 cases
├── src/asf/                        # Python engine
│   ├── models.py                   # Core data models
│   ├── analyzer.py                 # Analysis pipeline
│   ├── scoring/engine.py           # Scoring computation
│   └── recommendations/engine.py  # Intervention logic
├── docs/
│   ├── formulas.md                 # Engineering formulas — TAL, ALS, AFL, LAE
│   ├── theoretical-foundations.md  # MAPE, OODA, Cybernetics, Senge, Meadows
│   ├── llm-adaptation.md           # ASF for LLMs — token cost, context rot, ROI
│   ├── deep-cases.md               # 10 deep cases with formula analysis
│   ├── vision.md                   # Universal adaptive systems model
│   ├── product-architecture.md     # Full system design
│   ├── case-studies.md             # Real-world evidence
│   └── company-taxonomy.md         # 100+ organizations classified
├── examples/
│   ├── att.yaml                    # HIGH risk — execution bottleneck
│   ├── toyota.yaml                 # LOW risk — world-class benchmark
│   ├── boeing.yaml                 # HIGH risk — governance failure
│   └── aks-upgrade.yaml            # Platform engineering case
├── research/
│   ├── asf_100_cases.csv           # 100-case dataset
│   ├── asf-dashboard.html          # Interactive dashboard (open locally)
│   ├── hypotheses.md               # 8 testable hypotheses
│   └── dataset-readme.md           # Key findings
└── models/
    └── asf-model.yaml              # Canonical ASF schema
```

---

## 100-Case Dataset — Key Findings

| Domain | Avg ALS | Best Case | Worst Case |
|---|---|---|---|
| AI Systems | 88/100 | OpenAI (88) | — |
| Manufacturing | 75/100 | Toyota (95) | Boeing (42) |
| Entertainment | 72/100 | Netflix (93) | Warner (38) |
| Telecom | 58/100 | T-Mobile (78) | AT&T (38) |
| Historical failures | 22/100 | Adobe (72) | Sears (12) |

Open [`research/asf-dashboard.html`](research/asf-dashboard.html) locally — no server needed.

---

## Roadmap

| Version | Scope | Status |
|---|---|---|
| v0.1 | Research framework, 100-case dataset | ✅ Done |
| v0.2 | Python engine, CLI, batch analyzer | ✅ Done |
| v0.3 | Document analyzer — upload any doc, ASF generates analysis | ✅ Done |
| v0.4 | REST API + web dashboard | Planned |
| v1.0 | ASF Copilot — analyze any system automatically | Future |

---

## About

**Hemanth Kumar Dannaboyina**
Forward-Deployed AI Infrastructure & Platform Engineer
AT&T · Procter & Gamble · Cisco · Spirion
Azure Solutions Architect Expert (AZ-305) · Azure AI Engineer (AI-102) · CKA · Six Sigma Green Belt

[hemanth1917@icloud.com](mailto:hemanth1917@icloud.com)

---

## License & Copyright

Copyright © 2026 Hemanth Kumar Dannaboyina. All rights reserved.

The Adaptive Systems Framework (ASF) — including the theoretical model, scoring methodology, formula definitions, dataset, and all associated documentation — is original research and intellectual property of the author.

**Research and personal use:** You may read, reference, and cite this work with attribution.

**Commercial use:** Contact the author before using ASF methodology, scoring models, or datasets in commercial products or services.

**Attribution:** If you reference ASF in research, presentations, or publications, please cite:

```
Dannaboyina, H.K. (2026). Adaptive Systems Framework (ASF).
GitHub: https://github.com/hdannabo/adaptive-systems-framework
```

[hemanth1917@icloud.com](mailto:hemanth1917@icloud.com)
