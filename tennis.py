from vrgaze.tennis import load_condition, ExperimentalData, plot_3d, plot_birdview, plot_side
from vrgaze.tennis import plot_gaze_ball_angle

"""
1. Copy this script and put it at the root/main folder of your project. Call the script `main.py`.
2. Place all experimental data (csv files) in a folder called 'data' in the root of your project.
3. Inside of the folder, it is possible to creat sub-folders for each experimental conditions. See the function load_condition for more details.
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
├── main.py

4. Set the group names in this script (here for example: Experts and Novices) 
5. Set the path to the data folder (where the data is located, relative to this script)
6. Run this script
"""

experts = load_condition("Experts", "data/GROUP_1_NAME")
novices = load_condition("Novices", "data/GROUP_2_NAME")

data = ExperimentalData([novices, experts])
data.analyze_trials()
data.to_csv("example_results.csv")

should_plot = True
if should_plot:
    # Visualize the gaze data for a specific trial
    # Adjust the desired trial as needed or loop over all trials to generate plots for all trials
    DESIRED_TRIAL = 5
    plot = plot_gaze_ball_angle(data, trial_number=DESIRED_TRIAL)
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



