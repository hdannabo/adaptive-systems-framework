# ASF Research Hypotheses — v0.1

These are working hypotheses. They are not conclusions.
The goal of early ASF research is to test, validate, or disprove each one
across multiple domains and system types.

---

## H1 — Friction, Not Capability

> Adaptation failure is more often caused by friction than by lack of capability or awareness.

**Observable implication:** Organizations that recognize a required change but fail to adapt will show measurable friction in at least one layer (observation, decision, execution) — not simply a lack of knowledge about what to do.

**Counter-hypothesis:** Some systems genuinely lack capability, not just execution. Distinguishing friction from capability gap is a core measurement challenge.

---

## H2 — Feedback Loop Velocity

> Systems with faster, higher-quality feedback loops adapt faster across successive cycles.

**Observable implication:** Organizations with real-time observability, automated testing, and short release cycles will show lower execution and feedback latency than those without — independent of team size or budget.

**Counter-hypothesis:** Feedback quality matters more than feedback speed. Noisy fast feedback may increase decision latency by creating ambiguity.

---

## H3 — Dependency Index

> Systems with lower dependency on manual processes, human approvals, and coordination overhead adapt faster.

**Observable implication:** Dependency Index will correlate negatively with Adaptation Rate across the company taxonomy.

**Counter-hypothesis:** Some manual dependencies are load-bearing — removing them creates risk rather than speed. The relationship may be non-linear.

---

## H4 — Recognition Is Not the Bottleneck

> Most systems that fail to adapt had already recognized the need for change.

**Observable implication:** Case studies of failed adaptation (Kodak, Nokia, Blockbuster) will show evidence of early recognition followed by delayed execution — not absence of recognition.

**Counter-hypothesis:** Recognition failure is more common than it appears. Organizations may believe they recognized a signal when they actually misinterpreted it (H5).

---

## H5 — Interpretation Accuracy

> Misinterpretation of signals is a significant but underdiagnosed source of adaptation latency.

**Observable implication:** Post-mortems of slow or failed adaptations will frequently reveal that the initial interpretation of the signal was incomplete or incorrect — leading to effort invested in the wrong response.

**Counter-hypothesis:** Interpretation errors are often corrected quickly once execution begins. The latency cost of misinterpretation may be lower than the latency cost of governance friction.

---

## H6 — Organizational Friction Dominates Technical Friction

> In mature organizations, organizational friction (approval layers, ownership ambiguity, siloed teams) creates more adaptation latency than technical friction (legacy systems, tooling).

**Observable implication:** Intervention programs that address organizational friction will show larger latency reductions than those that only address technical friction.

**Counter-hypothesis:** Technical debt compounds over time and eventually exceeds organizational friction as the dominant bottleneck. The relative weight shifts with organizational age.

---

## H7 — Learning Velocity Compounds

> Systems that improve their learning velocity show compounding adaptation rate improvements over successive cycles.

**Observable implication:** Organizations with strong post-mortem cultures, knowledge management, and institutional memory will show accelerating adaptation rates over time — not just consistent rates.

**Counter-hypothesis:** Learning velocity gains plateau as organizations scale. Complexity and coordination overhead grow faster than learning systems can compensate.

---

## H8 — Universal Model Applicability

> The universal adaptive system model (Observation → Interpretation → Decision → Execution → Feedback → Learning → Adaptation) applies meaningfully across all domains — human, organizational, technical, biological.

**Observable implication:** The same metrics (observation latency, decision latency, execution latency, feedback delay, learning velocity) will produce coherent and comparable measurements when applied to a human learner, an enterprise transformation, and an AI agent in the same analytical framework.

**Counter-hypothesis:** Domain-specific factors may make cross-domain comparison misleading. A human's "decision latency" and an organization's "decision latency" may not be meaningfully comparable.

---

## Research Priority

| Hypothesis | Priority | Testability |
|---|---|---|
| H4 — Recognition is not the bottleneck | High | High — public case data available |
| H1 — Friction, not capability | High | Medium — requires organizational data |
| H3 — Dependency Index | High | Medium — requires measurement tooling |
| H2 — Feedback loop velocity | Medium | High — engineering metrics available |
| H6 — Org friction > technical friction | Medium | Medium — case study dependent |
| H5 — Interpretation accuracy | Medium | Low — hard to observe retrospectively |
| H7 — Learning velocity compounds | Low | Low — requires longitudinal data |
| H8 — Universal model applicability | Low | Low — requires cross-domain dataset |

---

## Next Steps

1. Select 10 initial case studies spanning at least 3 domains
2. Apply the universal model to each and score all 8 metrics
3. Identify which hypotheses are supported, challenged, or inconclusive
4. Publish findings and invite contributions
