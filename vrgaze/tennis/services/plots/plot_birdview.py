from matplotlib import pyplot as plt

from vrgaze.tennis import ExperimentalData
from vrgaze.tennis.models.datamodel import Trajectory
from vrgaze.tennis.services.plots.trial_enumerator import TrialEnumerator


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
	enumerator = TrialEnumerator()
	data.process(enumerator)
	for trial in enumerator.trials:
		length = [frame.ball_position_x for frame in trial.frames]
		width = [frame.ball_position_z for frame in trial.frames]
		trajectories.append(Trajectory(length, [], width))

	number_of_trajectories = len(trajectories)
	alpha = 1 / number_of_trajectories
	if number_of_trajectories > 100:
		alpha = 0.01

	for trajectory in trajectories:
		plt.plot(trajectory.length, trajectory.width, c='black', alpha=alpha)

	return plt
