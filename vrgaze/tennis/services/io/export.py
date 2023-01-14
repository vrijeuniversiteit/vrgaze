import csv
import dataclasses
from dataclasses import field, dataclass
from typing import List

from vrgaze.tennis.models.abstraction import Visitable, Visitor
from vrgaze.tennis.models.eventmodel import PredictiveSaccade, FirstBounceEvent, BallHitFrontWall, SecondBounceEvent


@dataclass
class TrialExportData:
	Condition: str
	Participant: str
	BallNumber: str
	BlockNumber: str
	TestID: str
	IsValid: bool
	SaccadeTimestamp: float
	SaccadeAngleAmplitude: float
	AngleBallToGazeAtSaccadeStart: float
	AngleBallToGazeAtSaccadeEnd: float
	BallLandingPositionX: float
	BallLandingPositionY: float
	BallLandingPositionZ: float
	BallDistanceToTarget: float


@dataclass
class CSVWriter(Visitor):
	condition: str = field(init=False)
	data: List[TrialExportData] = field(default_factory=list)

	def visit(self, trial: Visitable):
		participant = trial.participant_id
		ball_number = trial.ball_number
		block_number = trial.block_number
		test_id = trial.test_id
		predictive_saccades = [event for event in trial.gaze_events if isinstance(event, PredictiveSaccade)]
		condition = self.condition

		# TODO Export the three below:
		first_bounce_timestamp = [event for event in trial.ball_events if isinstance(event, FirstBounceEvent)][
			0].timestamp
		second_bounce_timestamp = [event for event in trial.ball_events if isinstance(event, SecondBounceEvent)][
			0].timestamp

		is_trial_valid = True
		hit_front_wall = [event for event in trial.ball_events if isinstance(event, BallHitFrontWall)]
		if len(hit_front_wall) > 0:
			hit_front_wall_timestamp = hit_front_wall[0].timestamp
			if second_bounce_timestamp > hit_front_wall_timestamp:
				is_trial_valid = False

		if len(predictive_saccades) == 0:
			trial_export_data = TrialExportData(
				condition,
				participant,
				ball_number,
				block_number,
				test_id,
				False,
				None,
				None,
				None,
				None,
				None,
				None,
				None,
				None,
			)
		else:
			saccade = predictive_saccades[-1]
			trial_export_data = TrialExportData(
				condition,
				participant,
				ball_number,
				block_number,
				test_id,
				is_trial_valid,
				f"{saccade.timestamp:.3f}",
				f"{saccade.angle_amplitude:.3f}",
				f"{saccade.angle_start:.3f}",
				f"{saccade.angle_end:.3f}",
				f"{trial.result_location_x:.3f}",
				f"{trial.result_location_y:.3f}",
				f"{trial.result_location_z:.3f}",
				f"{trial.distance_to_closest_target:.3f}"
			)

		self.data.append(trial_export_data)

	def visit_with_context(self, condition: Visitable, condition_name: str):
		self.condition = condition_name
		condition.process(self)

	def save(self, filepath):
		dict_data = []
		for data_point in self.data:
			dict_data.append(dataclasses.asdict(data_point))

		with open(filepath, 'w', newline='') as csvfile:
			fieldnames = list(dict_data[0].keys())
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			for row in dict_data:
				writer.writerow(row)