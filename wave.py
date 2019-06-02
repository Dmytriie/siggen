import numpy as np
import matplotlib.pyplot as plt

class Wave:
    def __init__(self, amplitude = 0, frequency = 0, phase = 0, start = 0, stop = 1, sampling_frequency = 1000):
        self.ampl = amplitude
        self.freq = frequency * 2 * np.pi # f = 2*3.14*omega. To have in seconds - use 6.28 factor
        self.ph = phase * 2 * np.pi / 360 # from degrees to rads
        self.start = start
        self.sampfreq = sampling_frequency
        self.stop = stop
        self.times = np.arange(self.start, self.stop, 1/self.sampfreq)

    def get_wave(self):
        self.wave = self.ampl * np.sin( self.freq * self.times + self.ph)
        return self.wave

    def check (self):
        plt.plot(self.times, Wave.get_wave(self) )
        plt.show()

if __name__ == "__main__":
    wave = Wave()
    wave.check()
