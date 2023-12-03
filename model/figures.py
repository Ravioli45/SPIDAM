# Handles generating figures for audio files

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from .utils import calculateLength

# global variables determining figure size and dimensions for all figures passed to view
g_figSize = (16, 7)
g_dpi = 75

def newWaveformFigure(sample_rate, data):
    """
    Returns a new figure of amplitude plotted over time.
    """
    fig = Figure(g_figSize, dpi=g_dpi)

    # determines the values of the x axis
    xValues = np.linspace(0, calculateLength(sample_rate, data), len(data))

    # creates the x axis on the figure
    ax = fig.add_subplot(111)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")

    # plot entire graph
    ax.plot(xValues, data)

    return fig

def newSpectrogramFigure(sample_rate, data):
    """
    Returns a new figure of the spectrogram of the audio file.
    """
    fig = Figure(g_figSize, dpi=g_dpi)

    # create spectrogram axis
    ax = fig.add_subplot(111)
    spectrum, freqs, t, im = ax.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap("autumn_r"))

    # gradient of colors matched to the intensity (dB) they represent
    cbar = fig.colorbar(im)

    # set relevant labels
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    cbar.set_label("Intensity (dB)")

    return fig
