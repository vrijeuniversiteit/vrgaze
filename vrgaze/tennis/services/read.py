import glob
import os

from vrgaze.tennis.models.datamodel import Trial, Frame, Participant

class Reader:
	def __init__(self):
		self.number_files = 0
		self.participants = []
		self.trials = []
		self.frames = []
		self.files = []

	def discover_files(self, path):
		if not os.path.exists(path):
			raise FileNotFoundError(f"Folder {path} does not exist.")

		files = glob.glob(path + "/*.csv")
		self.number_files = len(files)
		self.files = files

	def read_files(self):
		participants = []
		for file in self.files:
			with open(file, "r") as file:
				content = file.readlines()
				expected_header = 'participant_id,test_id,block_number,ball_number,timestamp,ball_position_x,ball_position_y,ball_position_z,shortest_path_normalized_x,shortest_path_normalized_y,shortest_path_normalized_z,look_direction_normalized_x,look_direction_normalized_y,look_direction_normalized_z,result_location_x,result_location_y,result_location_z,target_type,distance_to_closest_target,smi_camera_raycast_x,smi_camera_raycast_y,smi_camera_raycast_z,smi_binocular_por_x,smi_binocular_por_y,smi_binocular_por_is_valid,smi_ipd,smi_ipd_is_valid,smi_left_por_x,smi_left_por_y,smi_left_por_is_valid,smi_right_por_x,smi_right_por_y,smi_right_por_is_valid,smi_left_basepoint_x,smi_left_basepoint_y,smi_left_basepoint_z,smi_left_basepoint_is_valid,smi_right_basepoint_x,smi_right_basepoint_y,smi_right_basepoint_z,smi_right_basepoint_is_valid,smi_left_gazedirection_x,smi_left_gazedirection_y,smi_left_gazedirection_z,smi_left_gazedirection_is_valid,smi_right_gazedirection_x,smi_right_gazedirection_y,smi_right_gazedirection_z,smi_right_gazedirection_is_valid,tobii_gazeray_isvalid,tobii_gazeray_origin_x,tobii_gazeray_origin_y,tobii_gazeray_origin_z,tobii_gazeray_direction_x,tobii_gazeray_direction_y,tobii_gazeray_direction_z,tobii_left_pupil_isvalid,tobii_left_pupildiameter,tobii_left_ray_isvalid,tobii_left_ray_origin_x,tobii_left_ray_origin_y,tobii_left_ray_origin_z,tobii_left_ray_direction_x,tobii_left_ray_direction_y,tobii_left_ray_direction_z,tobii_right_pupil_isvalid,tobii_right_pupildiameter,tobii_right_ray_isvalid,tobii_right_ray_origin_x,tobii_right_ray_origin_y,tobii_right_ray_origin_z,tobii_right_ray_direction_x,tobii_right_ray_direction_y,tobii_right_ray_direction_z,participant_head_position_x,participant_head_position_y,participant_head_position_z,participant_head_rotation_x,participant_head_rotation_y,participant_head_rotation_z,racket_knob_position_x,racket_knob_position_y,racket_knob_position_z,racket_knob_rotation_x,racket_knob_rotation_y,racket_knob_rotation_z\n'
				if content[0] != expected_header:
					raise ValueError(f"File {file} does not have the expected header.")

				ball_number_changes = []
				for i in range(1, len(content)):
					if content[i].split(",")[3] != content[i - 1].split(",")[3]:
						ball_number_changes.append(i)

				trials = []
				for i in range(len(ball_number_changes)):
					start = ball_number_changes[i]
					end = ball_number_changes[i + 1] if i + 1 < len(ball_number_changes) else len(content)
					frames = []
					last_frame = 1
					for line in content[start:end - last_frame]:
						parts = line.split(",")
						frames.append(
							Frame(
								timestamp=float(parts[4]),
								ball_position_x=float(parts[5]),
								ball_position_y=float(parts[6]),
								ball_position_z=float(parts[7])
							)
						)
					trials.append(
						Trial(
							participant_id=int(parts[0]),
							test_id=int(parts[1]),
							block_number=int(parts[2]),
							ball_number=int(parts[3]),
							frames=frames
						)
					)

			participants.append(
				Participant(
					participant_id=int(parts[0]),
					trials=trials
				)
			)

			self.participants = participants


class Validator:
	@staticmethod
	def validate_header(expected: str, actual: str):
		if actual != expected:
			raise ValueError(f"The csv file has a different heading than expected.")
