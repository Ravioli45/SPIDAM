import librosa
from model import receiveSoundFile

def loadFile(path):
    y, sr = librosa.load(path, sr=None)
    receiveSoundFile(sr, y)