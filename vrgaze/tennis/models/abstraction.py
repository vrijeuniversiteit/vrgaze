from abc import ABC, abstractmethod


class Visitable(ABC):
	@abstractmethod
	def analyze(self, visitor: "Visitor"):
		...


class Visitor(ABC):
	@abstractmethod
	def visit(self, trial: Visitable):
		...
