# Handles generating figures for audio files

import matplotlib.pyplot as plt

def newWaveformFigure(data):
    """
    Returns a new figure of frequency plotted over time.
    """
    fig = plt.figure()

    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.plot(data)

    return fig

def newSpectrogramFigure(sample_rate, data):
    """
    Returns a new figure of the spectrogram of the audio file.
    """
    fig = plt.figure()
    spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap("autumn_r"))

    cbar = plt.colorbar(im)
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    cbar.set_label("Intensity (dB)")

    return fig
