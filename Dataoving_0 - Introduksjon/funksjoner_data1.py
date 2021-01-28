from numpy import arange, linspace, log10   # Sentrale funksjoner for oppgaven
from scipy.signal import welch              # Lar oss generere et efektspekter for å analsyer et signal i frekvensplanet
import matplotlib.pyplot as plt             # Importer pyplot modulen i matplotlib med prefiks "plt"


def signalAnalyzer(xn, fs, n_start, n_stop):
    N = len(xn)
    if (n_start >= N) or (n_stop > N):
        print("Error: index out of bounds.")
    elif (n_start >= n_stop):
        print("Error: end sample for segment must be greater than start sample.")
    else:
        M = n_stop - n_start
        plt.figure(figsize=(10, 14))
        xn_sub = xn[n_start:n_stop]

        t = linspace(n_start*1.0/fs, n_stop*1.0/fs, M, False)
        f, Sxx_sub = welch(xn_sub, fs, 'hamming', int(M/4), int(M/8), int(M/2))
        
        plt.subplot(11,1,(1, 4))
        plt.plot(t, xn_sub)
        plt.xlim(n_start*1.0/fs, n_stop*1.0/fs)
        plt.xlabel("Time t (s)")
        plt.ylabel("Signal Value x(t)")
        plt.grid(True)
        plt.title("Selected Signal Segment")
        
        plt.subplot(11,1,(6, 9))
        plt.plot(f, 10*log10(Sxx_sub))
        plt.xlim(0, fs/2)
        plt.xlabel("Frequency f (Hz)")
        plt.ylabel("Power Pxx(f) (dB)")
        plt.grid(True)
        plt.title("Signal Segment Frequency Spectrum")
        
        plt.subplot(11, 1, 11)
        plt.plot(arange(0, N*1.0/fs, 1/fs), xn)
        plt.plot(t, xn_sub, color='#D95319')
        plt.xlim(0, N*1.0/fs)
        plt.yticks([])
        plt.xticks([0, n_start*1.0/fs, n_stop*1.0/fs, N*1.0/fs])
        plt.xlabel("Time t (s)")
        plt.grid(True)
        plt.title("Full Signal plot")

def signalAnalyzer2(xn, fs, n_start, n_stop):
    N = len(xn)
    if (n_start >= N) or (n_stop > N):
        print("Error: index out of bounds.")
    elif (n_start >= n_stop):
        print("Error: end sample for segment must be greater than start sample.")
    else:
        M = n_stop - n_start
        
        xn_sub = xn[n_start:n_stop]

        t = linspace(n_start*1.0/fs, n_stop*1.0/fs, M, False)
        f, Sxx_sub = welch(xn_sub, fs, 'hamming', int(M/4), int(M/8), int(M/2))
        
        plt.figure(figsize=(10, 6))
        plt.plot(t, xn_sub)
        plt.xlim(n_start*1.0/fs, n_stop*1.0/fs)
        plt.xlabel("Time t (s)")
        plt.ylabel("Signal Value x(t)")
        plt.grid(True)
        plt.title("Selected Signal Segment")
        
        plt.figure(figsize=(10, 6))
        plt.plot(f, 10*log10(Sxx_sub))
        plt.xlim(0, fs/2)
        plt.xlabel("Frequency f (Hz)")
        plt.ylabel("Power Pxx(f) (dB)")
        plt.grid(True)
        plt.title("Signal Segment Frequency Spectrum")
        
        plt.figure(figsize=(10, 2))
        plt.plot(arange(0, N*1.0/fs, 1/fs), xn)
        plt.plot(t, xn_sub, color='#D95319')
        plt.xlim(0, N*1.0/fs)
        plt.yticks([])
        plt.xticks([0, n_start*1.0/fs, n_stop*1.0/fs, N*1.0/fs])
        plt.xlabel("Time t (s)")
        plt.grid(True)
        plt.title("Full Signal plot")
