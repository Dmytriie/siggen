from scipy.stats import norm
import random
import matplotlib.pyplot as plt
import numpy as np
from barion import *
from barion.particle import *
from barion.ui_interface import *
from barion.amedata import *
from barion.ring import Ring
import sys

class Nuclide:
    def __init__(self, Z, A, charge_state, E_kin):
        self.Z = Z
        self.A = A
        self.charge_state = charge_state
        self.E_kin = E_kin
        self.kHz = 1E3
        self.MHz = 1E6
        self.gamma_t = 1.4 #barion, ring.py esr.gamma_t was changed from 2.30 to 1.4   STD Mode: 2.30 or 2.44 theoretical value, ISO: 1.4
        self.speed = 0
        self.isospeed = 214233263.72441977 #speed of 12C 6+
        self.freqs = np.arange(244, 245.5, 0.0001)
        self.pos_coor = []
        self.pos_pow = []
        self.ame_data = AMEData(DummyIFace())
        self.cil_pos = np.genfromtxt(sys.argv[1], skip_header = 15)[:,0]
        self.el_pos = np.genfromtxt(sys.argv[2], skip_header = 15)[:,0]
        self.cil_rq = np.genfromtxt(sys.argv[1], skip_header = 15)[:,1]
        self.el_rq = np.genfromtxt(sys.argv[2], skip_header = 15)[:,1]

        self.p = Particle(self.Z, self.A-self.Z, self.ame_data, Ring('ESR', 108.5))
        self.p.qq = self.charge_state
        self.p.ke_u = self.E_kin
        self.p.path_length_m = 108.5
        self.p.f_analysis_mhz = 245
        self.p.i_beam_uA = 1.2
        self.speed = self.p.get_velocity()
        self.gamma = self.p.get_gamma()

    def gen_freq(self):

        freq = self.p.calculate_revolution_frequency()
        harm = self.p.f_analysis_mhz//freq
        freq = freq*harm

        return freq

    def gen_peak(self, pos, cil):

        index = np.where(self.cil_pos == pos) #to find the R/Q for the given position
        sigma = np.abs( (1 - self.gamma**2 / self.gamma_t**2) * ((self.speed - self.isospeed)/self.isospeed)*self.gen_freq()/5 ) #isochronicity

        if cil == 1: #if we generate peak for the cylindrical cavity
            peak = self.Z**2 * self.cil_rq[index] * norm.pdf(self.freqs, self.gen_freq(), sigma) #area under the plot = 1*FWHM*RQ
            print ("Position: ", pos, " R/Q: ",self.el_rq[index], " Charge: ", self.Z, " Mu, MHz: ", self.gen_freq(), " Sigma, Hz: ", sigma*1E6)

        if cil == 0: #if peak is for elliptical cavity
            peak = self.Z**2 * self.el_rq[index] * norm.pdf(self.freqs, self.gen_freq(), sigma)  #area under the plot = 1*FWHM*RQ
            print ("Position: ", pos, " R/Q: ",self.el_rq[index], " Charge: ", self.Z, " Mu, MHz: ", self.gen_freq(), " Sigma, Hz: ", sigma*1E6)

        return peak

    def check(self):
        plt.plot(self.freqs, self.gen_peak(2, 1))
        plt.show()

if __name__ == "__main__":
        P = Nuclide(92,238,92,400)
        print (P.speed)
        P.check()
