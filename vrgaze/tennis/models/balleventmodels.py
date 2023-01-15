from dataclasses import dataclass

from vrgaze.tennis.models.common import Event


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
