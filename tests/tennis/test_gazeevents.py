import unittest

from tests.tennis.trial_builder import TrialBuilder


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




