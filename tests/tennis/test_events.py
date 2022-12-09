# setup unittest class
import unittest
from dataclasses import dataclass, field
from typing import List

from unittest.mock import MagicMock

from vrgaze.tennis.models import Frame, Trial

height_of_ball = [2.5, 0, 0, 1]
distance_of_ball = [-1, 0, 1, 0.5]

frame_0 = MagicMock(spec=Frame)
frame_0.timestamp = 0.0
frame_0.ball_position_z = distance_of_ball[0]
frame_0.ball_position_y = height_of_ball[0]

frame_1 = MagicMock(spec=Frame)
frame_1.timestamp = 1.0
frame_1.ball_position_z = distance_of_ball[1]
frame_1.ball_position_y = height_of_ball[1]

frame_2 = MagicMock(spec=Frame)
frame_2.timestamp = 2.0
frame_2.ball_position_z = distance_of_ball[2]
frame_2.ball_position_y = height_of_ball[2]

frame_3 = MagicMock(spec=Frame)
frame_3.timestamp = 3.0
frame_3.ball_position_z = distance_of_ball[3]
frame_3.ball_position_y = height_of_ball[3]

trial = MagicMock(spec=Trial)
trial.frames = [frame_0, frame_1, frame_2, frame_3]

trial_without_racket_hit = MagicMock(spec=Trial)
trial_without_racket_hit.frames = [frame_0, frame_1, frame_2]


class TestEvents(unittest.TestCase):

	def test_detect_ball_crosses_net(self):
		events = BallEvents(trial)
		events.detect_ball_crosses_net(trial)
		self.assertEqual(events.Events[0].timestamp, 2.0)

	def test_identify_hit_with_racket(self):
		events = BallEvents(trial)
		events.identify_hit_with_racket(trial)
		self.assertTrue(events.contains(BallHitWithRacket))

	def test_identify_hit_with_racket_without_racket_hit(self):
		events = BallEvents(trial_without_racket_hit)
		events.identify_hit_with_racket(trial_without_racket_hit)
		self.assertFalse(events.contains(BallHitWithRacket))

	def test_identify_bounce_event(self):
		events = BallEvents(trial)
		events.identify_bounce_event(trial)
		self.assertTrue(events.contains(FirstBounceEvent))


	def test_was_returned_without_hitting_net_or_wall(self):
		assert True == False

	def test_identify_only_first_bounce_event(self):
		assert True == False

	def test_identify_hit_with_racket_should_only_return_true_if_close_to_baseline(self):
		assert True == False

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

