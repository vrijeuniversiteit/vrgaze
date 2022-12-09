from unittest import TestCase

import matplotlib.pyplot as plt

from vrgaze.tennis.models import Trial, Frame


class TestReader(TestCase):

	def test_plot_trial(self):

		# matplotlib figure
		fig = plt.figure()

		# plot trial
		trial = Trial(1, 1, 1, 1, [])
		frame_1 = Frame(1, 1, 1, 1)
		frame_2 = Frame(2, 2, 2, 2)
		frame_3 = Frame(3, 3, 3, 3)




