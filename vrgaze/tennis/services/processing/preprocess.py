from vrgaze.tennis.models.common import Visitor
from vrgaze.tennis.models.datamodel import Condition, Trial


# TODO: Implement preprocessor to interpolate missing frames (gaze where not valid)
class Preprocess(Visitor):
	def visit_condition(self, condition: Condition, condition_name: str):
		pass

	def visit(self, trial: Trial):
		pass
