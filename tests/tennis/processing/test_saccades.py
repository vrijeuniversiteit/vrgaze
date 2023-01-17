import unittest

from vrgaze.tennis.services.processing.saccade_detector import SaccadeDetector
from vrgaze.tennis.services.processing.integration import Integration


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
		saccades = SaccadeDetector.find(acceleration, median_acceleration)
		self.assertEqual(1, len(saccades))
		self.assertEqual(3, saccades[0].start_index)
		self.assertEqual(4, saccades[0].end_index)


	def test_should_not_return_saccades_that_dont_have_an_end(self):
		acceleration = [0, 10, 20, 30, 40]
		median_acceleration = 20
		saccades = SaccadeDetector.find(acceleration, median_acceleration)
		self.assertEqual([], saccades)



	def test_should_return_two_saccades(self):
		acceleration = [0, 10, 20, 30, 10, 40, 40, 0]
		median_acceleration = 20
		saccades = SaccadeDetector.find(acceleration, median_acceleration)

		self.assertEqual(2, len(saccades))
		self.assertEqual(3, saccades[0].start_index)
		self.assertEqual(4, saccades[0].end_index)
		self.assertEqual(5, saccades[1].start_index)
		self.assertEqual(7, saccades[1].end_index)


