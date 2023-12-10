import librosa
import model
import warnings

# used to supress warnings from librosa
# since exception handling is being used
warnings.filterwarnings('ignore')

def loadFile(path):
    y = None
    sr = None
    success = False
    try:
        # librosa.load is indifferent to the presence or lack of metadata and can open .mp3 and .wav files
        # it also converts the audio to mono by default
        y, sr = librosa.load(path, sr=None)
        success = True
    except Exception:
        model.openFileError()

    if success:
        model.receiveSoundFile(sr, y)


