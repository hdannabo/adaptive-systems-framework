#!/usr/bin/env python3
"""
ASF Conformance Agent
=====================
The engineering translation of Conformance:
A system that continuously checks whether LLM outputs are aligned
with their defined purpose and acceptance criteria.

Core principle:
  Every LLM action has a defined purpose (acceptance criteria).
  Every output must be checked against that purpose.
  Drift from purpose = governance failure = purpose drift in engineering terms.

Usage:
    python asf_conformance_agent.py --task analyze_document --input report.pdf
    python asf_conformance_agent.py --task score_program --input program.yaml
    python asf_conformance_agent.py --validate output.json --criteria criteria.yaml
"""

import json
import time
import uuid
import argparse
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any
import sys

sys.path.insert(0, str(Path(__file__).parent / "src"))


# ── Acceptance Criteria Registry ──────────────────────────────────────────────
# This is the Conformance of the system.
# Each task has a defined purpose. The agent checks every output against it.

ACCEPTANCE_CRITERIA = {

    "analyze_document": {
        "purpose": "Extract adaptation signals from a document and produce a scored ASF diagnosis",
        "criteria": [
            {
                "id": "AC-01",
                "description": "All 6 ASF dimensions must be scored (1–5)",
                "check": lambda r: all(
                    k in r.get("scores", {}).get("layers", {})
                    for k in ["observation_latency", "decision_latency", "execution_latency",
                              "feedback_delay", "learning_velocity", "dependency_index"]
                ),
                "severity": "CRITICAL"
            },
            {
                "id": "AC-02",
                "description": "Adaptation latency score must be in range 0.0–5.0",
                "check": lambda r: 0.0 <= r.get("scores", {}).get("adaptation_latency_score", -1) <= 5.0,
                "severity": "CRITICAL"
            },
            {
                "id": "AC-03",
                "description": "Risk band must be Low, Medium, or High",
                "check": lambda r: r.get("scores", {}).get("risk_band") in ["Low", "Medium", "High"],
                "severity": "CRITICAL"
            },
            {
                "id": "AC-04",
                "description": "At least one intervention must be generated",
                "check": lambda r: len(r.get("interventions", [])) >= 1,
                "severity": "CRITICAL"
            },
            {
                "id": "AC-05",
                "description": "Primary friction must be identified",
                "check": lambda r: bool(r.get("primary_friction")),
                "severity": "HIGH"
            },
            {
                "id": "AC-06",
                "description": "Bottleneck dimension must be named",
                "check": lambda r: bool(r.get("bottleneck")),
                "severity": "HIGH"
            },
            {
                "id": "AC-07",
                "description": "Summary must be present and non-empty",
                "check": lambda r: len(r.get("summary", "")) > 20,
                "severity": "MEDIUM"
            },
            {
                "id": "AC-08",
                "description": "Token cost must be within budget ($0.50 per analysis)",
                "check": lambda r: r.get("metadata", {}).get("token_cost_usd", 0) <= 0.50,
                "severity": "HIGH"
            },
            {
                "id": "AC-09",
                "description": "Analysis duration must be under 30 seconds",
                "check": lambda r: r.get("metadata", {}).get("duration_ms", 0) <= 30000,
                "severity": "HIGH"
            },
        ],
        "token_budget_usd": 0.50,
        "latency_budget_ms": 30000,
    },

    "score_program": {
        "purpose": "Score an AI governance program and produce prioritized interventions",
        "criteria": [
            {
                "id": "AC-01",
                "description": "Governance score must be 0–100",
                "check": lambda r: 0 <= r.get("score", -1) <= 100,
                "severity": "CRITICAL"
            },
            {
                "id": "AC-02",
                "description": "At least 3 interventions must be generated",
                "check": lambda r: len(r.get("interventions", [])) >= 3,
                "severity": "CRITICAL"
            },
            {
                "id": "AC-03",
                "description": "Each intervention must have a priority (P0/P1/P2)",
                "check": lambda r: all(
                    i.get("priority") in ["P0", "P1", "P2"]
                    for i in r.get("interventions", [])
                ),
                "severity": "HIGH"
            },
            {
                "id": "AC-04",
                "description": "Primary bottleneck must be identified",
                "check": lambda r: bool(r.get("primary_bottleneck")),
                "severity": "HIGH"
            },
            {
                "id": "AC-05",
                "description": "Value realization ratio must be computed",
                "check": lambda r: "value_realization_ratio" in r,
                "severity": "MEDIUM"
            },
        ],
        "token_budget_usd": 0.10,
        "latency_budget_ms": 5000,
    },

    "generate_intervention": {
        "purpose": "Generate a specific, actionable intervention for a named bottleneck",
        "criteria": [
            {
                "id": "AC-01",
                "description": "Intervention must target the named bottleneck dimension",
                "check": lambda r: bool(r.get("target_dimension")),
                "severity": "CRITICAL"
            },
            {
                "id": "AC-02",
                "description": "Priority must be P0, P1, or P2",
                "check": lambda r: r.get("priority") in ["P0", "P1", "P2"],
                "severity": "CRITICAL"
            },
            {
                "id": "AC-03",
                "description": "Expected reduction in weeks must be a positive integer",
                "check": lambda r: isinstance(r.get("expected_reduction_weeks"), int)
                                   and r.get("expected_reduction_weeks", 0) > 0,
                "severity": "HIGH"
            },
            {
                "id": "AC-04",
                "description": "Effort estimate must be low, medium, or high",
                "check": lambda r: r.get("effort") in ["low", "medium", "high"],
                "severity": "MEDIUM"
            },
        ],
        "token_budget_usd": 0.05,
        "latency_budget_ms": 3000,
    },
}


