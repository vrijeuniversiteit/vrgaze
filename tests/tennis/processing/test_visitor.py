import unittest
from dataclasses import dataclass

from vrgaze.tennis.models.abstraction import Visitor, Visitable


class TestVisitor(unittest.TestCase):
	def test_visitor_should_iterate_over_all_trials(self):
		"""Visitor should iterate over all conditions."""
		visitor = MockVisitor()
		data = MockExperiment()
		data.process(visitor)
		self.assertEqual(visitor.number_trials_visited, 4)


class MockExperiment(Visitable):

	def __init__(self, ):
		self.conditions = [MockCondition(), MockCondition()]

	def process(self, visitor: "Visitor"):
		for condition in self.conditions:
			condition.process(visitor)


class MockCondition(Visitable):

	def __init__(self, ):
		self.trials = [MockTrial(), MockTrial()]

	def process(self, visitor: "Visitor"):
		for trial in self.trials:
			trial.process(visitor)


class MockTrial(Visitable):
	def process(self, visitor: "Visitor"):
		visitor.visit(self)


@dataclass
class MockVisitor(Visitor):
	number_trials_visited = 0

	def visit_with_context(self, trial: Visitable, condition_name: str):
		pass

	def visit(self, trial: Visitable):
		self.number_trials_visited += 1
