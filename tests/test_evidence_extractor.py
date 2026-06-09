#!/usr/bin/env python3
"""
ASF v0.4 — Evidence Extractor Validation Tests

Run: python tests/test_evidence_extractor.py
All tests run locally without LLM calls.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import json

# ── Import test targets ────────────────────────────────────────────────
from asf.evidence.extractor import (
    DimensionEvidence, EvidencePackage,
    validate_quote, DIMENSION_DEFINITIONS,
    _keyword_score, evidence_to_analysis_input,
    export_cited_report, _estimate_cost,
)
from asf import analyze, AnalysisInput
from asf.scoring.crt_engine import CRTInput, calculate_crt


def test_quote_validator():
    """Every evidence quote must appear verbatim in the source document."""
    doc = "Boeing is producing at approximately 18 aircraft per month against our target of 38"
    assert validate_quote("producing at approximately 18 aircraft per month", doc)
    assert not validate_quote("Boeing produces 50 aircraft per month exceeding targets", doc)
    assert validate_quote("", doc)  # empty quote is valid (Low confidence)
    assert validate_quote("   ", doc)  # whitespace-only is also valid
    print("  PASS: test_quote_validator")


def test_confidence_aggregation():
    """Overall confidence = weakest link across all dimensions."""
    make = lambda c: DimensionEvidence("k","L",3,"q","p","r",c)

    dims_all_high = {f"d{i}": make("High") for i in range(4)}
    dims_all_high.update({f"d{i}": make("Medium") for i in range(4, 6)})
    pkg = EvidencePackage("T","d","m","",0,0.0,False,dims_all_high)
    assert pkg.overall_confidence == "High", f"Expected High, got {pkg.overall_confidence}"

    dims_with_low = {**dims_all_high, "d5": make("Low")}
    pkg2 = EvidencePackage("T","d","m","",0,0.0,False,dims_with_low)
    assert pkg2.overall_confidence == "Low", f"Expected Low, got {pkg2.overall_confidence}"
    print("  PASS: test_confidence_aggregation")


def test_keyword_fallback():
    """Keyword fallback must return valid scores in 1-5 range."""
    text = "We have significant manual processes blocking our deployment pipeline. Legacy systems require weeks."
    for dim_key in DIMENSION_DEFINITIONS:
        ev = _keyword_score(text, dim_key)
        assert 1 <= ev.score <= 5, f"{dim_key}: score {ev.score} out of range"
        assert ev.fallback_used is True
        assert ev.confidence == "Low"
    print("  PASS: test_keyword_fallback")


def test_bridge_to_analysis_input():
    """evidence_to_analysis_input must produce valid AnalysisInput."""
    dims = {
        "observation_latency": DimensionEvidence("observation_latency","OL",3,"q","p","r","Medium"),
        "decision_latency":    DimensionEvidence("decision_latency","DL",4,"q","p","r","High"),
        "execution_latency":   DimensionEvidence("execution_latency","EL",5,"q","p","r","High"),
        "feedback_delay":      DimensionEvidence("feedback_delay","FD",4,"q","p","r","Medium"),
        "learning_velocity":   DimensionEvidence("learning_velocity","LV",2,"q","p","r","High"),
        "dependency_index":    DimensionEvidence("dependency_index","DI",4,"q","p","r","Medium"),
    }
    pkg = EvidencePackage("Boeing","Boeing_AR.pdf","gpt-4o","",0,0.0,False,dims)
    inp = evidence_to_analysis_input(pkg, domain="Manufacturing")
    assert inp.system_name == "Boeing"
    assert inp.execution_latency == 5
    assert inp.learning_velocity == 2
    print("  PASS: test_bridge_to_analysis_input")


def test_full_pipeline():
    """Full pipeline: fake evidence → AnalysisInput → ASFReport → correct score."""
    dims = {
        "observation_latency": DimensionEvidence("observation_latency","OL",3,"q","p","r","Medium"),
        "decision_latency":    DimensionEvidence("decision_latency","DL",4,"q","p","r","High"),
        "execution_latency":   DimensionEvidence("execution_latency","EL",5,"q","p","r","High"),
        "feedback_delay":      DimensionEvidence("feedback_delay","FD",4,"q","p","r","Medium"),
        "learning_velocity":   DimensionEvidence("learning_velocity","LV",2,"q","p","r","High"),
        "dependency_index":    DimensionEvidence("dependency_index","DI",4,"q","p","r","Medium"),
    }
    pkg = EvidencePackage("Boeing","Boeing_AR.pdf","gpt-4o","",0,0.0,False,dims)
    inp = evidence_to_analysis_input(pkg, domain="Manufacturing")
    report = analyze(inp)

    expected_als = round((3*0.15)+(4*0.25)+(5*0.30)+(4*0.15)+(4*0.15)-(2*0.10), 2)
    assert report.scores.adaptation_latency_score == expected_als, \
        f"ALS {report.scores.adaptation_latency_score} != expected {expected_als}"
    assert report.bottleneck_dimension == "Execution Latency"
    assert report.scores.risk_band.value == "High"
    print(f"  PASS: test_full_pipeline (ALS={expected_als}, bottleneck=Execution Latency)")


def test_json_export():
    """JSON export must produce valid parseable JSON with all required fields."""
    dims = {k: DimensionEvidence(k,"L",3,"q","p","r","Medium") for k in DIMENSION_DEFINITIONS}
    pkg = EvidencePackage("TestCo","doc.pdf","gpt-4o","",0,0.0,False,dims)
    inp = evidence_to_analysis_input(pkg)
    report = analyze(inp)
    out = export_cited_report(pkg, report)
    parsed = json.loads(json.dumps(out))  # verify serializable
    assert parsed["asf_version"] == "0.4.0"
    assert len(parsed["dimensions"]) == 6
    assert "bottleneck_dimension" in parsed
    assert "overall_confidence" in parsed
    print("  PASS: test_json_export")


def test_cost_estimate():
    """Cost per document must be in reasonable range."""
    cost = _estimate_cost(12000, "gpt-4o")
    assert 0.02 < cost < 0.15, f"Cost out of expected range: ${cost}"
    print(f"  PASS: test_cost_estimate (${cost:.4f} per ~12K tokens)")


def test_all_dimension_definitions_present():
    """All 6 required dimensions must be defined."""
    required = {"observation_latency", "decision_latency", "execution_latency",
                "feedback_delay", "learning_velocity", "dependency_index"}
    assert required == set(DIMENSION_DEFINITIONS.keys()), \
        f"Missing dimensions: {required - set(DIMENSION_DEFINITIONS.keys())}"
    for dim_key, defn in DIMENSION_DEFINITIONS.items():
        assert "label" in defn
        assert "definition" in defn
        assert "scale" in defn
    print("  PASS: test_all_dimension_definitions_present")


if __name__ == "__main__":
    print("\nASF v0.4 — Evidence Extractor Tests\n" + "="*40)
    test_quote_validator()
    test_confidence_aggregation()
    test_keyword_fallback()
    test_bridge_to_analysis_input()
    test_full_pipeline()
    test_json_export()
    test_cost_estimate()
    test_all_dimension_definitions_present()
    print("\n" + "="*40)
    print("ALL TESTS PASSED")
    print("="*40 + "\n")
