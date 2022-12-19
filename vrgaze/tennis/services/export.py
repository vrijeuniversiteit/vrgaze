import csv
from dataclasses import field, dataclass
from typing import List

from vrgaze.tennis.models.abstraction import Visitable, Visitor
from vrgaze.tennis.models.eventmodel import PredictiveSaccade


@dataclass
class CSVWriter(Visitor):
	condition: str = field(init=False)
	data: List[str] = field(default_factory=list)

	def visit(self, trial: Visitable):
		participant = trial.participant_id
		ball_number = trial.ball_number
		block_number = trial.block_number
		test_id = trial.test_id
		predictive_saccades = [event for event in trial.gaze_events if isinstance(event, PredictiveSaccade)]
		condition = self.condition

		for saccade in predictive_saccades:
			self.data.append(
				[
					condition,
					participant,
					ball_number,
					block_number,
					test_id,
					f"{saccade.timestamp:.3f}",
					f"{saccade.angle_amplitude:.3f}",
					f"{saccade.angle_start:.3f}",
					f"{saccade.angle_end:.3f}",
					f"{trial.result_location_x:.3f}",
					f"{trial.result_location_y:.3f}",
					f"{trial.result_location_z:.3f}",
					f"{trial.distance_to_closest_target:.3f}",
				]
			)

	def visit_with_context(self, trial: Visitable, condition_name: str):
		self.condition = condition_name
		trial.analyze(self)

	def save(self, filepath):
		with open(filepath, 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
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

			for row in self.data:
				writer.writerow(row)
