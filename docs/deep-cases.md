# ASF Deep Case Studies — 10 Systems

Each case applies the full ASF formula stack: TAL, ALS, AFL, and primary friction identification.

---

## 1. OpenAI

**Domain:** AI Systems | **Type:** AI Lab / Product Platform

**Adaptation Scenario:** Enterprise agents need reliable, governed workflow execution

| Metric | Value | Notes |
|---|---|---|
| Observation Latency | Low (1–2 days) | Strong telemetry, fast signal detection |
| Decision Latency | Low–Medium (1–2 weeks) | Fast product cycle, some governance overhead |
| Execution Latency | Low (1–3 weeks) | Continuous deployment, API-first |
| Feedback Delay | Low (real-time) | Usage metrics, evals, red-teaming |
| Learning Velocity | Very High | Rapid model iteration |
| Dependency Index | 0.30 | Low manual dependency |
| **TAL** | **3–6 weeks** | |
| **ALS** | **88/100** | High adaptability |
| **Risk Band** | **Low** | |

**Primary friction:** Governance, cost, reliability at scale

**AFL analysis:**
- 100 user signals → 92 correctly interpreted (high observation accuracy)
- 92 → 85 decisions made (governance adds some delay)
- 85 → 78 executed (strong execution capability)
- 78 → 75 measured (real-time feedback)
- 75 → 70 learned from (rapid model refinement)
- **Total AFL: 30%** — best-in-class

**Key intervention:** Standardize agent observability and cost controls before scaling agentic deployments

---

## 2. Anthropic

**Domain:** AI Systems | **Type:** AI Safety Lab / Product Platform

**Adaptation Scenario:** Deploy trusted AI for enterprise workflows without compromising safety

| Metric | Value | Notes |
|---|---|---|
| Observation Latency | Low (1–3 days) | Strong safety monitoring |
| Decision Latency | Medium (2–4 weeks) | Safety review adds intentional latency |
| Execution Latency | Low–Medium (2–4 weeks) | Governed deployment |
| Feedback Delay | Low | Constitutional AI feedback loops |
| Learning Velocity | Very High | Safety + capability co-optimization |
| Dependency Index | 0.35 | Safety review is a deliberate dependency |
| **TAL** | **4–8 weeks** | |
| **ALS** | **85/100** | High adaptability |
| **Risk Band** | **Low** | |

**Primary friction:** Safety validation vs speed — intentional, not pathological

**Key insight:** Anthropic's governance friction is load-bearing. The intervention is not to remove it but to automate safety evaluation to reduce DL without reducing safety assurance.

---

## 3. Microsoft (Azure + Copilot)

**Domain:** Data & Cloud Platforms | **Type:** Enterprise Cloud Platform

**Adaptation Scenario:** Integrate AI natively across enterprise cloud and productivity stack

| Metric | Value | Notes |
|---|---|---|
| Observation Latency | Low | Strong telemetry across Azure estate |
| Decision Latency | Low–Medium | Large org but strong platform culture |
| Execution Latency | Low | Azure DevOps, CI/CD maturity |
| Feedback Delay | Low | Real-time usage analytics |
| Learning Velocity | High | Systematic product iteration |
| Dependency Index | 0.30 | Low for a company this size |
| **TAL** | **3–6 weeks** | |
| **ALS** | **87/100** | |
| **Risk Band** | **Low** | |

**Primary friction:** Enterprise customer complexity — customers adapt slower than the platform

**Key insight:** Microsoft's own adaptation is fast. The latency lives in customer adoption, not Microsoft's execution.

---

## 4. NVIDIA

**Domain:** Manufacturing & AI Infrastructure | **Type:** Semiconductor + AI Platform

**Adaptation Scenario:** Build data-center-scale AI infrastructure ahead of demand curve

