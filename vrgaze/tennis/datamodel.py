from dataclasses import dataclass
from typing import List, Union


@dataclass
class Frame:
	timestamp: float
	ball_position_x: float
	ball_position_y: float
	ball_position_z: float



@dataclass
class Trial:
	participant_id: int
	test_id: int
	block_number: int
	ball_number: int
	frames: List[Frame]


@dataclass
class Participant:
	participant_id: int
	trials: List[Trial]


@dataclass
class ConditionData:
	name: str
	participants: List[Participant]

	def __repr__(self):
		return f"Name={self.name}, Participants={len(self.participants)})"


@dataclass
class ExperimentalData:
	conditions: List[ConditionData]

	def __init__(self, data: Union[List[ConditionData], ConditionData]):
		if isinstance(data, list):
			self.conditions = data
		else:
			self.conditions = [data]

