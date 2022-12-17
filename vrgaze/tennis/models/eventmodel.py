from dataclasses import dataclass

from vrgaze.tennis.models.datamodel import Frame


@dataclass
class Event:
	timestamp: float
	frame: Frame


class BallCrossesNetAfterServe(Event):
	pass


class BallHitWithRacket(Event):
	pass


class FirstBounceEvent(Event):
	pass
