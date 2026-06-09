# ASF Roadmap

## The Central Question

> What am I building?

A framework for measuring adaptation velocity and capability realization.

> What makes it valuable?

Not the UI. The methodology, the evidence model, and the CRT engine.
A consultant should be able to use ASF with only paper and the methodology.
The code and dashboards make it faster, not possible.

---

## v0.3 — Current (Complete)

**What it is:** Research framework with working scoring engine and manually-produced dataset.

**What works:**
- Python scoring engine — deterministic, tested, correct
- CLI analyzer — YAML → full ASF report in seconds
- CRT engine — capability realization time estimation
- Conformance agent — output validation against acceptance criteria
- 5 live dashboards — company benchmarks with multi-objective + decision support
- 100-case dataset — manually scored across 10 domains
- Methodology folder — what-is-asf, vs-other-frameworks, assumptions

**What is manual:**
- Company dimension scores are assigned by human analyst reading public documents
- Document analyzer counts keywords, not semantic meaning
- No automated extraction from source documents

---

## v0.4 — Evidence-Based Scoring (Next)

**Mission:** Replace keyword counting with LLM-based evidence extraction.
**Status:** ✅ Complete. Evidence extractor ships in v0.4.

**What changes:**
- `asf_document_analyzer.py` calls Azure OpenAI GPT-4o with structured output
- For each dimension, the LLM returns: `{score, evidence_quote, page_number, confidence}`
- Every score is now traceable to a specific sentence in the source document
- Confidence levels become objective based on evidence quality criteria

**What the output looks like:**
```json
{
  "execution_latency": {
    "score": 4,
    "evidence": "The Change Advisory Board review process adds 2-4 weeks to every AI deployment decision",
    "source_page": 12,
    "confidence": "Medium"
  }
}
```

**Why this matters:** The moment scoring is evidence-based, ASF becomes trustable by executives who need to defend their conclusions. A CEO can point to page 12 of Boeing's annual report. That is credibility a keyword counter cannot provide.

**Acceptance criteria for v0.4:**
- Upload any corporate PDF → receive full ASF report with evidence citations
- Every dimension score has at least one cited quote
- Analysis completes in under 30 seconds
- Token cost under $0.10 per analysis
- Output validated by ConformanceAgent (ALIGNED status)

---

## v0.5 — Automated Capability Extraction

**Mission:** Extract capability and objective data automatically from documents.
**Timeline:** 2–3 weeks of engineering.

**What changes:**
- Strategic objective extraction — LLM reads document, identifies stated goals and metrics
- Current capability estimation — LLM identifies current state metrics from document
- Required capability derivation — LLM infers required state from stated objectives
- Adaptation Gap computed automatically from extracted data

**The output changes from:**
"User provides: required_capability=8, current_capability=3.5"

**To:**
"System extracts from Boeing 2025 Annual Report:
  objective: '38 planes/month by 2026'
  current: '18 planes/month (Q4 2025)'
  gap: 20 planes/month = 3.8 capability points"

**Why this matters:** Self-service. No analyst required to assign numbers. Anyone uploads a document and gets the analysis.

---

## v0.6 — CRT Prediction Engine

**Mission:** Calibrate CRT estimates against outcome data.
**Timeline:** Requires 6–12 months of outcome data collection.

**What changes:**
- Retrospective validation study — 20+ organizations that closed capability gaps
- CRT formula recalibrated based on actual outcomes vs predictions
- Domain-specific calibration — manufacturing vs software vs government
- Confidence intervals tightened based on empirical evidence
- Learning velocity dimension calibrated against actual time-to-improvement data

**Why this matters:** CRT currently estimates. After v0.6, CRT predicts with validated accuracy. That is the difference between "this is our best estimate" and "in similar programs, 70% completed within this range."

---

## v1.0 — Enterprise ASF Platform

**Mission:** Productize ASF as a deployable enterprise platform.
**Timeline:** 3–6 months after v0.5 is proven.

**What it includes:**
- Azure deployment package (ARM templates / Bicep) — deploy in one command
- REST API with OpenAPI specification
- Web interface — upload document, receive full report (no Python required)
- Multi-tenant support — enterprise clients with isolated data
- Power BI report pack — executive cockpit for internal tracking
- Purview lineage integration — full audit trail for governance-sensitive environments
- SOC 2 Type II readiness documentation

**What the user experience is:**
```
1. Open browser to https://asf.yourdomain.com
2. Upload annual report or strategy document
3. Enter: system name, domain, target date
4. Receive: full ASF report with evidence, CRT, bottleneck, interventions
5. Share: URL to report for colleagues
6. Track: re-run quarterly to measure velocity change
```

---

## What Is NOT on the Roadmap

- More dashboards (unless directly improving methodology understanding)
- More company benchmarks (the 49-company MNC set is sufficient)
- More visualization types (the current UI is adequate)
- Mobile app
- Community features or social sharing

The long-term value of ASF is the **methodology, evidence model, and CRT engine** — not the UI.

Every hour spent on dashboards is an hour not spent on:
- Validation studies that make the methodology credible
- Evidence-based scoring that makes the output trustable
- CRT calibration that makes the predictions accurate

---

## The Question That Guides Every Decision

> Does this make the methodology stronger, the evidence more trustable, or the CRT more accurate?

If yes: do it.
If no: do not do it.
