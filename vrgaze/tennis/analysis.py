from dataclasses import dataclass
from typing import List


@dataclass
class Trajectory:
	length: List[float]
	height: List[float]
	width: List[float]
