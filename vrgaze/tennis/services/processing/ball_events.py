from dataclasses import field, dataclass
from typing import List

from vrgaze.tennis.models.common import Visitable, Visitor
from vrgaze.tennis.models.balleventmodels import Event, BallCrossesNetAfterServe, BallHitWithRacket, FirstBounceEvent, BallHitFrontWall, SecondBounceEvent


class BallEvents(Visitor):
	def visit_with_context(self, trial: Visitable, condition_name: str):
		self.visit(trial)

	def visit(self, trial: Visitable):
		trial = trial
		events = BallEventsCalculator(trial)
		events.detect_ball_crosses_net()
		events.identify_bounce_events()
		events.identify_hit_with_racket()
		events.identify_ball_hit_front_wall()
		trial.ball_events = events.events


@dataclass
class BallEventsCalculator:
	trial: "Trial"
	events: List[Event] = field(default_factory=list)

	def contains(self, event_type: Event):
		return any(isinstance(event, event_type) for event in self.events)

	def detect_ball_crosses_net(self):
		z_positions = [frame.ball_position_z for frame in self.trial.frames]
		index = next((i for i, x in enumerate(z_positions) if x < 0), None)
		timestamp = self.trial.frames[index].timestamp
		frame = self.trial.frames[index]
		self.events.append(BallCrossesNetAfterServe(timestamp, frame))

	def identify_hit_with_racket(self):
		z_positions = [frame.ball_position_z for frame in self.trial.frames]

		derivative = [z_positions[i + 1] - z_positions[i] for i in range(len(z_positions) - 1)]

		derivative.insert(0, derivative[0])
		change_of_direction_index = next((i for i, x in enumerate(derivative) if x > 0), None)

		if change_of_direction_index is None:
			return

		timestamp = self.trial.frames[change_of_direction_index].timestamp
		frame = self.trial.frames[change_of_direction_index]
		self.events.append(BallHitWithRacket(timestamp, frame))

	def identify_bounce_events(self):
		y_positions = [frame.ball_position_y for frame in self.trial.frames]

		derivative_moving_upwards = [y_positions[i + 1] - y_positions[i] for i in range(len(y_positions) - 1)]
		derivative_moving_upwards.append(0)

		is_close_to_ground = [abs(y) < 0.5 for y in y_positions]
		is_moving_up = [d > 0 for d in derivative_moving_upwards]

		is_changing_direction = [is_moving_up[i + 1] - is_moving_up[i] for i in range(len(is_moving_up) - 1)]
		is_changing_direction.insert(0, 0)

		is_changing_direction_in_upwards_direction = [d > 0 for d in is_changing_direction]

		is_bouncing = [d and p for d, p in zip(is_changing_direction_in_upwards_direction, is_close_to_ground)]
		number_of_bounces = is_bouncing.count(True)

		if number_of_bounces == 0:
			return

		if number_of_bounces == 1:
			first_bounce_index = is_bouncing.index(True)
			timestamp = self.trial.frames[first_bounce_index].timestamp
			frame = self.trial.frames[first_bounce_index]
			self.events.append(FirstBounceEvent(timestamp, frame))

		if number_of_bounces > 1:
			first_bounce_index = is_bouncing.index(True)
			timestamp = self.trial.frames[first_bounce_index].timestamp
			frame = self.trial.frames[first_bounce_index]
			self.events.append(FirstBounceEvent(timestamp, frame))

			is_bouncing[first_bounce_index] = False
			second_bounce_index = is_bouncing.index(True)
			timestamp = self.trial.frames[second_bounce_index].timestamp
			frame = self.trial.frames[second_bounce_index]
			self.events.append(SecondBounceEvent(timestamp, frame))

	def identify_ball_hit_front_wall(self):
		ball_z_positions = [frame.ball_position_z for frame in self.trial.frames]

		derivative = [ball_z_positions[i + 1] - ball_z_positions[i] for i in range(len(ball_z_positions) - 1)]
		derivative.append(0)

		derivative_is_negative = [d < 0 for d in derivative]
		position_is_positive = [z > 0 for z in ball_z_positions]

		bounce_off_back_wall_or_hit_by_racket_index = derivative_is_negative.index(False)
		derivative_is_negative[:bounce_off_back_wall_or_hit_by_racket_index] = [
																				   False] * bounce_off_back_wall_or_hit_by_racket_index

		change_direction_on_opponent_side = [d and p for d, p in zip(derivative_is_negative, position_is_positive)]

		hit_front_wall_index = next((i for i, d in enumerate(change_direction_on_opponent_side) if d), None)

		if hit_front_wall_index is None:
			return

		timestamp = self.trial.frames[hit_front_wall_index].timestamp
		frame = self.trial.frames[hit_front_wall_index]
		self.events.append(BallHitFrontWall(timestamp, frame))

	def get_events_of_type(self, FirstBounceEvent):
		return [event for event in self.events if isinstance(event, FirstBounceEvent)]
