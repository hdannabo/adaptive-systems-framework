#!/usr/bin/env python3
"""
ASF — Adaptive Systems Framework
Batch analyzer: scores all 100 cases from the dataset and exports results.

Usage:
    python asf_analyze.py                          # scores all 100 cases
    python asf_analyze.py --domain "Telecom & Networks"   # filter by domain
    python asf_analyze.py --risk High              # filter by risk band
    python asf_analyze.py --top 10                 # show top 10 highest latency
"""

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.asf import analyze, AnalysisInput

RESET = "\033[0m"; BOLD = "\033[1m"; DIM = "\033[2m"
RED = "\033[91m"; YELLOW = "\033[93m"; GREEN = "\033[92m"; CYAN = "\033[96m"

def load_dataset(path="/home/claude/adaptive-systems-framework/research/asf_100_cases.csv"):
    cases = []
    with open(path) as f:
        for row in csv.DictReader(f):
            cases.append(AnalysisInput(
                system_name=row["System Name"],
                domain=row["Domain"],
                system_type=row["System Type"],
                adaptation_scenario=row["Adaptation Scenario"],
                input_event=row["Input Event / Trigger"],
                adaptation_requirement=row["Adaptation Requirement"],
                current_operating_state=row["Current Operating State"],
                observation_latency=int(row["Observation Latency (1-5)"]),
                decision_latency=int(row["Decision Latency (1-5)"]),
                execution_latency=int(row["Execution Latency (1-5)"]),
                feedback_delay=int(row["Feedback Delay (1-5)"]),
                learning_velocity=int(row["Learning Velocity (1-5)"]),
                dependency_index=int(row["Dependency Index (1-5)"]),
            ))
    return cases

def risk_color(band):
    return {"Low": GREEN, "Medium": YELLOW, "High": RED}.get(band, "")

def score_color(s):
    return GREEN if s < 2.5 else (YELLOW if s < 3.5 else RED)

def bar(v, w=12):
    f = int((v/5)*w)
    c = GREEN if v < 2.5 else (YELLOW if v < 3.5 else RED)
    return f"{c}{'█'*f}{'░'*(w-f)}{RESET}"

def main():
    parser = argparse.ArgumentParser(description="ASF Batch Analyzer")
    parser.add_argument("--domain", help="Filter by domain")
    parser.add_argument("--risk", choices=["Low","Medium","High"], help="Filter by risk band")
    parser.add_argument("--top", type=int, help="Show top N highest latency systems")
    parser.add_argument("--export", help="Export results to JSON file")
    args = parser.parse_args()

    cases = load_dataset()
    reports = [analyze(c) for c in cases]

    if args.domain:
        reports = [r for r in reports if args.domain.lower() in r.input.domain.lower()]
    if args.risk:
        reports = [r for r in reports if r.scores.risk_band.value == args.risk]

    reports.sort(key=lambda r: -r.scores.adaptation_latency_score)
    if args.top:
        reports = reports[:args.top]

    print(f"\n{BOLD}{CYAN}{'─'*72}{RESET}")
    print(f"{BOLD}  ASF Batch Analysis — {len(reports)} systems{RESET}")
    print(f"{BOLD}{CYAN}{'─'*72}{RESET}\n")
    print(f"  {'System':<28} {'Domain':<26} {'Score':>5}  {'Risk':<8} {'Bottleneck'}")
    print(f"  {'─'*28} {'─'*26} {'─'*5}  {'─'*8} {'─'*20}")

    for r in reports:
        s = r.scores.adaptation_latency_score
        rc = risk_color(r.scores.risk_band.value)
        sc = score_color(s)
        name = r.input.system_name[:27]
        domain = r.input.domain[:25]
        risk = r.scores.risk_band.value
        bottleneck = r.bottleneck_dimension[:20]
        print(f"  {name:<28} {DIM}{domain:<26}{RESET} {sc}{s:.2f}{RESET}  {bar(s)}  {rc}{risk:<8}{RESET} {bottleneck}")

    print()
    scores = [r.scores.adaptation_latency_score for r in reports]
    avg = sum(scores)/len(scores)
    high = sum(1 for r in reports if r.scores.risk_band.value == "High")
    low  = sum(1 for r in reports if r.scores.risk_band.value == "Low")
    print(f"  {BOLD}Average latency score:{RESET} {score_color(avg)}{avg:.2f}{RESET}  |  "
          f"{RED}High risk: {high}{RESET}  |  {GREEN}Fast adapters: {low}{RESET}")
    print(f"{BOLD}{CYAN}{'─'*72}{RESET}\n")

    if args.export:
        out = [{"system": r.input.system_name, "domain": r.input.domain,
                "score": r.scores.adaptation_latency_score,
                "risk": r.scores.risk_band.value,
                "bottleneck": r.bottleneck_dimension,
                "friction": r.primary_friction,
                "top_intervention": r.interventions[0].action if r.interventions else ""}
               for r in reports]
        with open(args.export, "w") as f:
            json.dump(out, f, indent=2)
        print(f"  {GREEN}Exported {len(out)} results to {args.export}{RESET}\n")

if __name__ == "__main__":
    main()
