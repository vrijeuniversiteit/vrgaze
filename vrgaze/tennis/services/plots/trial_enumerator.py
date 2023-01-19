from dataclasses import dataclass

from vrgaze.tennis.models.common import Visitor
from vrgaze.tennis.models.datamodel import Trial, Condition


@dataclass
class TrialEnumerator(Visitor):
	trials = []

	def visit_condition(self, condition: Condition, condition_name: str):
		pass

	def visit(self, trial: Trial):
		self.trials.append(trial)
