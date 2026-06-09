"""
ASF v0.4 — Evidence Extractor
==============================
Replaces keyword counting with LLM-based evidence extraction.

Every score is now traceable to a specific quote in the source document.

Usage:
    from asf.evidence.extractor import extract_evidence_from_document

    pkg = extract_evidence_from_document(
        document_text="...",
        system_name="Boeing",
        source_document="Boeing_Annual_Report_2025.pdf",
    )
"""

import json
import os
import time
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)

# ── Data models ────────────────────────────────────────────────────────────

@dataclass
class DimensionEvidence:
    """Evidence for one ASF dimension, returned by the LLM."""
    dimension_key: str          # e.g. "execution_latency"
    dimension_label: str        # e.g. "Execution Latency"
    score: int                  # 1–5
    evidence_quote: str         # exact verbatim quote from document
    source_location: str        # page number or section description
    reasoning: str              # one sentence explaining the score
    confidence: str             # "High" | "Medium" | "Low"
    fallback_used: bool = False # True if LLM failed and keyword fallback used


@dataclass
class EvidencePackage:
    """Full six-dimension extraction result for one document."""
    system_name: str
    source_document: str
    extraction_model: str
    extraction_timestamp: str
    total_tokens_used: int
    estimated_cost_usd: float
    fallback_used: bool
    dimensions: dict = field(default_factory=dict)  # key → DimensionEvidence

    @property
    def overall_confidence(self) -> str:
        """Weakest-link confidence across all dimensions."""
        if not self.dimensions:
            return "Low"
        confidences = [d.confidence for d in self.dimensions.values()]
        if "Low" in confidences or self.fallback_used:
            return "Low"
        high_count = confidences.count("High")
        if high_count >= 4:
            return "High"
        return "Medium"

    def to_scores_dict(self) -> dict:
        """Convert to the integer scores AnalysisInput expects."""
        return {k: v.score for k, v in self.dimensions.items()}


# ── Dimension definitions — injected into every LLM prompt ─────────────────

DIMENSION_DEFINITIONS = {
    "observation_latency": {
        "label": "Observation Latency",
        "definition": (
            "How quickly the organization detects signals that change is needed. "
            "Includes: monitoring systems, incident detection, market signal awareness, "
            "reporting cycles, data freshness, telemetry coverage."
        ),
        "scale": (
            "1 = real-time detection with automated alerting | "
            "3 = weekly or monthly manual review processes | "
            "5 = quarterly or purely reactive detection after problems occur"
        ),
    },
    "decision_latency": {
        "label": "Decision Latency",
        "definition": (
            "How quickly the organization commits to action after detecting a need. "
            "Includes: approval cycles, committee reviews, ownership clarity, "
            "governance overhead, escalation paths, change advisory boards."
        ),
        "scale": (
            "1 = same-day empowered decisions with clear ownership | "
            "3 = weekly approval cycles with defined process | "
            "5 = monthly or longer multi-layer approval with unclear ownership"
        ),
    },
    "execution_latency": {
        "label": "Execution Latency",
        "definition": (
            "How quickly the organization implements committed actions. "
            "Includes: deployment speed, manual steps in delivery pipeline, "
            "legacy system constraints, integration complexity, coordination overhead, "
            "production rate vs target rate."
        ),
        "scale": (
            "1 = automated same-day delivery with minimal manual steps | "
            "3 = weeks to implement with some manual coordination | "
            "5 = months or purely manual delivery significantly below target"
        ),
    },
    "feedback_delay": {
        "label": "Feedback Delay",
        "definition": (
            "How quickly the organization sees results from actions taken. "
            "Includes: measurement systems, KPI reporting frequency, "
            "outcome visibility, leading vs lagging indicators, review cadence."
        ),
        "scale": (
            "1 = real-time outcome visibility with automated dashboards | "
            "3 = monthly reporting with some lag | "
            "5 = annual or no systematic measurement of outcomes"
        ),
    },
    "learning_velocity": {
        "label": "Learning Velocity",
        "definition": (
            "How quickly the organization improves from experience. "
            "Includes: postmortem culture, knowledge documentation, "
            "recurring incident patterns, systematic improvement processes, "
            "whether the same failures repeat. "
            "IMPORTANT: Higher score = FASTER learning (this is a positive dimension)."
        ),
        "scale": (
            "5 = continuous improvement culture with documented learnings applied | "
            "3 = occasional retrospectives with partial application | "
            "1 = same failures recurring with no systematic improvement"
        ),
    },
    "dependency_index": {
        "label": "Dependency Index",
        "definition": (
            "How many manual approvals, external dependencies, or coordination "
            "steps are required before action can be taken. "
            "Includes: regulatory approvals, external vendor dependencies, "
            "cross-team coordination requirements, approval gate count."
        ),
        "scale": (
            "1 = fully autonomous with minimal external dependencies | "
            "3 = several approval gates but manageable coordination | "
            "5 = every action requires multiple external approvals or dependencies"
        ),
    },
}

