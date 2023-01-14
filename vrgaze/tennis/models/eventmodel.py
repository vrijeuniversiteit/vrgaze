from dataclasses import dataclass


@dataclass
class Event:
	timestamp: float
	frame: "Frame"


class BallCrossesNetAfterServe(Event):
	pass


class BallHitWithRacket(Event):
	pass


@dataclass
class FirstBounceEvent(Event):
	pass

class BallHitFrontWall(Event):
	"""Ball was returned too hard and hit the front wall before landing on the court"""
	pass

class SecondBounceEvent(Event):
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
