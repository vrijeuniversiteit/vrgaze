from vrgaze.tennis import load_condition, ExperimentalData, plot_3d, plot_birdview, plot_side
from vrgaze.tennis import plot_gaze_ball_angle

"""
1. Place all experimental data in a folder called 'data' in the root of your project.
The folder structure should look like this:
project root folder/
│
├── data/
│   ├── GROUP_1_NAME/
│   │   ├── participant_1.csv
│   │   └── participant_2.csv
│   └── GROUP_2_NAME/
│       ├── participant_3.csv
│       └── participant_4.csv
│
├── THIS_SCRIPT.py

2. Set the group names (here: Experts and Novices) and the path to the data folder
"""
experts = load_condition("Experts", "data/GROUP_1_NAME/")
novices = load_condition("Novices", "data/GROUP_2_NAME/")

data = ExperimentalData([novices, experts])
data.analyze_trials()
data.to_csv("example_results.csv")

should_plot = False
if should_plot:
    plot = plot_gaze_ball_angle(data, trial_number=5)
    plot.savefig("plot_gaze_ball_angle.png")
    plot.show()

    plot = plot_3d(data)
    plot.savefig("plot_3d.png")
    plot.show()

    plot = plot_birdview(data)
    plot.savefig("plot_birdview.png")
    plot.show()

    plot = plot_side(data)
    plot.savefig("plot_side.png")
    plot.show()



