# ASF Applications

ASF is a measurement framework. The same core model — Observation, Decision, Execution, Feedback, Learning — applies across five distinct application domains.

```
ASF Applications
├── Enterprise AI ROI
├── AI Agent Economics
├── LLM Adaptation Efficiency
├── Platform Engineering
└── Manufacturing Systems
```

Each application uses the same scoring engine. What changes is the data source, the friction taxonomy, and the intervention playbook.

---

## 1. Enterprise AI ROI

**The problem:** Most enterprises cannot measure whether their AI investment is generating value proportional to spend. CFOs see token costs rising. Engineering teams see adoption stalling. The gap between AI procurement and AI value is unmeasured.

**What ASF measures:**

| Metric | Formula | What it reveals |
|---|---|---|
| AI Adoption Velocity | `Adopted Teams / Total Teams × (1 / Months to Adoption)` | How fast the org is absorbing AI capability |
| Value Realization Lag | `First Value Date − Deployment Date` | How long between deploy and measurable outcome |
| ROI Efficiency | `Measured Value / Total AI Spend` | Whether cost is justified |
| Adaptation Debt | `Σ Friction Score × Weeks Unresolved` | Accumulated cost of slow adaptation |

**ASF diagnosis:**
```
Input Event:        AI tools deployed
Current State:      Low adoption, unclear ROI
Friction:           Skill gap + governance delay + ownership ambiguity
Adaptation Latency: High
Intervention:       Reduce adoption friction before increasing spend
```

**Key finding:** Organizations that measure AI adoption latency before scaling spend show 3–5× better ROI than those that scale spend first.

---

## 2. AI Agent Economics

**The problem:** Agentic workflows consume dramatically more tokens than standard chat. Research indicates agentic tasks can use 10–100× more tokens than simple completions — while higher token consumption does not necessarily improve outcomes.

**What ASF measures:**

| Metric | Formula | What it reveals |
|---|---|---|
| Agent Efficiency Ratio | `Task Value / Token Cost` | Value per dollar of agent spend |
| Loop Overhead | `(Agent Tokens − Baseline Tokens) / Baseline Tokens` | Token inflation from orchestration |
| Tool Call Latency | `Σ Tool Execution Time / Task Completion Time` | What fraction of agent time is execution vs reasoning |
| Feedback Utilization | `Actions Changed After Feedback / Total Actions` | Whether the agent actually learns within session |
| Cost Per Adaptation | `Total Agent Cost / Number of Successful Adaptations` | True cost of one useful outcome |

**The ASF Agent Efficiency Formula:**

```
Agent Efficiency Score =
    (Task Completion Rate × 0.35)
  + (Token Efficiency     × 0.25)   ← value per token
  + (Feedback Utilization × 0.20)   ← does it learn?
  + (Tool Accuracy        × 0.20)   ← does it execute correctly?
```

**ASF diagnosis for over-spending agents:**
```
Symptom:        Token spend rising, outcomes flat
Friction:       Loop overhead — agent replanning without new information
Intervention:   Cache intermediate results, reduce redundant tool calls,
                add early-exit conditions when confidence is sufficient
```

---

## 3. LLM Adaptation Efficiency

**The problem:** LLMs differ not just in capability but in *adaptation efficiency* — how much useful output they generate per unit of context, cost, and computation. Context window size is marketed as a feature, but performance often degrades as context grows ("context rot").

**The three major LLM industry problems ASF addresses:**

**Problem 1 — Token Cost Explosion**
Token-based pricing makes costs unpredictable. Most CFOs cannot accurately track AI spend. ASF measures cost-per-outcome, not cost-per-token.

**Problem 2 — Context Window Degradation**
Research shows model performance degrades before reaching advertised context limits. A 1M token window does not mean 1M tokens of reliable reasoning. ASF measures *effective* context utilization.

**Problem 3 — Agent Cost vs Agent Value**
Agentic workflows consume orders of magnitude more tokens. Higher spend does not guarantee better outcomes. ASF measures adaptation efficiency — the ratio of value generated to resources consumed.

**The LLM Adaptation Cycle:**

```
User Request
     ↓
Observation       ← how accurately does the model read the task?
     ↓
Reasoning         ← how efficiently does it process context?
     ↓
Tool Usage        ← how precisely does it invoke external capabilities?
     ↓
Execution         ← how reliably does it complete the action?
     ↓
Feedback          ← how quickly does it incorporate corrections?
     ↓
Learning / Memory ← does it improve within and across sessions?
     ↓
Outcome
```

**LLM Adaptation Efficiency Formula:**

```
LLM Adaptation Efficiency =
    (Task Accuracy          × 0.30)   ← did it get the right answer?
  + (Context Utilization    × 0.20)   ← useful output per token consumed
  + (Retrieval Precision    × 0.20)   ← did it retrieve the right information?
  + (Reasoning Depth        × 0.15)   ← multi-step coherence
  + (Feedback Responsiveness× 0.15)   ← correction uptake speed
```

**Publicly Available Landscape (2026):**

| Model | Context Window | Cost Profile | Retrieval | Reasoning | ASF Efficiency |
|---|---|---|---|---|---|
| Claude (Anthropic) | 1M tokens | High | High | High | 88 |
| Gemini (Google) | 1M+ tokens | Medium | High | Medium-High | 84 |
| GPT-5 (OpenAI) | Large | Medium | High | High | 86 |
| DeepSeek | Lower | Low | Medium | Medium | 78 |

