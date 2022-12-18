from matplotlib import pyplot as plt

from vrgaze.tennis.models.datamodel import ExperimentalData, Trajectory
from vrgaze.tennis.models.eventmodel import PredictiveSaccade, FirstBounceEvent
from vrgaze.tennis.utils import Angles

plt.style.use(['vrgaze/style.mplstyle'])


def plot_3d(data: ExperimentalData, show_predictive_saccades: bool = False) -> plt:
	"""Plot ball trajectories in 3D space.

	Args:
		show_predictive_saccades (bool): Whether to overlay predictive saccades on the plot.

	Returns:
		plt: The plot.

	Examples:
		>>> from vrgaze.tennis import plot_3d
		>>>
		>>> plot = plot_3d(data, show_predictive_saccades=True)
		>>> plot.show()
		>>> plot.savefig("plot_3d.png")
	"""

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

	if show_predictive_saccades:
		ball_bounce_events = [e for e in trial.ball_events if isinstance(e, FirstBounceEvent)]

		for trial in data.conditions[0].participants[0].trials:
			predictive_saccades = trial.gaze_events
			for saccade in predictive_saccades:
				if isinstance(saccade, PredictiveSaccade):

					start_x = saccade.start_frame.ball_position_x
					start_y = saccade.start_frame.ball_position_z
					start_z = saccade.start_frame.ball_position_y
					ax.scatter3D(start_x, start_y, start_z, color='green', marker='o', s=20, alpha=0.5)
					end_x = saccade.frame.ball_position_x
					end_y = saccade.frame.ball_position_z
					end_z = saccade.frame.ball_position_y
					# filled point green at end
					ax.scatter3D(end_x, end_y, end_z, color='green', marker='o', s=20, alpha=1)

	ax.set_title("Ball Trajectories")
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


def plot_gaze_ball_angle(data):
	trial = data.conditions[0].participants[0].trials[0]
	frames = trial.frames
	ball_angle = [Angles.calculate_ball_gaze_angle(
		frame.ball_position_y,
		frame.ball_position_z,
		frame.gaze_direction_y,
		frame.gaze_direction_z,
		frame.gaze_origin_y,
		frame.gaze_origin_z
	) for frame in frames]

	# plot with aspect ratio 5:2
	fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(5,5), sharex=True)

	timestamps = [frame.timestamp for frame in frames]
	bounce_event = next((event for event in trial.ball_events if isinstance(event, FirstBounceEvent)), None)


	# lambda time filter
	seconds_to_show_after_bounce = 0
	end_time = bounce_event.timestamp + seconds_to_show_after_bounce
	time_filter = lambda time: time <= end_time
	filtered_timestamps = list(filter(time_filter, timestamps))

	ax1.set_title("Ball-Gaze Angle")
	ball_angle_at_timestamps = [ball_angle[timestamps.index(time)] for time in filtered_timestamps]
	ax1.plot(filtered_timestamps, ball_angle_at_timestamps)
	ax1.axvline(x=bounce_event.timestamp, color="red", linestyle="--")
	predictive_saccades = [event for event in trial.gaze_events if isinstance(event, PredictiveSaccade)]

	y_limits = (50, -50)
	for saccade in predictive_saccades:
		ax1.fill_between(
			[saccade.timestamp, saccade.start_frame.timestamp], y_limits[1], y_limits[0], color="green",
			alpha=0.2
		)
		ax2.plot(saccade.start_frame.timestamp, saccade.angle_start, "go")
		ax2.plot(saccade.frame.timestamp, saccade.angle_end, "go")

	ax1.set_ylim(y_limits)
	ax1.invert_yaxis()

	ax1.set_ylabel("Angle [deg]")
	# ax1.legend(
	# 	[
	# 		"Ball-Gaze angle. Positive values indicate gaze is above the ball",
	# 		"Ball Bounce",
	# 		"Predictive Saccade"
	# 	]
	# )

	# legend but outside of plot
	# ax1.legend(
	# 	[
	# 		"Ball-Gaze angle. Positive values indicate gaze is above the ball",
	# 		"Ball Bounce",
	# 		"Predictive Saccade"
	# 	],
	# 	loc="upper center",
	# 	bbox_to_anchor=(0.5, -0.1),
	# 	fancybox=True,
	# 	shadow=True,
	# )

	# # add a suptitle and a rich text description
	# fig.suptitle("Ball-Gaze Angle", fontsize=16)
	# fig.text(
	# 	"Positive values indicate gaze is above the ball",
	# 	ha="center",
	# 	va="center",
	# 	fontsize=12,
	# 	y=0.95,
	# 	s=0.95
	# )


	ax2.set_title("Ball-World Angle")
	gaze_world_y = [frame.gaze_direction_y for frame in frames]
	gaze_world_z = [frame.gaze_direction_z for frame in frames]
	gaze_world_angle = [Angles.calculate_gaze_world_angle(gaze_world_y[i], gaze_world_z[i]) for i in
						range(len(gaze_world_y))]
	gaze_world_angle_at_timesteps = [gaze_world_angle[timestamps.index(time)] for time in filtered_timestamps]
	ax2.plot(filtered_timestamps, gaze_world_angle_at_timesteps)
	ax2.set_ylabel("Angle [deg]")


	# plot ball trajectory y in ax2
	ax3.set_title("Ball Flight Curve")
	ball_position_y_at_timesteps = [frame.ball_position_y for frame in frames if time_filter(frame.timestamp)]
	ax3.plot(filtered_timestamps, ball_position_y_at_timesteps)
	ax3.set_ylim((0, 5))
	ax3.set_ylabel("Ball [m]")
	ax3.set_xlabel("Time [s]")
	return plt
