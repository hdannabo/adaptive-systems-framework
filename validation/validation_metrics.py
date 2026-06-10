#!/usr/bin/env python3
"""
ASF Validation Metrics Engine
==============================
Computes prediction accuracy, confidence calibration, and lead time
from the prediction register.

Usage:
    python validation_metrics.py                    # current state
    python validation_metrics.py --update P001 confirmed "BFSI +2.1% Q1FY27" 2026-07-22
    python validation_metrics.py --report           # full report
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime, date

REGISTER_PATH = Path(__file__).parent / "prediction_register.json"


def load_register() -> list[dict]:
    """Load predictions from JSON register."""
    if not REGISTER_PATH.exists():
        print(f"ERROR: {REGISTER_PATH} not found.")
        sys.exit(1)
    return json.loads(REGISTER_PATH.read_text())


def save_register(predictions: list[dict]):
    """Save predictions to JSON register."""
    REGISTER_PATH.write_text(json.dumps(predictions, indent=2))


def compute_metrics(predictions: list[dict]) -> dict:
    """Compute all validation metrics from current prediction register."""
    resolved = [p for p in predictions if p["outcome_status"] != "Pending"]
    confirmed = [p for p in resolved if p["outcome_status"] == "Confirmed"]
    refuted = [p for p in resolved if p["outcome_status"] == "Refuted"]

    total = len(predictions)
    n_resolved = len(resolved)

    if n_resolved == 0:
        return {
            "total_predictions": total,
            "resolved": 0,
            "pending": total,
            "accuracy": None,
            "high_conf_accuracy": None,
            "false_positive_rate": None,
            "false_negative_rate": None,
            "avg_lead_time_months": None,
            "meets_accuracy_target": None,
            "meets_high_conf_target": None,
        }

    # Prediction accuracy: confirmed / resolved
    accuracy = len(confirmed) / n_resolved if n_resolved > 0 else None

    # High confidence accuracy
    high_conf = [p for p in resolved if p["confidence"] == "High"]
    high_conf_confirmed = [p for p in high_conf if p["outcome_status"] == "Confirmed"]
    high_conf_acc = len(high_conf_confirmed) / len(high_conf) if high_conf else None

    # False positive rate: predicted issue that didn't occur / total predictions of issues
    # In ASF context: predicted constraint/risk that did not materialize
    issue_preds = [p for p in resolved 
                   if any(x in p["category"].lower() 
                          for x in ["risk", "constraint", "execution", "strategic"])]
    fp = [p for p in issue_preds if p["outcome_status"] == "Refuted"]
    fpr = len(fp) / len(issue_preds) if issue_preds else None

    # False negative rate would require knowing what ASF did NOT predict — not computable from register alone
    fnr = None

    # Lead time: months between assessment_date and outcome_date for confirmed predictions
    lead_times = []
    for p in confirmed:
        if p.get("outcome_date") and p.get("assessment_date"):
            try:
                assess = datetime.strptime(p["assessment_date"], "%Y-%m-%d").date()
                outcome = datetime.strptime(p["outcome_date"], "%Y-%m-%d").date()
                months = (outcome - assess).days / 30.44
                lead_times.append(months)
            except:
                pass

    avg_lead = sum(lead_times) / len(lead_times) if lead_times else None

    return {
        "total_predictions": total,
        "resolved": n_resolved,
        "pending": total - n_resolved,
        "confirmed": len(confirmed),
        "refuted": len(refuted),
        "accuracy": round(accuracy, 3) if accuracy is not None else None,
        "high_conf_accuracy": round(high_conf_acc, 3) if high_conf_acc is not None else None,
        "false_positive_rate": round(fpr, 3) if fpr is not None else None,
        "false_negative_rate": fnr,
        "avg_lead_time_months": round(avg_lead, 1) if avg_lead is not None else None,
        "meets_accuracy_target": accuracy >= 0.70 if accuracy is not None else None,
        "meets_high_conf_target": high_conf_acc >= 0.80 if high_conf_acc is not None else None,
    }


def update_prediction(predictions: list[dict], pred_id: str, 
                       outcome: str, notes: str, outcome_date: str) -> list[dict]:
    """Record an outcome for a prediction."""
    valid_outcomes = ("Confirmed", "Refuted", "Partial", "Pending")
    if outcome not in valid_outcomes:
        print(f"ERROR: outcome must be one of {valid_outcomes}")
        sys.exit(1)

    found = False
    for p in predictions:
        if p["id"] == pred_id:
            # Immutability: only add, never remove
            p["outcome_status"] = outcome
            p["outcome_date"] = outcome_date
            p["outcome_notes"] = notes
            p["outcome_result"] = f"Recorded {datetime.now().strftime('%Y-%m-%d')}"
            found = True
            print(f"Updated {pred_id}: {outcome}")
            break

    if not found:
        print(f"ERROR: prediction {pred_id} not found")
        sys.exit(1)

    return predictions


def print_report(predictions: list[dict]):
    """Print full validation metrics report."""
    metrics = compute_metrics(predictions)
    pending = [p for p in predictions if p["outcome_status"] == "Pending"]
    resolved = [p for p in predictions if p["outcome_status"] != "Pending"]

    print("\n" + "="*62)
    print("ASF PREDICTION VALIDATION REPORT")
    print("="*62)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"\nTotal predictions: {metrics['total_predictions']}")
    print(f"Resolved:          {metrics['resolved']}")
    print(f"Pending:           {metrics['pending']}")

    if metrics["resolved"] > 0:
        print(f"\n{'─'*40}")
        print("VALIDATION METRICS")
        print(f"{'─'*40}")

        def fmt(v, target_str):
            if v is None: return "N/A (no resolved)"
            pct = f"{v*100:.1f}%"
            return f"{pct} (target: {target_str})"

        print(f"Prediction accuracy:    {fmt(metrics['accuracy'], '≥70%')}")
        print(f"High conf accuracy:     {fmt(metrics['high_conf_accuracy'], '≥80%')}")
        print(f"False positive rate:    {fmt(metrics['false_positive_rate'], '≤20%')}")
        print(f"Avg lead time:          {metrics['avg_lead_time_months']} months (target: ≥6)")

        print(f"\n{'─'*40}")
        print("STATUS FLAGS")
        print(f"{'─'*40}")
        acc_ok = metrics["meets_accuracy_target"]
        hca_ok = metrics["meets_high_conf_target"]
        print(f"Accuracy target (≥70%): {'✅ PASS' if acc_ok else ('❌ FAIL' if acc_ok is False else '⏳ pending')}")
        print(f"High conf (≥80%):       {'✅ PASS' if hca_ok else ('❌ FAIL' if hca_ok is False else '⏳ pending')}")

        print(f"\n{'─'*40}")
        print("RESOLVED PREDICTIONS")
        print(f"{'─'*40}")
        for p in resolved:
            icon = "✅" if p["outcome_status"] == "Confirmed" else "❌"
            print(f"  {icon} {p['id']} | {p['company'][:20]} | {p['outcome_status']}")
            if p.get("outcome_notes"):
                print(f"       {p['outcome_notes'][:60]}")

    if pending:
        print(f"\n{'─'*40}")
        print("PENDING PREDICTIONS (next checkpoints)")
        print(f"{'─'*40}")
        # Sort by expected horizon
        for p in pending:
            print(f"  ⏳ {p['id']} | {p['company'][:20]} | {p['confidence']} | {p['horizon'][:45]}")

    print("\n" + "="*62 + "\n")


def main():
    parser = argparse.ArgumentParser(description="ASF Validation Metrics Engine")
    parser.add_argument("--update", nargs=4, 
                        metavar=("ID", "OUTCOME", "NOTES", "DATE"),
                        help="Record an outcome: ID Confirmed|Refuted|Partial 'notes' YYYY-MM-DD")
    parser.add_argument("--report", action="store_true",
                        help="Print full validation report")
    parser.add_argument("--metrics", action="store_true",
                        help="Print metrics as JSON")
    args = parser.parse_args()

    predictions = load_register()

    if args.update:
        pred_id, outcome, notes, outcome_date = args.update
        predictions = update_prediction(predictions, pred_id, outcome, notes, outcome_date)
        save_register(predictions)

    if args.metrics:
        print(json.dumps(compute_metrics(predictions), indent=2))
    else:
        print_report(predictions)


if __name__ == "__main__":
    main()
