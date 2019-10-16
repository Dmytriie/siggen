from nuclide import *
import random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
np.set_printoptions(threshold=np.inf)
#several parameters could be adjusted in matplotlib. Basically - everything
#wherever we want to have a resolution map - we have to have array of resolutions for every y coordinate and binded errors
#matplotlib.rcParams.update({'font.size': 14})
#matplotlib.rcParams['axes.edgecolor'] = 'limegreen'
#matplotlib.rcParams['axes.facecolor'] = 'black'
#matplotlib.rcParams['axes.labelcolor'] = 'limegreen'
#matplotlib.rcParams['xtick.color'] = 'limegreen'
#matplotlib.rcParams['ytick.color'] = 'limegreen'
#matplotlib.rcParams['text.color'] = 'limegreen'
#matplotlib.rcParams['figure.facecolor'] = 'black'
#matplotlib.rcParams['figure.figsize'] = (8, 3)

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

print('Particles creation...')
E_kin = 400 #MeV/u
He = Nuclide(2,4,2,E_kin)
H = Nuclide(1,1,1,E_kin)
N = Nuclide(7,14,7,E_kin)
C = Nuclide(6,12,6,E_kin)
O = Nuclide(8,16,8,E_kin)
isoparticle = Nuclide(3,6,3,E_kin)
nuclides = [H,He, N, C, O]
print('Particles created!')

freqs = []
cil_peaks = np.zeros(len(He.freqs))
el_peaks = np.zeros(len(He.freqs))
positions = []
pos_coor = []
pos_pow = []
cav_max = 5
cav_min = -5

cil_pos = np.genfromtxt(sys.argv[1], skip_header = 15)[:,0]
cil_rq = np.genfromtxt(sys.argv[1], skip_header = 15)[:,1]
el_rq = np.genfromtxt(sys.argv[2], skip_header = 15)[:,1]

print('Frequency spectrum making...')
for item in nuclides:
        item.isospeed = isoparticle.speed
        print (item.isospeed)
        pos = random.randint(cav_min*10,cav_max*10)/20
        freqs.append(item.gen_freq())
        cil_peaks = np.add(cil_peaks, item.gen_peak(pos, 1))
        el_peaks = np.add(el_peaks, item.gen_peak(pos, 0))
ratio = np.divide(cil_peaks, el_peaks) #get the power ratios bin by bin for cavities
coord_power = np.divide(cil_rq, el_rq) # get the power ratio for the CST data for each coordinate
print('Frequency spectrum ready!')

print('Calculation of the positions...')

ratio = np.nan_to_num(ratio)#to remove nan`s
for item in ratio:
    pow = find_nearest(coord_power, float(item))# find the closest CST power ratio to simulated one
    pow_idx = np.where(coord_power == pow) #find the index of closest CST power ratio
    pos = cil_pos[pow_idx]# get the position related to the given power ratio
    pos_coor.append(pos)
    pos_pow.append(pow)

print('Calculation of the positions finished!')

fig = plt.figure()
#fig.add_subplot(321)
plt.ticklabel_format(style='sci', axis='x')
plt.title('Simulated power ratio - coordinate plot')
plt.xlabel('Position, cm')
plt.ylabel('Signal power')
plt.yscale('linear')
plt.plot(cil_pos, coord_power)
plt.savefig('ratio_CST.png')
plt.show()

fig.add_subplot(322)
plt.ticklabel_format(style='sci', axis='x' )
plt.title('Cil_cav signal')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Signal power')
plt.yscale('symlog')
plt.plot(He.freqs, cil_peaks)
plt.tight_layout()
plt.savefig('Cil_sim.png')
plt.show()

fig.add_subplot(323)
plt.ticklabel_format(style='sci', axis='x' )
plt.title('El_cav signal')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Signal power')
plt.yscale('symlog')
plt.plot(He.freqs, el_peaks)
plt.tight_layout()
plt.savefig('El_sim.png')
plt.show()

fig.add_subplot(324)
plt.ticklabel_format(style='sci', axis='x' )
plt.title('Signals power ratio cil/el')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power ratio')
plt.plot(He.freqs, ratio)
plt.tight_layout()
plt.savefig('Ratio_sim.png')
plt.show()

fig.add_subplot(325)
plt.ticklabel_format(style='sci', axis='x' )
plt.title('Peaks power ratio and coordinates cil/el')
plt.xlabel('Frequency, Hz')
plt.ylabel('Position , cm')
plt.plot(He.freqs, pos_coor)
plt.tight_layout()
plt.savefig('Coord_sim.PNG')
plt.show()

fig.add_subplot(326)
plt.ticklabel_format(style='sci', axis='x')
plt.title('Peaks power ratio and coordinates cil/el')
plt.xlabel('Coordinate, cm')
plt.ylabel('Power ratio')
#plt.plot(pos_coor, pos_pow, 'b.')
#plt.show()
