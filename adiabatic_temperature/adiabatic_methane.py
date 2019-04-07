"""
Adiabatic flame temperature and equilibrium composition for a fuel/air mixture
as a function of equivalence ratio, including formation of solid carbon.
"""

import cantera as ct
import numpy as np
import sys
import csv
import matplotlib.pyplot as plt

def aft(T, P, lambdaMin, lambdaMax, noPoints, ch4, c2h6, c3h8, co, co2, h2):

	##############################################################################
	# Edit these parameters to change the initial temperature, the pressure, and
	# the phases in the mixture.
	#print('Pamietaj, aby skład gazu podac molowo!')
	#file_name = input('Podaj nazwe pliku: ')
	T = T
	P = P

	# phases
	gas = ct.Solution('gri30.xml')
	carbon = ct.Solution('graphite.xml')

	# the phases that will be included in the calculation, and their initial moles
	mix_phases = [(gas, 1.0), (carbon, 0.0)]

	# gaseous fuel species
	fuel_species_1 = 'CO'
	fuel_species_2 = 'CH4'
	fuel_species_3 = 'O2'
	fuel_species_4 = 'CO2'
	fuel_species_5 = 'N2'
	fuel_species_6 = 'C3H8'
	fuel_species_7 = 'C2H6'

	# air composition
	air_N2_O2_ratio = 3.76

	# equivalence ratio range
	phi_min = 1/lambdaMax
	phi_max = 1/lambdaMin
	npoints = noPoints

	##############################################################################

	mix = ct.Mixture(mix_phases)

	# create some arrays to hold the data
	phi = np.zeros(npoints)
	tad = np.zeros(npoints)
	xeq = np.zeros((mix.n_species,npoints))

	# find fuel, nitrogen, and oxygen indices
	i_co = gas.species_index('CO')
	i_ch4 = gas.species_index('CH4')
	i_h2 = gas.species_index('H2')
	i_co2 = gas.species_index('CO2')
	i_n2 = gas.species_index('N2')
	i_c3h8 = gas.species_index('C3H8')
	i_c2h6 = gas.species_index('C2H6')

	io2 = gas.species_index('O2')
	in2 = gas.species_index('N2')

	#if gas.n_atoms(fuel_species,'O') > 0 or gas.n_atoms(fuel_species,'N') > 0:
	#    raise "Error: only hydrocarbon fuels are supported."

	stoich_O2_co = 0.5
	stoich_O2_ch4 = 2
	stoich_O2_h2 = 0.5
	stoich_O2_c3h8 = 5
	stoich_O2_c2h6 = 3.5

	metan = ch4
	tlenek_wegla = co
	wodor = h2
	etan = c2h6
	propan = c3h8
	dwutlenek_wegla = co2
	azot = 1 - (metan + tlenek_wegla + wodor + etan + propan + dwutlenek_wegla)

	for i in range(npoints):
		X = np.zeros(gas.n_species)
		X[i_ch4] = metan
		X[i_co] = tlenek_wegla
		X[i_h2] = wodor
		X[i_c2h6] = etan
		X[i_c3h8] = propan
		X[i_co2] = dwutlenek_wegla
		X[i_n2] = azot
		
		phi[i] = phi_min + (phi_max - phi_min)*i/(npoints - 1)

		stoich_O2 = X[i_co] * stoich_O2_co + X[i_ch4] * stoich_O2_ch4 + X[i_h2] * stoich_O2_h2 + X[i_c3h8] * stoich_O2_c3h8 + X[i_c2h6] * stoich_O2_c2h6
		stoich_air = (stoich_O2 / 0.21) / 100
		X[io2] = X[io2] + stoich_O2 / phi[i]
		X[in2] = X[in2] + stoich_O2 * air_N2_O2_ratio / phi[i]
		

		# set the gas state
		gas.TPX = T, P, X

		# create a mixture of 1 mole of gas, and 0 moles of solid carbon.
		mix = ct.Mixture(mix_phases)
		mix.T = T
		mix.P = P

		# equilibrate the mixture adiabatically at constant P
		mix.equilibrate('HP', solver='gibbs', max_steps=1000)

		tad[i] = mix.T
		#print('At phi = {0:12.4g}, Tad = {1:12.4g}, Stoichometric value = {2:12.4g}'.format(phi[i], tad[i], stoich_air))
		xeq[:,i] = mix.species_moles
		
	# write output CSV file for importing into Excel
	
	csv_file = 'aft.csv'
	with open(csv_file, 'w') as outfile:
		writer = csv.writer(outfile)
		writer.writerow(['phi','T (K)'] + mix.species_names)
		for i in range(npoints):
			writer.writerow([phi[i], tad[i]] + list(xeq[:,i]))
	#print('Output written to {0}'.format(csv_file))

	max_index = np.argmax(tad)
	tad_max = tad[max_index]
	lambda_max = 1/phi[max_index]
	plt.plot(phi, tad)
	plt.xlabel('Equivalence ratio')
	plt.ylabel('Adiabatic flame temperature [K]')
	plt.savefig('static/aft.png')
	return (tad_max, lambda_max)

'''
	#if '--plot' in sys.argv:
	plt.plot(phi, tad)
	plt.xlabel('Equivalence ratio')
	plt.ylabel('Adiabatic flame temperature [K]')
	plt.savefig(file_name+'_wykres.png')
'''