import unittest

from vrgaze.tennis.services.processing.saccade_detector import SaccadeDetector


class TestNumerics(unittest.TestCase):
	def test_return_median(self):
		values = [1, 2, 3]
		median = SaccadeDetector.get_median(values)
		self.assertEqual(median, 2)

	def test_return_next_greater_if_even_numbers(self):
		values = [1, 2, 3, 4]
		median = SaccadeDetector.get_median(values)
		self.assertEqual(median, 3)

	def test_works_with_even_numbers(self):
		values = [-1, -2, 3]
		median = SaccadeDetector.get_median(values)
		self.assertEqual(median, -1)

	def test_works_with_unsorted_values(self):
		values = [-1, -2, 3, 4]
		median = SaccadeDetector.get_median(values)
		self.assertEqual(median, 3)
