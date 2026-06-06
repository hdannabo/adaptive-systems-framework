from .models import AnalysisInput, ASFReport
from .scoring.engine import score
from .recommendations.engine import (
    recommend,
    summarize,
    bottleneck_dimension,
    primary_friction,
)


def analyze(input: AnalysisInput, top_interventions: int = 5) -> ASFReport:
    scores = score(input)
    interventions = recommend(input, scores, top_n=top_interventions)

    return ASFReport(
        input=input,
        scores=scores,
        primary_friction=primary_friction(scores),
        bottleneck_dimension=bottleneck_dimension(scores),
        interventions=interventions,
        summary=summarize(input, scores),
    )
