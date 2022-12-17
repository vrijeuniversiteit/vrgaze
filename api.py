from matplotlib import pyplot as plt

from vrgaze.tennis.models.datamodel import ExperimentalData
from vrgaze.tennis.services.ball_events import BallEvents
from vrgaze.tennis.services.gaze_events import GazeEvents
from vrgaze.tennis.services.load_data import load_condition
from vrgaze.tennis.services.writer import CSVWriter

experts = load_condition("Experts", "example_data/tennis_data/experimental_condition")
novices = load_condition("Novices", "example_data/tennis_data/experimental_condition")

data = ExperimentalData([experts, novices])

data.analyze(BallEvents())
data.analyze(GazeEvents())
data.to_csv(CSVWriter("example_data/tennis_data/example_results.csv"))

from vrgaze.tennis.services.plots import plot_3d, plot_birdview, plot_side

plot = plot_3d(data, show_predictive_saccades=True)
plot.show()

plot = plot_birdview(data)
plot.show()

plot_side(data)
plt.show()
