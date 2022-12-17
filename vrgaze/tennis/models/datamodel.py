from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Union


class Visitable(ABC):
	@abstractmethod
	def detect(self, visitor: "Visitor"):
		...


class Visitor(ABC):
	@abstractmethod
	def visit(self, visitable: Visitable):
		...


@dataclass
class Frame:
	timestamp: float
	ball_position_x: float
	ball_position_y: float
	ball_position_z: float


@dataclass
class Trial(Visitable):
	participant_id: int
	test_id: int
	block_number: int
	ball_number: int
	frames: List[Frame]

	def detect(self, visitor: "Visitor"):
		visitor.visit(self)


@dataclass
class Participant(Visitable):
	participant_id: int
	trials: List[Trial]

	def detect(self, visitor: "Visitor"):
		for trial in self.trials:
			trial.detect(visitor)


@dataclass
class ConditionData(Visitable):
	name: str
	participants: List[Participant]

	def detect(self, visitor: "Visitor"):
		for participant in self.participants:
			participant.detect(visitor)

	def __repr__(self):
		return f"Name={self.name}, Participants={len(self.participants)})"


@dataclass
class ExperimentalData(Visitable):
	conditions: List[ConditionData]

	def detect(self, visitor: "Visitor"):
		for condition in self.conditions:
			condition.detect(visitor)

	def __init__(self, data: Union[List[ConditionData], ConditionData]):
		if isinstance(data, list):
			self.conditions = data
		else:
			self.conditions = [data]
