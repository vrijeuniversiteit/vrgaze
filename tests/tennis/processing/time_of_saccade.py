class Timing:
	@staticmethod
	def is_within_window(ball_bounce_timestamp, duration_time_window, saccade_start_timesamps):
		earliest_start_time = ball_bounce_timestamp - duration_time_window
		is_within_window = [False] * len(saccade_start_timesamps)
		for index, saccade_start_time in enumerate(saccade_start_timesamps):
			started_before_event = saccade_start_time < ball_bounce_timestamp
			started_within_window = saccade_start_time > earliest_start_time

			if started_before_event and started_within_window:
				is_within_window[index] = True
		return is_within_window
