import pyaudio as pa
import pyopenjtalk as jt
import numpy as np


def speech(text):
    x, sr = jt.tts(text)
    a = pa.PyAudio()
    stream = a.open(rate=sr, channels=1, format=pa.paInt16, output=True)
    stream.write(x.astype(np.int16).tostring())
    stream.stop_stream()
    stream.close()


if __name__ == "__main__":
    import sys
    speech(sys.argv[1])