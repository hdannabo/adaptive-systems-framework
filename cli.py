#!/usr/bin/env python3
"""
ASF — Adaptive Systems Framework
Command-line analyzer
"""

import argparse
import json
import sys
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.asf import analyze, AnalysisInput
from src.asf.models import RiskBand

RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
WHITE  = "\033[97m"
BLUE   = "\033[94m"

RISK_COLOR = {
    RiskBand.LOW:    GREEN,
    RiskBand.MEDIUM: YELLOW,
    RiskBand.HIGH:   RED,
}

PRIORITY_COLOR = {
    "P0": RED,
    "P1": YELLOW,
    "P2": CYAN,
}


def bar(value: float, max_val: float = 5.0, width: int = 20, invert: bool = False) -> str:
    ratio = value / max_val
    if invert:
        ratio = 1 - ratio
    filled = int(ratio * width)
    empty = width - filled
    color = GREEN if ratio < 0.5 else (YELLOW if ratio < 0.7 else RED)
    if invert:
        color = GREEN if ratio > 0.5 else (YELLOW if ratio > 0.3 else RED)
    return f"{color}{'█' * filled}{'░' * empty}{RESET}"


def score_color(score: float) -> str:
    if score < 2.5:
        return GREEN
    elif score < 3.5:
        return YELLOW
    return RED


def print_report(report) -> None:
    inp = report.input
    s = report.scores
    risk = s.risk_band
    rc = RISK_COLOR[risk]

    print()
    print(f"{BOLD}{CYAN}{'─' * 64}{RESET}")
    print(f"{BOLD}{WHITE}  Adaptive Systems Framework — Analysis Report{RESET}")
    print(f"{BOLD}{CYAN}{'─' * 64}{RESET}")
    print()

    print(f"  {BOLD}System{RESET}       {WHITE}{inp.system_name}{RESET}")
    print(f"  {BOLD}Domain{RESET}       {DIM}{inp.domain}{RESET}")
    print(f"  {BOLD}Type{RESET}         {DIM}{inp.system_type}{RESET}")
    print(f"  {BOLD}Scenario{RESET}     {DIM}{inp.adaptation_scenario}{RESET}")
    print()

    als = s.adaptation_latency_score
    print(f"  {BOLD}Latency Score{RESET}   {score_color(als)}{BOLD}{als:.2f}{RESET} / 5.0   "
          f"{bar(als)}   Risk: {rc}{BOLD}{risk.value.upper()}{RESET}")
    print(f"  {BOLD}Friction Score{RESET}  {score_color(s.friction_score)}{s.friction_score:.2f}{RESET} / 5.0")
    print(f"  {BOLD}Adapt Capability{RESET} {GREEN}{s.adaptation_capability:.2f}{RESET} / 5.0")
    print()

    print(f"  {BOLD}{CYAN}Layer Analysis{RESET}")
    print(f"  {'─' * 58}")

    dims = [
        ("Observation latency", s.observation_latency, False),
        ("Decision latency",    s.decision_latency,    False),
        ("Execution latency",   s.execution_latency,   False),
        ("Feedback delay",      s.feedback_delay,      False),
        ("Learning velocity",   s.learning_velocity,   True),
        ("Dependency index",    s.dependency_index,    False),
    ]

    for label, val, invert in dims:
        marker = f" {YELLOW}◀ bottleneck{RESET}" if label.lower().replace(" ", "_") in report.bottleneck_dimension.lower().replace(" ", "_") else ""
        color = GREEN if (invert and val >= 4) or (not invert and val <= 2) else (YELLOW if val == 3 else RED)
        print(f"  {label:<22} {color}{val:.0f}{RESET}/5  {bar(val, invert=invert)}{marker}")

    print()
    print(f"  {BOLD}Primary friction{RESET}    {YELLOW}{report.primary_friction}{RESET}")
    print(f"  {BOLD}Bottleneck{RESET}          {RED}{report.bottleneck_dimension}{RESET}")
    print()

    print(f"  {BOLD}{CYAN}Recommended Interventions{RESET}")
    print(f"  {'─' * 58}")

    for i, rec in enumerate(report.interventions, 1):
        pc = PRIORITY_COLOR.get(rec.priority, WHITE)
        print(f"  {pc}{BOLD}[{rec.priority}]{RESET}  {WHITE}{rec.action}{RESET}")
        print(f"        {DIM}Target: {rec.target_dimension} · "
              f"Est. reduction: {rec.expected_reduction_weeks}w · "
              f"Effort: {rec.effort}{RESET}")
        print()

    print(f"  {BOLD}{CYAN}Summary{RESET}")
    print(f"  {'─' * 58}")
    words = report.summary.split(". ")
    for sentence in words:
        if sentence:
            print(f"  {sentence.strip()}.")
    print()
    print(f"{BOLD}{CYAN}{'─' * 64}{RESET}")
    print()


