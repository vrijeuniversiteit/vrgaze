import pkg_resources

from .services.processing.ball_events import BallEvents
from .services.processing.gaze_events import GazeEvents
from .services.io.load import load_condition
from .models.experiment import ExperimentalData
from .services.plots.plot_gaze_ball_angle import plot_gaze_ball_angle
from .services.plots.plot_side import plot_side
from .services.plots.plot_birdview import plot_birdview
from .services.plots.plot_3d import plot_3d


def path_to_folder_with_csv_data():
    folder_path = pkg_resources.resource_filename('vrgaze', 'example_data/tennis_data/experimental_condition/')
    return folder_path