| Metric | Value | Notes |
|---|---|---|
| Observation Latency | Very Low | Deep customer relationships, early signal access |
| Decision Latency | Very Low | CEO-driven, fast strategic decisions |
| Execution Latency | Medium | Hardware manufacturing has physical constraints |
| Feedback Delay | Low | Revenue, adoption, developer ecosystem signals |
| Learning Velocity | Very High | CUDA ecosystem compounds year over year |
| Dependency Index | 0.25 | Supply chain is the main dependency |
| **TAL** | **Hardware: 18–24 months / Software: 4–8 weeks** | |
| **ALS** | **91/100** | |
| **Risk Band** | **Low** | |

**Primary friction:** Physical manufacturing latency — cannot be compressed below supply chain floor

**Key insight:** NVIDIA separates hardware adaptation (long TAL, unavoidable) from software adaptation (short TAL, continuously improving). This dual-track model is a reference pattern.

---

## 5. Databricks

**Domain:** Data & Cloud Platforms | **Type:** Data + AI Platform

**Adaptation Scenario:** Operationalize enterprise data into governed, AI-ready assets

| Metric | Value | Notes |
|---|---|---|
| Observation Latency | Low | Strong customer success feedback |
| Decision Latency | Low–Medium | Product-led, fast roadmap cycles |
| Execution Latency | Low | Cloud-native, continuous delivery |
| Feedback Delay | Medium | Data quality issues create measurement lag |
| Learning Velocity | High | Unity Catalog and Delta Lake compound |
| Dependency Index | 0.40 | Customer data ownership creates dependencies |
| **TAL** | **4–8 weeks** | |
| **ALS** | **82/100** | |
| **Risk Band** | **Low–Medium** | |

**Primary friction:** Data quality and ownership ambiguity in customer environments

---

## 6. Toyota

**Domain:** Manufacturing | **Type:** Global Manufacturing System

**Adaptation Scenario:** Continuous quality improvement at global scale

| Metric | Value | Notes |
|---|---|---|
| Observation Latency | Hours | Andon cord — any worker stops the line immediately |
| Decision Latency | Hours–Days | Kaizen events, standardized problem-solving |
| Execution Latency | Days–Weeks | PDCA cycles, standardized work |
| Feedback Delay | Real-time | Jidoka — defect detection is built into the process |
| Learning Velocity | Very High | 50+ years of compounding kaizen |
| Dependency Index | 0.20 | Low — workers empowered to act |
| **TAL** | **Days to weeks** | Lowest in dataset |
| **ALS** | **95/100** | |
| **Risk Band** | **Low** | |

**Primary friction:** Supplier variability — outside Toyota's direct control

**AFL analysis:**
- Near 100% of production signals reach adaptation
- Andon cord eliminates observation latency at the source
- **Total AFL: ~10%** — world-class

**Key insight:** Toyota's adaptation system is not technology — it is culture and process. The Andon cord is the world's simplest and most effective observation latency reduction tool.

---

## 7. Boeing

**Domain:** Manufacturing | **Type:** Aerospace Manufacturing

**Adaptation Scenario:** Restore quality governance across complex global production

| Metric | Value | Notes |
|---|---|---|
| Observation Latency | Medium–High (days–weeks) | Quality signals exist but routing is slow |
| Decision Latency | High (weeks–months) | Multiple approval layers, executive escalation required |
| Execution Latency | Very High (months) | Supply chain complexity, regulatory requirements |
| Feedback Delay | High | Quality outcomes are lagging indicators |
| Learning Velocity | Low | Organizational silos prevent learning transfer |
| Dependency Index | 0.85 | Extremely high — almost every change requires human approval |
| **TAL** | **8–26 weeks** | |
| **ALS** | **42/100** | |
| **Risk Band** | **High** | |

**Primary friction:** Organizational silos + supply chain complexity + governance overhead

**AFL analysis:**
```
100 quality signals
 70 detected (observation gap — distributed manufacturing)
 50 correctly analyzed (interpretation gap — siloed data)
 35 decisions made (decision gap — approval overhead)
 20 executed (execution gap — supply chain complexity)
 12 measured (feedback gap — lagging quality KPIs)
  6 learned from (learning gap — knowledge silos)

Total AFL: 94% — among the highest in dataset
```

**Key intervention:** Real-time quality telemetry across manufacturing network; escalation path redesign to reduce DL from weeks to days