def load_yaml_input(path: str) -> AnalysisInput:
    with open(path) as f:
        data = yaml.safe_load(f)
    a = data.get("asf_analysis", data)
    return AnalysisInput(
        system_name=a.get("system_name", a.get("title", "Unknown")),
        domain=a.get("domain", ""),
        system_type=a.get("system_type", ""),
        adaptation_scenario=a.get("adaptation_scenario", ""),
        input_event=a.get("input_event", {}).get("description", "") if isinstance(a.get("input_event"), dict) else a.get("input_event", ""),
        adaptation_requirement=a.get("adaptation_requirement", ""),
        current_operating_state=a.get("current_operating_state", {}).get("technical_maturity", "") if isinstance(a.get("current_operating_state"), dict) else a.get("current_operating_state", ""),
        observation_latency=a.get("observation_latency", 3),
        decision_latency=a.get("decision_latency", 3),
        execution_latency=a.get("execution_latency", 3),
        feedback_delay=a.get("feedback_delay", 3),
        learning_velocity=a.get("learning_velocity", 3),
        dependency_index=a.get("dependency_index", 3),
    )


def interactive_input() -> AnalysisInput:
    print(f"\n{BOLD}{CYAN}  ASF Interactive Analyzer{RESET}")
    print(f"  {DIM}Rate each dimension 1 (best) → 5 (worst){RESET}")
    print(f"  {DIM}Learning velocity: 1 (slow) → 5 (fast){RESET}\n")

    def ask(prompt, default=3):
        while True:
            try:
                val = input(f"  {prompt} [{default}]: ").strip()
                val = int(val) if val else default
                if 1 <= val <= 5:
                    return val
                print(f"  {RED}Enter a value between 1 and 5{RESET}")
            except (ValueError, KeyboardInterrupt):
                return default

    system_name = input(f"  {BOLD}System name{RESET}: ").strip() or "Unknown System"
    domain      = input(f"  {BOLD}Domain{RESET} (e.g. Telecom, AI Systems): ").strip() or "Enterprise"
    system_type = input(f"  {BOLD}System type{RESET}: ").strip() or ""
    scenario    = input(f"  {BOLD}Adaptation scenario{RESET}: ").strip() or ""

    print()
    obs  = ask("Observation latency  (how fast do you detect change?)")
    dec  = ask("Decision latency     (how fast do you commit to action?)")
    exc  = ask("Execution latency    (how fast do you implement?)")
    fdb  = ask("Feedback delay       (how fast do you see results?)")
    lrn  = ask("Learning velocity    (how fast do you improve?)")
    dep  = ask("Dependency index     (how many manual/approval dependencies?)")

    return AnalysisInput(
        system_name=system_name,
        domain=domain,
        system_type=system_type,
        adaptation_scenario=scenario,
        input_event="",
        adaptation_requirement="",
        current_operating_state="",
        observation_latency=obs,
        decision_latency=dec,
        execution_latency=exc,
        feedback_delay=fdb,
        learning_velocity=lrn,
        dependency_index=dep,
    )


def export_json(report, path: str) -> None:
    s = report.scores
    out = {
        "system_name": report.input.system_name,
        "domain": report.input.domain,
        "scores": {
            "adaptation_latency_score": s.adaptation_latency_score,
            "friction_score": s.friction_score,
            "adaptation_capability": s.adaptation_capability,
            "risk_band": s.risk_band.value,
            "layers": {
                "observation_latency": s.observation_latency,
                "decision_latency": s.decision_latency,
                "execution_latency": s.execution_latency,
                "feedback_delay": s.feedback_delay,
                "learning_velocity": s.learning_velocity,
                "dependency_index": s.dependency_index,
            }
        },
        "primary_friction": report.primary_friction,
        "bottleneck": report.bottleneck_dimension,
        "interventions": [
            {
                "priority": r.priority,
                "action": r.action,
                "target_dimension": r.target_dimension,
                "expected_reduction_weeks": r.expected_reduction_weeks,
                "effort": r.effort,
            }
            for r in report.interventions
        ],
        "summary": report.summary,
    }
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"  {GREEN}Report exported to {path}{RESET}\n")


def main():
    parser = argparse.ArgumentParser(
        description="ASF — Adaptive Systems Framework Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python asf.py                              # interactive mode
  python asf.py --file examples/att.yaml    # analyze from file
  python asf.py --file examples/att.yaml --export outputs/att.json
        """
    )
    parser.add_argument("--file", "-f", help="YAML input file")
    parser.add_argument("--export", "-e", help="Export report as JSON")
    parser.add_argument("--top", "-n", type=int, default=5,
                        help="Number of interventions to show (default: 5)")
    args = parser.parse_args()

    if args.file:
        try:
            inp = load_yaml_input(args.file)
        except Exception as ex:
            print(f"\n  {RED}Error loading {args.file}: {ex}{RESET}\n")
            sys.exit(1)
    else:
        inp = interactive_input()

    report = analyze(inp, top_interventions=args.top)
    print_report(report)

    if args.export:
        export_json(report, args.export)


if __name__ == "__main__":
    main()
