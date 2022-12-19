from abc import ABC, abstractmethod


class Visitable(ABC):
	@abstractmethod
	def analyze(self, visitor: "Visitor"):
		...


class Visitor(ABC):
	@abstractmethod
	def visit(self, trial: Visitable):
		...

	@abstractmethod
	def visit_with_context(self, trial: Visitable, condition_name: str):
		...
