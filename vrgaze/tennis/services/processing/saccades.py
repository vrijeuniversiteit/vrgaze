from typing import List


class Saccades:

	@staticmethod
	def get_median(values: List[float]):
		return sorted(values)[len(values) // 2]

	@staticmethod
	def begin_and_end_of_saccade(acceleration, median_absolute_acceleration):
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

		return starts, ends
