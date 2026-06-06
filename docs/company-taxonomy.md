# ASF Company Taxonomy

Classifies organizations by their expected ASF signal — adaptation latency profile,
dominant friction sources, and control layer characteristics.

---

## Taxonomy Groups

### 1. Fast Adapters
**Expected signal:** Low adaptation latency

| Company | Notes |
|---|---|
| Microsoft | Sustained platform investment; Azure + AI pivots executed at scale |
| NVIDIA | Hardware + software roadmap tightly coupled to market demand |
| Netflix | Completed transformation; now a reference model for cloud-native ops |
| Amazon | Platform-first culture; AWS as both product and internal infrastructure |
| Toyota | Lean manufacturing = built-in friction reduction methodology |
| OpenAI | Born in the adaptation era; minimal legacy constraint |

**Dominant pattern:** Recognition and execution are organizationally aligned. Platform investments made early reduce friction compounding over time.

---

### 2. Strong but Complex
**Expected signal:** Medium adaptation latency

| Company | Notes |
|---|---|
| Google | Strong engineering; complex org structure slows cross-product adaptation |
| Meta | Fast on consumer; slower on enterprise/regulatory adaptation |
| Databricks | Fast product; customer adoption latency varies by segment |
| Snowflake | Data platform reduces customer friction; own roadmap execution strong |
| JPMorgan | Heavy compliance layer; significant tech investment offsetting governance delay |
| Walmart | Scale creates coordination friction; strong logistics but data adaptation complex |

**Dominant pattern:** Technical capability is strong but organizational complexity and governance requirements introduce medium adaptation latency. Interventions focus on coordination, not capability.

---

### 3. Legacy-Heavy
**Expected signal:** High friction

| Company | Notes |
|---|---|
| AT&T | Large installed base; significant manual dependency and legacy systems |
| Verizon | Similar profile to AT&T; network infrastructure constraints |
| Vodafone | Multi-market regulatory and legacy complexity |
| Boeing | Governance + skill gap + safety culture friction (see case studies) |
| Ford | EV transition exposes legacy manufacturing and org model friction |
| GE | Decade-long restructuring reflects accumulated adaptation debt |

**Dominant pattern:** Recognition is not the problem. Legacy systems and manual dependencies create structural friction that requires sustained multi-year intervention programs to reduce.

---

### 4. Governance-Heavy
**Expected signal:** Control layer dominates

| Company | Notes |
|---|---|
| Anthropic | AI safety governance is core design constraint — intentional control layer |
| Boeing | Regulatory + safety controls (overlaps with legacy-heavy group) |
| Finance (sector) | Compliance, audit, regulatory approval gates at every layer |
| Healthcare (sector) | Patient safety + HIPAA + FDA approval cycles |
| AI labs (general) | Model deployment governance, responsible AI review processes |

**Dominant pattern:** Adaptation latency is not primarily from legacy systems or skill gaps — it is from legitimate and required control layer processes. The intervention is automation of controls, not removal.

---

### 5. Historical Slow Adapters
**Expected signal:** High adaptation latency (terminal in some cases)

| Company | Notes |
|---|---|
| Kodak | Invented digital camera; film revenue protection delayed business-model adaptation ~37 years |
| Nokia | Recognized smartphone shift; internal fragmentation prevented coordinated response |
| Blockbuster | Recognition failure compounded adaptation failure |
| Yahoo | Multiple strategic pivots without sustained platform execution |
| BlackBerry | Strong enterprise position; consumer shift adaptation too slow |

**Dominant pattern:** The most dangerous friction is not technical. Business-model protection and ownership ambiguity create organizational resistance that outlasts technical recognition by years or decades.

---

### 6. Operations-Heavy
**Expected signal:** Coordination latency

| Company | Notes |
|---|---|
| FedEx | Distributed physical network; software adaptation fast, physical coordination slow |
| UPS | Similar to FedEx; strong technology investment but physical floor on latency |
| DHL | Multi-market physical operations; coordination complexity high |
| Maersk | Container shipping; adaptation latency has physical lower bound |
| Airlines (sector) | Safety + operations + regulatory = triple-layer friction |

**Dominant pattern:** Adaptation latency has a physical floor. Intervention focus: reduce *organizational* latency to approach the physical lower bound. Cannot compress below it.

---

### 7. Manufacturing
**Expected signal:** Legacy + automation friction

| Company | Notes |
|---|---|
| Siemens | Strong digital ambition; installed base replacement cycles are decade-scale |
| ABB | Industrial automation leader; own transformation constrained by customer legacy |
| Honeywell | Similar to ABB; software layer strategy on legacy hardware |
| Caterpillar | Heavy equipment; autonomous/electric transition friction high |
| Foxconn | Scale manufacturing; automation investment significant but org complexity high |

**Dominant pattern:** Hardware asset lifecycles create hard constraints on adaptation speed. Intervention: software and data layers on existing hardware rather than hardware replacement.

---

### 8. Retail / Consumer
**Expected signal:** Data + customer behavior adaptation

| Company | Notes |
|---|---|
| Target | Strong data investment; supply chain and digital/physical integration friction |
| Nike | Digital transformation ongoing; direct-to-consumer shift well-executed |
| Costco | Intentionally low-tech model; adaptation latency by design |
| Coca-Cola | Brand adaptation fast; operational/supply chain adaptation slower |
| P&G | Data and consumer behavior adaptation ongoing; organizational scale creates friction |

**Dominant pattern:** Customer behavior shifts are the primary input event. Data quality and organizational complexity are dominant friction sources. Companies that built data infrastructure early show lower latency.

---

## Taxonomy as ASF Input

This taxonomy is the starting point for an ASF analysis — not the conclusion.
The expected signal per group reflects historical and public patterns.
Actual adaptation latency for any organization requires a full ASF diagnostic:

1. Identify the specific input event
2. Map the current operating state
3. Run delta and friction analysis
4. Measure actual latency against the group baseline

The taxonomy tells you where to look first.
The ASF diagnostic tells you what is actually there.
