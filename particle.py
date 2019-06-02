#small class to calculate revolution time of a given nucleus in a storage ring
#first file from Schottky signal simulator. You have to add particle before you
#will be able to calculate all things.
#Dmytro Dmytriiev, GSI, 3.05.2019
# TO DO: coefficient for the signal amplitude
import numpy as np
import math

class Particle:
	def __init__(self, Brho = 13, ring_length = 103.4):
		self.Brho = Brho
		self.ring_length = ring_length
		self.e_mass = 0.5109989 #Mev
		self.light_speed = 299792458        # unit in m/s
		self.atommassunit = 931.494061         # MeV/C^2
		self.mass_exs_db = np.genfromtxt( 'input/db_Mass_excess_normal.txt', skip_header = 1, dtype = None, encoding = 'utf-8') #Name, N, Z, A, MassExcess
		self.bind_en_db = np.genfromtxt( 'input/ElBiEn_2007.dat', skip_header = 11) #Z, Z_el, Z-1_el, Z-2_el, ..., Z-100_el
		self.particle_list = []

	def add_particle_Z(self, A, Z, charge_state):
		particle = []
		for nuclei in self.mass_exs_db:
			if nuclei[2] == int(Z)  and  nuclei[3] == int(A):
				mass_excess = nuclei[4]
				for param in nuclei:
					particle.append(param)

		if Z < 3:
			particle.append(charge_state)
			particle.append(0)
		self.particle_list.append(particle)

		if Z > 2:
			for nuclei in self.bind_en_db:
				if nuclei[0] == int(Z):
					particle.append(charge_state)
					particle.append(nuclei[2 + charge_state])
		self.particle_list.append(particle)

	def add_particle_name(self, A, name, charge_state):
		particle = []
		Z = 0
		for nuclei in self.mass_exs_db:
			if nuclei[3] == int(A)  and  nuclei[0].lower() == name.lower():
				mass_excess = nuclei[4]
				Z = nuclei[2]
				for param in nuclei:
					particle.append(param)

		if Z < 3:
			particle.append(charge_state)
			particle.append(0)
		self.particle_list.append(particle)

		if Z > 2:
			for nuclei in self.bind_en_db:
				if nuclei[0] == int(Z):
					particle.append(charge_state)
					particle.append(nuclei[2 + charge_state])
		self.particle_list.append(particle)

	def remove_particle(self, A, Z, charge_state):
		for item in self.particle_list:
			if Z in item and A in item and charge_state in item:
				self.particle_list.remove(item)
				print(item)

	def get_mass(self, A, Z, charge_state):
		for item in self.particle_list:
			if Z in item and A in item and charge_state in item:
				m = A*self.atommassunit + item[4]/1000 - Z*self.e_mass + item[5]/1000 #kev to MeV
				return m

	def get_gamma(self, A, Z, charge_state):
		gamma = math.sqrt( ( self.Brho * Z * self.light_speed / self.get_mass(A, Z, charge_state)/10E6 )**2 + 1) #mass from MeV to eV
		return gamma

	def get_beta(self, A, Z, charge_state):
		beta = math.sqrt(1 - 1 / (self.get_gamma(A, Z, charge_state)**2) )
		return beta

	def get_speed(self, A, Z, charge_state):
		speed = self.light_speed * self.get_beta(A, Z, charge_state)
		return speed

	def get_freq(self, A, Z, charge_state):
		freq = 1/(self.ring_length/self.get_speed(A, Z, charge_state)) # to Mhz
		return freq

	def get_amplitude(self, A, Z, charge_state):
		amplitude = Z**2 #add coeff
		return amplitude

if __name__ == "__main__":
	P = Particle()
	P.add_particle_Z(105, 51, 0)
	P.add_particle_Z(236, 92, 0)
	P.add_particle_name(238, 'U', 0)
	print (P.particle_list)
	P.remove_particle(236, 92, 0)
	print ("mass: ", P.get_mass(238, 92, 0), "MeV")
	print ("gamma: ", P.get_gamma(238, 92, 0))
	print ("beta: ", P.get_beta(238, 92, 0))
	print ("speed: ", P.get_speed(238, 92, 0), "m/s")
	print ("freq: ", P.get_freq(105, 51, 0), 'Hz')
	print ("Ampl: ", P.get_amplitude(105, 51, 0), 'V')
