from vrgaze.tennis import load_condition, ExperimentalData, path_to_folder_with_csv_data, plot_3d, plot_birdview, plot_side
from vrgaze.tennis import plot_gaze_ball_angle

# Place all experimental data in a folder called 'data' in the root of your project.
# Replace the second parameter below with the location of your data folder (e.g., 'data/experts/')
experts = load_condition("Experts", path_to_folder_with_csv_data())
novices = load_condition("Novices", path_to_folder_with_csv_data())

data = ExperimentalData([novices, experts])

data.analyze_trials()

plot = plot_gaze_ball_angle(data, trial_number=5)
plot.savefig("plot_gaze_ball_angle.png")
plot.show()

plot = plot_3d(data)
plot.savefig("plot_3d.png")
plot.show()

plot = plot_birdview(data)
plot.savefig("plot_birdview.png")
plot.show()

plot_side(data)
plot.savefig("plot_side.png")
plot.show()

data.to_csv("example_results.csv")

