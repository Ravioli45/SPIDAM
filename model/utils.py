# Provides calculations related to audio and sound design

import numpy as np

def calculateLength(sample_rate, data):
    """
    Returns the length, in seconds, of the audio 
    
    sample_rate is frequency in Hz
    data is an array of amplitudes measured at the sample_rate
    """
    return len(data)/sample_rate

def getClosestValue(values, target):
    """
    Returns the index of the frequency value in freqs closest to freq
    """
    array = np.asarray(values)
    i = (np.abs(array - target)).argmin()
    return array[i]

def convertToDecibels(data):
    """
    Returns the decibel values of an audio file relative to itself.

    Expects data as a numpy array in amplitude.
    """
    return 10 * np.log10(data)

def getDecibels(spectrum, freqs, targetFreq):
    """
    Returns the audio's decibel values by trying to match targetFreq to the closest sampled
    frequency.
    """

    closestFreq = getClosestValue(freqs, targetFreq)
    freqIndex = np.where(freqs == closestFreq)[0][0]
    return convertToDecibels(spectrum[freqIndex])

def calculateRT60(decibels, times):
    """
    Calculates the RT60 value of the audio by taking the difference in time between a decibel
    value of max - 5 dB and a decibel value of max - 25 dB

    Returns a tuple:
    [0] RT60
    [1] maximum decibel index
    [2] maximum decibel value
    """

    indexMax = np.argmax(decibels)
    valueMax = decibels[indexMax]

    # slice array to eliminate algorithm finding values before the max
    postMax = decibels[indexMax:]

    # value and index minus 5 dB
    valueMaxM5 = getClosestValue(postMax, valueMax - 5)
    indexMaxM5 = np.where(postMax == valueMaxM5)[0][0]

    # value and index minus 25 dB
    valueMaxM25 = getClosestValue(postMax, valueMax - 25)
    indexMaxM25 = np.where(postMax == valueMaxM25)[0][0]

    offset = len(decibels) - len(postMax)

    rt20 = times[indexMaxM25 + offset] - times[indexMaxM5 + offset]

    return (3 * rt20, indexMax, valueMax, indexMaxM25 + offset)

def calculateResonantFreq(spectrum, freqs):
    """
    Calculates the resonant frequency given spectrum and frequencies.

    Resonant frequency is the frequency at which the greatest power (in dB) occurs.
    Since the application converts amplitude to dB with 10 * log10(amp), no conversion to decibels
    is actually done as it is not necessary (the greatest amp should result in the greatest dB).
    """
    val = spectrum.argmax()
    indices = np.unravel_index(val, spectrum.shape)
    res_freq = freqs[indices[0]]
    return res_freq
