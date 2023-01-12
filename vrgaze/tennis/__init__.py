import pkg_resources

from .services.ball_events import BallEvents
from .services.gaze_events import GazeEvents
from .services.load import load_condition
from .models.experiment import ExperimentalData

from vrgaze.tennis.services.plots import plot_3d, plot_birdview, plot_side, plot_gaze_ball_angle

def path_to_folder_with_csv_data():
    folder_path = pkg_resources.resource_filename('vrgaze', 'example_data/tennis_data/experimental_condition/')
    return folder_path