from abc import ABC, abstractmethod
from dataclasses import dataclass


class Visitable(ABC):
	@abstractmethod
	def process(self, visitor: "Visitor"):
		...


class Visitor(ABC):
	@abstractmethod
	def visit(self, trial: Visitable):
		...

	@abstractmethod
	def visit_with_context(self, trial: Visitable, condition_name: str):
		...

@dataclass
class Event:
	timestamp_start: float
	frame: "Frame"
