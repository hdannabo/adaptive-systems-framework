# ASF — Current State (Honest Assessment)

**Version:** 0.3  
**Date:** June 2026  
**Author:** Hemanth Kumar Dannaboyina

---

## What Actually Works

### 1. Python Scoring Engine — Working

```bash
python cli.py --file examples/att.yaml
```

Give it a YAML file with six scores (1–5). It computes the weighted formula, identifies the bottleneck dimension, and generates P0/P1/P2 interventions.

The formula is:
```
ALS = (Observation × 0.15) + (Decision × 0.25) + (Execution × 0.30)
    + (Feedback × 0.15) + (Dependency × 0.15) − (Learning × 0.10)
```

This is real, deterministic computation. It runs correctly.

### 2. Batch Analyzer — Working

```bash
python asf_analyze.py --domain "Telecom & Networks" --risk High
```

Reads the 100-case CSV, applies the scoring engine to all rows, filters, sorts, and exports. Works correctly.

### 3. Document Analyzer — Partially Working

```bash
python asf_document_analyzer.py --file report.pdf
```

Scans document text for ~60 signal words across six ASF dimensions. Counts matches. Derives scores from counts.

**What it does:** Keyword frequency analysis.  
**What it does not do:** Semantic understanding, reasoning about context, or evidence-based scoring.

A document that mentions "manual process" 5 times scores higher on execution latency than one that mentions it once — regardless of what the sentences actually say.

**The gap:** The document analyzer needs an LLM to read the document and score each dimension with reasoning and evidence citation. That is v0.4.

### 4. Dashboards — Working (Locally)

All dashboards open in any browser with no server required. The charts render correctly. The filters work. The data is embedded.

The charts require Chart.js CDN — they appear blank if opened as raw GitHub files (GitHub serves raw HTML, not rendered pages). Solution: download and open locally, or host on GitHub Pages.

### 5. 100-Case Dataset — Complete

100 systems, 10 domains, all manually scored. The scores are research estimates based on public information — not algorithmically derived from primary data sources.

---

## What Is Manual Right Now

### Company Analyses

The enterprise benchmark (NVIDIA, Meta, AT&T, Adobe, Datadog) and manufacturing benchmark (Toyota, Foxconn, Siemens, BYD, Boeing) were produced by:

1. Reading public sources (annual reports, press releases, research papers)
2. Manually assigning dimension scores based on evidence
3. Writing findings and interventions based on those scores

This is legitimate research methodology. It is not automated. A human analyst produced these scores, not an algorithm.

### 100-Case Dataset

Same methodology. The dataset is an illustrative research baseline — structured inference from public information, not extracted primary data.

---

## What v0.4 Needs to Do

One thing. Connect the document analyzer to an LLM that:

1. Reads the document
2. Scores each of the six dimensions with a justification
3. Cites the specific text that led to each score
4. Identifies the primary friction category
5. Generates interventions based on the evidence

That turns ASF from a keyword counter into a genuine diagnostic tool.

**Example of what the output should look like:**

```
Dimension: Decision Latency
Score: 4/5 (High latency)
Evidence: "The report describes a Change Advisory Board review process 
that adds 2-4 weeks to every AI deployment decision (page 12). 
Three additional approval layers are mentioned across pages 8, 14, 
and 19."
Friction: Governance delay
```

---

## What the Framework Gets Right

**The theory is sound.** Every system that needs to change has:
- A speed of detecting the need (observation)
- A speed of deciding what to do (decision)
- A speed of implementing (execution)
- A speed of seeing results (feedback)
- A rate of improving from results (learning)

This applies to hospitals, supply chains, AI agents, governments, and individuals. The five-layer model is not invented — it is grounded in MAPE-K (IBM), OODA Loop (Boyd), and Systems Thinking (Senge, Meadows).

**The key finding is real.** The 100-case dataset, the enterprise benchmarks, and the manufacturing benchmarks all show the same pattern: systems that fail to adapt had usually already recognized the need to change. The bottleneck is execution and governance, not awareness.

That is a genuine, testable, and useful insight.

---

## What Would Make This Credible at Scale

1. **Automated scoring from documents** — LLM reads any doc, produces scored diagnosis with evidence
2. **Primary data integration** — connect to financial APIs, news feeds, regulatory filings
3. **Validation study** — compare ASF scores to subsequent organizational outcomes over 12+ months
4. **Peer review** — submit methodology to a management science or information systems journal

The framework is at step 1. It has the theory, the structure, the tooling, and the dataset. The next step is making the scoring automatic and evidence-based.

---

## The Honest Summary

ASF is a research framework with a working scoring engine and a manually produced dataset.

It is not yet a product. It is a solid foundation for one.

The gap between here and a real product is one engineering milestone: LLM-assisted automatic scoring from documents, with evidence citation.

Everything else is already built.
