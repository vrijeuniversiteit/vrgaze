from dataclasses import dataclass, field
from typing import List

from vrgaze.tennis.datamodel import Trial, Frame

@dataclass
class Event:
	timestamp: float
	frame: Frame

class BallCrossesNetAfterServe(Event):
	pass

class BallHitWithRacket(Event):
	pass

class FirstBounceEvent(Event):
	pass


@dataclass
class BallEvents:
	Trial: Trial
	Events: List[Event] = field(default_factory=list)

	def contains(self, event_type: Event):
		return any(isinstance(event, event_type) for event in self.Events)

	def detect_ball_crosses_net(self, trial: Trial):
		z_positions = [frame.ball_position_z for frame in trial.frames]
		index = next((i for i, x in enumerate(z_positions) if x > 0), None)
		timestamp = trial.frames[index].timestamp
		frame = trial.frames[index]
		self.Events.append(BallCrossesNetAfterServe(timestamp, frame))

	def identify_hit_with_racket(self, trial: Trial):
		z_positions = [frame.ball_position_z for frame in trial.frames]

		derivative = [z_positions[i + 1] - z_positions[i] for i in range(len(z_positions) - 1)]
		derivative.insert(0, 0)
		change_of_direction_index = next((i for i, x in enumerate(derivative) if x < 0), None)

		if change_of_direction_index is None:
			return

		timestamp = trial.frames[change_of_direction_index].timestamp
		frame = trial.frames[change_of_direction_index]
		self.Events.append(BallHitWithRacket(timestamp, frame))

	def identify_bounce_event(self, trial):
		y_positions = [frame.ball_position_y for frame in trial.frames]

		derivative = [y_positions[i + 1] - y_positions[i] for i in range(len(y_positions) - 1)]
		derivative.insert(0, 0)
		change_of_direction_index = next((i for i, x in enumerate(derivative) if x < 0), None)

		if change_of_direction_index is None:
			return

		timestamp = trial.frames[change_of_direction_index].timestamp
		frame = trial.frames[change_of_direction_index]
		self.Events.append(FirstBounceEvent(timestamp, frame))



