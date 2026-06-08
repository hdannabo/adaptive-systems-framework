from ..models import AnalysisInput, LayerScores, Intervention, RiskBand

_DIMENSION_MAP = {
    "observation_latency": {
        "label": "Observation Latency",
        "friction": "Data / tooling gap",
        "actions": [
            ("Instrument observability pipelines (Prometheus, Grafana, Application Insights)", "P0", "low"),
            ("Build signal detection dashboards with automated alerting", "P1", "medium"),
            ("Define SLOs and create feedback dashboards for key signals", "P1", "medium"),
        ],
    },
    "decision_latency": {
        "label": "Decision Latency",
        "friction": "Governance / ownership ambiguity",
        "actions": [
            ("Publish RACI for all adaptation decisions — eliminate ownership ambiguity", "P0", "low"),
            ("Replace CAB review gates with automated compliance checks in pipeline", "P0", "high"),
            ("Implement time-boxed decision protocols with clear escalation paths", "P1", "medium"),
        ],
    },
    "execution_latency": {
        "label": "Execution Latency",
        "friction": "Manual dependency / legacy systems",
        "actions": [
            ("Automate top 3 manual handoffs blocking delivery pipeline", "P0", "high"),
            ("Build self-service platform patterns for common execution tasks", "P1", "high"),
            ("Containerize legacy workloads to reduce infrastructure dependency", "P1", "high"),
        ],
    },
    "feedback_delay": {
        "label": "Feedback Delay",
        "friction": "Missing observability / measurement gaps",
        "actions": [
            ("Add telemetry to all production systems — zero blind spots", "P0", "medium"),
            ("Implement real-time operational dashboards with automated anomaly detection", "P1", "medium"),
            ("Create feedback loop from outcomes back to input signal detection", "P1", "low"),
        ],
    },
    "dependency_index": {
        "label": "Dependency Index",
        "friction": "Manual approvals / coordination overhead",
        "actions": [
            ("Map and eliminate top 5 manual dependencies in the critical path", "P0", "medium"),
            ("Build policy-as-code guardrails to replace manual approval gates", "P1", "high"),
            ("Implement GitOps workflows to reduce coordination overhead", "P1", "medium"),
        ],
    },
    "learning_velocity": {
        "label": "Learning Velocity",
        "friction": "No postmortem culture / knowledge silos",
        "actions": [
            ("Mandate blameless postmortems — every incident drives a runbook update", "P0", "low"),
            ("Build institutional knowledge base from operational learnings", "P1", "medium"),
            ("Implement feedback loops from measured outcomes back to operating procedures", "P1", "low"),
        ],
    },
}


def _bottleneck(scores: LayerScores) -> str:
    dims = {
        "observation_latency": scores.observation_latency,
        "decision_latency":    scores.decision_latency,
        "execution_latency":   scores.execution_latency,
        "feedback_delay":      scores.feedback_delay,
        "dependency_index":    scores.dependency_index,
    }
    lv_gap = 5.0 - scores.learning_velocity
    dims["learning_velocity"] = lv_gap
    return max(dims, key=dims.get)


def _primary_friction(scores: LayerScores) -> str:
    bottleneck = _bottleneck(scores)
    return _DIMENSION_MAP[bottleneck]["friction"]


