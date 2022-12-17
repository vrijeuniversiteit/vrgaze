import unittest
from unittest.mock import MagicMock

from vrgaze.tennis.models.datamodel import Frame, Trial
from vrgaze.tennis.models.eventmodel import BallEvents, BallHitWithRacket, FirstBounceEvent, BallCrossesNetAfterServe


class TrialBuilder:
	def __init__(self):
		self.frames = []
		self.timestamps = []
		self.ball_position_z = []
		self.ball_position_y = []

	def with_frame(self, timestamp: float, ball_position_z: float, ball_position_y: float):
		self.timestamps.append(timestamp)
		self.ball_position_z.append(ball_position_z)
		self.ball_position_y.append(ball_position_y)
		return self

	def build(self):
		for timestamp, ball_position_z, ball_position_y in zip(
				self.timestamps,
				self.ball_position_z,
				self.ball_position_y
		):
			frame = MagicMock(spec=Frame)
			frame.timestamp = timestamp
			frame.ball_position_z = ball_position_z
			frame.ball_position_y = ball_position_y
			self.frames.append(frame)

		trial = MagicMock(spec=Trial)
		trial.frames = self.frames
		return trial


height_of_ball = [2.5, 1, 0, 1]
distance_of_ball = [11, -11, -3, 11]
timestamps = [0, 1, 2, 3, 4]

builder = TrialBuilder()
builder.with_frame(timestamps[0], distance_of_ball[0], height_of_ball[0])
builder.with_frame(timestamps[1], distance_of_ball[1], height_of_ball[1])
builder.with_frame(timestamps[2], distance_of_ball[2], height_of_ball[2])
builder.with_frame(timestamps[3], distance_of_ball[3], height_of_ball[3])
trial = builder.build()




class TestEvents(unittest.TestCase):

	def test_detect_ball_crosses_net_returns_first_frame_after_ball_crosses_net(self):
		events = BallEvents(trial)
		events.detect_ball_crosses_net()
		net_cross = events.get_events_of_type(BallCrossesNetAfterServe)[0]
		self.assertEqual(net_cross.timestamp, 1)

	def test_identify_hit_with_racket(self):
		events = BallEvents(trial)
		events.identify_hit_with_racket()
		self.assertTrue(events.contains(BallHitWithRacket))

	def test_identify_bounce_event(self):
		events = BallEvents(trial)
		events.identify_bounce_event()
		self.assertTrue(events.contains(FirstBounceEvent))

	def test_identify_hit_with_racket_without_racket_hit(self):
		height_of_ball = [2.5, 0, 1]
		z_position_ball = [11, 0, -11]
		timestamps = [0, 1, 2]

		builder = TrialBuilder()
		builder.with_frame(timestamps[0], z_position_ball[0], height_of_ball[0])
		builder.with_frame(timestamps[1], z_position_ball[1], height_of_ball[1])
		builder.with_frame(timestamps[2], z_position_ball[2], height_of_ball[2])
		trial_without_racket_hit = builder.build()

		events = BallEvents(trial_without_racket_hit)
		events.identify_hit_with_racket()
		self.assertFalse(events.contains(BallHitWithRacket))


	def test_identify_only_first_bounce_event(self):
		timestamps = [0.0, 1.0, 2.0, 3.0, 4.0]
		z_position_ball = [11, -11, -12, -13, -14]
		height_of_ball = [2.5, 0, 1.0, 0.0, 0.5]

		builder = TrialBuilder()
		builder.with_frame(timestamps[0], z_position_ball[0], height_of_ball[0])
		builder.with_frame(timestamps[1], z_position_ball[1], height_of_ball[1])
		builder.with_frame(timestamps[2], z_position_ball[2], height_of_ball[2])
		builder.with_frame(timestamps[3], z_position_ball[3], height_of_ball[3])
		builder.with_frame(timestamps[4], z_position_ball[4], height_of_ball[4])
		trial = builder.build()

		events = BallEvents(trial)
		events.identify_bounce_event()
		bounce_events = events.get_events_of_type(FirstBounceEvent)
		self.assertEqual(len(bounce_events), 1)

	def test_ignore_when_ball_bounces_at_the_back_wall(self):
		timestamps = [0.0, 1.0, 2.0]
		z_position_ball = [-11.0, -15.1, -14]
		height_of_ball = [1, 0, 1]

		builder = TrialBuilder()
		builder.with_frame(timestamps[0], z_position_ball[0], height_of_ball[0])
		builder.with_frame(timestamps[1], z_position_ball[1], height_of_ball[1])
		builder.with_frame(timestamps[2], z_position_ball[2], height_of_ball[2])
		trial = builder.build()

		events = BallEvents(trial)
		events.identify_bounce_event()
		has_bounce_event = events.contains(FirstBounceEvent)
		self.assertFalse(has_bounce_event)

	def test_ignore_when_ball_bounces_off_the_tennis_net(self):
		timestamps = [0.0, 1.0, 2.0]
		z_position_ball = [11.0, 0, 0.5]
		height_of_ball = [1, 0, 1]

		builder = TrialBuilder()
		builder.with_frame(timestamps[0], z_position_ball[0], height_of_ball[0])
		builder.with_frame(timestamps[1], z_position_ball[1], height_of_ball[1])
		builder.with_frame(timestamps[2], z_position_ball[2], height_of_ball[2])
		trial = builder.build()

		events = BallEvents(trial)
		events.identify_bounce_event()
		has_bounce_event = events.contains(FirstBounceEvent)
		self.assertFalse(has_bounce_event)