# ── Conformance Result ───────────────────────────────────────────────────────

@dataclass
class CriterionResult:
    criterion_id: str
    description: str
    severity: str
    passed: bool
    reason: str = ""


@dataclass
class ConformanceReport:
    conformance_id: str
    task: str
    timestamp: str
    passed: bool
    score: float                        # 0.0 – 1.0
    critical_failures: int
    high_failures: int
    medium_failures: int
    criteria_results: list[CriterionResult]
    token_cost_usd: float
    duration_ms: int
    within_token_budget: bool
    within_latency_budget: bool
    conformance_status: str                  # ALIGNED | DRIFTING | VIOLATED
    conformance_explanation: str
    recommended_action: str

    def to_dict(self) -> dict:
        d = asdict(self)
        d["criteria_results"] = [asdict(c) for c in self.criteria_results]
        return d


# ── Conformance Checker ────────────────────────────────────────────────────────

class ConformanceAgent:
    """
    The sentinel.

    In systems engineering terms, this is the Conformance layer —
    the mechanism that ensures every LLM output stays aligned
    with its defined purpose and acceptance criteria.

    It checks:
      1. Did the output satisfy all acceptance criteria?
      2. Did the process stay within token budget?
      3. Did the process stay within latency budget?
      4. Is the system aligned (conformant) or drifting (purpose drift)?
    """

    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.history: list[ConformanceReport] = []

    def check(
        self,
        task: str,
        output: dict,
        token_cost_usd: float = 0.0,
        duration_ms: int = 0,
    ) -> ConformanceReport:

        if task not in ACCEPTANCE_CRITERIA:
            raise ValueError(f"Unknown task: '{task}'. Defined tasks: {list(ACCEPTANCE_CRITERIA.keys())}")

        spec = ACCEPTANCE_CRITERIA[task]
        criteria = spec["criteria"]
        token_budget = spec["token_budget_usd"]
        latency_budget = spec["latency_budget_ms"]

        results: list[CriterionResult] = []
        critical_failures = 0
        high_failures = 0
        medium_failures = 0

        for c in criteria:
            try:
                passed = c["check"](output)
                reason = "" if passed else f"Output did not satisfy: {c['description']}"
            except Exception as e:
                passed = False
                reason = f"Check raised exception: {e}"

            if not passed:
                if c["severity"] == "CRITICAL":
                    critical_failures += 1
                elif c["severity"] == "HIGH":
                    high_failures += 1
                else:
                    medium_failures += 1

            results.append(CriterionResult(
                criterion_id=c["id"],
                description=c["description"],
                severity=c["severity"],
                passed=passed,
                reason=reason,
            ))

        total = len(criteria)
        passed_count = sum(1 for r in results if r.passed)
        score = passed_count / total if total > 0 else 0.0

        within_token = token_cost_usd <= token_budget
        within_latency = duration_ms <= latency_budget if duration_ms > 0 else True
        overall_passed = critical_failures == 0 and within_token and within_latency

        # Conformance classification
        if critical_failures == 0 and high_failures == 0 and within_token and within_latency:
            conformance_status = "ALIGNED"
            conformance_explanation = (
                f"System is operating within its defined purpose. "
                f"All critical and high-priority criteria met. "
                f"Token cost ${token_cost_usd:.4f} within budget ${token_budget:.2f}."
            )
            recommended_action = "Continue. Log this run as a learning baseline."

        elif critical_failures == 0 and (high_failures > 0 or not within_token or not within_latency):
            conformance_status = "DRIFTING"
            issues = []
            if high_failures > 0:
                issues.append(f"{high_failures} high-priority criteria failed")
            if not within_token:
                issues.append(f"token cost ${token_cost_usd:.4f} exceeds budget ${token_budget:.2f}")
            if not within_latency:
                issues.append(f"latency {duration_ms}ms exceeds budget {latency_budget}ms")
            conformance_explanation = (
                f"System is drifting from its defined purpose: {'; '.join(issues)}. "
                "Core function delivered but governance constraints violated."
            )
            recommended_action = "Flag for review. Investigate cost or latency drift. Do not scale until resolved."

        else:
            conformance_status = "VIOLATED"
            conformance_explanation = (
                f"System violated its defined purpose: {critical_failures} critical criteria failed. "
                "Output cannot be trusted or used."
            )
            recommended_action = "Halt. Do not use this output. Investigate root cause before retry."

        report = ConformanceReport(
            conformance_id=str(uuid.uuid4())[:8],
            task=task,
            timestamp=datetime.utcnow().isoformat(),
            passed=overall_passed,
            score=round(score, 3),
            critical_failures=critical_failures,
            high_failures=high_failures,
            medium_failures=medium_failures,
            criteria_results=results,
            token_cost_usd=token_cost_usd,
            duration_ms=duration_ms,
            within_token_budget=within_token,
            within_latency_budget=within_latency,
            conformance_status=conformance_status,
            conformance_explanation=conformance_explanation,
            recommended_action=recommended_action,
        )

        self.history.append(report)

        if self.verbose:
            self._print_report(report)

        return report

    def _print_report(self, r: ConformanceReport) -> None:
        RESET = "\033[0m"; BOLD = "\033[1m"; DIM = "\033[2m"
        GREEN = "\033[92m"; YELLOW = "\033[93m"; RED = "\033[91m"; CYAN = "\033[96m"

        STATUS_COLOR = {"ALIGNED": GREEN, "DRIFTING": YELLOW, "VIOLATED": RED}
        sc = STATUS_COLOR.get(r.conformance_status, RESET)

        print()
        print(f"{BOLD}{CYAN}{'─' * 64}{RESET}")
        print(f"{BOLD}  ASF Conformance Report — {r.task}{RESET}")
        print(f"{BOLD}{CYAN}{'─' * 64}{RESET}")
        print()
        print(f"  ID          {DIM}{r.conformance_id}{RESET}")
        print(f"  Timestamp   {DIM}{r.timestamp}{RESET}")
        print(f"  Score       {BOLD}{int(r.score * 100)}%{RESET} ({sum(1 for c in r.criteria_results if c.passed)}/{len(r.criteria_results)} criteria passed)")
        print(f"  Conformance {sc}{BOLD}{r.conformance_status}{RESET}")
        print()

        print(f"  {BOLD}Criteria results:{RESET}")
        for c in r.criteria_results:
            icon = f"{GREEN}✓{RESET}" if c.passed else f"{RED}✗{RESET}"
            sev = f"{RED}[{c.severity}]{RESET}" if not c.passed and c.severity == "CRITICAL" else \
                  f"{YELLOW}[{c.severity}]{RESET}" if not c.passed else f"{DIM}[{c.severity}]{RESET}"
            print(f"  {icon} {c.criterion_id} {sev} {c.description}")
            if not c.passed and c.reason:
                print(f"      {RED}{c.reason}{RESET}")

        print()
        print(f"  Token cost  ${r.token_cost_usd:.4f} / budget ${ACCEPTANCE_CRITERIA[r.task]['token_budget_usd']:.2f}  "
              f"{'✓' if r.within_token_budget else '✗ OVER BUDGET'}")
        if r.duration_ms > 0:
            print(f"  Latency     {r.duration_ms}ms / budget {ACCEPTANCE_CRITERIA[r.task]['latency_budget_ms']}ms  "
                  f"{'✓' if r.within_latency_budget else '✗ TOO SLOW'}")
        print()
        print(f"  {BOLD}Conformance:{RESET} {r.conformance_explanation}")
        print(f"  {BOLD}Action:{RESET} {r.recommended_action}")
        print()
        print(f"{BOLD}{CYAN}{'─' * 64}{RESET}")
        print()

    def drift_summary(self) -> dict:
        """Summarize drift patterns across all runs — learning velocity signal."""
        if not self.history:
            return {"runs": 0, "message": "No history yet"}

        runs = len(self.history)
        aligned = sum(1 for r in self.history if r.conformance_status == "ALIGNED")
        drifting = sum(1 for r in self.history if r.conformance_status == "DRIFTING")
        violated = sum(1 for r in self.history if r.conformance_status == "VIOLATED")
        avg_cost = sum(r.token_cost_usd for r in self.history) / runs
        avg_score = sum(r.score for r in self.history) / runs

        # Most common failure
        all_failures = [
            c for r in self.history
            for c in r.criteria_results
            if not c.passed
        ]
        failure_counts = {}
        for f in all_failures:
            failure_counts[f.description] = failure_counts.get(f.description, 0) + 1
        top_failure = max(failure_counts, key=failure_counts.get) if failure_counts else "None"

        return {
            "runs": runs,
            "aligned_pct": round(aligned / runs * 100, 1),
            "drifting_pct": round(drifting / runs * 100, 1),
            "violated_pct": round(violated / runs * 100, 1),
            "avg_conformance_score": round(avg_score, 3),
            "avg_token_cost_usd": round(avg_cost, 4),
            "most_common_failure": top_failure,
            "learning_signal": (
                "System is learning — conformance improving" if runs > 1 and
                self.history[-1].score > self.history[0].score
                else "Conformance stable" if runs > 1
                else "Insufficient history"
            )
        }


