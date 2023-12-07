# Handles primary communication between the controller and model

import numpy as np
import matplotlib.pyplot as plt
from view import AppWindow

from .figures import newWaveformFigure, newSpectrogramFigure, newDecibelFigure
from .utils import getDecibels, calculateRT60, calculateLength

# external variables that store state
g_current_sample_rate = None
g_current_data = None
g_window = None

# constants for low, mid, and high frequencies
g_lowFreq = 1000
g_midFreq = 2500
g_highFreq = 5000

def get_window_instance(app: AppWindow):
    global window
    window = app


def receiveSoundFile(sample_rate, data):
    """
    Called by the controller when a new file should be extracted.

    Takes in the sample_rate and a numpy array of data that represents the audio file.
    """

    # TODO
    # Error information should be passed over to view
    # Consider the controller calling a separate function that indicates some exception or error
    # so that the code more clearly expresses its intention.
    if sample_rate is None or data is None:
        pass


    global g_current_sample_rate
    global g_current_data

    # updates internal state
    g_current_sample_rate = sample_rate
    g_current_data = data

    # creates new figures
    waveform = newWaveformFigure(sample_rate, data)
    specgram, freqs, spectrum = newSpectrogramFigure(sample_rate, data)

    times = np.linspace(0, calculateLength(sample_rate, data), len(data))

    # perform RT60 calculations for low, mid, and high frequencies
    low_freq_decibels = getDecibels(spectrum, freqs, g_lowFreq)
    low_freq_calc = calculateRT60(low_freq_decibels, times)

    mid_freq_decibels = getDecibels(spectrum, freqs, g_midFreq)
    mid_freq_calc = calculateRT60(mid_freq_decibels, times)
    
    high_freq_decibels = getDecibels(spectrum, freqs, g_highFreq)
    high_freq_calc = calculateRT60(high_freq_decibels, times)

    # TODO
    # retrieve relevant decibel information for each frequency (low, mid, and high) and create
    # labelled figures to send to the view
    # low_fig = newDecibelFigure(sample_rate, low_freq_decibels)
    # mid_fig = newDecibelFigure(sample_rate, low_freq_decibels)
    # high_fig = newDecibelFigure(sample_rate, low_freq_decibels)

    # passes figures to the view
    window.update_images(waveform)

    # frees memory used by figures
    plt.close(waveform)
    plt.close(specgram)
    # plt.close(low_fig)
    # plt.close(mid_fig)
    # plt.close(high_fig)