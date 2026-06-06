from ..models import AnalysisInput, LayerScores


def score(input: AnalysisInput) -> LayerScores:
    return LayerScores(
        observation_latency=float(input.observation_latency),
        decision_latency=float(input.decision_latency),
        execution_latency=float(input.execution_latency),
        feedback_delay=float(input.feedback_delay),
        learning_velocity=float(input.learning_velocity),
        dependency_index=float(input.dependency_index),
    )