---

## 8. AT&T

**Domain:** Telecom & Networks | **Type:** Telecom Operator

**Adaptation Scenario:** AI-native network operations and autonomous incident response

| Metric | Value | Notes |
|---|---|---|
| Observation Latency | Medium (hours) | Telemetry exists but fragmented across systems |
| Decision Latency | High (weeks) | Legacy approval processes, CAB reviews |
| Execution Latency | Very High (months) | Legacy systems, manual dependencies, coordination overhead |
| Feedback Delay | High | Outcome measurement is slow and fragmented |
| Learning Velocity | Medium | Postmortem culture exists but knowledge transfer is weak |
| Dependency Index | 0.88 | Very high — nearly every change requires multiple approvals |
| **TAL** | **12–26 weeks** | |
| **ALS** | **38/100** | |
| **Risk Band** | **High** | |

**Primary friction:** Manual dependency + legacy systems

**Measurable improvement from MCP-based AI agent deployment (public reporting):**
- Replaced 15–20 analyst-equivalent workflows with production agent suite
- Reduced contract cost analysis cycle from weeks to hours
- Demonstrated positive ROI on AI infrastructure investment

**Key intervention:** Automate the top 5 manual dependencies in the network operations critical path; replace CAB gates with policy-as-code

---

## 9. Netflix

**Domain:** Entertainment & Media | **Type:** Streaming Platform

**Adaptation Scenario:** Maintain streaming dominance through personalization and content optimization

| Metric | Value | Notes |
|---|---|---|
| Observation Latency | Real-time | Every user interaction is instrumented |
| Decision Latency | Very Low (hours–days) | A/B testing infrastructure, data-driven culture |
| Execution Latency | Very Low (hours) | Full CI/CD, chaos engineering maturity |
| Feedback Delay | Real-time | Engagement metrics, completion rates, retention |
| Learning Velocity | Very High | Experimentation platform runs thousands of tests simultaneously |
| Dependency Index | 0.15 | Extremely low — highly automated |
| **TAL** | **Days** | |
| **ALS** | **93/100** | |
| **Risk Band** | **Low** | |

**Primary friction:** Content saturation — market-level constraint, not operational

**Key insight:** Netflix is the organizational embodiment of the ASF ideal state. Zero observation latency, near-zero decision latency, automated execution, real-time feedback. The remaining friction is external (content market), not internal.

**Reference pattern:** Netflix's experimentation platform is a reusable blueprint for any organization wanting to reduce TAL.

---

## 10. Kodak

**Domain:** Historical | **Type:** Consumer Electronics / Film

**Adaptation Scenario:** Transition from film to digital photography

| Metric | Value | Notes |
|---|---|---|
| Observation Latency | Low — signal was clear | Kodak engineer invented the digital camera in 1975 |
| Decision Latency | **Catastrophic — decades** | Film revenue protection blocked every decision |
| Execution Latency | Never reached | Decision was never made at business-model level |
| Feedback Delay | Not applicable | Outcome was never measured against digital |
| Learning Velocity | Near zero | No organizational learning from digital pilots |
| Dependency Index | 1.0 | Entire organization dependent on film revenue |
| **TAL** | **~37 years (1975–2012)** | |
| **ALS** | **8/100** | |
| **Risk Band** | **Critical — terminal** | |

**AFL analysis:**
```
100 market signals (digital photography emergence)
 90 observed (Kodak knew — they invented it)
 60 analyzed (internal reports documented the threat)
 10 decisions made (film revenue protection blocked action)
  2 executed (small digital pilots, never scaled)
  1 measured (no systematic outcome tracking)
  0 adapted (business model never changed)

Total AFL: 100% — complete adaptation failure despite full signal visibility
```

**Primary friction:** Revenue protection inertia — the most dangerous friction category

**The Kodak Theorem:** *Recognition of required change is not sufficient for adaptation. The primary bottleneck is not observation — it is the organizational will to act on what is already known.*

This finding is confirmed across all 9 historical failure cases in the dataset: every system that failed had recognized the need for change. None failed because they lacked information.
