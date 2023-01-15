from dataclasses import dataclass
from typing import List

@dataclass
class SaccadeCandidate:
	start_index: int
	end_index: int
	# Flags to be set by analysis
	is_saccade_angle_bigger_than_threshold: bool = False



class SaccadeDetector:

	@staticmethod
	def get_median(values: List[float]):
		return sorted(values)[len(values) // 2]

	@staticmethod
	def find(acceleration, median_absolute_acceleration):
		start_candidates = [i for i in range(len(acceleration)) if abs(acceleration[i]) > median_absolute_acceleration]
		end_candidates = [i for i in range(len(acceleration)) if abs(acceleration[i]) < median_absolute_acceleration]

		starts = []
		ends = []
		for start in start_candidates:

			has_found_at_least_one_end = len(ends) > 0
			is_current_start_before_last_end = has_found_at_least_one_end and start < ends[-1]

			if is_current_start_before_last_end:
				continue

			for end in end_candidates:
				if end > start:
					starts.append(start)
					ends.append(end)
					break


		saccades = []
		for start, end in zip(starts, ends):
			saccades.append(SaccadeCandidate(start, end))

		return saccades
