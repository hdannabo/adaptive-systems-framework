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
    risk = scores.risk_band.value
    score = scores.adaptation_latency_score
    bottleneck = _bottleneck(scores)
    friction = _primary_friction(scores)
    label = _DIMENSION_MAP[bottleneck]["label"]

    lines = [
        f"{input.system_name} is a {risk.upper()} risk system with an adaptation latency score of {score}/5.0.",
        f"Primary bottleneck: {label} — driven by {friction}.",
    ]

    if scores.risk_band == RiskBand.HIGH:
        lines.append("Immediate systemic intervention required to reduce adaptation latency.")
    elif scores.risk_band == RiskBand.MEDIUM:
        lines.append("Targeted interventions recommended. Monitor adaptation rate quarterly.")
    else:
        lines.append("System is adapting well. Maintain current trajectory and learning velocity.")

    return " ".join(lines)


def bottleneck_dimension(scores: LayerScores) -> str:
    return _DIMENSION_MAP[_bottleneck(scores)]["label"]


def primary_friction(scores: LayerScores) -> str:
    return _primary_friction(scores)
