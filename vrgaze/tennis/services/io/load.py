from vrgaze.tennis.models.datamodel import ConditionData
from vrgaze.tennis.services.io.read import Reader


def load_condition(name: str, folder_path: str) -> ConditionData:
	"""Load data from an experimental condition

	Args:
		name (str): Name of the experimental condition.
		folder_path (str): Path to the folder containing the data files

	Returns:
		ConditionData: Data from the experimental condition

	Examples:
		# For a single condition:
		>>> condition = load_condition("Experts", "path/to/folder")
		>>> print(condition)
		>>> Name=Experts, Participants=10
		>>>
		>>> data = ExperimentalData(condition)



		# For several conditions:
		>>> experts = load_condition("Experts", "path/to/folder")
		>>> novices = load_condition("Novices", "path/to/folder")
		>>> data = ExperimentalData([experts, novices])
	"""

	reader = Reader()
	reader.discover_files(folder_path)
	reader.read_files()
	condition = ConditionData(name, reader.participants)

	return condition
