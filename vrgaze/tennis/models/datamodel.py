from dataclasses import dataclass, field
from typing import List

from vrgaze.tennis.models.abstraction import Visitable


@dataclass
class Frame:
	timestamp: float
	ball_position_x: float
	ball_position_y: float
	ball_position_z: float
	head_position_x: float
	head_position_y: float
	head_position_z: float
	gaze_origin_x: float
	gaze_origin_y: float
	gaze_origin_z: float
	gaze_direction_x: float
	gaze_direction_y: float
	gaze_direction_z: float
	gaze_is_valid: bool


@dataclass
class Trial(Visitable):
	participant_id: int
	test_id: int
	block_number: int
	ball_number: int
	result_location_x: float
	result_location_y: float
	result_location_z: float
	distance_to_closest_target: float
	frames: List[Frame]
	ball_events: List["Event"] = field(default_factory=list)
	gaze_events: List["Event"] = field(default_factory=list)

	def process(self, visitor: "Visitor"):
		visitor.visit(self)


@dataclass
class Participant(Visitable):
	participant_id: int
	trials: List[Trial]

	def process(self, visitor: "Visitor"):
		for trial in self.trials:
			trial.process(visitor)


@dataclass
class ConditionData(Visitable):
	name: str
	participants: List[Participant]

	def process(self, visitor: "Visitor"):
		for participant in self.participants:
			participant.process(visitor)

	def __repr__(self):
		return f"Name={self.name}, Participants={len(self.participants)})"


@dataclass
class Trajectory:
	length: List[float]
	height: List[float]
	width: List[float]
