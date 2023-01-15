from dataclasses import dataclass

from vrgaze.tennis.models.common import Event


@dataclass
class SaccadeCandidate:
	start_index: int
	end_index: int
	# Flags to be set by analysis
	is_eye_moving_enough: bool = False
	is_eye_moving_faster_than_ball = False
	is_within_bounce_window = False
	is_corrective = False


@dataclass
class Saccade(Event):
	start_frame: "Frame"
	angle_amplitude: float
	angle_start: float
	angle_end: float
	is_corrective: bool
	is_within_bounce_window: bool


class PredictiveSaccade(Saccade):
	pass


class CorrectiveSaccade(Saccade):
	pass
