"""
ASF Value Realization Engine
Measures how effectively AI investment converts to business value.

The core output:
"This system consumed X resources, generated Y outcomes, achieved Z value,
and its primary adaptation bottleneck is ______."
"""

from dataclasses import dataclass


@dataclass
class ValueRealizationInput:
    provider: str
    model: str
    monthly_spend_usd: float
    token_usage_millions: float
    users: int
    adoption_rate_pct: float
    hours_saved_monthly: float
    cost_avoidance_usd: float
    revenue_impact_usd: float
    hourly_rate_usd: float = 75.0


@dataclass
class ValueRealizationReport:
    input: ValueRealizationInput
    business_value_usd: float
    value_realization_ratio: float
    productivity_efficiency: float
    adoption_efficiency: float
    token_efficiency: float
    asf_value_score: float
    risk_band: str
    primary_friction: str
    primary_strength: str
    recommendation: str
    summary: str


def compute(inp: ValueRealizationInput) -> ValueRealizationReport:
    productivity_value = inp.hours_saved_monthly * inp.hourly_rate_usd
    business_value = inp.cost_avoidance_usd + inp.revenue_impact_usd + productivity_value

    value_realization_ratio = round(business_value / max(inp.monthly_spend_usd, 1), 2)
    productivity_efficiency = round(inp.hours_saved_monthly / max(inp.monthly_spend_usd, 1) * 1000, 2)
    adoption_efficiency     = round(inp.adoption_rate_pct / max(inp.monthly_spend_usd, 1), 6)
    token_efficiency        = round(business_value / max(inp.token_usage_millions, 1), 2)

    vrr_norm = min(value_realization_ratio / 20.0, 1.0)
    pe_norm  = min(productivity_efficiency / 30.0, 1.0)
    ae_norm  = min(adoption_efficiency * 10000, 1.0)
    te_norm  = min(token_efficiency / 50.0, 1.0)
    ar_norm  = inp.adoption_rate_pct / 100.0

    asf_score = round(
        (vrr_norm * 0.35 + pe_norm * 0.25 +
         ae_norm  * 0.15 + te_norm * 0.15 + ar_norm * 0.10) * 100, 1
    )

    risk_band = "Low" if asf_score >= 75 else ("Medium" if asf_score >= 55 else "High")

    scores = {
        "Value Realization Ratio": vrr_norm,
        "Productivity Efficiency": pe_norm,
        "Adoption Efficiency":     ae_norm,
        "Token Efficiency":        te_norm,
        "Adoption Rate":           ar_norm,
    }
    primary_strength = max(scores, key=scores.get)
    primary_friction = min(scores, key=scores.get)

    friction_map = {
        "Value Realization Ratio": "Low business value relative to spend — redefine success metrics",
        "Productivity Efficiency": "Low hours saved per dollar — expand use case coverage",
        "Adoption Efficiency":     "Low adoption relative to spend — reduce onboarding friction",
        "Token Efficiency":        "High token consumption per unit of value — optimize prompts",
        "Adoption Rate":           "Low user adoption — address skill gap and change management",
    }
    recommendation_map = {
        "Value Realization Ratio": "Define measurable business outcomes before scaling spend",
        "Productivity Efficiency": "Identify highest-leverage use cases and expand automation",
        "Adoption Efficiency":     "Implement guided onboarding and reduce time-to-first-value",
        "Token Efficiency":        "Implement prompt optimization, caching, and token budget controls",
        "Adoption Rate":           "Launch internal enablement program with clear success metrics",
    }

    summary = (
        f"{inp.provider} {inp.model} consumed ${inp.monthly_spend_usd:,}/month, "
        f"generated ${business_value:,.0f} in business value, "
        f"achieving a {value_realization_ratio:.1f}x value realization ratio. "
        f"ASF Value Score: {asf_score}/100 — {risk_band} risk. "
        f"Primary adaptation bottleneck: {friction_map[primary_friction]}"
    )

    return ValueRealizationReport(
        input=inp,
        business_value_usd=round(business_value, 2),
        value_realization_ratio=value_realization_ratio,
        productivity_efficiency=productivity_efficiency,
        adoption_efficiency=adoption_efficiency,
        token_efficiency=token_efficiency,
        asf_value_score=asf_score,
        risk_band=risk_band,
        primary_friction=friction_map[primary_friction],
        primary_strength=primary_strength,
        recommendation=recommendation_map[primary_friction],
        summary=summary,
    )
