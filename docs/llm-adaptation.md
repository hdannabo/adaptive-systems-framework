# ASF for LLMs — Adaptation Efficiency Module

## The Problem

The current LLM industry has three structural problems that ASF directly addresses.

---

### Problem 1 — Token Cost Explosion

Companies are discovering AI usage is not free. Token-based pricing creates unpredictable costs. Most CFOs cannot accurately track AI spend. Executives are asking whether AI value justifies AI cost.

**ASF reframes the question:**
> Stop measuring cost per token. Start measuring value per token.

```
Token ROI = Business Value Generated / Total Tokens Consumed
```

---

### Problem 2 — Context Window Degradation

Large context windows are marketed as capability. Research shows performance often degrades as context fills — "context rot." A 1M token window does not mean 1M tokens of reliable reasoning.

**ASF measures effective context utilization:**

```
Effective Context Utilization (ECU) =
    Useful Output Tokens / Total Input Tokens Consumed

Context Rot Score =
    1 − (Performance at 80% fill / Performance at 20% fill)

Score > 0.15 = significant degradation
Score > 0.30 = severe — the window is a liability
```

---

### Problem 3 — Agent Cost vs Agent Value

Agentic workflows consume dramatically more tokens than standard completions. Some research reports 10–100× token inflation from orchestration overhead. Higher spend does not guarantee better outcomes.

**ASF measures agent efficiency:**

```
Agent Efficiency Ratio = Task Value / Token Cost

Loop Overhead = (Agent Tokens − Baseline Tokens) / Baseline Tokens

Cost Per Adaptation = Total Agent Cost / Successful Adaptations
```

---

## The LLM as an Adaptive System

ASF treats an LLM interaction as a complete adaptive cycle:

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

Each stage has a measurable latency and friction source — identical to the organizational ASF model.

---

## LLM Adaptation Efficiency Formula

```
LLM Adaptation Efficiency =
    (Task Accuracy           × 0.30)   ← did it get the right answer?
  + (Context Utilization     × 0.20)   ← useful output per token consumed
  + (Retrieval Precision     × 0.20)   ← did it find the right information?
  + (Reasoning Depth         × 0.15)   ← multi-step coherence
  + (Feedback Responsiveness × 0.15)   ← correction uptake speed

Scale: 0–100
```

---

## Publicly Available LLM Landscape (2026)

Based on publicly available benchmarks and reported performance. Not vendor-endorsed.

| Model | Context Window | Cost Profile | Retrieval | Reasoning | ASF Efficiency |
|---|---|---|---|---|---|
| Claude (Anthropic) | 1M tokens | High | High | High | 88 |
| GPT-5 (OpenAI) | Large | Medium | High | High | 86 |
| Gemini (Google) | 1M+ tokens | Medium | High | Medium-High | 84 |
| DeepSeek | Lower | Low | Medium | Medium | 78 |

**Key insight:** A model with a smaller but more efficiently used context window outperforms a larger-window model suffering from context rot. Efficiency beats raw capacity.

---

## ASF Friction Map for LLMs

| ASF Friction Category | LLM Manifestation | Intervention |
|---|---|---|
| Technical friction | Context rot, hallucination, tool call failures | Prompt optimization, RAG tuning, smaller focused prompts |
| Organizational friction | No eval framework, no cost governance | Token budgets, model selection policy, eval pipelines |
| Human friction | Prompt quality variance, no feedback loops | Prompt libraries, user training, structured templates |
| Governance friction | No AI policy, no output review | AI governance framework, human-in-the-loop checkpoints |
| Data friction | Poor retrieval, stale knowledge bases | RAG hygiene, chunking strategy, re-ranking |

---

## Enterprise AI ROI via ASF

```
AI Value Realization Score =
    (Adoption Velocity       × 0.30)
  + (Value Realization Speed × 0.25)
  + (ROI Efficiency          × 0.25)
  + (Cost Predictability     × 0.20)

ROI Efficiency =
    Measured Business Value / Total AI Spend

Value Realization Lag =
    First Measurable Value Date − AI Deployment Date  (weeks)
```

**The ASF diagnosis for low AI ROI:**

```
Symptom:     High AI spend, low measured value
Friction:    Skill gap + ownership ambiguity + no feedback loops
Pattern:     Token costs rising, adoption flat, ROI unclear
Intervention:
  P0: Define measurable value metrics before scaling spend
  P0: Assign clear AI product ownership
  P1: Build adoption telemetry — who is using what, how often
  P1: Reduce time-to-first-value with guided onboarding
  P2: Implement token budget governance per team/use case
```

---

## The Core ASF Insight for AI

> Organizations are not failing because AI models are bad.
> They are failing because their **adaptation latency** — the time between deploying AI and realizing value — is too long.

The model is not the bottleneck.
The organization is.

ASF measures the organizational adaptation latency around AI — and tells you exactly where the friction is.
