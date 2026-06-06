# ASF AI Token Economics Framework

> **The question is not which model is cheapest per token.
> The question is which model generates the most value per dollar spent.**

---

## The Problem

Enterprise AI teams face three structural token economics problems:

### 1. Price Reversal
A model that appears cheaper on paper ends up costing more in practice. Research has documented cases where actual costs were **up to 28× higher than expected** — driven by excessive reasoning-token consumption in models that auto-activate extended thinking.

### 2. Agent Token Explosion
Agentic workflows consume dramatically more tokens than standard completions. Research shows agentic tasks can consume **1000× more tokens** than equivalent reasoning tasks. Higher consumption does not improve accuracy — accuracy plateaus while costs continue rising.

### 3. Context Rot
Larger context windows sound like capability. Performance frequently degrades before models reach their advertised context limits. A 1M token window does not mean 1M tokens of reliable reasoning.

---

## ASF Token Efficiency Formula

```
ASF Token Efficiency Score (0–100) =

    (Cost Efficiency Score      × 0.30)   ← value per dollar
  + (Context Efficiency Score   × 0.25)   ← useful output per token
  + (Reasoning Depth Score      × 0.20)   ← multi-step task capability
  + (Price Transparency Score   × 0.15)   ← predictability of actual cost
  - (Agent Overhead Risk        × 0.10)   ← risk of token explosion in agentic use

Where each dimension is scored 1–5 (1=poor, 5=excellent)
Agent Overhead Risk is inverted (High=penalty)
```

---

## Scoring Dimensions

| Dimension | What It Measures | Why It Matters |
|---|---|---|
| Cost Efficiency | Business value generated per $1M tokens | Direct ROI signal |
| Context Efficiency | Useful output per token consumed | Measures context rot risk |
| Reasoning Depth | Multi-step task success rate | Capability for complex work |
| Price Transparency | Predictability of actual vs listed cost | CFO visibility |
| Agent Overhead Risk | Token inflation in agentic workflows | Agentic cost control |

---

## Dataset — Public Pricing (USD per 1M tokens)

Sources: Provider pricing pages, public benchmarks, research papers.
All prices are approximate and subject to change. Last updated: 2026.

| Provider | Model | Input | Output | Context | Reasoning | ASF Score | Risk |
|---|---|---|---|---|---|---|---|
| Google | Gemini 1.5 Flash | $0.075 | $0.30 | 1M | No | 88 | Low |
| DeepSeek | V3.2 | $0.14 | $0.28 | 128K | No | 87 | Low |
| DeepSeek | V3 | $0.27 | $1.10 | 64K | No | 86 | Low |
| Meta | Llama 3.3 70B | Self-hosted | Self-hosted | 128K | No | 84 | Low |
| Google | Gemini 1.5 Pro | $1.25 | $5.00 | 1M | No | 84 | Low |
| Google | Gemini 2.5 Flash | $0.15 | $0.60 | 1M | Yes | 83 | Low |
| OpenAI | GPT-4o mini | $0.15 | $0.60 | 128K | No | 82 | Low |
| Mistral | Codestral | $0.20 | $0.60 | 32K | No | 82 | Low |
| Anthropic | Claude Sonnet 4.6 | $3.00 | $15.00 | 200K | No | 81 | Low |
| Mistral | Mistral Small | $0.20 | $0.60 | 32K | No | 81 | Low |
| Google | Gemini 2.0 Pro | $2.00 | $10.00 | 1M | No | 80 | Low |
| xAI | Grok-2 mini | $0.20 | $0.40 | 131K | No | 79 | Low |
| OpenAI | GPT-4o | $2.50 | $10.00 | 128K | No | 78 | Medium |
| Meta | Llama 3.1 405B | Self-hosted | Self-hosted | 128K | No | 77 | Medium |
| Mistral | Mistral Large | $2.00 | $6.00 | 128K | No | 76 | Medium |
| OpenAI | GPT-5 | $5.00 | $30.00 | 200K | No | 74 | Medium |
| DeepSeek | R1 | $0.55 | $2.19 | 128K | Yes | 74 | Medium |
| OpenAI | o4-mini | $1.10 | $4.40 | 200K | Yes | 72 | Medium |
| xAI | Grok-2 | $2.00 | $10.00 | 131K | No | 72 | Medium |
| Anthropic | Claude Opus 4.6 | $15.00 | $75.00 | 200K | No | 68 | High |
| OpenAI | o3 | $10.00 | $40.00 | 200K | Yes | 61 | High |

