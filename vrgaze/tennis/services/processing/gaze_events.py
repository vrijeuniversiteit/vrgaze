from dataclasses import dataclass, field
from typing import List

from vrgaze.tennis.models.abstraction import Visitable, Visitor
from vrgaze.tennis.models.datamodel import Trial
from vrgaze.tennis.models.eventmodel import Event, FirstBounceEvent, CorrectiveSaccade, PredictiveSaccade
from vrgaze.tennis.services.processing.saccades import Saccades
from vrgaze.tennis.services.processing.integration import Integration
from vrgaze.tennis.services.processing.angles import Angles


class GazeEvents(Visitor):
	def visit_with_context(self, trial: Visitable, condition_name: str):
		self.visit(trial)

	def visit(self, trial: Visitable):
		trial = trial
		calculator = GazeEventCalculator(trial)
		calculator.calculate_saccades()
		trial.gaze_events = calculator.events


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

		acceleration = Integration.get_acceleration(world_gaze_angle)
		absolute_acceleration = [abs(a) for a in acceleration]
		median_acceleration = Saccades.get_median(absolute_acceleration)
		starts, ends = Saccades.begin_and_end_of_saccade(acceleration, median_acceleration)

		minimal_saccade_angle_degree = 1
		acceleration_differences = [world_gaze_angle[end] - world_gaze_angle[start] for start, end in zip(starts, ends)]
		acceleration_differences_mask = [abs(a) > minimal_saccade_angle_degree for a in acceleration_differences]

		minimal_velocity_difference_from_ball_pct = 0.2
		gaze_velocity_at_start = [world_gaze_angle[start + 1] - world_gaze_angle[start] for start in starts]
		ball_velocity_at_start = [ball_gaze_angle[start + 1] - ball_gaze_angle[start] for start in starts]
		ball_velocity_mask = [abs(gaze_velocity_at_start[i]) > abs(ball_velocity_at_start[i]) * (
					1 + minimal_velocity_difference_from_ball_pct) for i in range(len(gaze_velocity_at_start))]

		bounce_event = next((e for e in self.trial.ball_events if isinstance(e, FirstBounceEvent)), None)
		bounce_time = bounce_event.timestamp
		start_timestamps = [frames[start].timestamp for start in starts]
		window_before_bounce = 0.4
		bounce_window_mask = [start_timestamps[i] < bounce_time + window_before_bounce for i in
							  range(len(start_timestamps))]

		all_saccades_mask = [acceleration_differences_mask[i] and ball_velocity_mask[i] and bounce_window_mask[i] for i
							 in range(len(acceleration_differences_mask))]

		# get only occurences where the gaze ball angle was closer to the end of the acceleration
		ball_gaze_angle_start = [ball_gaze_angle[start] for start in starts]
		ball_gaze_angle_end = [ball_gaze_angle[end] for end in ends]
		corrective_saccade_mask = [abs(ball_gaze_angle_start[i]) < abs(ball_gaze_angle_end[i]) for i in
								   range(len(ball_gaze_angle_start))]

		for start, end, is_saccade, is_corrective in zip(starts, ends, all_saccades_mask, corrective_saccade_mask):

			if not is_saccade:
				continue

			end_frame = frames[end]
			start_frame = frames[start]
			angle_amplitude = world_gaze_angle[end] - world_gaze_angle[start]
			angle_start = world_gaze_angle[start]
			angle_end = world_gaze_angle[end]
			if is_corrective:
				self.events.append(
					CorrectiveSaccade(
						end_frame.timestamp,
						end_frame,
						start_frame,
						angle_amplitude,
						angle_start,
						angle_end
					)
				)
			else:
				self.events.append(
					PredictiveSaccade(
						end_frame.timestamp,
						end_frame,
						start_frame,
						angle_amplitude,
						angle_start,
						angle_end
					)
				)
