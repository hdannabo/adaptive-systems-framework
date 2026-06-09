# ASF Azure Reference Architecture

## Design Principles

1. **Evidence flows forward** — every score must trace back to a source document
2. **No secrets in code** — all credentials via Key Vault and Managed Identity
3. **Audit trail is immutable** — every analysis is append-only in Cosmos DB
4. **Confidence is explicit** — every output states the confidence level and evidence basis
5. **Human stays in the loop** — AI scores are presented as input to human decision, not final verdict

---

## Architecture Overview

```
DATA SOURCES                    INGESTION                    PROCESSING
─────────────                   ─────────                    ──────────
Annual Reports (PDF)   ──────►  Azure Blob Storage  ──────►  Azure AI Foundry
Earnings Calls (MP3)   ──────►  Speech-to-Text      ──────►  Document Chunking
Investor Decks (PPTX)  ──────►  Form Recognizer     ──────►  AI Search Index
Strategy Documents     ──────►  Data Factory        ──────►  GPT-4o Scoring
Internal Program Data  ──────►  SQL MI (structured) ──────►  ASF Engine (Python)

SCORING PIPELINE
────────────────
Azure OpenAI GPT-4o
  Input:  Document chunks + ASF dimension prompt template
  Output: {
    dimension: "execution_latency",
    score: 4,
    evidence: "exact quote from document",
    source_page: 12,
    confidence: "Medium"
  }
    ↓
ASF Python Engine (deterministic)
  Input:  Scored dimensions
  Output: ALS, CRT, bottleneck, interventions, CEO summary
    ↓
Audit Trail (Cosmos DB — append-only)
  Every analysis stored with: analysis_id, timestamp, source_docs, raw_scores,
  evidence_citations, model_version, confidence_level

STORAGE
───────
Azure SQL MI          → Analysis results, intervention tracking, user sessions
Azure Data Lake       → Raw documents, extracted text, model outputs
Cosmos DB             → Audit trail, conformance records (append-only, TTL configurable)
Azure AI Search       → Searchable document corpus, semantic similarity index
Azure Blob Storage    → Raw uploaded documents (lifecycle policy: delete after 30 days)

GOVERNANCE
──────────
Azure Purview         → Data lineage: source doc → extracted text → score → output
Azure Key Vault       → OpenAI key, SQL connection string, API signing key
Managed Identity      → Functions → Key Vault → OpenAI (no secrets anywhere in code)
RBAC                  → Analyst (score), Executive (read), Admin (configure)
Private Endpoints     → All storage behind VNet — no public access to data
Kyverno               → AKS admission policies — no privileged containers
APIM                  → Rate limiting, API key auth, usage quotas per client

PRESENTATION
────────────
ASF Dashboard         → Public benchmarks (GitHub Pages / Static Web Apps)
Power BI              → Internal program tracking (executive cockpit)
Azure API Management  → REST API for third-party integration
```

---

## The Trust Chain

Every ASF output must be traceable through this chain:

```
CEO Summary Statement
        ↑
   Bottleneck Identification
        ↑
   Dimension Score (e.g., Execution Latency = 4)
        ↑
   Evidence Quote ("page 12: manual approvals required for all AI deployments")
        ↑
   Source Document (Boeing_Annual_Report_2025.pdf)
        ↑
   Page / Section Reference (page 12, section 3.2)
        ↑
   Confidence Level (Medium — based on disclosed process description)
        ↑
   Model Version (gpt-4o-2025-05-20, ASF engine v0.4)
        ↑
   Analysis Timestamp (2026-06-08T14:32:00Z)
        ↑
   Analysis ID (uuid)
```

Without this chain, executives cannot challenge or trust the output. The trust chain is not optional.

---

## Data Flow

### Step 1 — Document Ingestion

```
User uploads: Boeing_Annual_Report_2025.pdf
    ↓
Azure Blob Storage (blob: boeing/2025/annual-report.pdf)
    ↓
Azure AI Foundry Document Intelligence
  → Extracts text, preserves page numbers
  → Output: {pages: [{page: 1, text: "..."}, ...]}
    ↓
Azure AI Search Index
  → Chunks by section, indexes with metadata
  → Enables semantic search across document corpus
```

### Step 2 — Dimension Scoring

```
For each ASF dimension (6 total):
    Azure OpenAI GPT-4o called with:
    {
      "system": "You are an ASF analyst. Score the provided document section...",
      "user": f"Document text: {chunk}\nDimension to score: {dimension_name}\n
                Score 1-5 where 1=fast/good and 5=slow/problematic.
                Provide: score, exact quote from text, page number, confidence (H/M/L)"
    }
    
    Response (JSON mode, structured output):
    {
      "score": 4,
      "evidence": "The Change Advisory Board review adds 2-4 weeks...",
      "source_page": 12,
      "confidence": "Medium"
    }
```

### Step 3 — ASF Engine

```python
# Deterministic computation — no LLM involved at this stage
scores = LayerScores(
    observation_latency=4,
    decision_latency=4,
    execution_latency=5,
    feedback_delay=3,
    learning_velocity=2,
    dependency_index=4,
)
report = analyze(input_with_scores)
# → ALS, risk band, bottleneck, CRT, interventions, CEO summary
```

### Step 4 — Audit Record

```json
{
  "analysis_id": "uuid",
  "timestamp": "2026-06-08T14:32:00Z",
  "system_name": "Boeing Quality Program",
  "source_documents": ["boeing/2025/annual-report.pdf"],
  "model_version": "gpt-4o-2025-05-20",
  "engine_version": "asf-0.4",
  "scores": {
    "execution_latency": {"score": 5, "evidence": "...", "page": 12, "confidence": "Medium"}
  },
  "output": {
    "als": 4.10,
    "risk": "High",
    "bottleneck": "Execution Latency",
    "crt_months": 22,
    "summary": "This manufacturing program is at risk of missing..."
  }
}
```

---

## API Contract

```
POST /api/v1/analyze
Authorization: Bearer {api_key}
Content-Type: multipart/form-data

Body:
  document: file (PDF/DOCX/TXT)
  system_name: string
  domain: string
  objective: string
  target_date: string (ISO)

Response 200:
{
  "analysis_id": "uuid",
  "system_name": "string",
  "scores": {
    "adaptation_latency_score": 0.0–5.0,
    "risk_band": "Low|Medium|High",
    "dimensions": {
      "execution_latency": {"score": 1–5, "evidence": "...", "confidence": "H|M|L"}
    }
  },
  "adaptation_gap": float,
  "crt_months": float,
  "crt_range": [low, high],
  "crt_risk": "Low|Medium|High|Critical",
  "primary_bottleneck": "string",
  "summary": "CEO-grade plain English statement",
  "interventions": [
    {"priority": "P0", "action": "...", "expected_impact": "...", "effort": "low|medium|high"}
  ],
  "evidence_confidence": "High|Medium|Low",
  "token_cost_usd": float,
  "duration_ms": int
}
```

---

## Cost Model (production estimate)

| Component | Monthly cost at 500 analyses/month |
|---|---|
| Azure OpenAI GPT-4o | ~$0.05/analysis × 500 = $25 |
| Azure Functions (Consumption) | ~$0 (well within free tier) |
| Azure Blob Storage | ~$2 |
| Azure SQL MI (dev/staging) | ~$100 |
| Azure AI Search (Basic) | ~$75 |
| Azure Static Web Apps | $0 (free tier) |
| **Total** | **~$200/month** |

At 5,000 analyses/month (enterprise scale), Azure OpenAI cost dominates at ~$250. Total ~$500/month.
