# Handles primary communication between the controller and model

import numpy as np
from view import AppWindow

from .figures import newFrequencyFigure, newSpectrogramFigure
# external variables that store state
current_sample_rate = None
current_data = None
window = None


def get_window_instance(app: AppWindow):
    global window
    window = app


def receiveSoundFile(sample_rate, data):
    """
    Called by the controller when a new file should be extracted.

    Takes in the sample_rate and a numpy array of data that represents the audio file.
    """

    global current_sample_rate
    global current_data

    # updates internal state
    current_sample_rate = sample_rate
    current_data = data

    # TODO pass newly created figures to the view
    #
    # window.update_images(some_data_for_the_view)