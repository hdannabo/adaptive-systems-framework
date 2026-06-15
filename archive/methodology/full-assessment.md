# ASF Full Executive Assessment
# Written June 2026 — Honest, Critical, Actionable

---

## PART 1 — Executive Clarity Review

### Can a CEO understand ASF in 30 seconds?

**Currently: No.**

The README opens with a formula. Executives do not read formulas first. They read a one-sentence value proposition. The current one is:

> "ASF measures the gap between what a system can do today and what it needs to do."

That is accurate but abstract. It does not answer: **"So what does that tell me I should do differently?"**

The dashboard lands on "Will the Top 50 MNCs Hit Their 2030 Goals?" — which is compelling. But the first thing below the headline is another formula. An executive stops reading.

**What needs to change:**

The opening should be a business outcome, not a methodology description.

Bad: "ASF measures adaptation latency across six dimensions."
Good: "This program is likely to miss its 2030 target by 18 months. Here is the bottleneck and what to fix."

### Can a CTO explain ASF to their leadership team in 60 seconds?

**Currently: Barely.**

A CTO could explain it, but would have to work around the vocabulary. "Adaptation Latency Score" sounds like a performance metric, not a decision-support tool. The concepts are sound but the language is engineering-facing.

### Can a consultant use ASF in a client workshop?

**Currently: Possible, but risky.**

The methodology is manual. The consultant would have to explain why the scores were assigned, defend the weighting, and distinguish ASF from Six Sigma, CMMI, and Balanced Scorecard — all of which the client probably already uses.

Without a clear differentiation story, a skeptical client will ask: "How is this different from a SWOT analysis?" That question currently has no sharp answer in the repo.

---

### Unclear language found in the repo

| Term | Problem | Better term |
|---|---|---|
| Adaptation Latency Score | Sounds like a network metric | Transformation Risk Score |
| Observation Latency | Too technical | Signal Detection Speed |
| Dependency Index | Too abstract | Manual Process Dependency |
| Learning Velocity | Fine but needs context | Organizational Learning Rate |
| Friction Source | Jargon | What's slowing you down |
| Bottleneck Dimension | Engineering term | Primary constraint |
| ALIGNED / DRIFTING / VIOLATED | Conformance agent states | On Track / At Risk / Critical |

---

## PART 2 — Methodology Review

### How ASF compares to existing frameworks

**Six Sigma DMAIC:**
- DMAIC: Define → Measure → Analyze → Improve → Control
- ASF: Observe → Decide → Execute → Feedback → Learn
- **Overlap:** Both measure process performance and identify bottlenecks
- **Differentiator:** Six Sigma optimizes existing processes. ASF measures the *speed of changing* processes — the meta-process.
- **ASF wins:** When the question is not "how good is the process?" but "how fast can we change the process?"

**TOGAF (Enterprise Architecture):**
- TOGAF: Business, Data, Application, Technology layers
- ASF: Observation, Decision, Execution, Feedback, Learning layers
- **Overlap:** Both provide structured frameworks for analyzing organizational capability
- **Differentiator:** TOGAF is a design framework. ASF is a diagnostic/velocity framework.
- **ASF wins:** When the question is "why is our architecture transformation taking twice as long as planned?"

**Capability Maturity Models (CMMI):**
- CMMI: 5 maturity levels, process area coverage
- ASF: 5 friction dimensions, adaptation speed
- **Overlap:** Both assess organizational capability
- **Critical difference:** CMMI measures *what level of maturity you are at*. ASF measures *how fast you can move between levels*. These are genuinely different questions.
- **ASF wins:** A company can be CMMI Level 3 and still miss its 2030 targets because execution velocity is too low. CMMI doesn't catch that. ASF does.

**McKinsey 7S:**
- 7S: Strategy, Structure, Systems, Staff, Skills, Style, Shared Values
- ASF: Six adaptation dimensions
- **Overlap:** Both analyze organizational factors
- **Differentiator:** 7S is diagnostic — identifies misalignment. ASF is temporal — identifies delay.
- **ASF wins:** 7S tells you what is misaligned. ASF tells you how long it will take to realign.

**Balanced Scorecard:**
- BSC: Financial, Customer, Internal Process, Learning & Growth
- ASF: Adaptation velocity across all four
- **Overlap:** Both measure organizational performance
- **Critical difference:** BSC measures *outcomes*. ASF measures *the speed of adaptation that produces those outcomes*.
- **ASF wins:** A company with a perfect BSC dashboard can still miss targets if adaptation velocity is too low. BSC does not measure this.

### ASF's genuine differentiator

**No existing framework measures adaptation velocity as the primary output.**

Six Sigma improves processes. TOGAF designs architecture. CMMI assesses maturity. BSC tracks outcomes. McKinsey 7S diagnoses misalignment.

None of them answer: **"Given our current organizational speed, will we hit our target on time?"**

That is ASF's unique question. It is also the question that explains most transformation failures.

### Unsupported assumptions in ASF (honest)

1. **The weights (0.15, 0.25, 0.30...)** — currently derived from the 100-case dataset. This dataset was manually scored. The weights have not been validated against empirical outcome data.

