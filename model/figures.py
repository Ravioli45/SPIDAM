# Handles generating figures for audio files

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from .utils import calculateLength, convertToDecibels

# global variables determining figure size and dimensions for all figures passed to view
g_figSize = (16, 7)
g_dpi = 75

def newWaveformFigure(sample_rate, data):
    """
    Returns a new figure of amplitude plotted over time.
    """
    fig = Figure(g_figSize, dpi=g_dpi)

    # determines the values of the x axis
    length = calculateLength(sample_rate, data)
    xValues = np.linspace(0, length, len(data))

    # creates the x axis on the figure
    ax = fig.add_subplot(111)
    ax.set_xlim(0, length)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title("Waveform")

    # plot entire graph
    ax.plot(xValues, data)

    return fig

def newSpectrogramFigure(sample_rate, data):
    """
    Returns three arguments:
    1. a new figure of the spectrogram of the audio file and
    2. frequencies of the audio file
    3. spectrum of the audio file
    """
    fig = Figure(g_figSize, dpi=g_dpi)

    # create spectrogram axis
    ax = fig.add_subplot(111)
    spectrum, freqs, t, im = ax.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap("autumn_r"))

    # gradient of colors matched to the intensity (dB) they represent
    cbar = fig.colorbar(im)
    cbar.set_label("Intensity (dB)")

    # set relevant labels
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Frequency (Hz)")
    ax.set_title("Audio spectrogram")

    return fig, freqs, spectrum, t

def newDecibelFigure(seconds, t, decibels):
    """
    Returns a new figure of decibels over time with proper labels
    """
    dec_fig = Figure(g_figSize, dpi=g_dpi)
    ax = dec_fig.add_subplot(111)
    ax.set_xlim(0, seconds)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Power (dB)")

    ax.plot(t, decibels)

    return dec_fig

def newCombinedDecibelFigure(seconds, t, low_decibel, mid_decibel, high_decibel):
    """
    Creates a combined graphic of the low decibel, mid decibel, and high decibel graphs
    """
    combined_figure = Figure(g_figSize, dpi=g_dpi)
    ax = combined_figure.add_subplot(111)
    ax.set_xlim(0, seconds)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Power (dB)")

    ax.plot(t, low_decibel, label="Low Frequency")
    ax.plot(t, mid_decibel, label="Mid Frequency")
    ax.plot(t, high_decibel, label="High Frequency")
    ax.legend(loc="upper left")

    return combined_figure
