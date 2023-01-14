import unittest

from vrgaze.tennis.services.processing.angles import Angles


class BallGazeAngleParams:
	def __init__(self):
		self.origin_y = None
		self.origin_z = None
		self.direction_y = None
		self.direction_z = None
		self.ball_position_y = None
		self.ball_position_z = None

	def with_origin(self, y, z):
		self.origin_y = y
		self.origin_z = z
		return self

	def with_direction(self, y, z):
		self.direction_y = y
		self.direction_z = z
		return self

	def with_ball_position(self, y, z):
		self.ball_position_y = y
		self.ball_position_z = z
		return self

	def build(self):
		return self.__dict__


class TestCalculateGazeWorldAngle(unittest.TestCase):

	def test_should_return_0_if_gaze_is_parallel_to_z_axis(self):
		directions_y_z = (0, 1)
		angle = Angles.calculate_gaze_world_angle(*directions_y_z)
		assert angle == 0

	def test_should_return_90_if_gaze_is_straight_up(self):
		directions_y_z = (1, 0)
		angle = Angles.calculate_gaze_world_angle(*directions_y_z)
		assert angle == -90

	def test_should_return_180_if_gaze_is_parallel_to_ground_but_backward(self):
		directions_y_z = (0, -1)
		angle = Angles.calculate_gaze_world_angle(*directions_y_z)
		assert angle == -180

	def test_should_return_minus_90_if_gaze_is_straight_down(self):
		directions_y_z = (-1, 0)
		angle = Angles.calculate_gaze_world_angle(*directions_y_z)
		assert angle == 90



class TestCalculateBallGazeAngle(unittest.TestCase):

	def test_should_return_0_when_gaze_directed_at_ball(self):
		params = (BallGazeAngleParams()
				  .with_origin(2, -11)
				  .with_direction(0, 1)
				  .with_ball_position(2, 11)
				  .build())
		angle = Angles.calculate_ball_gaze_angle(**params)

		self.assertEqual(angle, 0)

	def test_should_calculate_45_degree_angle(self):
		params = (BallGazeAngleParams()
				  .with_origin(2, -11)
				  .with_direction(0, 1)
				  .with_ball_position(1, -10)
				  .build())
		angle = Angles.calculate_ball_gaze_angle(**params)

		self.assertAlmostEqual(angle, 45, delta=0.001)

	def test_should_return_minus_45_degree_if_ball_is_above(self):
		params = (BallGazeAngleParams()
				  .with_origin(2, -11)
				  .with_direction(0, 1)
				  .with_ball_position(3, -10)
				  .build())
		angle = Angles.calculate_ball_gaze_angle(**params)

		self.assertAlmostEqual(angle, -45, delta=0.001)

	def test_should_return_minus_180_degree_if_gaze_directly_behind(self):
		params = (BallGazeAngleParams()
				  .with_origin(2, -11)
				  .with_direction(0, 1)
				  .with_ball_position(2, -12)
				  .build())
		angle = Angles.calculate_ball_gaze_angle(**params)

		self.assertAlmostEqual(angle, -180, delta=0.001)
