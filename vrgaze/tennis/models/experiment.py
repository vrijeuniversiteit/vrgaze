from dataclasses import dataclass
from typing import List, Union

from vrgaze.tennis import BallEvents, GazeEvents
from vrgaze.tennis.models.common import Visitable
from vrgaze.tennis.models.datamodel import Condition
from vrgaze.tennis.services.io.export import CSVWriter
from vrgaze.tennis.services.processing.preprocess import Preprocess


@dataclass
class ExperimentalData(Visitable):
	conditions: List[Condition]

	def __init__(self, data: Union[List[Condition], Condition]):
		if isinstance(data, list):
			self.conditions = data
		else:
			self.conditions = [data]

	def process(self, visitor: "Visitor"):
		for condition in self.conditions:
			condition.process(visitor)

	def analyze_trials(self):
		visitors = [
			Preprocess(),
			BallEvents(),
			GazeEvents()
		]

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
			>>> data.analyze_trials()
			>>> data.to_csv("example_results.csv")

			# Understanding the data
			FirstBounceTimestamp,FirstBouncePositionX,FirstBouncePositionY,FirstBouncePositionZ,SaccadeTimestamp,SaccadeAngleAmplitude,AngleBallToGazeAtSaccadeStart,AngleBallToGazeAtSaccadeEnd,BallLandingPositionX,BallLandingPositionY,BallLandingPositionZ,BallDistanceToTarget

			>>> "Condition": The name of the condition given when the data is loaded
			>>> "Participant": The participant ID
			>>> "BallNumber": The current ball number
			>>> "BlockNumber": The current block number
			>>> "TestID": The current test number
			>>> "IsValid": Whether the trial is valid or not. A trial is not valid if the ball is not returned or if
			the ball hits the front wall before the second bounce.
			>>> FirstBounceTimestamp: The timestamp of the first bounce
			>>> FirstBouncePositionX: The X position of the first bounce
			>>> FirstBouncePositionY: The Y position of the first bounce
			>>> FirstBouncePositionZ: The Z position of the first bounce
			>>> SaccadeTimestamp: The timestamp of the predictive saccade
			>>> SaccadeAngleAmplitude: The angle amplitude of the predictive saccade [degrees]
			>>> AngleBallToGazeAtSaccadeStart: The angle between the ball and the gaze direction at the start of the predictive saccade [degrees]
			>>> AngleBallToGazeAtSaccadeEnd: The angle between the ball and the gaze direction at the end of the predictive saccade [degrees]
			>>> BallLandingPositionX: The X position of the ball at the end of the predictive saccade
			>>> BallLandingPositionY: The Y position of the ball at the end of the predictive saccade
			>>> BallLandingPositionZ: The Z position of the ball at the end of the predictive saccade
			>>> BallDistanceToTarget: The distance between the ball and the target at the end of the predictive saccade
		"""

		writer = CSVWriter()
		for condition in self.conditions:
			writer.visit_condition(condition, condition.name)
		writer.save(filepath)
