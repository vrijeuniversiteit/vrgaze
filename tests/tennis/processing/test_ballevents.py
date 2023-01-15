import unittest

from tests.tennis.builders.trial_builder import TrialBuilder
from vrgaze.tennis.models.balleventmodels import BallHitWithRacket, FirstBounceEvent, BallCrossesNetAfterServe, BallHitFrontWall, SecondBounceEvent
from vrgaze.tennis.services.processing.ball_events import BallEventsCalculator


class TestEvents(unittest.TestCase):

	def setUp(self):
		height_of_ball = [2.5, 1, 0, 1]
		z_position_ball = [11, -11, -3, 11]
		timestamps = [0, 1, 2, 3, 4]

		builder = TrialBuilder()
		builder.with_frame(timestamps[0], z_position_ball[0], height_of_ball[0])
		builder.with_frame(timestamps[1], z_position_ball[1], height_of_ball[1])
		builder.with_frame(timestamps[2], z_position_ball[2], height_of_ball[2])
		builder.with_frame(timestamps[3], z_position_ball[3], height_of_ball[3])
		self.trial = builder.build()

	def test_detect_ball_crosses_net_returns_first_frame_after_ball_crosses_net(self):
		events = BallEventsCalculator(self.trial)
		events.detect_ball_crosses_net()
		net_cross = events.get_events_of_type(BallCrossesNetAfterServe)[0]
		self.assertEqual(net_cross.timestamp, 1)

	def test_identify_hit_with_racket(self):
		events = BallEventsCalculator(self.trial)
		events.identify_hit_with_racket()
		self.assertTrue(events.contains(BallHitWithRacket))

	def test_identify_bounce_event(self):
		events = BallEventsCalculator(self.trial)
		events.identify_bounce_events()
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

		events = BallEventsCalculator(trial_without_racket_hit)
		events.identify_hit_with_racket()
		self.assertFalse(events.contains(BallHitWithRacket))

	def test_identify_first_bounce_event(self):
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

		events = BallEventsCalculator(trial)
		events.identify_bounce_events()
		bounce_events = events.get_events_of_type(FirstBounceEvent)
		self.assertEqual(len(bounce_events), 1)


	def test_identify_second_bounce_event(self):
		timestamps = [0.0, 1.0, 2.0, 3.0, 4.0]
		z_position_ball = [0, 0, 0, 0, 0]
		height_of_ball = [2.5, 0, 1.0, 0.0, 0.5]

		builder = TrialBuilder()
		builder.with_frame(timestamps[0], z_position_ball[0], height_of_ball[0])
		builder.with_frame(timestamps[1], z_position_ball[1], height_of_ball[1])
		builder.with_frame(timestamps[2], z_position_ball[2], height_of_ball[2])
		builder.with_frame(timestamps[3], z_position_ball[3], height_of_ball[3])
		builder.with_frame(timestamps[4], z_position_ball[4], height_of_ball[4])
		trial = builder.build()

		events = BallEventsCalculator(trial)
		events.identify_bounce_events()
		bounce_events = events.get_events_of_type(SecondBounceEvent)
		self.assertEqual(len(bounce_events), 1)

	def test_identify_ball_bounce_off_back_wall_event(self):
		timestamps = [0.0, 1.0, 2.0]
		front_wall_position = 15
		z_position_ball = [0, front_wall_position, 14]
		height_of_ball = [2, 3, 2]

		builder = TrialBuilder()
		builder.with_frame(timestamps[0], z_position_ball[0], height_of_ball[0])
		builder.with_frame(timestamps[1], z_position_ball[1], height_of_ball[1])
		builder.with_frame(timestamps[2], z_position_ball[2], height_of_ball[2])
		trial = builder.build()

		events = BallEventsCalculator(trial)
		events.identify_ball_hit_front_wall()
		has_event = events.contains(BallHitFrontWall)
		self.assertTrue(has_event)

	def test_identify_ball_bounce_off_back_wall_event_ignore_when_ball_is_served(self):
		timestamps = [0.0, 1.0, 2.0]
		z_position_ball = [11, 10, 9]
		height_of_ball = [2, 3, 2]

		builder = TrialBuilder()
		builder.with_frame(timestamps[0], z_position_ball[0], height_of_ball[0])
		builder.with_frame(timestamps[1], z_position_ball[1], height_of_ball[1])
		builder.with_frame(timestamps[2], z_position_ball[2], height_of_ball[2])
		trial = builder.build()

		events = BallEventsCalculator(trial)
		events.identify_ball_hit_front_wall()
		has_event = events.contains(BallHitFrontWall)
		self.assertFalse(has_event)

	def test_identify_ball_bounce_off_back_wall_event_should_not_trigger_when_not_hit_wall(self):
		timestamps = [0.0, 1.0, 2.0]
		z_position_ball = [0, -11, 0]
		height_of_ball = [1, 1, 1]

		builder = TrialBuilder()
		builder.with_frame(timestamps[0], z_position_ball[0], height_of_ball[0])
		builder.with_frame(timestamps[1], z_position_ball[1], height_of_ball[1])
		builder.with_frame(timestamps[2], z_position_ball[2], height_of_ball[2])
		trial = builder.build()

		events = BallEventsCalculator(trial)
		events.identify_ball_hit_front_wall()
		has_event = events.contains(BallHitFrontWall)
		self.assertFalse(has_event)
