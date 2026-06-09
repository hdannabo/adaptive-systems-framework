#!/usr/bin/env python3
"""
ASF Document Analyzer — v0.4
Evidence-based scoring with cited quotes.

Every dimension score is now traceable to a specific sentence in the source document.

Usage:
    python asf_document_analyzer.py --file report.pdf
    python asf_document_analyzer.py --file annual_report.pdf --org "Boeing"
    python asf_document_analyzer.py --file strategy.pdf --export output.json
    python asf_document_analyzer.py --file report.pdf --mode keyword  # v0.3 fallback

Environment variables required for LLM mode:
    AZURE_OPENAI_KEY       Your Azure OpenAI API key
    AZURE_OPENAI_ENDPOINT  https://your-resource.openai.azure.com/
    AZURE_OPENAI_DEPLOYMENT  gpt-4o (or your deployment name)
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

RESET = "\033[0m"; BOLD = "\033[1m"; DIM = "\033[2m"
RED = "\033[91m"; YELLOW = "\033[93m"; GREEN = "\033[92m"
CYAN = "\033[96m"; WHITE = "\033[97m"


def extract_text(filepath: str) -> str:
    """Extract plain text from PDF, DOCX, TXT, or MD files."""
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
            import docx
            doc = docx.Document(path)
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception:
            pass

    # Fallback: read as text
    return path.read_text(encoding="utf-8", errors="ignore")


def detect_org_name(text: str, fallback: str) -> str:
    """Auto-detect organization name from document text."""
    if fallback:
        return fallback
    patterns = [
        r"(?:prepared for|submitted to|report for|analysis of)[:\s]+([A-Z][A-Za-z\s&,.]{2,40})",
        r"^([A-Z][A-Za-z\s&]{3,30})\s+(?:Annual Report|Strategic Plan|Assessment)",
        r"(?:Company|Organization)[:\s]+([A-Z][A-Za-z\s&]{3,30})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text[:2000], re.MULTILINE)
        if match:
            return match.group(1).strip()
    return "Document Analysis"


def detect_domain(text: str) -> str:
    """Detect the primary domain from document text."""
    text_lower = text.lower()
    domains = {
        "AI Systems": ["llm", "machine learning", "ai agent", "openai", "gpt"],
        "Platform Engineering": ["kubernetes", "ci/cd", "devops", "infrastructure"],
        "Telecom & Networks": ["network", "telecom", "5g", "spectrum", "carrier"],
        "Manufacturing": ["factory", "production", "defect", "manufacturing", "assembly"],
        "Finance & Healthcare": ["financial", "banking", "clinical", "patient", "hipaa"],
        "Retail & Consumer": ["retail", "inventory", "e-commerce", "supply chain"],
        "Enterprise Transformation": ["transformation", "migration", "modernization", "cloud"],
    }
    scores = {d: sum(1 for s in signals if s in text_lower)
              for d, signals in domains.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "Enterprise Transformation"


def run_llm_analysis(
    text: str,
    org_name: str,
    source_file: str,
    domain: str,
) -> dict:
    """
    Run evidence-based LLM scoring.
    Returns dict with pkg (EvidencePackage), report (ASFReport), input (AnalysisInput).
    """
    # Import the v0.4 extractor
    extractor_path = Path(__file__).parent / "src" / "asf" / "evidence"
    if str(extractor_path.parent.parent) not in sys.path:
        sys.path.insert(0, str(extractor_path.parent.parent))

    try:
        from asf.evidence.extractor import (
            extract_evidence_from_document,
            evidence_to_analysis_input,
            print_evidence_report,
            export_cited_report,
        )
    except ImportError:
        # Extractor not installed yet — fall back
        print(f"\n  {YELLOW}Evidence extractor not found — using keyword fallback{RESET}")
        return None

    print(f"\n  {CYAN}Extracting evidence from document...{RESET}")
    print(f"  {DIM}This calls Azure OpenAI for each of 6 dimensions.{RESET}")
    print(f"  {DIM}Set AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT{RESET}")
    print(f"  {DIM}to enable LLM mode. Without these, keyword fallback will run.{RESET}\n")

    pkg = extract_evidence_from_document(
        document_text=text,
        system_name=org_name,
        source_document=source_file,
    )

    inp = evidence_to_analysis_input(
        pkg=pkg,
        domain=domain,
        system_type="Enterprise",
    )

    report = analyze(inp, top_interventions=5)

    # Optional CRT
    crt_output = None
    try:
        from asf.scoring.crt_engine import CRTInput, calculate_crt
        als = report.scores.adaptation_latency_score
        friction = als / 5.0
        crt_inp = CRTInput(
            system_name=org_name,
            use_case=domain,
            required_capability_score=10.0,
            current_capability_score=10.0 - (als * 1.5),
            governance_friction=friction * 0.8,
            execution_friction=friction,
            dependency_risk=friction * 0.9,
            learning_velocity=max(0.1, 1.0 - friction),
            evidence_confidence={"High": 0.85, "Medium": 0.65, "Low": 0.40}.get(
                pkg.overall_confidence, 0.65
            ),
            objective_integrity_score=0.80,
            base_realization_time_months=4.0,
        )
        crt_output = calculate_crt(crt_inp)
    except Exception:
        pass

    return {
        "pkg": pkg,
        "report": report,
        "input": inp,
        "crt": crt_output,
    }


def run_keyword_analysis(
    text: str,
    org_name: str,
    domain: str,
) -> dict:
    """
    Run v0.3 keyword-based scoring (fallback mode).
    """
    print(f"\n  {YELLOW}Running keyword analysis (v0.3 fallback mode){RESET}")

    # Import keyword scorer from extractor if available, else inline
    try:
        from asf.evidence.extractor import _keyword_score, EvidencePackage
        dims = {}
        for dim_key in ["observation_latency", "decision_latency", "execution_latency",
                        "feedback_delay", "learning_velocity", "dependency_index"]:
            dims[dim_key] = _keyword_score(text, dim_key)
        pkg = EvidencePackage(
            system_name=org_name,
            source_document="keyword-mode",
            extraction_model="keyword-fallback",
            extraction_timestamp="",
            total_tokens_used=0,
            estimated_cost_usd=0.0,
            fallback_used=True,
            dimensions=dims,
        )
        scores = pkg.to_scores_dict()
    except ImportError:
        # Inline fallback if extractor not installed
        from asf.evidence.extractor import _keyword_score
        scores = {}
        for dim_key in ["observation_latency", "decision_latency", "execution_latency",
                        "feedback_delay", "learning_velocity", "dependency_index"]:
            ev = _keyword_score(text, dim_key)
            scores[dim_key] = ev.score
        pkg = None

    inp = AnalysisInput(
        system_name=org_name,
        domain=domain,
        system_type="Document-derived analysis",
        adaptation_scenario="Keyword-based document analysis",
        input_event="Extracted from uploaded document",
        adaptation_requirement="Identified from document context",
        current_operating_state="Assessed from document signals",
        observation_latency=scores.get("observation_latency", 3),
        decision_latency=scores.get("decision_latency", 3),
        execution_latency=scores.get("execution_latency", 3),
        feedback_delay=scores.get("feedback_delay", 3),
        learning_velocity=scores.get("learning_velocity", 3),
        dependency_index=scores.get("dependency_index", 3),
    )

    report = analyze(inp, top_interventions=5)
    return {"pkg": pkg, "report": report, "input": inp, "crt": None}


def print_basic_report(report, domain: str, source_file: str) -> None:
    """Simple report for keyword mode (v0.3 format)."""
    s = report.scores
    rc = GREEN if s.risk_band == RiskBand.LOW else (YELLOW if s.risk_band == RiskBand.MEDIUM else RED)
    als = s.adaptation_latency_score

    print()
    print(f"{BOLD}{CYAN}{'─' * 66}{RESET}")
    print(f"{BOLD}{WHITE}  ASF Document Analysis — Keyword Mode (v0.3){RESET}")
    print(f"{BOLD}{CYAN}{'─' * 66}{RESET}")
    print()
    print(f"  {BOLD}Source{RESET}     {DIM}{source_file}{RESET}")
    print(f"  {BOLD}System{RESET}     {WHITE}{report.input.system_name}{RESET}")
    print(f"  {BOLD}Domain{RESET}     {DIM}{domain}{RESET}")
    print()
    print(f"  {BOLD}ASF Score{RESET}  {rc}{BOLD}{als:.2f}{RESET} / 5.0   "
          f"Risk: {rc}{BOLD}{s.risk_band.value.upper()}{RESET}")
    print()

    dims = [
        ("Observation latency", s.observation_latency, False),
        ("Decision latency", s.decision_latency, False),
        ("Execution latency", s.execution_latency, False),
        ("Feedback delay", s.feedback_delay, False),
        ("Learning velocity", s.learning_velocity, True),
        ("Dependency index", s.dependency_index, False),
    ]
    for label, val, invert in dims:
        is_bn = label.lower().replace(" ", "_") in report.bottleneck_dimension.lower().replace(" ", "_")
        marker = f" {YELLOW}◀ bottleneck{RESET}" if is_bn else ""
        good = val >= 4 if invert else val <= 2
        color = GREEN if good else (RED if (val <= 2 if invert else val >= 4) else YELLOW)
        filled = int((val / 5) * 20)
        bar = f"{color}{'█' * filled}{'░' * (20 - filled)}{RESET}"
        print(f"  {label:<22} {color}{val:.0f}{RESET}/5  {bar}{marker}")

    print()
    print(f"  {BOLD}Bottleneck{RESET}   {RED}{report.bottleneck_dimension}{RESET}")
    print()

    print(f"  {BOLD}{CYAN}Interventions{RESET}")
    for rec in report.interventions[:3]:
        pc = RED if rec.priority == "P0" else (YELLOW if rec.priority == "P1" else CYAN)
        print(f"  {pc}{BOLD}[{rec.priority}]{RESET}  {WHITE}{rec.action}{RESET}")
    print()

    print(f"  {BOLD}Summary{RESET}")
    for s in report.summary.split(". "):
        if s.strip():
            print(f"  {s.strip()}.")
    print()
    print(f"  {YELLOW}Note: Upgrade to LLM mode for evidence-cited scoring.{RESET}")
    print(f"  {DIM}Set AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT{RESET}")
    print()
    print(f"{BOLD}{CYAN}{'─' * 66}{RESET}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="ASF Document Analyzer v0.4 — evidence-based scoring with citations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python asf_document_analyzer.py --file annual_report.pdf
  python asf_document_analyzer.py --file report.pdf --org "Boeing"
  python asf_document_analyzer.py --file report.pdf --export output.json
  python asf_document_analyzer.py --file report.pdf --mode keyword

LLM mode (default) requires:
  export AZURE_OPENAI_KEY=your-key
  export AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
  export AZURE_OPENAI_DEPLOYMENT=gpt-4o
        """
    )
    parser.add_argument("--file", "-f", required=True, help="Document to analyze (PDF, DOCX, TXT, MD)")
    parser.add_argument("--org", "-o", help="Organization name (auto-detected if not provided)")
    parser.add_argument("--export", "-e", help="Export JSON report to this file path")
    parser.add_argument("--mode", choices=["llm", "keyword"], default="llm",
                        help="Scoring mode: llm (default, requires Azure OpenAI) or keyword (v0.3 fallback)")
    args = parser.parse_args()

    if not Path(args.file).exists():
        print(f"\n  {RED}File not found: {args.file}{RESET}\n")
        sys.exit(1)

    print(f"\n  {CYAN}ASF v0.4 Document Analyzer{RESET}")
    print(f"  {DIM}Reading: {args.file}{RESET}")

    text = extract_text(args.file)
    if not text or len(text.strip()) < 100:
        print(f"  {RED}Could not extract text from {args.file}{RESET}")
        sys.exit(1)

    word_count = len(text.split())
    print(f"  {DIM}Extracted {word_count:,} words{RESET}")

    org_name = detect_org_name(text, args.org)
    domain = detect_domain(text)

    print(f"  {DIM}Organization: {org_name} | Domain: {domain}{RESET}")

    if args.mode == "llm":
        result = run_llm_analysis(text, org_name, args.file, domain)
        if result is None:
            # LLM unavailable — fall through to keyword
            result = run_keyword_analysis(text, org_name, domain)
    else:
        result = run_keyword_analysis(text, org_name, domain)

    pkg = result.get("pkg")
    report = result["report"]
    crt = result.get("crt")

    # Print report
    if pkg and not pkg.fallback_used and args.mode == "llm":
        try:
            from asf.evidence.extractor import print_evidence_report
            print_evidence_report(pkg, report, crt)
        except ImportError:
            print_basic_report(report, domain, args.file)
    else:
        print_basic_report(report, domain, args.file)

    # Export
    if args.export:
        if pkg:
            try:
                from asf.evidence.extractor import export_cited_report
                data = export_cited_report(pkg, report, crt, args.export)
                print(f"  {GREEN}Exported to {args.export}{RESET}\n")
            except ImportError:
                pass
        else:
            s = report.scores
            out = {
                "system_name": report.input.system_name,
                "asf_score": s.adaptation_latency_score,
                "risk_band": s.risk_band.value,
                "bottleneck": report.bottleneck_dimension,
                "summary": report.summary,
                "mode": "keyword-fallback",
            }
            with open(args.export, "w") as f:
                json.dump(out, f, indent=2)
            print(f"  {GREEN}Exported to {args.export}{RESET}\n")


if __name__ == "__main__":
    main()
