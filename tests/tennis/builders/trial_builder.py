from unittest.mock import MagicMock

from vrgaze.tennis.models.datamodel import Frame, Trial


class TrialBuilder:
	def __init__(self):
		self.frames = []
		self.timestamps = []
		self.ball_position_z = []
		self.ball_position_y = []
		self.gaze_origin_x = []
		self.gaze_origin_y = []
		self.gaze_origin_z = []
		self.gaze_direction_x = []
		self.gaze_direction_y = []
		self.gaze_direction_z = []

	def with_frame(self, timestamp: float, ball_position_z: float, ball_position_y: float):
		self.timestamps.append(timestamp)
		self.ball_position_z.append(ball_position_z)
		self.ball_position_y.append(ball_position_y)
		return self

	def with_gaze(
		self,
		timestamp: float,
		ball_position_z: float,
		ball_position_y: float,
		gaze_origin_x: float,
		gaze_origin_y: float,
		gaze_origin_z: float,
		gaze_direction_x: float,
		gaze_direction_y: float,
		gaze_direction_z: float,
	):
		self.timestamps.append(timestamp)
		self.ball_position_z.append(ball_position_z)
		self.ball_position_y.append(ball_position_y)
		self.gaze_origin_x.append(gaze_origin_x)
		self.gaze_origin_y.append(gaze_origin_y)
		self.gaze_origin_z.append(gaze_origin_z)
		self.gaze_direction_x.append(gaze_direction_x)
		self.gaze_direction_y.append(gaze_direction_y)
		self.gaze_direction_z.append(gaze_direction_z)
		return self

	def build(self):
		if len(self.gaze_origin_x) == 0:
			self.append_ball_data()
		else:
			self.append_ball_and_gaze()

		trial = MagicMock(spec=Trial)
		trial.frames = self.frames
		return trial

	def append_ball_and_gaze(self):
		for timestamp, ball_position_z, ball_position_y, gaze_origin_x, gaze_origin_y, gaze_origin_z, gaze_direction_x, gaze_direction_y, gaze_direction_z in zip(
				self.timestamps,
				self.ball_position_z,
				self.ball_position_y,
				self.gaze_origin_x,
				self.gaze_origin_y,
				self.gaze_origin_z,
				self.gaze_direction_x,
				self.gaze_direction_y,
				self.gaze_direction_z,
		):
			frame = MagicMock(spec=Frame)
			frame.timestamp = timestamp
			frame.ball_position_z = ball_position_z
			frame.ball_position_y = ball_position_y
			frame.gaze_origin_x = gaze_origin_x
			frame.gaze_origin_y = gaze_origin_y
			frame.gaze_origin_z = gaze_origin_z
			frame.gaze_direction_x = gaze_direction_x
			frame.gaze_direction_y = gaze_direction_y
			frame.gaze_direction_z = gaze_direction_z
			self.frames.append(frame)

	def append_ball_data(self):
		for timestamp, ball_position_z, ball_position_y in zip(
				self.timestamps,
				self.ball_position_z,
				self.ball_position_y,
		):
			frame = MagicMock(spec=Frame)
			frame.timestamp = timestamp
			frame.ball_position_z = ball_position_z
			frame.ball_position_y = ball_position_y
			self.frames.append(frame)

