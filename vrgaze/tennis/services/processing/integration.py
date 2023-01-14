from typing import List


class Integration:

	@staticmethod
	def get_acceleration(positions: List[float]):
		velocity = [positions[i + 1] - positions[i] for i in range(len(positions) - 1)]
		velocity.insert(0, 0)

		acceleration = [velocity[i + 1] - velocity[i] for i in range(len(velocity) - 1)]
		acceleration.insert(0, 0)

		return acceleration