def recommend(
    input: AnalysisInput,
    scores: LayerScores,
    top_n: int = 5,
) -> list[Intervention]:
    dims = {
        "observation_latency": scores.observation_latency,
        "decision_latency":    scores.decision_latency,
        "execution_latency":   scores.execution_latency,
        "feedback_delay":      scores.feedback_delay,
        "dependency_index":    scores.dependency_index,
        "learning_velocity":   5.0 - scores.learning_velocity,
    }

    ranked = sorted(dims.items(), key=lambda x: -x[1])

    interventions: list[Intervention] = []
    for dim_key, dim_score in ranked:
        if dim_score < 2.5:
            continue
        entry = _DIMENSION_MAP[dim_key]
        for action, priority, effort in entry["actions"]:
            reduction = max(1, int((dim_score - 1) * 1.5))
            interventions.append(Intervention(
                priority=priority,
                action=action,
                target_dimension=entry["label"],
                friction_type=entry["friction"],
                expected_reduction_weeks=reduction,
                effort=effort,
            ))
        if len(interventions) >= top_n:
            break

    interventions.sort(key=lambda x: (x.priority, -x.expected_reduction_weeks))
    
    # Always return at least one intervention — from the worst dimension
    if not interventions:
        worst = sorted(dims.items(), key=lambda x: -x[1])[0][0]
        entry = _DIMENSION_MAP[worst]
        for action, priority, effort in entry["actions"][:1]:
            reduction = max(1, int((dims[worst]) * 1.5))
            interventions.append(Intervention(
                priority=priority,
                action=action,
                target_dimension=entry["label"],
                friction_type=entry["friction"],
                expected_reduction_weeks=reduction,
                effort=effort,
            ))
    
    return interventions[:top_n]


def summarize(input: AnalysisInput, scores: LayerScores) -> str:
    """
    Produce a CEO-grade summary.

    Simon's standard:
      BAD:  "HIGH risk system. Adaptation latency score 4.0/5.0."
      GOOD: "This program is likely to miss its target by 18 months
             because Execution Latency is the critical bottleneck."
    """
    risk = scores.risk_band.value
    score = scores.adaptation_latency_score
    bottleneck = _bottleneck(scores)
    friction = _primary_friction(scores)
    label = _DIMENSION_MAP[bottleneck]["label"]

    # Estimate miss timeline from score
    # ALS 3.5–4.0 → ~12–18 months behind
    # ALS 4.0–4.5 → ~18–24 months behind
    # ALS 4.5–5.0 → 24+ months behind
    # ALS 2.5–3.5 → 6–12 months at risk
    if score >= 4.5:
        delay = "likely to miss its target by 24 months or more"
        urgency = "Fundamental restructuring required before further investment."
    elif score >= 4.0:
        delay = "at risk of missing its target by 18–24 months"
        urgency = "Immediate executive intervention required."
    elif score >= 3.5:
        delay = "at risk of missing its target by 12–18 months"
        urgency = "Targeted intervention required this quarter."
    elif score >= 3.0:
        delay = "at risk of missing its target by 6–12 months"
        urgency = "Address the primary bottleneck within 90 days."
    elif score >= 2.5:
        delay = "slightly behind the required adaptation velocity"
        urgency = "Monitor and address friction before it compounds."
    else:
        delay = "adapting at or above the required velocity"
        urgency = "Maintain current trajectory."

    # What executives don't know — the non-obvious insight
    friction_insight = {
        "execution_latency": (
            f"The constraint is not capability or budget — "
            f"it is the speed of implementation. "
            f"Manual dependencies and legacy systems are consuming adaptation time "
            f"that cannot be recovered."
        ),
        "decision_latency": (
            f"The constraint is governance, not execution. "
            f"Approval cycles and ownership ambiguity are adding weeks to every decision. "
            f"The organization can build faster than it can decide."
        ),
        "feedback_delay": (
            f"The constraint is measurement, not implementation. "
            f"Without real-time outcome visibility, the organization is making "
            f"decisions without knowing whether previous decisions worked."
        ),
        "observation_latency": (
            f"The constraint is signal detection, not response. "
            f"By the time problems are visible, the adaptation window has narrowed."
        ),
        "dependency_index": (
            f"The constraint is coordination overhead. "
            f"Every change requires too many approvals and handoffs. "
            f"Each dependency multiplies delay."
        ),
        "learning_velocity": (
            f"The constraint is organizational learning. "
            f"The same friction patterns are recurring without structural improvement."
        ),
    }

    insight = friction_insight.get(bottleneck, "")

    return (
        f"This {input.system_type or 'program'} is {delay} "
        f"because {label} is the critical bottleneck. "
        f"{insight} "
        f"{urgency}"
    )


def bottleneck_dimension(scores: LayerScores) -> str:
    return _DIMENSION_MAP[_bottleneck(scores)]["label"]


def primary_friction(scores: LayerScores) -> str:
    return _primary_friction(scores)
