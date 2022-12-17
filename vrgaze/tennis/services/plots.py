from matplotlib import pyplot as plt

from vrgaze.tennis.models.datamodel import ExperimentalData, Trajectory

plt.style.use(['vrgaze/style.mplstyle'])


def plot_3d(data: ExperimentalData):
	trajectories = []

	ax = plt.axes(projection='3d')
	greys = ['#000000', '#333333', '#666666', '#999999']
	ax.prop_cycle = 'cycler(color, ' + str(greys) + ')'

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

	ax.set_aspect('equal')
	ax.set_zlim(bottom=0)

	return plt


def plot_birdview(data: ExperimentalData):
	fig, ax = plt.subplots()
	ax.set_aspect('equal')
	ax.set_xlabel("Width [m]")
	ax.set_ylabel("Length [m]")

	half_width = 10.97 / 2
	half_length = 23.77 / 2
	half_single_width = 8.23 / 2
	to_service_t = 6.4
	half_net_width = (10.97 + 0.91) / 2

	# Service lines
	ax.plot([-half_width, half_width], [half_length, half_length], color='black')
	ax.plot([-half_width, half_width], [-half_length, -half_length], color='black')

	# Sidelines
	ax.plot([-half_width, -half_width], [-half_length, half_length], color='black')
	ax.plot([half_width, half_width], [-half_length, half_length], color='black')

	# Single lines
	ax.plot([-half_single_width, -half_single_width], [-half_length, half_length], color='black')
	ax.plot([half_single_width, half_single_width], [-half_length, half_length], color='black')

	# T line
	ax.plot([-half_single_width, half_single_width], [-to_service_t, -to_service_t], color='black')
	ax.plot([-half_single_width, half_single_width], [to_service_t, to_service_t], color='black')
	ax.plot([0, 0], [-to_service_t, to_service_t], [0, 0], color='black')

	# center nubbin
	ax.plot([0, 0], [-half_length, -half_length + 0.3], color='black')
	ax.plot([0, 0], [half_length, half_length - 0.3], color='black')

	# Net
	ax.plot([-half_net_width, half_net_width], color='black', linewidth=1)

	trajectories = []
	for trial in data.conditions[0].participants[0].trials:
		length = [frame.ball_position_x for frame in trial.frames]
		width = [frame.ball_position_z for frame in trial.frames]
		trajectories.append(Trajectory(length, [], width))

	for trajectory in trajectories:
		plt.plot(trajectory.length, trajectory.width)

	return plt


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