# ── CLI ────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="ASF Conformance Agent — checks LLM outputs against acceptance criteria",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python asf_conformance_agent.py --validate output.json --task analyze_document
  python asf_conformance_agent.py --demo
  python asf_conformance_agent.py --list-criteria
        """
    )
    parser.add_argument("--validate", help="JSON output file to validate")
    parser.add_argument("--task", default="analyze_document",
                        choices=list(ACCEPTANCE_CRITERIA.keys()),
                        help="Task type to validate against")
    parser.add_argument("--token-cost", type=float, default=0.0,
                        help="Token cost in USD for this run")
    parser.add_argument("--duration-ms", type=int, default=0,
                        help="Execution duration in milliseconds")
    parser.add_argument("--demo", action="store_true",
                        help="Run a demonstration with synthetic outputs")
    parser.add_argument("--list-criteria", action="store_true",
                        help="List all acceptance criteria for all tasks")
    args = parser.parse_args()

    agent = ConformanceAgent(verbose=True)

    if args.list_criteria:
        CYAN = "\033[96m"; BOLD = "\033[1m"; RESET = "\033[0m"; DIM = "\033[2m"
        for task, spec in ACCEPTANCE_CRITERIA.items():
            print(f"\n{BOLD}{CYAN}{task}{RESET}")
            print(f"  Purpose: {spec['purpose']}")
            print(f"  Token budget: ${spec['token_budget_usd']:.2f}")
            print(f"  Latency budget: {spec['latency_budget_ms']}ms")
            print(f"  Criteria:")
            for c in spec["criteria"]:
                print(f"    [{c['severity']}] {c['id']}: {c['description']}")
        return

    if args.demo:
        print("\n=== DEMO: Conformance Agent ===")
        print("Running three scenarios: aligned, drifting, violated\n")

        # Scenario 1: Perfect output
        perfect = {
            "scores": {
                "adaptation_latency_score": 3.75,
                "risk_band": "High",
                "layers": {
                    "observation_latency": 3,
                    "decision_latency": 4,
                    "execution_latency": 5,
                    "feedback_delay": 4,
                    "learning_velocity": 3,
                    "dependency_index": 5,
                }
            },
            "primary_friction": "Manual dependency / legacy systems",
            "bottleneck": "Execution Latency",
            "interventions": [
                {"priority": "P0", "action": "Automate top 3 manual handoffs", "target_dimension": "Execution Latency"}
            ],
            "summary": "AT&T is a HIGH risk system with adaptation latency score of 4.0/5.0.",
            "metadata": {"token_cost_usd": 0.03, "duration_ms": 8200}
        }
        print("SCENARIO 1: Well-formed output, within budget")
        agent.check("analyze_document", perfect, token_cost_usd=0.03, duration_ms=8200)

        # Scenario 2: Over budget
        print("SCENARIO 2: Correct output but token cost exceeded")
        agent.check("analyze_document", perfect, token_cost_usd=0.85, duration_ms=45000)

        # Scenario 3: Missing critical fields
        broken = {"scores": {}, "interventions": [], "summary": ""}
        print("SCENARIO 3: Broken output — critical criteria violated")
        agent.check("analyze_document", broken, token_cost_usd=0.02, duration_ms=3000)

        print("\n=== DRIFT SUMMARY ===")
        print(json.dumps(agent.drift_summary(), indent=2))
        return

    if args.validate:
        with open(args.validate) as f:
            output = json.load(f)
        agent.check(args.task, output,
                    token_cost_usd=args.token_cost,
                    duration_ms=args.duration_ms)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
