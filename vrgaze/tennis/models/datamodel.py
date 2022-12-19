import csv
from dataclasses import dataclass, field
from typing import List, Union

from vrgaze.tennis.models.abstraction import Visitable
from vrgaze.tennis.services.export import CSVWriter


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
	result_location_x: float
	result_location_y: float
	result_location_z: float
	distance_to_closest_target: float
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

	def to_csv(self, filepath: str) -> None:
		"""Export gaze data to a CSV file.

		Args:
			filepath (str): File path to save the results

		Examples:
			# Exporting data
			>>> experts = load_condition("Experts", "example_data/tennis_data/experimental_condition")
			>>> novices = load_condition("Novices", "example_data/tennis_data/experimental_condition")
			>>>
			>>> data = ExperimentalData([experts, novices])
			>>> data.analyze(BallEvents())
			>>> data.analyze(GazeEvents())
			>>>
			>>> data.to_csv("example_results.csv")

			# Understanding the data
			>>> "Condition": The name of the condition given when the data is loaded
			>>> "Participant": The participant ID
			>>> "Ball Number": The current ball number
			>>> "Block Number": The current block number
			>>> "Test": The current test number
			>>> "Timestamp": The timestamp of the predictive saccade
			>>> "Saccade Angle Amplitude": The angle amplitude of the predictive saccade [degrees]
			>>> "Angle Ball-Gaze Start": The angle between the ball and the gaze direction at the start of the predictive saccade [degrees]
			>>> "Angle Ball-Gaze End": The angle between the ball and the gaze direction at the end of the predictive saccade [degrees]
			>>> "Result X": The x-coordinate of the ball's final position when hitting the ground
			>>> "Result Y": The y-coordinate of the ball's final position when hitting the ground
			>>> "Result Z": The z-coordinate of the ball's final position when hitting the ground
			>>> "Distance To Target": The distance between the ball's final position and the closest target [meters]

		"""

		data = []
		for condition in self.conditions:
			exporter = CSVWriter(condition.name)
			condition.analyze(exporter)
			data.extend(exporter.data)

		with open(filepath, 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')

			# write header
			writer.writerow(
				[
					"Condition",
					"Participant",
					"Ball Number",
					"Block Number",
					"Test",
					"Timestamp",
					"Saccade Angle Amplitude",
					"Angle Ball-Gaze Start",
					"Angle Ball-Gaze End",
					"Result X",
					"Result Y",
					"Result Z",
					"Distance To Target"
				]
			)

			for row in data:
				writer.writerow(row)


@dataclass
class Trajectory:
	length: List[float]
	height: List[float]
	width: List[float]
