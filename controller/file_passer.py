import librosa
import model

def loadFile(path):
    y, sr = librosa.load(path, sr=None)
    model.receiveSoundFile(sr, y)