---

## Key Findings

### Finding 1 — Price Reversal is Real
Reasoning models (o3, DeepSeek R1) score lower on ASF Token Efficiency despite competitive listed prices. Extended thinking activation can multiply actual costs 10–28×. **ASF Agent Overhead Risk score flags this before deployment.**

### Finding 2 — Context Window × Cost is the Key Ratio
Gemini 1.5 Flash scores highest (88) because it combines the lowest input price ($0.075/1M) with the largest context window (1M tokens). This maximizes context efficiency — the single strongest predictor of production value.

### Finding 3 — 600× Price Decline, Frontier Premium Persists
Research documents ~600× decline in token prices since 2023. Despite this, frontier and reasoning models maintain a significant premium. The gap between efficient models ($0.075) and frontier reasoning models ($40+) is 500×.

### Finding 4 — Self-Hosted Changes the Equation
Meta's Llama models show high ASF efficiency because token cost is replaced by infrastructure cost — which scales differently and is more predictable. For high-volume enterprise use cases, self-hosting may be the highest-efficiency option.

### Finding 5 — The 1000× Agent Problem
Agentic tasks consuming 1000× more tokens than equivalent reasoning tasks is not a model problem — it is an **orchestration problem**. ASF intervention: add token budget controls and early-exit conditions to agent pipelines before scaling.

---

## ASF Recommendations by Use Case

| Use Case | Recommended Model | Reason |
|---|---|---|
| High-volume classification | Gemini 1.5 Flash or GPT-4o mini | Ultra-low cost, adequate capability |
| Long-document analysis | Gemini 1.5 Pro or Claude Sonnet 4.6 | 1M context at competitive price |
| Complex reasoning tasks | o4-mini or Gemini 2.5 Flash | Reasoning at lower overhead risk than o3 |
| European data sovereignty | Mistral Large or Mistral Small | EU-based provider |
| Code generation | Codestral or Claude Sonnet 4.6 | Specialized or general capability |
| Agentic workflows | Claude Sonnet 4.6 | Lowest agent overhead risk in frontier tier |
| Cost-first enterprise | DeepSeek V3.2 | Lowest absolute cost in dataset |
| Self-hosted / air-gapped | Llama 3.3 70B | Zero token cost, strong capability |

---

## The ASF Framing

Traditional benchmarks ask: **which model is most capable?**

ASF Token Economics asks: **which model generates the most value per dollar in your specific use case?**

Those are different questions with different answers.

A model scoring 90 on MMLU but causing price reversal in production is a worse choice than a model scoring 82 on MMLU with predictable, efficient token consumption.

**ASF measures production efficiency, not benchmark performance.**

---

## Files

| File | Description |
|---|---|
| `token-pricing.csv` | Raw pricing data — input/output cost, context window, reasoning flag |
| `asf-token-scores.csv` | ASF efficiency scores — all dimensions + risk band |
| `README.md` | This document |

---

## Data Sources

- Provider pricing pages (OpenAI, Anthropic, Google, DeepSeek, xAI, Mistral, Meta)
- Artificial Analysis public benchmarks
- Research: "TokenBench: A Benchmark for Token Economics in Large Language Models" (2026)
- Research: "Price Reversal in Reasoning Models" (2026)
- Public reporting on enterprise AI spend patterns

*All prices approximate. Verify against current provider pricing before production decisions.*
