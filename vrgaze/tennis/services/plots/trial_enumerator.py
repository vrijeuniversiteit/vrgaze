from dataclasses import dataclass

from vrgaze.tennis.models.common import Visitor, Visitable


@dataclass
class TrialEnumerator(Visitor):
	trials = []

	def visit_with_context(self, trial: Visitable, condition_name: str):
		pass

	def visit(self, trial: Visitable):
		self.trials.append(trial)