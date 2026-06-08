# ASF Core Architecture Integration

## How the Framework Actually Works — Complete Technical Picture

```
INPUT LAYER          ANALYSIS LAYER         GOVERNANCE LAYER       OUTPUT LAYER
─────────────        ──────────────         ────────────────       ────────────
Structured YAML  ──► AnalysisInput      ──► ConformanceAgent  ──► ASFReport JSON
Uploaded doc     ──► document_analyzer  ──► ConformanceAgent  ──► ASFReport JSON
Form input       ──► score_program()    ──► ConformanceAgent  ──► Score + interventions
CSV dataset      ──► asf_analyze.py     ──► batch validation  ──► Ranked table
```

## The Data Flow — What "Takes Any Data" Means

ASF accepts three types of input. All produce the same structured output.

### Path 1: Structured YAML (fully deterministic)
```yaml
# examples/att.yaml
system_name: AT&T
observation_latency: 3   # human-assigned 1–5
decision_latency: 4
execution_latency: 5
feedback_delay: 4
learning_velocity: 3
dependency_index: 5
```
→ `cli.py` → `AnalysisInput` → `score()` → `LayerScores` → `recommend()` → `ASFReport`

### Path 2: Unstructured document (signal detection)
```
Any PDF / DOCX / TXT
→ extract_text() → keyword signal counting → AnalysisInput → same pipeline
```
Current limitation: keyword counting, not semantic reasoning.
v0.4 fix: replace with Azure OpenAI structured output.

### Path 3: Form input (governance scorer)
```
Monthly spend + users + adoption + hours saved + governance questions
→ weighted formula → governance score 0–100 → interventions
```

## The Conformance Agent — How It Enforces Purpose

Every output goes through the conformance check before delivery:

```python
agent = ConformanceAgent()

# After any analysis runs:
report = agent.check(
    task="analyze_document",
    output=result_dict,
    token_cost_usd=0.03,
    duration_ms=8200,
)

# report.conformance_status: ALIGNED | DRIFTING | VIOLATED
# ALIGNED  → deliver result
# DRIFTING → deliver with warning, flag for review
# VIOLATED → block result, log incident
```

The three states map to engineering reality:
- ALIGNED = system operating within purpose boundary (Conformance)
- DRIFTING = output correct but governance constraints violated (cost, latency; Purpose Drift)
- VIOLATED = output cannot be trusted — critical acceptance criteria failed

## Kyverno Integration — Policy as Code at Admission

Kyverno enforces ASF governance **before** any analysis job consumes resources.

```
Request arrives at AKS
        ↓
Kyverno admission webhook fires BEFORE pod is scheduled
        ↓
Policy check: does this job have acceptance criteria declared?
        ↓
NO  → REJECT immediately (zero cost, zero execution)
YES → ALLOW → pod scheduled → analysis runs → ConformanceAgent validates output
```

This is the engineering equivalent of:
"Right action, right process, right purpose — before any work begins."

## OPA Integration — API Gateway Policy

OPA (Open Policy Agent) enforces governance at the API layer:

```
POST /api/v1/analyze/document
        ↓
OPA Rego policy evaluates:
  - Is API key valid?
  - Is token budget declared and within org limit?
  - Is agentic workflow declared with budget controls?
  - Is the requesting domain authorized?
        ↓
DENY  → 403 Forbidden with policy reason
ALLOW → request proceeds to AKS
```

OPA + Kyverno together create two enforcement checkpoints:
1. API gateway (OPA) — before the request enters the cluster
2. Admission controller (Kyverno) — before the pod runs in the cluster

## Wiz.io Integration — Runtime Security

Wiz.io scans the entire AKS cluster continuously:
- Container image vulnerabilities
- Misconfigurations in running pods
- Secrets exposed in environment variables
- Network exposure of private services

For ASF: Wiz.io ensures the analysis pipeline itself is not compromised.
A governance framework that is itself insecure is not trustworthy.

## The Complete Governance Stack

```
Layer 1: API Gateway (Azure APIM)
  → Rate limiting, API key auth, quota enforcement

Layer 2: OPA at APIM
  → Business policy: token budget, domain authorization, agent controls

Layer 3: Kyverno at AKS admission
  → Infrastructure policy: acceptance criteria required, resource limits enforced

Layer 4: ASF Scoring Engine
  → Analysis: 6 dimensions, weighted formula, deterministic output

Layer 5: ConformanceAgent
  → Output validation: ALIGNED / DRIFTING / VIOLATED

Layer 6: Wiz.io runtime scan
  → Security: vulnerabilities, misconfigurations, secret exposure

Layer 7: App Insights
  → Observability: every analysis logged with cost, latency, conformance status

Layer 8: Kubecost
  → FinOps: GPU cost per analysis, cluster cost per team
```

Eight layers. Each with a single responsibility.
Each operating within its defined purpose boundary.
That is the engineering definition of a well-governed system.

## Global Compliance Mapping

The governance stack satisfies:

| Framework | Satisfied by |
|---|---|
| NIST AI RMF — GOVERN | Kyverno policies + ACCEPTANCE_CRITERIA registry |
| NIST AI RMF — MAP | AnalysisInput domain/type classification |
| NIST AI RMF — MEASURE | LayerScores 6-dimension weighted scoring |
| NIST AI RMF — MANAGE | Intervention P0/P1/P2 prioritization |
| EU AI Act — Technical documentation | ASFReport JSON + ConformanceReport |
| EU AI Act — Post-market monitoring | ConformanceAgent.history + drift_summary() |
| ISO 42001 — Clause 9 Performance | ConformanceAgent per-run scoring |
| ISO 42001 — Clause 10 Improvement | drift_summary() learning signal |
| Australia NAIC — Accountability | ConformanceReport with audit trail |
| India MeitY — Traceability | conformance_id + timestamp per analysis |
| OECD — Robustness | ConformanceAgent ALIGNED/DRIFTING/VIOLATED states |
| New Zealand Algorithm Charter | ASFReport transparency + audit log |
