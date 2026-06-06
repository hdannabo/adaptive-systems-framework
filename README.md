# Adaptive Systems Framework (ASF)

> **Why do some systems adapt faster than others when exposed to the same information?**

ASF is a research and engineering framework that diagnoses adaptation bottlenecks in organizations, AI systems, platform engineering, manufacturing, telecom, and supply chains — then generates prioritized interventions to close the gap.

Built by a Forward-Deployed AI Infrastructure & Platform Engineer with 7+ years designing and operating production systems at Fortune 500 scale.

---

## The Core Finding

Across 100 analyzed systems — from Toyota to Kodak, AT&T to Netflix:

> Organizations rarely fail because they don't know what to do.  
> They fail because **manual dependency, governance friction, and organizational complexity delay adaptation** long after the need is recognized.

ASF makes that delay measurable. And fixable.

---

## How It Works

```
Input (YAML or interactive)
          ↓
  Six-dimension analysis
  Observation · Decision · Execution
  Feedback · Learning · Dependency
          ↓
  Weighted scoring
  Adaptation Latency Score (1–5)
  Risk Band: Low / Medium / High
          ↓
  Root cause mapping
  Bottleneck dimension identified
  Primary friction source named
          ↓
  Prioritized interventions
  P0 / P1 / P2 ranked by impact
          ↓
  JSON export for downstream use
```

---

## Quickstart

```bash
git clone https://github.com/hdannabo/adaptive-systems-framework
cd adaptive-systems-framework

pip install pyyaml

# Analyze AT&T
python cli.py --file examples/att.yaml

# Analyze Toyota
python cli.py --file examples/toyota.yaml

# Interactive mode — analyze any system
python cli.py

# Export JSON report
python cli.py --file examples/boeing.yaml --export outputs/boeing.json
```

---

## Demo Output

```
  System         AT&T
  Domain         Telecom & Networks
  Scenario       AI-native network operations

  Latency Score  4.00 / 5.0  ████████████████░░░░  Risk: HIGH
  Friction Score 4.60 / 5.0
  Adapt Capabil. 2.00 / 5.0

  Layer Analysis
  Observation latency    3/5  ████████████░░░░░░░░
  Decision latency       4/5  ████████████████░░░░
  Execution latency      5/5  ████████████████████  ◀ bottleneck
  Feedback delay         4/5  ████████████████░░░░
  Learning velocity      3/5  ████████░░░░░░░░░░░░
  Dependency index       5/5  ████████████████████

  Primary friction    Manual dependency / legacy systems
  Bottleneck          Execution Latency

  [P0]  Automate top 3 manual handoffs blocking delivery pipeline
        Target: Execution Latency · Est. reduction: 6w · Effort: high

  [P0]  Map and eliminate top 5 manual dependencies in the critical path
        Target: Dependency Index · Est. reduction: 6w · Effort: medium
```

---

## Scoring Model

```
Adaptation Latency Score =
    (Observation Latency  × 0.15)
  + (Decision Latency     × 0.25)  ← highest weight: decisions kill orgs
  + (Execution Latency    × 0.30)  ← highest weight: execution is the gap
  + (Feedback Delay       × 0.15)
  + (Dependency Index     × 0.15)
  − (Learning Velocity    × 0.10)  ← reduces score: learning accelerates adaptation
```

| Score | Risk Band | What It Means |
|---|---|---|
| 1.0 – 2.4 | Low | System adapts well — maintain trajectory |
| 2.5 – 3.4 | Medium | Targeted interventions recommended |
| 3.5 – 5.0 | High | Systemic intervention required |

---

## Input Format

```yaml
system_name: Your Organization
domain: Telecom & Networks
system_type: Telecom Operator
adaptation_scenario: AI-native network operations

observation_latency: 3    # 1=fast, 5=slow
decision_latency: 4
execution_latency: 5
feedback_delay: 4
learning_velocity: 3      # 1=slow, 5=fast
dependency_index: 5       # 1=low dependency, 5=high dependency
```

---

## Repository Structure

```
adaptive-systems-framework/
├── cli.py                          # Main CLI analyzer
├── src/
│   └── asf/
│       ├── models.py               # Core data models
│       ├── analyzer.py             # Analysis pipeline
│       ├── scoring/engine.py       # Scoring computation
│       └── recommendations/engine.py  # Intervention logic
├── examples/
│   ├── att.yaml                    # High-latency case
│   ├── boeing.yaml                 # Governance failure case
│   └── toyota.yaml                 # Low-latency benchmark
├── docs/
│   ├── vision.md                   # Universal adaptive systems model
│   ├── product-architecture.md     # Full system design
│   ├── case-studies.md             # Real-world evidence
│   └── company-taxonomy.md         # 100+ companies classified
├── research/
│   ├── asf_100_cases.csv           # 100-case dataset
│   ├── dataset-readme.md           # Key findings
│   ├── hypotheses.md               # 8 testable hypotheses
│   └── asf-dashboard.html          # Interactive dashboard
└── models/
    └── asf-model.yaml              # Canonical schema
```

---

## 100-Case Dataset

10 domains · 100 systems · fully scored

| Domain | Avg Score | Notable |
|---|---|---|
| AI Systems | 2.53 | Lowest latency — minimal legacy |
| Data & Cloud | 2.64 | Fast execution culture |
| Manufacturing | 2.92 | Toyota (1.20) anchors the low end |
| Historical failures | 4.26 | Kodak, Nokia, Blockbuster, Sears |
| Telecom | 3.58 | AT&T (4.20) — legacy system drag |

Open the [interactive dashboard](research/asf-dashboard.html) locally to explore all 100 cases.

---

## Roadmap

| Version | Scope | Status |
|---|---|---|
| v0.1 | Research, 100-case dataset, scoring formula | ✅ Done |
| v0.2 | Python engine, CLI, JSON export, 3 examples | ✅ Done |
| v0.3 | LLM-assisted analysis from annual reports / postmortems | Planned |
| v0.4 | REST API + web dashboard | Planned |
| v1.0 | Adaptive Systems Copilot | Future |

---

## About

Hemanth Kumar Dannaboyina  
Forward-Deployed AI Infrastructure & Platform Engineer  
AT&T · Procter & Gamble · Cisco · Spirion  
Azure Solutions Architect Expert (AZ-305) · AI Engineer (AI-102) · CKA  
[hemanth1917@icloud.com](mailto:hemanth1917@icloud.com)
