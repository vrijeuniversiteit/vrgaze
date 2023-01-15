import unittest

from tests.tennis.builders.trial_builder import TrialBuilder
from tests.tennis.processing.time_of_saccade import Timing


class TestGazeEvents(unittest.TestCase):

	def setUp(self):
		builder = TrialBuilder()
		ball_position_z = [0, 0]
		ball_position_y = [0, 0]
		gaze_origin_x = [0, 0]
		gaze_origin_y = [2, 2]
		gaze_origin_z = [0, 0]
		gaze_direction_x = [0, 0]
		gaze_direction_y = [0, 0]
		gaze_direction_z = [1, 1]
		timestamps = [0, 1]

		self.trial = builder.with_gaze(
			timestamps,
			ball_position_z,
			ball_position_y,
			gaze_origin_x,
			gaze_origin_y,
			gaze_origin_z,
			gaze_direction_x,
			gaze_direction_y,
			gaze_direction_z,
		).build()

	def test_should_only_include_saccades_starting_within_window(self):

		saccade_start_timesamps = [0.0, 0.5, 1.0]
		assumed_window_seconds = 0.5
		assumed_ball_bounce_time = 0.9

		mask = Timing.is_within_window(
			assumed_ball_bounce_time,
			assumed_window_seconds,
			saccade_start_timesamps
			)

		self.assertEqual(mask, [False, True, False])






