import math


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
