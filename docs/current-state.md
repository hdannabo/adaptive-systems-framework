# ASF — Current State

**Version:** 0.4  
**Date:** June 2026

---

## What Works in v0.4

### 1. Evidence-Based Scoring — New in v0.4

```bash
export AZURE_OPENAI_KEY=your-key
export AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
export AZURE_OPENAI_DEPLOYMENT=gpt-4o

python asf_document_analyzer.py --file annual_report.pdf
```

Each of the six ASF dimensions is now scored by an LLM reading the document.
Every score comes with:
- An exact verbatim quote from the document
- The page or section location of that quote
- A one-sentence reasoning
- A confidence level (High / Medium / Low)

Example output:

```
Execution Latency: 5/5 — High confidence
Evidence: "We are producing at approximately 18 aircraft per month against our target of 38"
Source: page 3, CEO Letter
Reasoning: 47% of target rate after 3 years of recovery indicates severe execution latency
```

This is the core change in v0.4. The document analyzer now produces scores that 
can be independently verified against the source document.

### 2. Keyword Fallback — Available

```bash
python asf_document_analyzer.py --file report.pdf --mode keyword
```

The v0.3 keyword-based scorer is still available as --mode keyword.
Use this when Azure OpenAI is not configured or for quick testing.
Fallback scores carry Low confidence and no evidence citations.

### 3. Python Scoring Engine — Working (unchanged)

The deterministic ALS formula is unchanged from v0.3:
```
ALS = (Obs×0.15) + (Dec×0.25) + (Exec×0.30) + (FB×0.15) + (Dep×0.15) − (LV×0.10)
```

### 4. CRT Engine — Working (unchanged)

### 5. Dashboards — Live (unchanged)

MNC 2030, Enterprise AI, Manufacturing, Token Governance, CRT dashboards all live on GitHub Pages.

---

## What Is Manual in v0.4

The benchmark company scores (Boeing 4.10, Toyota 0.95, etc.) are still human-assigned.
They were derived by reading public documents and applying the ASF methodology manually.

v0.5 will run the evidence extractor against those same public documents to produce
auto-scored versions with citations. The manual scores serve as the validation baseline.

---

## What v0.5 Needs to Do

Automated capability and objective extraction from documents.
Currently a user provides: system_name, domain, target objective.
v0.5 will extract these from the document automatically.

---

## Honest Summary

v0.4 converts ASF from a keyword counter into a genuine diagnostic tool.
A user can now upload any annual report or strategy document and receive a
scored analysis where every score is traced to a specific sentence in the document.

The remaining gap is scale and validation:
- Running the extractor against the benchmark companies to produce auto-cited scores
- Comparing auto-scores to manually assigned scores (inter-rater reliability)
- Tracking outcome validation — did the bottleneck ASF identified match what the company later disclosed?
