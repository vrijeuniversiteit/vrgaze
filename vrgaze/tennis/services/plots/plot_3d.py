from matplotlib import pyplot as plt

from vrgaze.tennis import ExperimentalData
from vrgaze.tennis.models.datamodel import Trajectory
from vrgaze.tennis.services.plots.trial_enumerator import TrialEnumerator


def plot_3d(data: ExperimentalData) -> plt:
	"""Plot ball trajectories in 3D space.

	Returns:
		plt: The plot.

	Examples:
		>>> plot = plot_3d(data)
		>>> plot.show()
		>>> plot.savefig("plot_3d.png")
	"""

	trajectories = []
	enumerator = TrialEnumerator()
	data.process(enumerator)
	for trial in enumerator.trials:
		width = [frame.ball_position_x for frame in trial.frames]
		length = [frame.ball_position_z for frame in trial.frames]
		height = [frame.ball_position_y for frame in trial.frames]
		trajectories.append(Trajectory(length, height, width))

	number_of_trajectories = len(trajectories)
	alpha = 1 / number_of_trajectories
	if number_of_trajectories > 100:
		alpha = 0.01

	ax = plt.axes(projection='3d')
	for trajectory in trajectories:
		ax.plot3D(trajectory.width, trajectory.length, trajectory.height, c='black', alpha=alpha)

	half_width = 10.97 / 2
	half_length = 23.77 / 2
	half_single_width = 8.23 / 2
	to_service_t = 6.4
	half_net_width = (10.97 + 0.91) / 2

	# Service lines
	ax.plot([-half_width, half_width], [half_length, half_length], [0, 0], color='black')
	ax.plot([-half_width, half_width], [-half_length, -half_length], [0, 0], color='black')

	# Sidelines
	ax.plot([-half_width, -half_width], [-half_length, half_length], [0, 0], color='black')
	ax.plot([half_width, half_width], [-half_length, half_length], [0, 0], color='black')

	# Single lines
	ax.plot([-half_single_width, -half_single_width], [-half_length, half_length], [0, 0], color='black')
	ax.plot([half_single_width, half_single_width], [-half_length, half_length], [0, 0], color='black')

	# T line
	ax.plot([-half_single_width, half_single_width], [-to_service_t, -to_service_t], [0, 0], color='black')
	ax.plot([-half_single_width, half_single_width], [to_service_t, to_service_t], [0, 0], color='black')
	ax.plot([0, 0], [-to_service_t, to_service_t], [0, 0], color='black')

	# center nubbin
	ax.plot([0, 0], [-half_length, -half_length + 0.3], [0, 0], color='black')
	ax.plot([0, 0], [half_length, half_length - 0.3], [0, 0], color='black')

	# Net
	ax.plot([-half_net_width, half_net_width], [0, 0], [1.065, 1.065], color='black')
	ax.plot([-half_net_width, half_net_width], [0, 0], [0, 0], color='black')
	# net posts
	ax.plot([-half_net_width, -half_net_width], [0, 0], [0, 1.065], color='black')
	ax.plot([half_net_width, half_net_width], [0, 0], [0, 1.065], color='black')

	ax.set_aspect('equal')
	ax.set_zlim(bottom=0)

	return plt
