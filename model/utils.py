# Provides calculations related to audio and sound design

import numpy as np

def calculateLength(sample_rate, data):
    """
    Returns the length, in seconds, of the audio 
    
    sample_rate is frequency in Hz
    data is an array of amplitudes measured at the sample_rate
    """
    return len(data)/sample_rate
