from math import sqrt

def y_plus(uref, rho, mu, lenght, Y):
	Rex = ((rho*uref*lenght)/mu)
	Cf = ((0.026)/pow(Rex,1/7))
	tauW = ((Cf*rho*uref*uref)/2)
	Ufric = sqrt(tauW/rho)
	distance = ((Y*mu)/(Ufric*rho))
	#nonlocal Rex
	#nonlocal distance
	return [Rex, distance]