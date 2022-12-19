from dataclasses import field, dataclass
from typing import List

from vrgaze.tennis.models.datamodel import Trial
from vrgaze.tennis.models.abstraction import Visitable, Visitor
from vrgaze.tennis.models.eventmodel import Event, BallCrossesNetAfterServe, BallHitWithRacket, FirstBounceEvent


class BallEvents(Visitor):
	def visit(self, trial: Visitable):
		trial = trial
		events = BallEventsCalculator(trial)
		events.detect_ball_crosses_net()
		events.identify_hit_with_racket()
		events.identify_bounce_event()
		trial.ball_events = events.events

@dataclass
class BallEventsCalculator:
	trial: Trial
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

	def identify_bounce_event(self):
		y_positions = [frame.ball_position_y for frame in self.trial.frames]
		z_positions = [frame.ball_position_z for frame in self.trial.frames]

		derivative = [y_positions[i + 1] - y_positions[i] for i in range(len(y_positions) - 1)]
		derivative.append(0)

		is_close_to_ground = [abs(y) < 0.5 for y in y_positions]
		derivative_is_positive = [d > 0 for d in derivative]

		change_of_direction_index = next((i for i, (d, y) in enumerate(zip(derivative_is_positive, is_close_to_ground)) if
										 d and y), None)

		if change_of_direction_index is None:
			return
		bounced_off_back_wall = z_positions[change_of_direction_index] < -15
		bounced_off_tennis_net = -1 < z_positions[change_of_direction_index] < 1

		if bounced_off_back_wall:
			return

		if bounced_off_tennis_net:
			return

		timestamp = self.trial.frames[change_of_direction_index].timestamp
		frame = self.trial.frames[change_of_direction_index]
		self.events.append(FirstBounceEvent(timestamp, frame))

	def get_events_of_type(self, FirstBounceEvent):
		return [event for event in self.events if isinstance(event, FirstBounceEvent)]


