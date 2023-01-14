import pkg_resources

from .services.processing.ball_events import BallEvents
from .services.processing.gaze_events import GazeEvents
from .services.io.load import load_condition
from .models.experiment import ExperimentalData
from .services.plots.plots import plot_3d, plot_birdview, plot_side, plot_gaze_ball_angle


def path_to_folder_with_csv_data():
    folder_path = pkg_resources.resource_filename('vrgaze', 'example_data/tennis_data/experimental_condition/')
    return folder_path