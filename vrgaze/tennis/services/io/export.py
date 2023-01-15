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
	FirstBounceTimestamp: float
	FirstBouncePositionX: float
	FirstBouncePositionY: float
	FirstBouncePositionZ: float
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

		first_bounce = [event for event in trial.ball_events if isinstance(event, FirstBounceEvent)][0]

		second_bounces = [event for event in trial.ball_events if isinstance(event, SecondBounceEvent)]

		if len(second_bounces) == 0:
			second_bounce = None

		is_trial_valid = True
		hit_front_wall = [event for event in trial.ball_events if isinstance(event, BallHitFrontWall)]
		if len(hit_front_wall) > 0:
			hit_front_wall_timestamp = hit_front_wall[0].timestamp
			if (second_bounce != None) & (second_bounce.timestamp > hit_front_wall_timestamp):
				is_trial_valid = False

		if len(predictive_saccades) == 0:
			trial_export_data = TrialExportData(
				Condition=condition,
				Participant=participant,
				BallNumber=ball_number,
				BlockNumber=block_number,
				TestID=test_id,
				IsValid=False,
				FirstBounceTimestamp=f"{first_bounce.timestamp:.3f}",
				FirstBouncePositionX=f"{first_bounce.frame.ball_position_x:.3f}",
				FirstBouncePositionY=f"{first_bounce.frame.ball_position_y:.3f}",
				FirstBouncePositionZ=f"{first_bounce.frame.ball_position_z:.3f}",
				SaccadeTimestamp=None,
				SaccadeAngleAmplitude=None,
				AngleBallToGazeAtSaccadeStart=None,
				AngleBallToGazeAtSaccadeEnd=None,
				BallLandingPositionX=None,
				BallLandingPositionY=None,
				BallLandingPositionZ=None,
				BallDistanceToTarget=None,
			)
		else:
			saccade = predictive_saccades[-1]
			trial_export_data = TrialExportData(
				Condition=condition,
				Participant=participant,
				BallNumber=ball_number,
				BlockNumber=block_number,
				TestID=test_id,
				IsValid=is_trial_valid,
				FirstBounceTimestamp=f"{first_bounce.timestamp:.3f}",
				FirstBouncePositionX=f"{first_bounce.frame.ball_position_x:.3f}",
				FirstBouncePositionY=f"{first_bounce.frame.ball_position_y:.3f}",
				FirstBouncePositionZ=f"{first_bounce.frame.ball_position_z:.3f}",
				SaccadeTimestamp=f"{saccade.timestamp:.3f}",
				SaccadeAngleAmplitude=f"{saccade.angle_amplitude:.3f}",
				AngleBallToGazeAtSaccadeStart=f"{saccade.angle_start:.3f}",
				AngleBallToGazeAtSaccadeEnd=f"{saccade.angle_end:.3f}",
				BallLandingPositionX=f"{trial.result_location_x:.3f}",
				BallLandingPositionY=f"{trial.result_location_y:.3f}",
				BallLandingPositionZ=f"{trial.result_location_z:.3f}",
				BallDistanceToTarget=f"{trial.distance_to_closest_target:.3f}"
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
