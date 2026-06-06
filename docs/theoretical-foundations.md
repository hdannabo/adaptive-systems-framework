# ASF Theoretical Foundations

ASF is not invented from scratch. It is grounded in six established bodies of knowledge. This document makes those connections explicit.

---

## 1. Systems Thinking

**Key contributors:** Peter Senge, Donella Meadows, Jay Forrester

Systems Thinking is the study of how feedback loops, delays, and nonlinear dynamics shape the behavior of complex systems over time.

### Connection to ASF

ASF's core model — Environment → Observation → Decision → Execution → Feedback → Learning → Adaptation — is a feedback loop in the Systems Thinking tradition. Every ASF latency metric corresponds to a delay in that loop.

Donella Meadows identified **delays** as one of the most dangerous system properties:
> "The information that's supposed to govern the system is delayed, incomplete, or filtered."

This is the precise mechanism ASF measures. Observation Latency, Decision Latency, and Execution Latency are the three primary delays in an adaptive system's feedback loop.

**Jay Forrester's System Dynamics** (MIT, 1950s) introduced stock-and-flow modeling for organizational behavior — the precursor to quantitative adaptation measurement.

**Peter Senge's The Fifth Discipline** (1990) introduced the concept of the **learning organization** — a system that continuously expands its capacity to adapt. ASF's Learning Velocity metric directly operationalizes Senge's framework.

### Key principle applied
> Systems with shorter feedback loops and higher learning velocity outperform those with longer delays — regardless of initial capability.

---

## 2. Learning Organizations

**Key contributor:** Peter Senge (The Fifth Discipline, 1990)

A Learning Organization is one that continuously transforms itself through five disciplines:
- Systems Thinking
- Personal Mastery
- Mental Models
- Shared Vision
- Team Learning

### Connection to ASF

ASF's **Learning Velocity** metric directly measures the degree to which an organization exhibits Learning Organization properties. Systems that repeat the same failures, lack postmortem culture, or fail to institutionalize lessons score low on Learning Velocity — regardless of their technical capability.

**The core ASF hypothesis maps directly to Senge:**
> "The only sustainable competitive advantage is an organization's ability to learn faster than the competition."

ASF makes this measurable.

---

## 3. OODA Loop

**Key contributor:** John Boyd (US Air Force, 1970s–1980s)

The OODA Loop — **Observe, Orient, Decide, Act** — was developed by fighter pilot and military strategist John Boyd to describe how combatants process information and respond to changing conditions.

The key insight: **the winner is not the strongest or most capable — it is the one who cycles through the OODA loop faster.**

### Connection to ASF

| OODA | ASF Layer | ASF Metric |
|---|---|---|
| Observe | Observation | Observation Latency |
| Orient | Interpretation | Interpretation Accuracy |
| Decide | Decision | Decision Latency |
| Act | Execution | Execution Latency |
| (loop) | Feedback + Learning | Feedback Delay + Learning Velocity |

Boyd's insight — that tempo, not power, determines outcomes — is the strategic foundation of ASF's core hypothesis: **systems succeed when their rate of adaptation exceeds the rate of environmental change.**

---

## 4. Cybernetics

**Key contributors:** Norbert Wiener (Cybernetics, 1948), W. Ross Ashby

Cybernetics is the study of **regulatory systems** — how systems maintain stability and adapt through feedback and control.

Ashby's **Law of Requisite Variety** states:
> "Only variety can absorb variety."

A system can only control its environment to the degree that its internal variety (adaptability) matches the variety (complexity) of that environment.

### Connection to ASF

ASF's **Adaptation Rate** metric is a direct operationalization of Ashby's Law. A system whose adaptation rate falls below the rate of environmental change will eventually fail to maintain control — regardless of past performance.

Wiener's cybernetic feedback loop (stimulus → response → measurement → correction) is the mathematical ancestor of the ASF adaptive cycle.

---

## 5. Adaptive Systems Theory

**Key contributors:** Holland (Complex Adaptive Systems, 1992), Kauffman, Gell-Mann (Santa Fe Institute)

Complex Adaptive Systems (CAS) research established that many real-world systems — organizations, ecosystems, markets, immune systems — exhibit emergent adaptation through local interactions rather than central control.

### Connection to ASF

ASF applies CAS principles to organizational and technical systems:
- **Emergence**: adaptation patterns emerge from the interaction of many friction sources, not from a single bottleneck
- **Fitness landscapes**: organizations navigate a changing environment; the Adaptation Latency Score approximates position on the fitness landscape
- **Co-evolution**: systems and environments adapt to each other simultaneously — ASF's feedback loop captures this dynamic

---

## 6. Control Theory and MAPE-K

**Key contributors:** Kephart & Chess (IBM, 2003) — MAPE-K for autonomic computing

**MAPE-K** — **Monitor, Analyze, Plan, Execute** with a shared **Knowledge** base — was introduced by IBM Research as a reference architecture for self-managing (autonomic) systems.

```
Monitor → Analyze → Plan → Execute
              ↑                    ↓
              └──── Knowledge ─────┘
```

### Connection to ASF

| MAPE-K | ASF Layer | ASF Metric |
|---|---|---|
| Monitor | Observation | Observation Latency |
| Analyze | Interpretation + Delta Analysis | Interpretation Accuracy |
| Plan | Decision + Intervention Plan | Decision Latency |
| Execute | Execution | Execution Latency |
| Knowledge | Learning + Feedback | Learning Velocity + Feedback Delay |

MAPE-K was designed for autonomic computing systems. ASF extends this pattern to organizational and AI systems, adding the **human friction layer** that MAPE-K did not account for.

Modern research combines MAPE-K with machine learning (ML-MAPE) — replacing rule-based analyzers and planners with learned models. ASF's LLM Adaptation Efficiency module (see `docs/llm-adaptation.md`) is a direct application of ML-MAPE principles.

---

## Summary

| Framework | Origin | What ASF takes from it |
|---|---|---|
| Systems Thinking | Forrester, Meadows, Senge | Feedback loops, delays, learning organizations |
| OODA Loop | John Boyd | Tempo as the primary competitive variable |
| Cybernetics | Wiener, Ashby | Law of Requisite Variety, feedback control |
| Adaptive Systems | Santa Fe Institute | Emergence, fitness landscapes |
| MAPE-K | IBM Research | Monitor-Analyze-Plan-Execute architecture |
| Learning Organizations | Peter Senge | Learning Velocity as organizational capability |

ASF is not a new theory. It is the **engineering operationalization** of these six frameworks — turning conceptual models into measurable metrics, scored cases, and prioritized interventions.