*ASF Efficiency scores are illustrative based on public benchmarks and reported performance. Not vendor-endorsed.*

**Key ASF insight:**
> A model with a smaller context window but higher context utilization efficiency outperforms a larger-window model suffering from context rot.

**Effective Context Utilization Formula:**

```
Effective Context Utilization =
    Useful Output Tokens / Total Input Tokens Consumed

Where:
  Useful Output Tokens = tokens contributing to task completion
  Total Input Tokens   = full prompt + context + retrieval
```

**Context Rot Detection:**

```
Context Rot Score =
    1 - (Performance at 80% context / Performance at 20% context)

Score > 0.15 = significant degradation
Score > 0.30 = severe degradation — context window is a liability
```

---

## 4. Platform Engineering

**The problem:** Platform engineering teams operate complex Kubernetes, cloud, and CI/CD ecosystems. Adaptation latency appears as: slow upgrade cycles, manual approval gates, incident response delays, and low deployment frequency.

**What ASF measures:**

| Metric | Formula | What it reveals |
|---|---|---|
| Upgrade Cycle Latency | `Operational Date − Recognition Date` (weeks) | How long platform changes take |
| Deployment Frequency | `Deployments / Time Period` | Execution velocity |
| MTTR | `Σ Recovery Time / Incident Count` | Feedback loop speed |
| Automation Coverage | `Automated Steps / Total Pipeline Steps` | Dependency Index proxy |
| Change Failure Rate | `Failed Deployments / Total Deployments` | Execution quality |

**Platform Engineering Adaptation Formula:**

```
Platform Adaptation Score =
    (Deployment Frequency    × 0.25)   ← execution velocity
  + (MTTR Efficiency         × 0.25)   ← feedback loop speed
  + (Automation Coverage     × 0.20)   ← dependency reduction
  + (Change Success Rate     × 0.20)   ← execution quality
  + (Upgrade Cycle Speed     × 0.10)   ← strategic adaptation
```

**DORA metrics as ASF inputs:**

| DORA Metric | ASF Dimension | ASF Layer |
|---|---|---|
| Deployment Frequency | Execution Latency | Execution |
| Lead Time for Changes | Decision + Execution Latency | Decision + Execution |
| MTTR | Feedback Delay | Feedback |
| Change Failure Rate | Execution Quality | Execution |

**Real case — AKS Upgrade Program:**
```
Observation Latency:  1 week   (version EOL detected immediately)
Decision Latency:     4 weeks  (CAB approval, owner sign-off)
Execution Latency:    8 weeks  (manual validation, no automation)
Feedback Delay:       2 weeks  (no automated smoke tests)
Total Latency:        15 weeks → target: 4 weeks
Primary Friction:     Manual dependency + governance delay
Intervention:         Automated validation pipeline + policy-as-code
```

---

## 5. Manufacturing Systems

**The problem:** Manufacturing adaptation latency appears as: slow defect detection cycles, long root-cause-to-fix pipelines, supplier quality delays, and sluggish continuous improvement loops.

**What ASF measures:**

| Metric | Formula | What it reveals |
|---|---|---|
| Defect Detection Latency | `Detection Date − Defect Introduction Date` | Observation loop speed |
| Root Cause Cycle Time | `Fix Date − Detection Date` | Decision + Execution speed |
| Supplier Adaptation Lag | `Supplier Correction Date − Issue Raised Date` | External dependency latency |
| Kaizen Velocity | `Improvements Implemented / Time Period` | Learning velocity proxy |
| First Pass Yield | `Units Passing First Inspection / Total Units` | Execution quality |

**Manufacturing Adaptation Formula:**

```
Manufacturing Adaptation Score =
    (Defect Detection Speed  × 0.25)   ← observation loop
  + (Root Cause Cycle Time   × 0.25)   ← decision + execution
  + (Kaizen Velocity         × 0.20)   ← learning rate
  + (First Pass Yield        × 0.20)   ← execution quality
  + (Supplier Adaptation     × 0.10)   ← external dependency
```

**Benchmark cases:**

| System | Score | Why |
|---|---|---|
| Toyota | 1.20 | Kaizen = built-in learning velocity; short feedback loops at every station |
| Boeing | 4.10 | Long defect-to-fix cycles; governance delays in quality escalation |
| Siemens | 2.95 | Strong automation; customer legacy systems create external friction |

**Toyota as the manufacturing ASF benchmark:**
Toyota's Production System is the closest real-world implementation of a low-latency adaptive system. Every Andon cord pull is an observation event. Every immediate line stop is a zero-delay decision. Every kaizen is a learning velocity increment.

---

## Cross-Application Formula Summary

Each application uses the same weighted scoring structure:

```
Adaptation Score =
    Σ (Dimension Score × Weight) − (Learning Velocity × Accelerator Weight)

Where:
  Dimension Scores  = 1 (fast/good) to 5 (slow/poor)
  Learning Velocity = 1 (slow) to 5 (fast) — subtracts from total
  Weights           = application-specific (sum to 1.0)
```

The same formula. Different weights. Different data sources. Same insight:

> **The system that closes its feedback loops fastest wins.**