# ── System prompt ──────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are an ASF (Adaptive Systems Framework) analyst.

ASF measures how fast an organization can close the gap between its current 
capabilities and the capabilities required to achieve its stated objectives.

You will score ONE adaptation dimension based on evidence in the provided document text.

SCORING RULES:
- Score 1 = strong positive signal (fast/good for this dimension)
- Score 2 = moderate positive signal
- Score 3 = neutral or mixed signals
- Score 4 = moderate negative signal (slow/problematic)
- Score 5 = strong negative signal (very slow/very problematic)
- Exception — Learning Velocity: 5 = fast learning (positive), 1 = slow (negative)

EVIDENCE RULES:
- evidence_quote MUST be an exact verbatim quote from the document text
- Do not paraphrase or summarize — copy text word-for-word
- If no direct quote supports the score, set evidence_quote to empty string ""
  and set confidence to "Low"
- source_location: use page number if visible in the text (e.g., "page 12"),
  otherwise describe the location (e.g., "Operations section, third paragraph")

CONFIDENCE RULES:
- High: score directly supported by quantitative data or explicit named process
- Medium: score inferred from qualitative language or indirect description
- Low: score estimated from absence of signals, or no direct quote available

OUTPUT: Return ONLY valid JSON. No text before or after the JSON object."""

# ── User prompt template ───────────────────────────────────────────────────

USER_PROMPT_TEMPLATE = """DIMENSION TO SCORE: {dimension_label}

DEFINITION: {definition}

SCORING SCALE: {scale}

---

DOCUMENT TEXT:
{document_text}

---

Score the document above on the dimension "{dimension_label}".

