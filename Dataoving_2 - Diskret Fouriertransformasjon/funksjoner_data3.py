import matplotlib.pyplot as plt
from numpy import arange, absolute, angle

def timeSpectrumStem(xn, Xk, N):
    plt.subplot(3,1,1)
    n = arange(N)
    # Create Stem Plot of discrete-time signal x[n]
    plt.stem(n, xn, linefmt = None, markerfmt ='.', basefmt = 'grey',use_line_collection=True)
    plt.xlim([0, N])
    plt.ylabel(r'x[n]')
    plt.subplot(3,1,2)
    # Create Stem Plot of DFT magnitude |X[k]|
    plt.stem(n, absolute(Xk), linefmt = None, markerfmt ='.', basefmt = 'grey',use_line_collection=True)
    plt.grid(True)
    plt.xlim([0, N])
    plt.ylabel(r'$|X[k]|$')
    plt.subplot(3,1,3)
    # Create Stem Plot of DFT angle <X[k]. Disregard spectral components |X[k]| < 1e-13
    plt.stem(n, 
             angle(Xk)*(absolute(Xk)>1e-12),
             linefmt = None, markerfmt ='.',
             basefmt = 'grey',
             use_line_collection=True)
    plt.grid(True)
    plt.xlim([0, N])
    plt.ylabel(r'$\angle X[k]$')
    plt.show()
    
def createTestSignal():
    N = 128
    n = arange(0, N)
    xn = sin(2*pi*2/N*n)+0.4*cos(2*pi*33*n/N - 3*pi/4)

    with open('lab3.csv', 'w', newline='') as csvfile:
        sig_writer = csv.writer(csvfile, delimiter=',')
        sig_writer.writerow(["sample","x1[n]"])
        for i in range(N):
            sig_writer.writerow([str(n[i]), str(xn[i])])
            