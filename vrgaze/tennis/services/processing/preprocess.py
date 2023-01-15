from vrgaze.tennis.models.common import Visitor, Visitable


# TODO: Implement preprocessor to interpolate missing frames (gaze where not valid)
class Preprocess(Visitor):
	def visit_with_context(self, trial: Visitable, condition_name: str):
		pass

	def visit(self, trial: Visitable):
		pass
