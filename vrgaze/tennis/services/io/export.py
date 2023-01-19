import csv
import dataclasses
import math
from dataclasses import field, dataclass
from typing import List, Optional

from vrgaze.tennis.models.common import Visitable, Visitor
from vrgaze.tennis.models.balleventmodels import FirstBounceEvent, BallHitFrontWall, SecondBounceEvent
from vrgaze.tennis.models.gazeeventmodels import PredictiveSaccade


@dataclass
class TrialExportData:
	Condition: str
	Participant: str
	BallNumber: str
	BlockNumber: str
	TestID: str
	IsValid: bool
	FirstBounceTimestamp: Optional[float]
	FirstBouncePositionX: Optional[float]
	FirstBouncePositionY: Optional[float]
	FirstBouncePositionZ: Optional[float]
	BallLandingPositionX: Optional[float]
	BallLandingPositionY: Optional[float]
	BallLandingPositionZ: Optional[float]
	BallDistanceToTarget: Optional[float]
	SaccadeTimestamp: Optional[float]
	SaccadeAngleAmplitude: Optional[float]
	AngleBallToGazeAtSaccadeStart: Optional[float]
	AngleBallToGazeAtSaccadeEnd: Optional[float]


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

		first_bounce = [event for event in trial.ball_events if isinstance(event, FirstBounceEvent)]

		if len(first_bounce) == 0:
			print("No first bounce event found for trial")
			return

		first_bounce = first_bounce[0]

		second_bounces = [event for event in trial.ball_events if isinstance(event, SecondBounceEvent)]

		if len(second_bounces) == 0:
			second_bounce = None
		else:
			second_bounce = second_bounces[0]

		is_trial_valid = True
		hit_front_wall = [event for event in trial.ball_events if isinstance(event, BallHitFrontWall)]
		if len(hit_front_wall) > 0:
			hit_front_wall_timestamp = hit_front_wall[0].timestamp_start
			if second_bounce != None:
				if second_bounce.timestamp_start > hit_front_wall_timestamp:
					is_trial_valid = False

		predictive_saccade_of_interest = [sac for sac in predictive_saccades if sac.is_within_bounce_window]

		if trial.result_location_x == None:
			result_x = None
			result_y = None
			result_z = None
			ball_distance_to_target = None
		else:
			result_x = f"{trial.result_location_x:.3f}"
			result_y = f"{trial.result_location_y:.3f}"
			result_z = f"{trial.result_location_z:.3f}"
			ball_distance_to_target = f"{trial.distance_to_closest_target:.3f}"

		if len(predictive_saccade_of_interest) == 0:
			trial_export_data = TrialExportData(
				Condition=condition,
				Participant=participant,
				BallNumber=ball_number,
				BlockNumber=block_number,
				TestID=test_id,
				IsValid=False,
				FirstBounceTimestamp=f"{first_bounce.timestamp_start:.3f}",
				FirstBouncePositionX=f"{first_bounce.frame.ball_position_x:.3f}",
				FirstBouncePositionY=f"{first_bounce.frame.ball_position_y:.3f}",
				FirstBouncePositionZ=f"{first_bounce.frame.ball_position_z:.3f}",
				BallLandingPositionX=result_x,
				BallLandingPositionY=result_y,
				BallLandingPositionZ=result_z,
				BallDistanceToTarget=ball_distance_to_target,
				SaccadeTimestamp=None,
				SaccadeAngleAmplitude=None,
				AngleBallToGazeAtSaccadeStart=None,
				AngleBallToGazeAtSaccadeEnd=None,

			)
		else:
			saccade = predictive_saccade_of_interest[-1]
			trial_export_data = TrialExportData(
				Condition=condition,
				Participant=participant,
				BallNumber=ball_number,
				BlockNumber=block_number,
				TestID=test_id,
				IsValid=is_trial_valid,
				FirstBounceTimestamp=f"{first_bounce.timestamp_start:.3f}",
				FirstBouncePositionX=f"{first_bounce.frame.ball_position_x:.3f}",
				FirstBouncePositionY=f"{first_bounce.frame.ball_position_y:.3f}",
				FirstBouncePositionZ=f"{first_bounce.frame.ball_position_z:.3f}",
				BallLandingPositionX=result_x,
				BallLandingPositionY=result_y,
				BallLandingPositionZ=result_z,
				BallDistanceToTarget=ball_distance_to_target,
				SaccadeTimestamp=f"{saccade.timestamp_start:.3f}",
				SaccadeAngleAmplitude=f"{saccade.angle_amplitude:.3f}",
				AngleBallToGazeAtSaccadeStart=f"{saccade.angle_start:.3f}",
				AngleBallToGazeAtSaccadeEnd=f"{saccade.angle_end:.3f}",
			)

		self.data.append(trial_export_data)

	def visit_condition(self, condition: Visitable, condition_name: str):
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
