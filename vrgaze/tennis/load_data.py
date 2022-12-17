from vrgaze.tennis.datamodel import ConditionData
from vrgaze.tennis.read import Reader


def load_condition(name: str, folder_path: str) -> ConditionData:
	"""Load data from an experimental condition

	Args:
		name (str): Name of the experimental condition.
		folder_path (str): Path to the folder containing the data files

	Returns:
		ConditionData: Data from the experimental condition

	Examples:
		>>> from vrgaze.tennis.load import load_condition
		>>> condition = load_condition("Experts", "path/to/folder")
		>>> print(condition)
		>>> Name=Experts, Participants=10

	"""

	reader = Reader()
	reader.discover_files(folder_path)
	reader.read_files()
	condition = ConditionData(name, reader.participants)

	# eventCalculator = EventCalculator()
	# eventCalculator.calculate_events(condition)
	# events = eventCalculator.events

	return condition
