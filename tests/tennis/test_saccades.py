import unittest

from vrgaze.tennis.utils import Integration, Saccades


class TestIntegration(unittest.TestCase):
	def test_calculate_acceleration(self):
		positions = [0, 10, -10]
		acceleration = Integration.get_acceleration(positions)
		self.assertEqual(len(acceleration), len(positions))
		self.assertEqual(acceleration, [0, 10, -30])

	def test_should_return_0_for_static_positions(self):
		positions = [0, 0, 0]
		acceleration = Integration.get_acceleration(positions)
		self.assertEqual(len(acceleration), len(positions))
		self.assertEqual(acceleration, [0, 0, 0])


class TestSaccadeDetection(unittest.TestCase):
	def test_begin_and_end_of_saccade_with_acceleration_greater_than_median(self):
		acceleration = [0, 10, 20, 30, 0]
		median_acceleration = 20
		starts, ends = Saccades.begin_and_end_of_saccade(acceleration, median_acceleration)
		self.assertEqual([3], starts)
		self.assertEqual([4], ends)


	def test_should_not_return_saccades_that_dont_have_an_end(self):
		acceleration = [0, 10, 20, 30, 40]
		median_acceleration = 20
		starts, ends = Saccades.begin_and_end_of_saccade(acceleration, median_acceleration)
		self.assertEqual([], starts)
		self.assertEqual([], ends)


	def test_should_not_return_two_saccades(self):
		acceleration = [0, 10, 20, 30, 10, 40, 40, 0]
		median_acceleration = 20
		starts, ends = Saccades.begin_and_end_of_saccade(acceleration, median_acceleration)
		self.assertEqual([3, 5], starts)
		self.assertEqual([4, 7], ends)

