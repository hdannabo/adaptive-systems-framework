"""
ASF — Capability Realization Time (CRT) Engine
===============================================
CRT is a derived ASF metric.

Core relationship:
  ASF finds the Adaptation Gap.
  CRT estimates how long it may take to close that gap.

Formula:
  Adaptation Gap = Required Capability Score - Current Capability Score

  Base months = Gap × Base Realization Time
  Friction multiplier = 1 + (Governance Friction × 0.3) + (Execution Friction × 0.4) + (Dependency Risk × 0.3)
  Learning accelerator = 1 - (Learning Velocity / 10)

  CRT = Base months × Friction multiplier × Learning accelerator

Risk classification:
  < 6 months   = Low
  6–18 months  = Medium
  18–36 months = High
  > 36 months  = Critical
"""

from dataclasses import dataclass
from typing import Literal


CRTRiskLevel = Literal["Low", "Medium", "High", "Critical"]


@dataclass
class CRTInput:
    """All inputs required to compute Capability Realization Time."""
    system_name: str
    use_case: str

    # Core gap inputs (1.0–10.0 scale)
    required_capability_score: float     # what the system must achieve
    current_capability_score: float      # where the system is today

    # Friction inputs (0.0–1.0)
    governance_friction: float           # approval overhead, policy delays
    execution_friction: float            # manual steps, legacy systems
    dependency_risk: float               # external blockers, coordination

    # Velocity inputs (0.0–1.0, higher = faster)
    learning_velocity: float             # how fast the system improves
    evidence_confidence: float           # how reliable the input data is

    # Objective integrity (0.0–1.0)
    objective_integrity_score: float     # how well-defined and stable the goal is

    # Base time estimate
    base_realization_time_months: float  # domain-specific baseline


@dataclass
class CRTOutput:
    """Full CRT analysis output."""
    system_name: str
    use_case: str

    # Gap
    adaptation_gap: float

    # Time estimates
    crt_months: float
    crt_years: float
    crt_range_low_months: float
    crt_range_high_months: float

    # Risk
    crt_risk_level: CRTRiskLevel

    # Diagnostics
    primary_bottleneck: str
    governance_readiness_score: float    # 0.0–1.0
    evidence_confidence_score: float     # 0.0–1.0

    # Plain English
    plain_english_explanation: str


def calculate_adaptation_gap(required: float, current: float) -> float:
    """
    Adaptation Gap = Required Capability - Current Capability.
    Clamped to 0.0 minimum (no negative gap).
    """
    return max(0.0, round(required - current, 2))


def calculate_governance_readiness(
    governance_friction: float,
    objective_integrity: float,
    evidence_confidence: float,
) -> float:
    """
    Governance readiness = how well-governed the realization effort is.
    Higher = more ready. Range: 0.0–1.0.
    """
    return round(
        (objective_integrity * 0.40)
        + (evidence_confidence * 0.35)
        + ((1.0 - governance_friction) * 0.25),
        3
    )


def estimate_crt_months(inp: CRTInput, gap: float) -> float:
    """
    Estimate how many months to close the adaptation gap.

    Base formula:
      raw_months = gap × base_realization_time_months
      friction_multiplier = 1 + (gov×0.30) + (exec×0.40) + (dep×0.30)
      learning_accelerator = 1 - (learning_velocity × 0.35)
      crt = raw_months × friction_multiplier × learning_accelerator
    """
    if gap <= 0:
        return 0.0

    raw = gap * inp.base_realization_time_months
    friction = 1.0 + (inp.governance_friction * 0.30) + \
                     (inp.execution_friction  * 0.40) + \
                     (inp.dependency_risk     * 0.30)
    accelerator = max(0.5, 1.0 - (inp.learning_velocity * 0.35))
    crt = raw * friction * accelerator

    # Adjust for low evidence confidence — widen estimate
    confidence_adj = 1.0 + ((1.0 - inp.evidence_confidence) * 0.20)
    return round(crt * confidence_adj, 1)


def classify_crt_risk(crt_months: float) -> CRTRiskLevel:
    """Classify CRT into risk bands."""
    if crt_months < 6:
        return "Low"
    elif crt_months < 18:
        return "Medium"
    elif crt_months < 36:
        return "High"
    return "Critical"


def identify_primary_bottleneck(inp: CRTInput) -> str:
    """Identify which friction source is most responsible for delay."""
    friction_map = {
        "Governance overhead": inp.governance_friction * 0.30,
        "Execution friction":  inp.execution_friction  * 0.40,
        "Dependency risk":     inp.dependency_risk     * 0.30,
        "Low learning velocity": (1.0 - inp.learning_velocity) * 0.20,
        "Low evidence confidence": (1.0 - inp.evidence_confidence) * 0.15,
    }
    return max(friction_map, key=friction_map.get)


def generate_plain_english_explanation(
    inp: CRTInput,
    gap: float,
    crt_months: float,
    risk: CRTRiskLevel,
    bottleneck: str,
) -> str:
    """Generate a plain-English explanation readable by non-technical users."""
    risk_desc = {
        "Low":      "This gap can be closed relatively quickly with focused effort.",
        "Medium":   "This will take meaningful time and sustained effort to close.",
        "High":     "This is a multi-year challenge requiring significant organizational investment.",
        "Critical": "At current adaptation velocity, this gap will not close without fundamental intervention.",
    }

    years = crt_months / 12
    time_str = f"approximately {crt_months:.0f} months" if crt_months < 18 else \
               f"approximately {years:.1f} years ({crt_months:.0f} months)"

    return (
        f"{inp.system_name} has an adaptation gap of {gap:.1f} points between "
        f"where it is today ({inp.current_capability_score:.1f}) and where it needs to be "
        f"({inp.required_capability_score:.1f}). "
        f"At current friction levels, closing this gap will take {time_str}. "
        f"Risk level: {risk}. "
        f"Primary bottleneck: {bottleneck}. "
        f"{risk_desc[risk]}"
    )


def calculate_crt(inp: CRTInput) -> CRTOutput:
    """
    Main entry point. Takes a CRTInput, returns a full CRTOutput.
    """
    gap = calculate_adaptation_gap(
        inp.required_capability_score,
        inp.current_capability_score
    )

    crt = estimate_crt_months(inp, gap)

    # Confidence range: ±20% adjusted by evidence quality
    uncertainty = 0.20 + ((1.0 - inp.evidence_confidence) * 0.15)
    low  = round(crt * (1.0 - uncertainty), 1)
    high = round(crt * (1.0 + uncertainty), 1)

    risk       = classify_crt_risk(crt)
    bottleneck = identify_primary_bottleneck(inp)
    gov_ready  = calculate_governance_readiness(
        inp.governance_friction,
        inp.objective_integrity_score,
        inp.evidence_confidence,
    )
    explanation = generate_plain_english_explanation(inp, gap, crt, risk, bottleneck)

    return CRTOutput(
        system_name=inp.system_name,
        use_case=inp.use_case,
        adaptation_gap=gap,
        crt_months=crt,
        crt_years=round(crt / 12, 2),
        crt_range_low_months=low,
        crt_range_high_months=high,
        crt_risk_level=risk,
        primary_bottleneck=bottleneck,
        governance_readiness_score=gov_ready,
        evidence_confidence_score=inp.evidence_confidence,
        plain_english_explanation=explanation,
    )
