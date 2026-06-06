#!/usr/bin/env python3
"""
ASF Document Analyzer — v0.3
Upload any document. ASF generates a full adaptation analysis.

Supported: PDF, DOCX, TXT, MD, annual reports, postmortems, strategy docs
Usage:
    python asf_document_analyzer.py --file report.pdf
    python asf_document_analyzer.py --file postmortem.txt --org "AT&T"
    python asf_document_analyzer.py --file strategy.docx --export output.json
"""

import argparse
import json
import sys
import os
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from asf import analyze, AnalysisInput
from asf.models import RiskBand

RESET  = "\033[0m"; BOLD = "\033[1m"; DIM = "\033[2m"
RED    = "\033[91m"; YELLOW = "\033[93m"; GREEN = "\033[92m"
CYAN   = "\033[96m"; WHITE  = "\033[97m"

# ── Signal dictionaries ────────────────────────────────────────────────────

OBS_SIGNALS = {
    "high_latency": [
        "delayed detection", "slow to recognize", "missed signal",
        "unaware", "blind spot", "no visibility", "lack of telemetry",
        "delayed alert", "no monitoring", "reactive",
    ],
    "low_latency": [
        "real-time", "immediate detection", "proactive monitoring",
        "early warning", "observability", "telemetry", "instrumented",
        "anomaly detection", "continuous monitoring",
    ],
}

DEC_SIGNALS = {
    "high_latency": [
        "delayed decision", "approval required", "committee review",
        "governance overhead", "escalation", "waiting for approval",
        "slow to decide", "bureaucratic", "multiple sign-offs",
        "change advisory board", "cab review", "lengthy review",
        "ownership unclear", "no clear owner", "ambiguous ownership",
    ],
    "low_latency": [
        "autonomous decision", "empowered teams", "decentralized",
        "fast decision", "clear ownership", "decisive",
        "policy as code", "automated approval",
    ],
}

EXEC_SIGNALS = {
    "high_latency": [
        "manual process", "slow deployment", "lengthy implementation",
        "delayed rollout", "implementation lag", "manual steps",
        "coordination required", "dependency on", "blocked by",
        "technical debt", "legacy system", "outdated infrastructure",
        "integration complexity", "migration required",
    ],
    "low_latency": [
        "automated deployment", "continuous delivery", "rapid implementation",
        "self-service", "one-click", "fast rollout", "ci/cd",
        "gitops", "infrastructure as code",
    ],
}

FEEDBACK_SIGNALS = {
    "high_delay": [
        "delayed feedback", "lagging indicator", "slow measurement",
        "quarterly review", "annual report", "no metrics",
        "unclear outcomes", "hard to measure",
    ],
    "low_delay": [
        "real-time feedback", "immediate measurement", "live dashboard",
        "continuous monitoring", "instant visibility", "slo", "sli",
        "kpi tracking", "automated reporting",
    ],
}

LEARNING_SIGNALS = {
    "low_velocity": [
        "repeated incident", "same mistake", "recurrence",
        "no postmortem", "lessons not applied", "knowledge silo",
        "tribal knowledge", "undocumented", "no runbook",
    ],
    "high_velocity": [
        "continuous improvement", "postmortem", "blameless review",
        "lessons learned", "kaizen", "retrospective",
        "knowledge base", "runbook", "playbook", "systematic improvement",
    ],
}

FRICTION_SIGNALS = {
    "technical":      ["legacy", "technical debt", "outdated", "integration", "migration", "deprecated"],
    "organizational": ["silo", "ownership", "coordination", "alignment", "politics", "restructur"],
    "human":          ["resistance", "culture", "behavior", "training", "skill gap", "adoption"],
    "governance":     ["compliance", "regulatory", "approval", "audit", "policy", "security review"],
    "data":           ["data quality", "data gap", "missing data", "inaccurate", "stale data"],
}

DOMAIN_SIGNALS = {
    "AI Systems":              ["llm", "model", "ai agent", "machine learning", "neural", "openai", "anthropic", "gpt"],
    "Platform Engineering":    ["kubernetes", "docker", "ci/cd", "deployment", "infrastructure", "devops", "sre", "platform"],
    "Telecom & Networks":      ["network", "telecom", "5g", "spectrum", "subscriber", "carrier", "bandwidth"],
    "Manufacturing":           ["factory", "production", "defect", "quality", "manufacturing", "supply chain", "assembly"],
    "Finance & Healthcare":    ["financial", "banking", "clinical", "patient", "regulatory", "fda", "hipaa"],
    "Retail & Consumer":       ["retail", "inventory", "customer", "e-commerce", "supply", "logistics"],
    "Enterprise Transformation":["transformation", "migration", "modernization", "cloud", "digital"],
}


