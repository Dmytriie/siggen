from wave import Wave
from scipy.fftpack import fft
import numpy as np
import PySimpleGUI as sg
class SignalGenerator:

    def __init__(self, meas_time = 1, sampfreq = 1000000):
        
        self.wave_array = np.zeros(meas_time*sampfreq)
        self.meas_time = meas_time 
        self.sampfreq = sampfreq
        self.fmax = sampfreq // 2
        self.wavefreqs = []
        self.sprfreqs = []     
        self.scale_factor = 1

    def add_wave(self, amp, central_frequency, phase):
        wave = Wave(amp, central_frequency, phase, stop = self.meas_time, sampling_frequency = self.sampfreq)
        self.wavefreqs.append(central_frequency)
        param_array = np.array([amp, central_frequency, phase, -1, -1])
        self.wave_array = np.sum( [ self.wave_array, wave.get_wave() ], axis = 0)
        del wave
        
    def add_spread_wave(self, amp, central_frequency, phase, freqspread, bunchsize):    
        param_array = np.array([amp, central_frequency, phase, freqspread, bunchsize])    
        freqs = np.random.normal(central_frequency, freqspread, size = bunchsize) #frequency Gaussian distribution 
              
        for freq in freqs:
            wave = Wave(amplitude = amp, frequency = freq, phase = phase, stop = self.meas_time, sampling_frequency = self.sampfreq)
            self.wavefreqs.append(freq)
            self.wave_array = np.sum([self.wave_array, wave.get_wave()], axis = 0) 
        del wave
    
    def delete_wave(self, amp, freqs, phase):
        if type(freqs) != type(self.wavefreqs):
            wave = Wave(amplitude = amp, frequency = freqs, phase = phase, stop = self.meas_time, sampling_frequency = self.sampfreq)
            self.wave_array = np.subtract( self.wave_array, wave.get_wave() )
            self.wavefreqs.remove(freqs)

        if type(freqs) == type(self.wavefreqs):
            for freq in freqs:
                wave = Wave(amplitude = amp, frequency = freq, phase = phase, stop = self.meas_time, sampling_frequency = self.sampfreq)
                self.wave_array = np.subtract(self.wave_array, wave.get_wave() )
                self.wavefreqs.remove(freq)
        
    def send_waves(self):
        return self.wave_array
    
    def freq_spectre(self, wave_array):
        fu = fft(wave_array)
        fu = np.abs(fu[0:self.fmax*self.meas_time] )/(self.fmax*self.meas_time)
        freqs = np.linspace(0.0, self.fmax, self.fmax*self.meas_time)
        return freqs[0::self.scale_factor], fu[0::self.scale_factor]   
    
    def check(self):
        siggen = SignalGenerator()
        siggen.add_wave(2, 40, 1)
        #siggen.add_wave(2, 40, 0)
        freqs = siggen.wavefreqs
        print (freqs)
        siggen.delete_wave(2, freqs[0], 1)
        
        wave = siggen.send_waves()
        freqs, fu = siggen.freq_spectre(wave)
        freqs=siggen.mean(freqs, 1)
        fu=siggen.mean(fu, 1)        
        plt.plot(freqs, fu)
        plt.show()                    
        
if __name__ == "__main__":
        siggen = SignalGenerator()
        siggen.check()

