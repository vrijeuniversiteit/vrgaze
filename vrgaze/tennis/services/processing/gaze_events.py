from dataclasses import dataclass, field
from enum import Enum
from typing import List

from tests.tennis.processing.time_of_saccade import Timing
from vrgaze.tennis.models.balleventmodels import FirstBounceEvent
from vrgaze.tennis.models.common import Visitor, Event
from vrgaze.tennis.models.datamodel import Trial, Condition
from vrgaze.tennis.models.gazeeventmodels import CorrectiveSaccade, PredictiveSaccade, SaccadeCandidate
from vrgaze.tennis.services.processing.angles import Angles
from vrgaze.tennis.services.processing.integration import Integration
from vrgaze.tennis.services.processing.saccade_detector import SaccadeDetector


class GazeEvents(Visitor):
	def visit_condition(self, condition: Condition, condition_name: str):
		self.visit(condition)

	def visit(self, trial: Trial):
		trial = trial
		calculator = GazeEventCalculator(trial)
		calculator.calculate_saccades()
		trial.gaze_events = calculator.events


class THRESHOLD(Enum):
	REQUIRED_GAZE_SPEED_FACTOR = 5  # Gaze needs to move 5x faster than the median gaze speed
	MINIMUM_SACCADE_ANGLE_AMPLITUDE_DEGREE = 1  # Minimum angle amplitude of a saccade. If smaller, the saccade is ignored
	MINIMUM_SPEED_FASTER_THAN_BALL_PCT = 0.2  # Gaze needs to be at least 20% faster than the ball
	MAXIMUM_TIME_WINDOW_START_BEFORE_BOUNCE_SECONDS = 0.4  # Tag whether the saccade started within 400ms before the ball bounce


@dataclass
class GazeEventCalculator:
	trial: Trial
	events: List[Event] = field(default_factory=list)

	def calculate_saccades(self):
		frames = self.trial.frames
		world_gaze_angle = [Angles.calculate_gaze_world_angle(frame.gaze_direction_y, frame.gaze_direction_z) for frame
							in frames]
		ball_gaze_angle = [Angles.calculate_ball_gaze_angle(
			frame.ball_position_y,
			frame.ball_position_z,
			frame.gaze_direction_y,
			frame.gaze_direction_z,
			frame.gaze_origin_y,
			frame.gaze_origin_z
		) for frame in frames]

		saccades = self.identify_saccade_candidates_based_on_gaze_velocity(
			THRESHOLD.REQUIRED_GAZE_SPEED_FACTOR,
			world_gaze_angle
		)

		saccades = self.identify_saccade_amplitude_bigger_than_threshhold(
			THRESHOLD.MINIMUM_SACCADE_ANGLE_AMPLITUDE_DEGREE,
			saccades,
			world_gaze_angle
		)

		saccades = self.identify_gaze_moves_faster_than_ball(
			THRESHOLD.MINIMUM_SPEED_FASTER_THAN_BALL_PCT,
			ball_gaze_angle,
			saccades,
			world_gaze_angle
		)

		saccades = self.identify_saccade_within_time_window(
			THRESHOLD.MAXIMUM_TIME_WINDOW_START_BEFORE_BOUNCE_SECONDS,
			frames,
			saccades
		)

		saccades = self.identify_is_saccade_corrective(ball_gaze_angle, saccades)

		for saccade in saccades:
			end_frame = frames[saccade.start_index]
			start_frame = frames[saccade.end_index]
			angle_amplitude = world_gaze_angle[saccade.end_index] - world_gaze_angle[saccade.start_index]
			angle_start = world_gaze_angle[saccade.start_index]
			angle_end = world_gaze_angle[saccade.end_index]

			if saccade.is_corrective:
				self.events.append(
					CorrectiveSaccade(
						start_frame.timestamp,
						start_frame,
						end_frame.timestamp,
						end_frame,
						angle_amplitude,
						angle_start,
						angle_end,
						saccade.is_corrective,
						saccade.is_within_bounce_window
					)
				)
			else:
				self.events.append(
					PredictiveSaccade(
						start_frame.timestamp,
						start_frame,
						end_frame.timestamp,
						end_frame,
						angle_amplitude,
						angle_start,
						angle_end,
						saccade.is_corrective,
						saccade.is_within_bounce_window
					)
				)

	def identify_is_saccade_corrective(self, ball_gaze_angle, saccades: List[SaccadeCandidate]):
		ball_gaze_angle_start = [ball_gaze_angle[saccade.start_index] for saccade in saccades]
		ball_gaze_angle_end = [ball_gaze_angle[saccade.end_index] for saccade in saccades]
		corrective_saccade_mask = [abs(ball_gaze_angle_start[i]) < abs(ball_gaze_angle_end[i]) for i in
								   range(len(ball_gaze_angle_start))]

		for i in range(len(saccades)):
			saccades[i].is_corrective = corrective_saccade_mask[i]

		return saccades

	def identify_saccade_within_time_window(self, threshold: THRESHOLD, frames, saccades: List[SaccadeCandidate]):
		bounce_event = next((e for e in self.trial.ball_events if isinstance(e, FirstBounceEvent)), None)

		if bounce_event is None:
			return saccades

		bounce_time = bounce_event.timestamp_start
		start_timestamps = [frames[saccade.start_index].timestamp for saccade in saccades]

		mask = Timing.is_within_window(
			bounce_time,
			threshold.value,
			start_timestamps
		)

		for i in range(len(saccades)):
			saccades[i].is_within_bounce_window = mask[i]

		return saccades

	def identify_gaze_moves_faster_than_ball(self, threshold: THRESHOLD, ball_gaze_angle, saccades, world_gaze_angle):

		gaze_velocity_at_start = [
			world_gaze_angle[saccade.start_index + 1] - world_gaze_angle[saccade.start_index] for saccade in saccades
		]

		ball_velocity_at_start = [
			ball_gaze_angle[saccade.start_index + 1] - ball_gaze_angle[saccade.start_index] for saccade in saccades
		]

		ball_velocity_mask = [
			abs(gaze_velocity_at_start[i]) > abs(ball_velocity_at_start[i]) * (1 + threshold.value) for i in
			range(len(gaze_velocity_at_start))
		]

		for i in range(len(saccades)):
			saccades[i].identify_gaze_moves_faster_than_ball = ball_velocity_mask[i]

		return saccades

	def identify_saccade_amplitude_bigger_than_threshhold(
		self, threshold: THRESHOLD, saccades: List[SaccadeCandidate],
		world_gaze_angle
	):
		acceleration_differences = [
			world_gaze_angle[saccade.end_index] - world_gaze_angle[saccade.start_index] for saccade in saccades
		]

		for i in range(len(saccades)):
			if abs(acceleration_differences[i]) > threshold.value:
				saccades[i].is_eye_moving_enough = True

		return saccades

	def identify_saccade_candidates_based_on_gaze_velocity(self, threshold: THRESHOLD, world_gaze_angle):
		acceleration = Integration.get_acceleration(world_gaze_angle)
		absolute_acceleration = [abs(a) for a in acceleration]
		median_acceleration = SaccadeDetector.get_median(absolute_acceleration)
		saccades = SaccadeDetector.find(acceleration, median_acceleration * threshold.value)
		return saccades
