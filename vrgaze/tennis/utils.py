import math
from typing import List


class Angles:

	@staticmethod
	def calculate_ball_gaze_angle(ball_position_y, ball_position_z, direction_y, direction_z, origin_y, origin_z):
		vector_ball_y = ball_position_y - origin_y
		vector_ball_z = ball_position_z - origin_z
		angle = math.degrees(math.atan2(vector_ball_z, vector_ball_y) - math.atan2(direction_z, direction_y))
		return angle

	@staticmethod
	def calculate_gaze_world_angle(direction_y, direction_z):
		return math.degrees(math.atan2(direction_z, direction_y) - math.atan2(1, 0))


class Integration:

	@staticmethod
	def get_acceleration(positions: List[float]):
		velocity = [positions[i + 1] - positions[i] for i in range(len(positions) - 1)]
		velocity.insert(0, 0)

		acceleration = [velocity[i + 1] - velocity[i] for i in range(len(velocity) - 1)]
		acceleration.insert(0, 0)

		return acceleration


class Saccades:

	@staticmethod
	def get_median(values: List[float]):
		return sorted(values)[len(values) // 2]

	@staticmethod
	def begin_and_end_of_saccade(acceleration, median_absolute_acceleration):
		start_candidates = [i for i in range(len(acceleration)) if abs(acceleration[i]) > median_absolute_acceleration]
		end_candidates = [i for i in range(len(acceleration)) if abs(acceleration[i]) < median_absolute_acceleration]

		starts = []
		ends = []
		for start in start_candidates:

			has_found_at_least_one_end = len(ends) > 0
			is_current_start_before_last_end = has_found_at_least_one_end and start < ends[-1]

			if is_current_start_before_last_end:
				continue

			for end in end_candidates:
				if end > start:
					starts.append(start)
					ends.append(end)
					break

		return starts, ends




