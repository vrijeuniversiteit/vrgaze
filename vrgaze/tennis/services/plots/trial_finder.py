from dataclasses import dataclass

from vrgaze.tennis.models.common import Visitor, Visitable
from vrgaze.tennis.models.datamodel import Trial


@dataclass
class TrialFinder(Visitor):
	desired_trial_number: int
	current_trial_number: int = 0
	condition_name: str = ""
	trial: Trial = None

	@property
	def trial_not_found(self):
		return self.trial is None

	def visit_with_context(self, trial: Visitable, condition_name: str):
		self.condition_name = condition_name
		trial.process(self)
		pass

	def visit(self, trial: Visitable):
		self.current_trial_number += 1
		if self.current_trial_number == self.desired_trial_number:
			self.trial = trial
		pass
