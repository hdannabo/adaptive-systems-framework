# ASF Conformance Agent

**File:** `asf_conformance_agent.py`  
**Purpose:** Validate that LLM-generated ASF outputs meet defined acceptance criteria.

---

## What it does

The Conformance Agent applies ASF's acceptance criteria as a verification layer on top of LLM-generated analysis.

Every LLM call has a defined purpose — an expected output structure with measurable criteria. The agent checks whether the actual output satisfies those criteria and flags drift.

**Core principle:** Every LLM action has a defined purpose. Every output must be checked against that purpose. Drift from purpose = governance failure.

---

## Usage

```bash
# Analyze a document and validate the output meets ASF criteria
python asf_conformance_agent.py --task analyze_document --input report.pdf

# Score a transformation program and validate completeness
python asf_conformance_agent.py --task score_program --input program.yaml

# Validate an existing ASF output against acceptance criteria
python asf_conformance_agent.py --validate output.json --criteria criteria.yaml
```

---

## Acceptance criteria enforced

| Task | Criteria checked |
|---|---|
| `analyze_document` | All 6 dimensions scored; evidence present for each score; bottleneck identified; ALS formula verifiable |
| `score_program` | Scores within 1–5 range; confidence levels assigned; source citations present |
| `validate` | Output schema complete; no hallucinated quotes; confidence calibrated to evidence quality |

---

## Relationship to ASF v0.4 evidence extractor

The conformance agent wraps `src/asf/evidence/extractor.py`. Where the extractor produces evidence-cited scores, the conformance agent verifies those scores meet the acceptance criteria before the output is used downstream.

**Without conformance:** LLM scores an organization → output used as-is  
**With conformance:** LLM scores → agent checks → flagged gaps → rerun or annotate

---

## Status

Working prototype. Acceptance criteria registry is in the file as `ACCEPTANCE_CRITERIA` dict. Extend by adding new task keys with `purpose` and `criteria` lists.
