from matplotlib import pyplot as plt

from vrgaze.tennis import ExperimentalData
from vrgaze.tennis.models.datamodel import Trajectory
from vrgaze.tennis.services.plots.trial_enumerator import TrialEnumerator


def plot_side(data: ExperimentalData):
	fig, ax = plt.subplots()
	ax.set_aspect('equal')
	ax.set_xlabel("Length [m]")
	ax.set_ylabel("Height [m]")

	half_court = 23.77 / 2
	ax.plot([-half_court, half_court], [0, 0], color="black", linewidth=1)
	plt.plot([0, 0], [0, 1.065], color="black", linewidth=2)

	trajectories = []
	enumerator = TrialEnumerator()
	data.process(enumerator)
	for trial in enumerator.trials:
		length = [frame.ball_position_z for frame in trial.frames]
		height = [frame.ball_position_y for frame in trial.frames]
		trajectories.append(Trajectory(length, height, []))

	number_of_trajectories = len(trajectories)
	alpha = 1 / number_of_trajectories
	if number_of_trajectories > 100:
		alpha = 0.01

	for trajectory in trajectories:
		plt.plot(trajectory.length, trajectory.height, c='black', alpha=alpha)

	return plt
