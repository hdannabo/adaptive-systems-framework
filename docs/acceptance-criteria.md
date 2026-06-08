# ASF — Acceptance Criteria and Azure Architecture

## What "Done" Looks Like

This document defines the acceptance criteria for ASF as a production product.
Each criterion is measurable, testable, and binary — it either passes or it does not.

---

## AC-01: Document Upload → ASF Report

**Status: Partially complete**

| Criterion | Status | How to test |
|---|---|---|
| User uploads PDF, DOCX, or TXT | ✅ Done | Upload `examples/boeing_report.pdf` |
| System extracts text reliably | ✅ Done | Check extracted word count > 100 |
| LLM scores all 6 dimensions with evidence | ⚠️ Partial | Currently keyword counting, not LLM reasoning |
| Each score cites page/section from document | ❌ Not done | Check report for citation strings |
| Report generated in under 30 seconds | ❌ Not done | Measure end-to-end latency |

**Acceptance test:**
```
GIVEN a user uploads Boeing's 2025 annual report PDF
WHEN the system analyzes it
THEN the output must contain:
  - All 6 dimension scores (1–5)
  - At least one evidence citation per dimension
  - Primary bottleneck identified
  - Minimum 3 P0/P1/P2 interventions
  - Total latency under 30 seconds
```

---

## AC-02: Governance Scorer

**Status: Complete**

| Criterion | Status | How to test |
|---|---|---|
| User enters spend, users, adoption, hours saved | ✅ Done | Fill form in token-governance.html |
| Score computed deterministically 0–100 | ✅ Done | Same inputs = same score every time |
| Primary bottleneck identified | ✅ Done | Check bottleneck label is non-null |
| P0/P1/P2 interventions generated | ✅ Done | Check at least 3 interventions returned |
| Output exportable as PDF or JSON | ❌ Not done | No export button exists yet |

---

## AC-03: Web Interface — No Install Required

**Status: Not done**

| Criterion | Status | How to test |
|---|---|---|
| Works in browser — no Python required | ❌ Not done | Open URL in fresh browser, no setup |
| Mobile responsive | ❌ Not done | Open on iPhone, check layout |
| File drag-and-drop upload | ❌ Not done | Drag PDF onto upload zone |
| Report renders in browser, downloadable | ❌ Not done | Download button produces PDF |
| No auth required for basic use | ❌ Not done | Access without login |

**Acceptance test:**
```
GIVEN a user opens https://asf.hdannabo.dev
WHEN they drag a document onto the upload zone
THEN within 30 seconds they see a rendered ASF report
AND can download it as PDF
AND can share the URL with a colleague
WITHOUT installing Python, cloning a repo, or reading documentation
```

---

## AC-04: API Contract

**Status: Not done**

```
POST /api/v1/analyze/document
Authorization: Bearer {api_key}
Content-Type: multipart/form-data

Response 200:
{
  "system_name": "string",
  "domain": "string",
  "scores": {
    "observation_latency": 1-5,
    "decision_latency": 1-5,
    "execution_latency": 1-5,
    "feedback_delay": 1-5,
    "learning_velocity": 1-5,
    "dependency_index": 1-5,
    "adaptation_latency_score": 0.0-5.0,
    "risk_band": "Low|Medium|High"
  },
  "evidence": {
    "observation_latency": "string — citation from document",
    "decision_latency": "string — citation from document",
    ...
  },
  "primary_friction": "string",
  "bottleneck_dimension": "string",
  "interventions": [
    {
      "priority": "P0|P1|P2",
      "action": "string",
      "target_dimension": "string",
      "expected_reduction_weeks": integer
    }
  ],
  "summary": "string",
  "token_cost_usd": float,
  "analysis_duration_ms": integer
}
```

---

## AC-05: Scoring Correctness

**Status: Complete**

These are the benchmark cases. The scoring engine must produce these results consistently.

| System | Expected Score | Expected Risk | Expected Bottleneck |
|---|---|---|---|
| Toyota | < 1.5 | Low | Dependency Index (minor) |
| Netflix (post-migration) | < 2.0 | Low | Feedback Delay (minor) |
| AT&T | 3.8–4.2 | High | Execution Latency |
| Boeing | 3.8–4.5 | High | Feedback Delay / Dependency |
| Kodak (historical) | > 4.5 | High | Decision Latency |