def extract_text(filepath: str) -> str:
    path = Path(filepath)
    suffix = path.suffix.lower()

    if suffix in [".txt", ".md"]:
        return path.read_text(encoding="utf-8", errors="ignore")

    if suffix == ".pdf":
        try:
            import subprocess
            result = subprocess.run(
                ["pdftotext", str(path), "-"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout
        except Exception:
            pass
        try:
            import PyPDF2
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                return "\n".join(p.extract_text() or "" for p in reader.pages)
        except Exception:
            pass

    if suffix == ".docx":
        try:
            import subprocess
            result = subprocess.run(
                ["extract-text", str(path)],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                return result.stdout
        except Exception:
            pass
        try:
            import docx
            doc = docx.Document(path)
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception:
            pass

    # Fallback: read as text
    return path.read_text(encoding="utf-8", errors="ignore")


def score_signals(text: str, high_signals: list, low_signals: list) -> int:
    text_lower = text.lower()
    high_hits = sum(1 for s in high_signals if s in text_lower)
    low_hits  = sum(1 for s in low_signals  if s in text_lower)
    net = high_hits - low_hits
    if net >= 4:   return 5
    if net >= 2:   return 4
    if net >= 0:   return 3
    if net >= -2:  return 2
    return 1


def detect_domain(text: str) -> str:
    text_lower = text.lower()
    scores = {}
    for domain, signals in DOMAIN_SIGNALS.items():
        scores[domain] = sum(1 for s in signals if s in text_lower)
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "Enterprise Transformation"


def detect_friction(text: str) -> list:
    text_lower = text.lower()
    found = []
    for ftype, signals in FRICTION_SIGNALS.items():
        hits = sum(1 for s in signals if s in text_lower)
        if hits > 0:
            found.append((ftype, hits))
    found.sort(key=lambda x: -x[1])
    return [f[0] for f in found[:3]]


def extract_org_name(text: str, fallback: str) -> str:
    if fallback:
        return fallback
    # Look for common org name patterns
    patterns = [
        r"(?:prepared for|submitted to|report for|analysis of)[:\s]+([A-Z][A-Za-z\s&,\.]{2,40})",
        r"^([A-Z][A-Za-z\s&]{3,30})\s+(?:Annual Report|Strategic Plan|Postmortem|Assessment)",
        r"(?:Company|Organization|Client)[:\s]+([A-Z][A-Za-z\s&]{3,30})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text[:2000], re.MULTILINE)
        if match:
            return match.group(1).strip()
    return "Document Analysis"


def extract_scenario(text: str) -> str:
    text_lower = text.lower()
    scenarios = {
        "AI adoption and value realization":         ["ai adoption", "ai value", "ai program", "llm deployment"],
        "Cloud migration and platform modernization": ["cloud migration", "azure", "aws", "modernization", "kubernetes"],
        "Incident response and reliability":          ["incident", "postmortem", "reliability", "sre", "outage"],
        "Quality and operational improvement":        ["quality", "defect", "kaizen", "improvement", "six sigma"],
        "Digital transformation":                     ["digital transformation", "transformation program"],
        "Network operations and automation":          ["network automation", "5g", "network operations"],
        "Strategic adaptation and market response":   ["strategy", "competitive", "market shift", "disruption"],
    }
    for scenario, signals in scenarios.items():
        if any(s in text_lower for s in signals):
            return scenario
    return "Organizational adaptation assessment"


def analyze_document(filepath: str, org_name: str = None) -> dict:
    print(f"\n  {CYAN}Reading document...{RESET}")
    text = extract_text(filepath)

    if not text or len(text.strip()) < 100:
        print(f"  {RED}Could not extract text from {filepath}{RESET}")
        sys.exit(1)

    word_count = len(text.split())
    print(f"  {DIM}Extracted {word_count:,} words{RESET}")

    print(f"  {CYAN}Analyzing adaptation signals...{RESET}")

    obs_score  = score_signals(text, OBS_SIGNALS["high_latency"],  OBS_SIGNALS["low_latency"])
    dec_score  = score_signals(text, DEC_SIGNALS["high_latency"],  DEC_SIGNALS["low_latency"])
    exec_score = score_signals(text, EXEC_SIGNALS["high_latency"], EXEC_SIGNALS["low_latency"])
    fb_score   = score_signals(text, FEEDBACK_SIGNALS["high_delay"],  FEEDBACK_SIGNALS["low_delay"])
    lv_score   = score_signals(text, LEARNING_SIGNALS["low_velocity"], LEARNING_SIGNALS["high_velocity"])
    lv_score   = 6 - lv_score  # invert: low_velocity signals = low LV score
    di_score   = score_signals(text, DEC_SIGNALS["high_latency"] + EXEC_SIGNALS["high_latency"], [])
    di_score   = min(5, max(1, di_score))

    domain   = detect_domain(text)
    friction = detect_friction(text)
    org      = extract_org_name(text, org_name)
    scenario = extract_scenario(text)

    inp = AnalysisInput(
        system_name=org,
        domain=domain,
        system_type="Document-derived analysis",
        adaptation_scenario=scenario,
        input_event="Extracted from uploaded document",
        adaptation_requirement="Identified from document context",
        current_operating_state="Assessed from document signals",
        observation_latency=obs_score,
        decision_latency=dec_score,
        execution_latency=exec_score,
        feedback_delay=fb_score,
        learning_velocity=lv_score,
        dependency_index=di_score,
    )

    report = analyze(inp, top_interventions=5)

    return {
        "report": report,
        "metadata": {
            "source_file": filepath,
            "word_count": word_count,
            "detected_domain": domain,
            "detected_friction": friction,
            "signal_counts": {
                "observation_high": sum(1 for s in OBS_SIGNALS["high_latency"]  if s in text.lower()),
                "decision_high":    sum(1 for s in DEC_SIGNALS["high_latency"]  if s in text.lower()),
                "execution_high":   sum(1 for s in EXEC_SIGNALS["high_latency"] if s in text.lower()),
                "learning_low":     sum(1 for s in LEARNING_SIGNALS["low_velocity"] if s in text.lower()),
                "learning_high":    sum(1 for s in LEARNING_SIGNALS["high_velocity"] if s in text.lower()),
            }
        }
    }


def print_report(result: dict) -> None:
    report = result["report"]
    meta   = result["metadata"]
    s      = report.scores
    risk   = s.risk_band
    rc     = {RiskBand.LOW: GREEN, RiskBand.MEDIUM: YELLOW, RiskBand.HIGH: RED}[risk]

    def bar(v, w=20):
        f = int((v/5)*w)
        c = GREEN if v < 2.5 else (YELLOW if v < 3.5 else RED)
        return f"{c}{'█'*f}{'░'*(w-f)}{RESET}"

    def sc(v):
        return GREEN if v < 2.5 else (YELLOW if v < 3.5 else RED)

    als = s.adaptation_latency_score

    print()
    print(f"{BOLD}{CYAN}{'─'*66}{RESET}")
    print(f"{BOLD}{WHITE}  ASF Document Analysis Report{RESET}")
    print(f"{BOLD}{CYAN}{'─'*66}{RESET}")
    print()
    print(f"  {BOLD}Source{RESET}       {DIM}{meta['source_file']}{RESET}  ({meta['word_count']:,} words)")
    print(f"  {BOLD}System{RESET}       {WHITE}{report.input.system_name}{RESET}")
    print(f"  {BOLD}Domain{RESET}       {DIM}{report.input.domain}{RESET}")
    print(f"  {BOLD}Scenario{RESET}     {DIM}{report.input.adaptation_scenario}{RESET}")
    print()
    print(f"  {BOLD}Latency Score{RESET}   {sc(als)}{BOLD}{als:.2f}{RESET} / 5.0   {bar(als)}   Risk: {rc}{BOLD}{risk.value.upper()}{RESET}")
    print(f"  {BOLD}Friction Score{RESET}  {sc(s.friction_score)}{s.friction_score:.2f}{RESET} / 5.0")
    print(f"  {BOLD}Adapt Capability{RESET} {GREEN}{s.adaptation_capability:.2f}{RESET} / 5.0")
    print()

    print(f"  {BOLD}{CYAN}Layer Analysis — from document signals{RESET}")
    print(f"  {'─'*60}")
    dims = [
        ("Observation latency", s.observation_latency, False),
        ("Decision latency",    s.decision_latency,    False),
        ("Execution latency",   s.execution_latency,   False),
        ("Feedback delay",      s.feedback_delay,      False),
        ("Learning velocity",   s.learning_velocity,   True),
        ("Dependency index",    s.dependency_index,    False),
    ]
    for label, val, invert in dims:
        is_bottleneck = label.lower().replace(" ","_") in report.bottleneck_dimension.lower().replace(" ","_")
        marker = f" {YELLOW}◀ bottleneck{RESET}" if is_bottleneck else ""
        color = GREEN if (invert and val >= 4) or (not invert and val <= 2) else (YELLOW if val == 3 else RED)
        print(f"  {label:<22} {color}{val:.0f}{RESET}/5  {bar(val, 20)}{marker}")

    print()
    print(f"  {BOLD}Detected friction{RESET}   {YELLOW}{', '.join(meta['detected_friction']) or 'None detected'}{RESET}")
    print(f"  {BOLD}Primary friction{RESET}    {YELLOW}{report.primary_friction}{RESET}")
    print(f"  {BOLD}Bottleneck{RESET}          {RED}{report.bottleneck_dimension}{RESET}")
    print()

    if meta["signal_counts"]["execution_high"] > 0 or meta["signal_counts"]["decision_high"] > 0:
        print(f"  {BOLD}{CYAN}Signal Evidence{RESET}")
        print(f"  {'─'*60}")
        sc2 = meta["signal_counts"]
        print(f"  Observation friction signals : {sc2['observation_high']}")
        print(f"  Decision friction signals    : {sc2['decision_high']}")
        print(f"  Execution friction signals   : {sc2['execution_high']}")
        print(f"  Low learning signals         : {sc2['learning_low']}")
        print(f"  High learning signals        : {sc2['learning_high']}")
        print()

    print(f"  {BOLD}{CYAN}Recommended Interventions{RESET}")
    print(f"  {'─'*60}")
    pc = {" P0": RED, "P1": YELLOW, "P2": CYAN}
    for rec in report.interventions:
        c = RED if rec.priority == "P0" else (YELLOW if rec.priority == "P1" else CYAN)
        print(f"  {c}{BOLD}[{rec.priority}]{RESET}  {WHITE}{rec.action}{RESET}")
        print(f"        {DIM}Target: {rec.target_dimension} · Reduction: {rec.expected_reduction_weeks}w · Effort: {rec.effort}{RESET}")
        print()

    print(f"  {BOLD}{CYAN}Summary{RESET}")
    print(f"  {'─'*60}")
    for sentence in report.summary.split(". "):
        if sentence.strip():
            print(f"  {sentence.strip()}.")
    print()
    print(f"{BOLD}{CYAN}{'─'*66}{RESET}")
    print()


def export_json(result: dict, path: str) -> None:
    report = result["report"]
    s      = report.scores
    out = {
        "source": result["metadata"]["source_file"],
        "system_name": report.input.system_name,
        "domain": report.input.domain,
        "scenario": report.input.adaptation_scenario,
        "scores": {
            "adaptation_latency_score": s.adaptation_latency_score,
            "friction_score": s.friction_score,
            "adaptation_capability": s.adaptation_capability,
            "risk_band": s.risk_band.value,
            "layers": {
                "observation_latency": s.observation_latency,
                "decision_latency":    s.decision_latency,
                "execution_latency":   s.execution_latency,
                "feedback_delay":      s.feedback_delay,
                "learning_velocity":   s.learning_velocity,
                "dependency_index":    s.dependency_index,
            }
        },
        "primary_friction": report.primary_friction,
        "bottleneck": report.bottleneck_dimension,
        "detected_friction_categories": result["metadata"]["detected_friction"],
        "interventions": [
            {"priority": r.priority, "action": r.action,
             "target": r.target_dimension, "effort": r.effort,
             "reduction_weeks": r.expected_reduction_weeks}
            for r in report.interventions
        ],
        "summary": report.summary,
        "metadata": result["metadata"],
    }
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"  {GREEN}Exported to {path}{RESET}\n")


def main():
    parser = argparse.ArgumentParser(
        description="ASF Document Analyzer — upload any document, get adaptation analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python asf_document_analyzer.py --file annual_report.pdf
  python asf_document_analyzer.py --file postmortem.txt --org "AT&T"
  python asf_document_analyzer.py --file strategy.docx --export output.json
        """
    )
    parser.add_argument("--file",   "-f", required=True, help="Document to analyze (PDF, DOCX, TXT, MD)")
    parser.add_argument("--org",    "-o", help="Organization name (optional — auto-detected if not provided)")
    parser.add_argument("--export", "-e", help="Export JSON report to file")
    args = parser.parse_args()

    if not Path(args.file).exists():
        print(f"\n  {RED}File not found: {args.file}{RESET}\n")
        sys.exit(1)

    result = analyze_document(args.file, args.org)
    print_report(result)

    if args.export:
        export_json(result, args.export)


if __name__ == "__main__":
    main()
