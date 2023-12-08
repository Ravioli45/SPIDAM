import librosa
import model

def loadFile(path):
    y = None
    sr = None
    success = False
    try:
        y, sr = librosa.load(path, sr=None)
    except Exception:
        model.openFileError()

    if success:
        model.receiveSoundFile(sr, y)


