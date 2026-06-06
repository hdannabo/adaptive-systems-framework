from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class RiskBand(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class FrictionType(str, Enum):
    TECHNICAL = "technical"
    ORGANIZATIONAL = "organizational"
    HUMAN = "human"
    GOVERNANCE = "governance"
    DATA = "data"


@dataclass
class FrictionSource:
    name: str
    type: FrictionType
    present: bool = False
    severity: int = 0          # 1–5
    estimated_delay_weeks: int = 0
    description: str = ""


@dataclass
class AnalysisInput:
    system_name: str
    domain: str
    system_type: str
    adaptation_scenario: str
    input_event: str
    adaptation_requirement: str
    current_operating_state: str

    observation_latency: int = 3       # 1–5
    decision_latency: int = 3
    execution_latency: int = 3
    feedback_delay: int = 3
    learning_velocity: int = 3
    dependency_index: int = 3

    friction_sources: list[FrictionSource] = field(default_factory=list)
    control_layer_present: bool = False
    notes: str = ""


@dataclass
class LayerScores:
    observation_latency: float
    decision_latency: float
    execution_latency: float
    feedback_delay: float
    learning_velocity: float
    dependency_index: float

    @property
    def adaptation_latency_score(self) -> float:
        return round(
            (self.observation_latency * 0.15)
            + (self.decision_latency   * 0.25)
            + (self.execution_latency  * 0.30)
            + (self.feedback_delay     * 0.15)
            + (self.dependency_index   * 0.15)
            - (self.learning_velocity  * 0.10),
            2
        )

    @property
    def risk_band(self) -> RiskBand:
        s = self.adaptation_latency_score
        if s < 2.5:
            return RiskBand.LOW
        elif s < 3.5:
            return RiskBand.MEDIUM
        return RiskBand.HIGH

    @property
    def friction_score(self) -> float:
        bottleneck = max(
            self.observation_latency,
            self.decision_latency,
            self.execution_latency,
            self.feedback_delay,
            self.dependency_index,
        )
        avg = (
            self.observation_latency
            + self.decision_latency
            + self.execution_latency
            + self.feedback_delay
            + self.dependency_index
        ) / 5
        return round((bottleneck * 0.5) + (avg * 0.5), 2)

    @property
    def adaptation_capability(self) -> float:
        return round(6.0 - self.adaptation_latency_score, 2)


@dataclass
class Intervention:
    priority: str          # P0 / P1 / P2
    action: str
    target_dimension: str
    friction_type: str
    expected_reduction_weeks: int
    effort: str            # low / medium / high


@dataclass
class ASFReport:
    input: AnalysisInput
    scores: LayerScores
    primary_friction: str
    bottleneck_dimension: str
    interventions: list[Intervention]
    summary: str
