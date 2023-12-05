import librosa
import model

def loadFile(path):
    try:
        y, sr = librosa.load(path, sr=None)
        model.receiveSoundFile(sr, y)
    except Exception:
        model.receiveSoundFile(None, None)