**Regression test:**
```bash
python cli.py --file examples/toyota.yaml
# Expected: score < 1.5, risk = Low

python cli.py --file examples/att.yaml
# Expected: score > 3.5, risk = High, bottleneck = Execution Latency

python cli.py --file examples/boeing.yaml
# Expected: score > 3.5, risk = High
```

---

## AC-06: Observability

**Status: Not done**

```
Every analysis must produce a telemetry record containing:
- analysis_id: uuid
- timestamp: ISO8601
- document_size_bytes: integer
- extraction_duration_ms: integer
- llm_duration_ms: integer
- total_duration_ms: integer
- token_input_count: integer
- token_output_count: integer
- token_cost_usd: float
- bottleneck_dimension: string
- risk_band: string
- error: null | string

Alert thresholds:
- total_duration_ms > 30000 → warning
- token_cost_usd > 0.50 → warning (price reversal risk)
- error_rate_1h > 0.01 → critical
```

Note: ASF monitoring its own token cost is the product demonstrating itself.

---

## Azure Architecture

### Components

| Layer | Azure Service | Purpose | Cost |
|---|---|---|---|
| Presentation | Azure Static Web Apps | Host frontend | Free |
| API | Azure Functions (Consumption) | /analyze endpoints | ~$0/month at low volume |
| Intelligence | Azure OpenAI GPT-4o | LLM scoring | ~$0.05/analysis |
| Document storage | Azure Blob Storage | Uploaded files (24h TTL) | ~$1/month |
| Report storage | Cosmos DB free tier | Analysis results | Free |
| Observability | Application Insights | Telemetry + alerts | Free tier |
| Security | Azure Key Vault | Secrets management | ~$1/month |
| API gateway | Azure API Management | Rate limiting, auth | Developer tier: $49/month |

**Total estimated cost at launch: < $60/month**

### Data flow

```
User uploads document (browser)
    ↓
Azure Static Web App (serves frontend)
    ↓
POST /api/v1/analyze/document
    ↓
Azure Functions (Python)
    ├── Extract text (PyMuPDF / python-docx)
    ├── Store raw file in Blob Storage (24h TTL)
    ├── Call Azure OpenAI GPT-4o (structured output)
    │   └── Score 6 ASF dimensions with evidence citations
    ├── Run ASF scoring engine (deterministic)
    ├── Generate interventions
    ├── Store report in Cosmos DB
    └── Return JSON report
    ↓
Frontend renders report
    ↓
User downloads PDF or shares URL
    ↓
App Insights logs: duration, token cost, scores
```

### Security

- All secrets in Azure Key Vault — no secrets in code
- Managed Identity for Function → Key Vault → OpenAI
- Documents auto-deleted from Blob after 24 hours
- No PII stored — reports contain only analysis metadata
- API key auth via APIM for all /api/v1/* endpoints
- HTTPS only — no HTTP

### CI/CD

```yaml
# .github/workflows/deploy.yml
on:
  push:
    branches: [main]
jobs:
  deploy-functions:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: Azure/functions-action@v1
        with:
          app-name: asf-analyzer
          package: .
          publish-profile: ${{ secrets.AZURE_FUNCTIONAPP_PUBLISH_PROFILE }}

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
```

---

## Definition of Done — v1.0

The product is done when:

1. A non-technical user can open a URL in their browser
2. Drag a PDF onto the page
3. Receive a full ASF report within 30 seconds
4. Download or share it without assistance
5. The token cost of that analysis is logged and visible
6. The system handles 100 concurrent users without degradation
7. All acceptance criteria above pass

Until all 7 are true, it is a framework. After all 7 are true, it is a product.

---

## The Honest Gap Summary

**What's done:** Scoring engine, dashboards, dataset, theory, CLI tools, GitHub Pages hosting.

**What's needed for v1.0:**
- LLM-powered document scoring with evidence citations (4 hours)
- Azure Functions API wrapping the scoring engine (6 hours)
- Web interface — file upload, report rendering (8 hours)
- CI/CD pipeline (3 hours)
- Observability (2 hours)

**Total: approximately 23 hours of engineering.**

You have done harder things in a week at AT&T and P&G.
The framework is built. The infrastructure is what remains.
