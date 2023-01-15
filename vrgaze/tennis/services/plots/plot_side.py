from matplotlib import pyplot as plt

from vrgaze.tennis import ExperimentalData
from vrgaze.tennis.models.datamodel import Trajectory


def plot_side(data: ExperimentalData):
	fig, ax = plt.subplots()
	ax.set_aspect('equal')
	ax.set_xlabel("Length [m]")
	ax.set_ylabel("Height [m]")

	half_court = 23.77 / 2
	ax.plot([-half_court, half_court], [0, 0], color="black", linewidth=1)
	plt.plot([0, 0], [0, 1.065], color="black", linewidth=2)

	trajectories = []
	for trial in data.conditions[0].participants[0].trials:
		length = [frame.ball_position_z for frame in trial.frames]
		height = [frame.ball_position_y for frame in trial.frames]
		trajectories.append(Trajectory(length, height, []))
	for trajectory in trajectories:
		plt.plot(trajectory.length, trajectory.height)

	return plt
