import matplotlib.pyplot as plt
import numpy as np

Fs = 100;  # sampling rate, how many samples we take
Ts = 1.0/Fs; # sampling interval
t = np.arange(0,1,Ts) # time vector

ff1 = 5;   # frequency of the signal
y1 = np.sin(2*np.pi*ff1*t)

ff2 = 10;   # frequency of the signal
y2 = np.sin(2*np.pi*ff2*t)

y = y1 + y2

n = len(y) # length of the signal
k = np.arange(n)
T = n/Fs
frq = k/T # two sides frequency range
frq = frq[range((n//2) + 1)] # one side frequency range

Y = np.fft.fft(y)/n # fft computing and normalization
Y = Y[range((n//2) + 1)]

fig, ax = plt.subplots(2, 1)
ax[0].plot(t,y)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Amplitude')
ax[1].plot(frq,abs(Y),'r') # plotting the spectrum
ax[1].set_xlabel('Freq (Hz)')
ax[1].set_ylabel('|Y(freq)|')

plt.show()

