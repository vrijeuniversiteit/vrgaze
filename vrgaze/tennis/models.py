from dataclasses import dataclass


@dataclass
class Trial:
	"""A single trial of a tennis match.

	Args:
		participant_name (str): The name of the participant.
		id (int): The trial id.
	"""
	participant_name: str