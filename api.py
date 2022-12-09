from dataclasses import dataclass
from typing import List

from matplotlib import pyplot as plt

from vrgaze.tennis.load_data import load_condition
from vrgaze.tennis.models import ExperimentalData

experts = load_condition("Experts", "example_data/tennis_data/experimental_condition")
novices = load_condition("Novices", "example_data/tennis_data/experimental_condition")

data = ExperimentalData([experts, novices])

@dataclass
class Trajectory:
	length: List[float]
	height: List[float]
	width: List[float]

trial = data.conditions[0].participants[0].trials[0]
trajectories = []
for trial in data.conditions[0].participants[0].trials:
	length = [frame.ball_position_z for frame in trial.frames]
	height = [frame.ball_position_y for frame in trial.frames]

	trajectories.append(Trajectory(length, height, []))

for trajectory in trajectories:
	plt.plot(trajectory.length, trajectory.height)

# label text
plt.xlabel("Length [m]")
plt.ylabel("Height [m]")

# add a small line to represent the tennis net
plt.plot([0, 0], [0, 1.065], color="black", linewidth=2)

# add a blue line to repreent the length of the court
half_court = 23.77 / 2
plt.plot([-half_court, half_court], [0, 0], color="lightblue", linewidth=1)

plt.show()

