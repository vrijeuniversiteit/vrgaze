from dataclasses import field, dataclass
from typing import List

from vrgaze.tennis.models.abstraction import Visitable, Visitor
from vrgaze.tennis.models.eventmodel import PredictiveSaccade

@dataclass
class CSVWriter(Visitor):
	filepath: str
	data: List[str] = field(default_factory=list)

	def visit(self, visitable: Visitable):
		trial = visitable
		participant = trial.participant_id
		ball_number = trial.ball_number
		block_number = trial.block_number
		test_id = trial.test_id
		predictive_saccades = [event for event in trial.gaze_events if isinstance(event, PredictiveSaccade)]
		for saccade in predictive_saccades:
			self.data.append([participant, ball_number, block_number, test_id, saccade.timestamp, saccade.angle_amplitude, saccade.angle_start, saccade.angle_end])

