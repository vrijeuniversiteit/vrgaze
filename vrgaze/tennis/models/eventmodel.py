from dataclasses import dataclass



@dataclass
class Event:
	timestamp: float
	frame: "Frame"


class BallCrossesNetAfterServe(Event):
	pass


class BallHitWithRacket(Event):
	pass


class FirstBounceEvent(Event):
	pass


@dataclass
class Saccade(Event):
	start_frame: "Frame"
	angle_amplitude: float
	angle_start: float
	angle_end: float

class PredictiveSaccade(Saccade):
	pass

class CorrectiveSaccade(Saccade):
	pass
