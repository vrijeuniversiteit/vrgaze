from dataclasses import dataclass, field
from typing import List, Union

from vrgaze.tennis.models.abstraction import Visitable
from vrgaze.tennis.services.writer import CSVWriter


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


@dataclass
class Trial(Visitable):
	participant_id: int
	test_id: int
	block_number: int
	ball_number: int
	frames: List[Frame]
	ball_events: List["Event"] = field(default_factory=list)
	gaze_events: List["Event"] = field(default_factory=list)

	def analyze(self, visitor: "Visitor"):
		visitor.visit(self)


@dataclass
class Participant(Visitable):
	participant_id: int
	trials: List[Trial]

	def analyze(self, visitor: "Visitor"):
		for trial in self.trials:
			trial.analyze(visitor)


@dataclass
class ConditionData(Visitable):
	name: str
	participants: List[Participant]

	def analyze(self, visitor: "Visitor"):
		for participant in self.participants:
			participant.analyze(visitor)

	def __repr__(self):
		return f"Name={self.name}, Participants={len(self.participants)})"


@dataclass
class ExperimentalData(Visitable):
	conditions: List[ConditionData]

	def analyze(self, visitor: "Visitor"):
		for condition in self.conditions:
			condition.analyze(visitor)

	def __init__(self, data: Union[List[ConditionData], ConditionData]):
		if isinstance(data, list):
			self.conditions = data
		else:
			self.conditions = [data]

	def to_csv(self, filepath: str):
		data = []
		for condition in self.conditions:
			exporter = CSVWriter(condition.name)
			condition.analyze(exporter)
			data.extend(exporter.data)

		import csv
		with open(filepath, 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			for row in data:
				writer.writerow(row)


@dataclass
class Trajectory:
	length: List[float]
	height: List[float]
	width: List[float]
