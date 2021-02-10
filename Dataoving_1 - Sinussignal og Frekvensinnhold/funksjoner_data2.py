import numpy as np
import matplotlib.pyplot as plt

def displayDualSpectrum(x, fs, color=None, label=None):
    N = len(x)
    Xk = np.fft.fft(x)/N
    Xk = np.fft.fftshift(Xk)
    f = np.array(np.arange(-fs/2, fs/2, fs/N))
    plt.xlim([-fs/2, fs/2])
    plt.plot(f, np.abs(Xk), color=color, label=label)
    plt.xlabel("Frekvens (Hz)")
    plt.grid(True)
    plt.ylim(ymin=0)
