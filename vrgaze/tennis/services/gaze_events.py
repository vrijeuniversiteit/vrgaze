from dataclasses import dataclass, field
from typing import List

from tests.tennis.test_angles import Angles
from vrgaze.tennis.models.datamodel import Trial
from vrgaze.tennis.models.abstraction import Visitable, Visitor
from vrgaze.tennis.models.eventmodel import Event, CorrectiveSaccade, PredictiveSaccade


class GazeEvents(Visitor):
	def visit(self, visitable: Visitable):
		trial = visitable
		events = GazeEventCalculator(trial)
		events.calculate_saccades()
		trial.gaze_events = events.events


@dataclass
class GazeEventCalculator:
	trial: Trial
	events: List[Event] = field(default_factory=list)

	def calculate_saccades(self):
		frames = self.trial.frames
		angles = [Angles.calculate_gaze_world_angle(frame.gaze_direction_y, frame.gaze_direction_z) for frame in frames]
		ball_angle = [Angles.calculate_ball_gaze_angle(
			frame.ball_position_y,
			frame.ball_position_z,
			frame.gaze_direction_y,
			frame.gaze_direction_z,
			frame.gaze_origin_y,
			frame.gaze_origin_z
		) for frame in frames]

		velocity = [angles[i + 1] - angles[i] for i in range(len(angles) - 1)]
		velocity.insert(0, 0)

		acceleration = [velocity[i + 1] - velocity[i] for i in range(len(velocity) - 1)]

		acceleration.insert(0, 0)

		median_acceleration = sorted(acceleration)[len(acceleration) // 2]

		# get mask where velocity is greater than 5x median velocity
		acceleration_mask = [abs(a) > 5 * median_acceleration for a in acceleration]

		# get begin and end of where the mask is true
		starts = [i for i, x in enumerate(acceleration_mask) if x and (i == 0 or not acceleration_mask[i - 1])]
		ends = [i for i, x in enumerate(acceleration_mask) if x and (i == len(acceleration_mask) - 1 or not
		acceleration_mask[i + 1])]

		# get difference in angle between start and end
		acceleration_differences = [angles[end] - angles[start] for start, end in zip(starts, ends)]

		# get occurences where the difference is greater than 1 degrees
		acceleration_differences_mask = [abs(a) > 1 for a in acceleration_differences]

		# get the ball velocity during start and end
		ball_velocity = [ball_angle[end] - ball_angle[start] for start, end in zip(starts, ends)]

		# get occurences where the angle velocity is 20% greater than the ball velocity
		ball_velocity_mask = [abs(a) > 0.2 * ball_velocity[i] for i, a in enumerate(acceleration_differences)]

		# get occurences where both masks are true
		acceleration_mask = [a and b for a, b in zip(acceleration_differences_mask, ball_velocity_mask)]

		# get only occurences where the gaze ball angle was closer to the end of the acceleration
		corrective_saccade_mask = [a and ball_angle[start] < ball_angle[end] for a, start, end in zip(
			acceleration_mask, starts, ends
		)]

		predictive_saccade_mask = [not a for a in corrective_saccade_mask]

		for start, end, is_corrective in zip(starts, ends, corrective_saccade_mask):
			end_frame = frames[end]
			start_frame = frames[start]
			angle_amplitude = angles[end] - angles[start]
			angle_start = angles[start]
			angle_end = angles[end]
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