Return this exact JSON structure:
{{
  "score": <integer 1-5>,
  "evidence_quote": "<exact verbatim quote from document, or empty string>",
  "source_location": "<page number or section description>",
  "reasoning": "<one sentence explaining why this quote leads to this score>",
  "confidence": "<High|Medium|Low>"
}}"""


# ── Document chunking ──────────────────────────────────────────────────────

def chunk_document(text: str, max_chars: int = 6000) -> list[str]:
    """
    Split document into chunks for LLM processing.

    Strategy: use the first max_chars of the document for each dimension call.
    For long documents, we use the full text if it fits, otherwise the first chunk.
    A more sophisticated chunker would search for dimension-relevant sections.
    That is a v0.5 improvement.
    """
    if len(text) <= max_chars:
        return [text]

    # For now: use first 6000 chars (intro/summary) + last 2000 (conclusions)
    # This captures most quantitative claims in annual reports
    first = text[:4000]
    last = text[-2000:] if len(text) > 6000 else ""
    chunk = first + "\n\n[...middle sections omitted...]\n\n" + last
    return [chunk]


# ── Quote validator ────────────────────────────────────────────────────────

def validate_quote(quote: str, document_text: str) -> bool:
    """
    Verify the evidence_quote appears verbatim in the document.
    Allows minor whitespace normalization.
    Returns True if quote is empty (Low confidence is valid).
    """
    if not quote or not quote.strip():
        return True

    # Normalize whitespace for comparison
    normalized_doc = " ".join(document_text.split()).lower()
    normalized_quote = " ".join(quote.split()).lower()

    # Accept if at least 80% of the quote matches (handles minor OCR issues)
    if normalized_quote in normalized_doc:
        return True

    # Check for truncated quote (LLM sometimes cuts off long quotes)
    if len(normalized_quote) > 40:
        fragment = normalized_quote[:40]
        return fragment in normalized_doc

    return False


# ── Keyword fallback (v0.3 behavior, used when LLM unavailable) ────────────

_KEYWORD_SIGNALS = {
    "observation_latency": {
        "high": ["delayed detection", "slow to recognize", "missed signal", "no visibility",
                 "lack of telemetry", "delayed alert", "no monitoring", "reactive",
                 "quarterly review", "annual report only"],
        "low":  ["real-time", "immediate detection", "proactive monitoring", "early warning",
                 "observability", "telemetry", "instrumented", "anomaly detection"],
    },
    "decision_latency": {
        "high": ["delayed decision", "approval required", "committee review", "governance overhead",
                 "escalation", "waiting for approval", "multiple sign-offs",
                 "change advisory board", "lengthy review", "ownership unclear"],
        "low":  ["autonomous decision", "empowered teams", "decentralized", "fast decision",
                 "clear ownership", "policy as code", "automated approval"],
    },
    "execution_latency": {
        "high": ["manual process", "slow deployment", "lengthy implementation",
                 "delayed rollout", "manual steps", "coordination required", "blocked by",
                 "technical debt", "legacy system", "integration complexity"],
        "low":  ["automated deployment", "continuous delivery", "rapid implementation",
                 "self-service", "fast rollout", "ci/cd", "gitops"],
    },
    "feedback_delay": {
        "high": ["delayed feedback", "lagging indicator", "slow measurement",
                 "quarterly review", "annual report", "no metrics", "unclear outcomes"],
        "low":  ["real-time feedback", "immediate measurement", "live dashboard",
                 "continuous monitoring", "instant visibility", "kpi tracking"],
    },
    "learning_velocity": {
        "low":  ["repeated incident", "same mistake", "recurrence", "no postmortem",
                 "lessons not applied", "knowledge silo", "undocumented"],
        "high": ["continuous improvement", "postmortem", "blameless review",
                 "lessons learned", "kaizen", "retrospective", "knowledge base"],
    },
    "dependency_index": {
        "high": ["approval required", "multiple sign-offs", "external approval",
                 "regulatory approval", "vendor dependency", "coordination required"],
        "low":  ["autonomous", "self-service", "automated", "no external dependency"],
    },
}


def _keyword_score(text: str, dimension_key: str) -> DimensionEvidence:
    """Keyword fallback scoring — used when LLM is unavailable."""
    text_lower = text.lower()
    signals = _KEYWORD_SIGNALS.get(dimension_key, {"high": [], "low": []})
    high_hits = sum(1 for s in signals.get("high", []) if s in text_lower)
    low_hits = sum(1 for s in signals.get("low", []) if s in text_lower)
    net = high_hits - low_hits

    if dimension_key == "learning_velocity":
        # Inverted: high signals = good (score 5), low signals = bad (score 1)
        net = -net

    if net >= 4:
        score = 5
    elif net >= 2:
        score = 4
    elif net >= 0:
        score = 3
    elif net >= -2:
        score = 2
    else:
        score = 1

    defn = DIMENSION_DEFINITIONS[dimension_key]
    return DimensionEvidence(
        dimension_key=dimension_key,
        dimension_label=defn["label"],
        score=score,
        evidence_quote="",
        source_location="keyword analysis — LLM unavailable",
        reasoning=f"Keyword fallback: {high_hits} friction signals, {low_hits} positive signals",
        confidence="Low",
        fallback_used=True,
    )


# ── LLM call ───────────────────────────────────────────────────────────────

def _call_openai(
    client,
    document_text: str,
    dimension_key: str,
    model: str,
    max_retries: int = 3,
) -> DimensionEvidence:
    """
    Call Azure OpenAI for one dimension. Returns DimensionEvidence.
    Falls back to keyword scoring if LLM fails after max_retries.
    """
    defn = DIMENSION_DEFINITIONS[dimension_key]
    chunks = chunk_document(document_text)
    doc_text = chunks[0]  # use first chunk

    user_prompt = USER_PROMPT_TEMPLATE.format(
        dimension_label=defn["label"],
        definition=defn["definition"],
        scale=defn["scale"],
        document_text=doc_text,
    )

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                max_tokens=500,
                temperature=0.1,  # low temperature for consistent, factual output
            )

            raw = response.choices[0].message.content
            data = json.loads(raw)

            score = int(data.get("score", 3))
            score = max(1, min(5, score))  # clamp to valid range

            quote = data.get("evidence_quote", "").strip()
            source = data.get("source_location", "").strip()
            reasoning = data.get("reasoning", "").strip()
            confidence = data.get("confidence", "Medium")

            if confidence not in ("High", "Medium", "Low"):
                confidence = "Medium"

            # Validate quote exists in document
            if quote and not validate_quote(quote, document_text):
                logger.warning(
                    f"Quote validation failed for {dimension_key} — "
                    f"quote not found in document, downgrading to Low confidence"
                )
                confidence = "Low"
                quote = ""
                source = "Quote not verifiable in source document"

            return DimensionEvidence(
                dimension_key=dimension_key,
                dimension_label=defn["label"],
                score=score,
                evidence_quote=quote,
                source_location=source,
                reasoning=reasoning,
                confidence=confidence,
                fallback_used=False,
            )

        except Exception as e:
            wait = 2 ** attempt
            logger.warning(f"LLM call failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(wait)

    # All retries failed — use keyword fallback
    logger.warning(f"All LLM retries failed for {dimension_key} — using keyword fallback")
    return _keyword_score(document_text, dimension_key)


# ── Token cost estimation ──────────────────────────────────────────────────

def _estimate_cost(total_tokens: int, model: str) -> float:
    """
    Estimate USD cost based on approximate token prices.
    gpt-4o: $2.50/1M input, $10/1M output (rough 80/20 split assumed)
    """
    if "gpt-4o" in model:
        # ~80% input tokens at $2.50/1M, ~20% output tokens at $10/1M
        input_cost = (total_tokens * 0.8 / 1_000_000) * 2.50
        output_cost = (total_tokens * 0.2 / 1_000_000) * 10.00
        return round(input_cost + output_cost, 4)
    return 0.0


# ── Main extraction function ───────────────────────────────────────────────

def extract_evidence_from_document(
    document_text: str,
    system_name: str,
    source_document: str = "unknown",
    model: Optional[str] = None,
    use_llm: bool = True,
) -> EvidencePackage:
    """
    Main entry point for evidence-based dimension scoring.

    Args:
        document_text: Full extracted text of the document
        system_name: Name of the organization being analyzed
        source_document: Filename or URL of the source document
        model: Azure OpenAI deployment name (defaults to env var)
        use_llm: If False, uses keyword fallback only (for testing)

    Returns:
        EvidencePackage with all six dimensions scored and cited
    """
    model = model or os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    timestamp = datetime.now(timezone.utc).isoformat()

    dimensions = {}
    total_tokens = 0
    any_fallback = False

    if use_llm:
        # Import here so the module works without openai installed
        try:
            from openai import AzureOpenAI
            client = AzureOpenAI(
                api_key=os.environ.get("AZURE_OPENAI_KEY"),
                api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01"),
                azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
            )
        except ImportError:
            logger.warning("openai package not installed — using keyword fallback")
            use_llm = False
        except Exception as e:
            logger.warning(f"OpenAI client init failed: {e} — using keyword fallback")
            use_llm = False

    for dim_key in DIMENSION_DEFINITIONS:
        if use_llm:
            evidence = _call_openai(client, document_text, dim_key, model)
        else:
            evidence = _keyword_score(document_text, dim_key)

        if evidence.fallback_used:
            any_fallback = True

        dimensions[dim_key] = evidence

        # Rough token estimate per call
        total_tokens += 2000  # ~2K tokens per dimension call (prompt + response)

    return EvidencePackage(
        system_name=system_name,
        source_document=source_document,
        extraction_model=model if use_llm else "keyword-fallback",
        extraction_timestamp=timestamp,
        total_tokens_used=total_tokens,
        estimated_cost_usd=_estimate_cost(total_tokens, model) if use_llm else 0.0,
        fallback_used=any_fallback,
        dimensions=dimensions,
    )


# ── Bridge to existing ASF engine ─────────────────────────────────────────

def evidence_to_analysis_input(
    pkg: EvidencePackage,
    domain: str = "",
    system_type: str = "Enterprise",
    adaptation_scenario: str = "",
) -> "AnalysisInput":
    """
    Convert EvidencePackage → AnalysisInput for the existing scoring engine.
    This is the bridge that keeps the core engine unchanged.
    """
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
    from asf.models import AnalysisInput

    scores = pkg.to_scores_dict()

    return AnalysisInput(
        system_name=pkg.system_name,
        domain=domain,
        system_type=system_type,
        adaptation_scenario=adaptation_scenario or f"Evidence-based analysis of {pkg.source_document}",
        input_event="Extracted from source document",
        adaptation_requirement="Identified from document context",
        current_operating_state=f"Assessed from {pkg.source_document}",
        observation_latency=scores.get("observation_latency", 3),
        decision_latency=scores.get("decision_latency", 3),
        execution_latency=scores.get("execution_latency", 3),
        feedback_delay=scores.get("feedback_delay", 3),
        learning_velocity=scores.get("learning_velocity", 3),
        dependency_index=scores.get("dependency_index", 3),
    )


# ── Cited report printer ───────────────────────────────────────────────────

def print_evidence_report(
    pkg: EvidencePackage,
    report,  # ASFReport from existing engine
    crt_output=None,  # optional CRTOutput
) -> None:
    """
    Print a full cited ASF report to terminal.
    Each dimension score is shown with its evidence quote.
    """
    RESET = "\033[0m"; BOLD = "\033[1m"; DIM = "\033[2m"
    RED = "\033[91m"; YELLOW = "\033[93m"; GREEN = "\033[92m"
    CYAN = "\033[96m"; WHITE = "\033[97m"

    def score_color(v, invert=False):
        good = v >= 4 if invert else v <= 2
        bad = v <= 2 if invert else v >= 4
        return GREEN if good else (RED if bad else YELLOW)

    def conf_color(c):
        return GREEN if c == "High" else (YELLOW if c == "Medium" else RED)

    s = report.scores
    als = s.adaptation_latency_score
    rc = GREEN if als < 2.5 else (YELLOW if als < 3.5 else RED)

    print()
    print(f"{BOLD}{CYAN}{'─' * 70}{RESET}")
    print(f"{BOLD}{WHITE}  ASF v0.4 — Evidence-Based Analysis{RESET}")
    print(f"{BOLD}{CYAN}{'─' * 70}{RESET}")
    print()
    print(f"  {BOLD}System{RESET}        {WHITE}{pkg.system_name}{RESET}")
    print(f"  {BOLD}Source{RESET}        {DIM}{pkg.source_document}{RESET}")
    print(f"  {BOLD}Model{RESET}         {DIM}{pkg.extraction_model}{RESET}")
    print(f"  {BOLD}Confidence{RESET}    {conf_color(pkg.overall_confidence)}{pkg.overall_confidence}{RESET}")
    if not pkg.fallback_used:
        print(f"  {BOLD}Est. cost{RESET}     {DIM}${pkg.estimated_cost_usd:.3f} USD{RESET}")
    print()
    print(f"  {BOLD}ASF Score{RESET}     {rc}{BOLD}{als:.2f}{RESET} / 5.0   "
          f"Risk: {rc}{BOLD}{s.risk_band.value.upper()}{RESET}")
    print()

    print(f"  {BOLD}{CYAN}Dimension Analysis — Evidence Cited{RESET}")
    print(f"  {'─' * 66}")

    dim_order = [
        "observation_latency", "decision_latency", "execution_latency",
        "feedback_delay", "learning_velocity", "dependency_index",
    ]

    for dim_key in dim_order:
        ev = pkg.dimensions.get(dim_key)
        if not ev:
            continue

        is_bottleneck = dim_key.replace("_", " ").title().lower() in report.bottleneck_dimension.lower()
        invert = dim_key == "learning_velocity"
        sc = score_color(ev.score, invert=invert)
        marker = f" {YELLOW}◀ PRIMARY BOTTLENECK{RESET}" if is_bottleneck else ""
        cc = conf_color(ev.confidence)

        print(f"\n  {BOLD}{ev.dimension_label}{RESET}")
        print(f"  Score: {sc}{BOLD}{ev.score}/5{RESET}  Confidence: {cc}{ev.confidence}{RESET}{marker}")
        print(f"  {DIM}Reasoning: {ev.reasoning}{RESET}")

        if ev.evidence_quote:
            # Wrap long quotes
            quote = ev.evidence_quote
            if len(quote) > 80:
                quote = quote[:77] + "..."
            print(f"  {YELLOW}Evidence: \"{quote}\"{RESET}")
            print(f"  {DIM}Source: {ev.source_location}{RESET}")
        elif ev.fallback_used:
            print(f"  {RED}[Keyword fallback — no LLM citation available]{RESET}")
        else:
            print(f"  {DIM}[No direct quote — Low confidence]{RESET}")

    print()
    print(f"  {'─' * 66}")
    print(f"  {BOLD}Primary Bottleneck{RESET}   {RED}{report.bottleneck_dimension}{RESET}")
    print(f"  {BOLD}Primary Friction{RESET}     {YELLOW}{report.primary_friction}{RESET}")
    print()

    if crt_output:
        rc2 = GREEN if crt_output.crt_risk_level == "Low" else \
              (YELLOW if crt_output.crt_risk_level == "Medium" else RED)
        print(f"  {BOLD}{CYAN}Capability Realization Time{RESET}")
        print(f"  {'─' * 66}")
        print(f"  CRT: {rc2}{BOLD}{crt_output.crt_months:.0f} months{RESET} "
              f"({crt_output.crt_risk_level} risk)   "
              f"Range: {crt_output.crt_range_low_months:.0f}–{crt_output.crt_range_high_months:.0f} months")
        print()

    print(f"  {BOLD}{CYAN}Recommended Interventions{RESET}")
    print(f"  {'─' * 66}")
    for rec in report.interventions[:3]:
        pc = RED if rec.priority == "P0" else (YELLOW if rec.priority == "P1" else CYAN)
        print(f"\n  {pc}{BOLD}[{rec.priority}]{RESET}  {WHITE}{rec.action}{RESET}")
        print(f"  {DIM}Target: {rec.target_dimension} · Effort: {rec.effort} · "
              f"Est. reduction: {rec.expected_reduction_weeks}w{RESET}")

    print()
    print(f"  {BOLD}{CYAN}Executive Summary{RESET}")
    print(f"  {'─' * 66}")
    for sentence in report.summary.split(". "):
        if sentence.strip():
            print(f"  {sentence.strip()}.")

    print()
    print(f"  {DIM}Confidence disclaimer: {_confidence_disclaimer(pkg.overall_confidence)}{RESET}")
    print()
    print(f"{BOLD}{CYAN}{'─' * 70}{RESET}")
    print()


def _confidence_disclaimer(confidence: str) -> str:
    return {
        "High":   "Scores directly supported by quantitative evidence in the document.",
        "Medium": "Scores inferred from qualitative disclosures. Internal data would increase confidence.",
        "Low":    "Limited evidence found. Scores are estimates. Independent verification recommended.",
    }.get(confidence, "")


# ── JSON export ────────────────────────────────────────────────────────────

def export_cited_report(
    pkg: EvidencePackage,
    report,           # ASFReport
    crt_output=None,  # optional CRTOutput
    output_path: str = None,
) -> dict:
    """
    Build and optionally save the full cited report as JSON.
    This is the authoritative output format for ASF v0.4.
    """
    s = report.scores

    out = {
        "asf_version": "0.4.0",
        "system_name": pkg.system_name,
        "source_document": pkg.source_document,
        "asf_score": s.adaptation_latency_score,
        "risk_band": s.risk_band.value,
        "bottleneck_dimension": report.bottleneck_dimension,
        "primary_friction": report.primary_friction,
        "overall_confidence": pkg.overall_confidence,
        "summary": report.summary,
        "dimensions": {},
        "interventions": [],
        "extraction_metadata": {
            "model": pkg.extraction_model,
            "timestamp": pkg.extraction_timestamp,
            "tokens_used": pkg.total_tokens_used,
            "estimated_cost_usd": pkg.estimated_cost_usd,
            "fallback_used": pkg.fallback_used,
        },
    }

    for dim_key, ev in pkg.dimensions.items():
        out["dimensions"][dim_key] = {
            "label": ev.dimension_label,
            "score": ev.score,
            "evidence_quote": ev.evidence_quote,
            "source_location": ev.source_location,
            "reasoning": ev.reasoning,
            "confidence": ev.confidence,
            "fallback_used": ev.fallback_used,
        }

    for rec in report.interventions:
        out["interventions"].append({
            "priority": rec.priority,
            "action": rec.action,
            "target_dimension": rec.target_dimension,
            "friction_type": rec.friction_type,
            "expected_reduction_weeks": rec.expected_reduction_weeks,
            "effort": rec.effort,
        })

    if crt_output:
        out["crt"] = {
            "months": crt_output.crt_months,
            "years": crt_output.crt_years,
            "range_low_months": crt_output.crt_range_low_months,
            "range_high_months": crt_output.crt_range_high_months,
            "risk_level": crt_output.crt_risk_level,
            "primary_bottleneck": crt_output.primary_bottleneck,
            "governance_readiness": crt_output.governance_readiness_score,
            "explanation": crt_output.plain_english_explanation,
        }

    if output_path:
        with open(output_path, "w") as f:
            json.dump(out, f, indent=2)

    return out
