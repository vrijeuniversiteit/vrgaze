import textwrap

from matplotlib import pyplot as plt

from vrgaze.tennis.models.balleventmodels import FirstBounceEvent
from vrgaze.tennis.models.gazeeventmodels import PredictiveSaccade, CorrectiveSaccade
from vrgaze.tennis.services.plots.trial_finder import TrialFinder
from vrgaze.tennis.services.processing.angles import Angles


def plot_gaze_ball_angle(data, trial_number: int = 0, time_after_bounce: float = 0.2):

	finder = TrialFinder(trial_number)
	for condition in data.conditions:
		finder.visit_with_context(condition, condition.name)

	if finder.trial_not_found:
		print(f"Trial not found for plotting, searched through {finder.current_trial_number} trials...")
		return plt.figure()

	trial = finder.trial
	frames = trial.frames
	ball_angle = [Angles.calculate_ball_gaze_angle(
		frame.ball_position_y,
		frame.ball_position_z,
		frame.gaze_direction_y,
		frame.gaze_direction_z,
		frame.gaze_origin_y,
		frame.gaze_origin_z
	) for frame in frames]

	# Data streams
	timestamps = [frame.timestamp for frame in frames]
	bounce_event = next((event for event in trial.ball_events if isinstance(event, FirstBounceEvent)), None)
	ball_position_y = [frame.ball_position_y for frame in frames]

	# Figure setup
	fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, 1, figsize=(8, 8))
	y_limits = (20, -20)
	x_limits = (0, bounce_event.timestamp_start + time_after_bounce)

	# Plot 1
	ax1.set_title("Ball-Gaze Angle")
	ax1.set_xlabel("Time [s]")
	ax1.plot(timestamps, ball_angle)
	ax1.axvline(x=bounce_event.timestamp_start, color="green", linestyle="--")
	ax1.set_ylim(y_limits)
	ax1.set_xlim(x_limits)
	ax1.invert_yaxis()
	ax1.set_ylabel("Angle [deg]")
	predictive_saccades = [event for event in trial.gaze_events if isinstance(event, PredictiveSaccade)]
	for saccade in predictive_saccades:
		ax1.fill_between(
			[saccade.timestamp_start, saccade.timestamp_end], y_limits[1], y_limits[0], color="red",
			alpha=0.1
		)
		if saccade.is_within_bounce_window:
			ax1.fill_between(
				[saccade.timestamp_start, saccade.timestamp_end], y_limits[1], y_limits[0], color="red",
				alpha=1
			)

	predictive_saccades = [event for event in trial.gaze_events if isinstance(event, CorrectiveSaccade)]
	for saccade in predictive_saccades:
		ax1.fill_between(
			[saccade.timestamp_start, saccade.timestamp_end], y_limits[1], y_limits[0], color="blue",
			alpha=0.1
		)

	# Description of Plot 1
	ax2.axis("off")
	text = "The green line shows the moment of ball bounce. All the predictive saccades are highlighted. Corrective " \
		   "saccades are highlighted in light blue, the predictive saccades in light red. In case there is a " \
		   "predictive saccade within the time window of interest (e.g. the last 400 ms before before bounce) " \
		   "the predictive saccade is shown in solid red."
	wrapped_text = textwrap.fill(text)
	ax2.text(0, 1, wrapped_text, ha="left", va="top", wrap=True)

	# Plot 2
	ax3.set_title("Gaze-World Angle")
	ax3.set_ylabel("Angle [deg]")
	ax3.set_xlabel("Time [s]")
	ax3.set_ylim(y_limits)
	ax3.set_xlim(x_limits)
	ax3.invert_yaxis()
	gaze_world_y = [frame.gaze_direction_y for frame in frames]
	gaze_world_z = [frame.gaze_direction_z for frame in frames]
	gaze_world_angle = [Angles.calculate_gaze_world_angle(gaze_world_y[i], gaze_world_z[i]) for i in range(len(gaze_world_y)
	)]
	ax3.plot(timestamps, gaze_world_angle)

	# Description of Plot 2
	ax4.axis("off")
	text = "The gaze-world angle is the angle between the gaze direction and the world coordinate system."
	wrapped_text = textwrap.fill(text)
	ax4.text(0, 1, wrapped_text, ha="left", va="top", wrap=True)

	#  Plot 3
	ax5.set_title("Ball Flight Curve")
	ax5.set_ylabel("Height [m]")
	ax5.set_xlabel("Time [s]")
	ax5.plot(timestamps, ball_position_y)
	ax5.set_ylim((0, 5))

	# Description of Plot 3
	ax6.axis("off")
	text = "The ball flight curve shows the ball position in the y-direction."
	wrapped_text = textwrap.fill(text)
	ax6.text(0, 1, wrapped_text, ha="left", va="top", wrap=True)
	return plt
