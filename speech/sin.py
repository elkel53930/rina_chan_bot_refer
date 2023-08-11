import numpy as np
from scipy.io.wavfile import write

freq = 440
x = np.linspace(0,10,160000)
y=np.sin(2 * np.pi * x * freq)
write("sin.wav", rate = 16000, data = y)