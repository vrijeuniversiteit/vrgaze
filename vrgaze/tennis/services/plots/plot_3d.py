from matplotlib import pyplot as plt

from vrgaze.tennis import ExperimentalData
from vrgaze.tennis.models.datamodel import Trajectory
from vrgaze.tennis.models.gazeeventmodels import PredictiveSaccade


def plot_3d(data: ExperimentalData) -> plt:
	"""Plot ball trajectories in 3D space.

	Returns:
		plt: The plot.

	Examples:
		>>> plot = plot_3d(data)
		>>> plot.show()
		>>> plot.savefig("plot_3d.png")
	"""

	ax = plt.axes(projection='3d')
	greys = ['#000000', '#333333', '#666666', '#999999']
	ax.prop_cycle = 'cycler(color, ' + str(greys) + ')'

	trajectories = []
	for trial in data.conditions[0].participants[0].trials:
		width = [frame.ball_position_x for frame in trial.frames]
		length = [frame.ball_position_z for frame in trial.frames]
		height = [frame.ball_position_y for frame in trial.frames]
		trajectories.append(Trajectory(length, height, width))
	for trajectory in trajectories:
		ax.plot3D(trajectory.width, trajectory.length, trajectory.height)

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

	for trial in data.conditions[0].participants[0].trials:
		predictive_saccades = trial.gaze_events
		for saccade in predictive_saccades:
			if isinstance(saccade, PredictiveSaccade):
				start_x = saccade.end_frame.ball_position_x
				start_y = saccade.end_frame.ball_position_z
				start_z = saccade.end_frame.ball_position_y
				ax.scatter3D(start_x, start_y, start_z, color='green', marker='o', s=20, alpha=0.5)
				end_x = saccade.frame.ball_position_x
				end_y = saccade.frame.ball_position_z
				end_z = saccade.frame.ball_position_y
				# filled point green at end
				ax.scatter3D(end_x, end_y, end_z, color='green', marker='o', s=20, alpha=1)

	ax.set_aspect('equal')
	ax.set_zlim(bottom=0)

	return plt