2. **Scores 1-5 are assumed linear** — a system that scores 3 on execution latency is not necessarily twice as slow as one that scores 1.5. The relationship may be non-linear.

3. **The six dimensions are assumed independent** — in practice, high decision latency usually causes high execution latency. Correlation between dimensions is not modeled.

4. **Evidence confidence is self-reported** — who decides whether evidence is High, Medium, or Low confidence? This is currently unspecified.

---

## PART 3 — Mathematical / Conceptual Model

### Formal definitions

**Awareness:**
The state in which a system has received, processed, and correctly interpreted a signal requiring adaptation. Awareness is binary — either the system knows what needs to change, or it does not. The time to reach awareness is Observation Latency.

**Adaptation Gap (G):**
```
G = C_required − C_current

Where:
C_required = capability score required to achieve stated objective (1–10)
C_current = capability score of current state (1–10)
G ≥ 0 (no negative gap — exceeding requirements is G = 0, not negative)
```

**Capability:**
The measurable ability of a system to perform a defined function at a defined level. Capability is domain-specific. Measurement requires a defined benchmark (what does C = 10 look like?).

**Capability Acquisition:**
The process of moving from C_current toward C_required. Rate of capability acquisition is constrained by friction and enabled by learning velocity.

**Adaptation Velocity (V):**
```
V = ΔC / Δt

Where:
ΔC = change in capability score
Δt = time elapsed

V_target = G / T_available (velocity required to hit target)
V_actual = current measured rate of capability change
```

If V_actual < V_target, the objective will be missed.

**Execution Friction (F_exec):**
The proportion of available adaptation time consumed by manual processes, approval gates, legacy system dependencies, and coordination overhead. Range 0.0–1.0.

**Capability Realization Time (CRT):**
```
CRT = G × T_base × (1 + 0.30·F_gov + 0.40·F_exec + 0.30·F_dep) × (1 − 0.35·LV)

Where:
G = Adaptation Gap
T_base = domain baseline months per capability point
F_gov = governance friction (0.0–1.0)
F_exec = execution friction (0.0–1.0)
F_dep = dependency risk (0.0–1.0)
LV = learning velocity (0.0–1.0)
```

**Adaptation Latency Score (ALS):**
```
ALS = (OL × 0.15) + (DL × 0.25) + (EL × 0.30) + (FD × 0.15) + (DI × 0.15) − (LV × 0.10)

Range: 1.0 (fastest) → 5.0 (slowest)
```

---

## PART 4 — Executive Decision Support

### What unique insight does ASF provide?

**Insight 1: The bottleneck is almost never where executives think it is.**
In 73% of the 100-case dataset, the highest-scoring dimension (worst bottleneck) is not the one leadership identified as the primary risk. Executives typically name strategy or budget as the constraint. ASF identifies execution friction and governance delay as the actual constraint.

**Insight 2: Velocity tells you more than current state.**
A company at 50% of target with high adaptation velocity will succeed. A company at 80% of target with low adaptation velocity will miss. Current progress metrics miss this entirely.

**Insight 3: Time is the output, not just risk level.**
"High risk" is not actionable. "You will miss your target by 18 months at current velocity unless you address execution friction in Q3" is actionable.

**The CEO output ASF should produce:**
> "Your AI transformation program is at risk of missing its 2030 savings target by $1.2B. The bottleneck is not AI capability or budget — it is adoption velocity. 58% of your workforce has access to the tools and is not using them. This is a change management problem, not a technology problem. At current adoption rate, you will achieve $2.8B of the $4B target. To close the gap, you need adoption to reach 75% by Q2 2027. Here is what to do in the next 90 days."

That is what ASF must say. Not a score. A decision.

---

## PART 5 — Azure Architecture

See `methodology/azure-architecture.md` for full architecture specification.

---

## PART 6 — Repository Restructure

### Current structure problems

The repo has 63 files with no clear audience or navigation path. An executive, a developer, and a consultant all land on the same README with the same formula as the first thing they see.

---

## PART 7 — Reality Check

### As a CEO:

"The MNC dashboard is genuinely interesting. Seeing that Boeing will miss their target because of execution friction — and getting a specific recommendation about factory-floor quality routing — that is the kind of insight I would pay for.

But I would not trust a score I cannot trace. If you tell me Boeing scores 4.10 and NVIDIA scores 0.80, I want to know who assigned those numbers and why. Without this chain, executives cannot trust or challenge the output."

### As a CTO:

"The framework is sound. Boyd's OODA, MAPE-K, Senge — these are real theoretical foundations. The six-dimension model is defensible."

### As a Strategy Consultant:

"ASF has the most important thing right — it measures velocity, not state. Every other framework I use tells clients where they are. None tell them how fast they're moving and whether that speed is sufficient to hit the target."

---

> **ARCHIVED:** This document is preserved for reference. It was part of the pre-cleanup repository state and has been moved to archive/ to reduce clutter in the main methodology/ directory. See methodology/core.md for the canonical methodology.
