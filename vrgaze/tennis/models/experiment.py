from dataclasses import dataclass
from typing import List, Union

from vrgaze.tennis import BallEvents, GazeEvents
from vrgaze.tennis.models.abstraction import Visitable
from vrgaze.tennis.models.datamodel import ConditionData
from vrgaze.tennis.services.export import CSVWriter
from vrgaze.tennis.services.preprocess import Preprocessor


@dataclass
class ExperimentalData(Visitable):
	conditions: List[ConditionData]

	def __init__(self, data: Union[List[ConditionData], ConditionData]):
		if isinstance(data, list):
			self.conditions = data
		else:
			self.conditions = [data]

	def process(self, visitor: "Visitor"):
		for condition in self.conditions:
			condition.process(visitor)

	def analyze_trials(self):
		visitors = [Preprocessor(), BallEvents(), GazeEvents()]

		for visitor in visitors:
			for condition in self.conditions:
				condition.process(visitor)

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
			>>> data.process(BallEvents())
			>>> data.process(GazeEvents())
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

		visitor = CSVWriter()
		for condition in self.conditions:
			visitor.visit_with_context(condition, condition.name)
		visitor.save(filepath)
