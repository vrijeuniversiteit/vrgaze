from matplotlib import pyplot as plt

from vrgaze.tennis.load_data import load_condition
from vrgaze.tennis.models import ExperimentalData

experts = load_condition("Experts", "example_data/tennis_data/experimental_condition")
novices = load_condition("Novices", "example_data/tennis_data/experimental_condition")

data = ExperimentalData([experts, novices])



from vrgaze.tennis.plots import plot_3d, plot_birdview, plot_side

plot = plot_3d(data)
plot.show()

plot = plot_birdview(data)
plot.show()

plot_side(data)
plt.show()
