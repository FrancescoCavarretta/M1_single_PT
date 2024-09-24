: References
: : Kole et al, 2006 for kinetics
: : Magee, 1998	for temperature dependence
: : mod files changed on 03/01/2024, adding trap function and q10, by Francesco Cavarretta (Emory University)

NEURON	{
	SUFFIX iH
        
	NONSPECIFIC_CURRENT ihcn

	RANGE gbar, ehcn
	GLOBAL vshift, htau_factor, htau_min
}


UNITS {
	(molar)	= (1/liter)
	(mM)	= (millimolar)
	(uM)	= (micromolar)
	(S)		= (siemens)
	(mA)	= (milliamp)
	(mV)	= (millivolt)
	FARADAY	= (faraday) (coulomb)
	R		= (k-mole) (joule/degC)
}


PARAMETER {
	gbar		= 0		(S/cm2) 
	vshift		= 0		(mV)
	htau_factor	= 1		(1)
	htau_min 	= 0		(ms)

	q10			= 4.6	(1)			: see Magee 1998
	T0			= 34	(degC)		: used for q10 calculation    

	ehcn		= -45.0	(mV)
}

ASSIGNED {
	celsius	(degC)
	q
  
	v		(mV)
	ihcn	(mA/cm2)
  
	hinf
	htau	(ms)
}


STATE	{ 
	h
}


INITIAL {
	q = q10 ^ ((celsius - T0) / 10) : temperature dependence factor, see Magee 1998

	rates(v + vshift)
	h = hinf
}


BREAKPOINT {
	SOLVE states METHOD cnexp
	ihcn = gbar * h * (v - ehcn)
}


DERIVATIVE states {
	rates(v + vshift)
	h' = (hinf - h) / htau
}


FUNCTION efun(z) {
  if(fabs(z) < 1e-5) {
    efun = 1
  } else {
    efun = z / (exp(z) - 1)
  }
}


PROCEDURE rates(v (mV)){ LOCAL a, b

	: 0.001*6.43*(v+154.9)/(exp((v+154.9)/11.9)-1) =
	: 0.00643*(v+154.9)*(exp((v+154.9)/11.9)-1) = 
	: 0.00643*11.9*(v+154.9)/11.9*(exp((v+154.9)/11.9)-1) =
	: 0.076517*(v+154.9)/11.9*(exp((v+154.9)/11.9)-1) =
	: 0.076517*efun((v+154.9)/11.9)

	a = 0.076517 * efun((v + 154.9) / 11.9)
	b = 0.193 * exp(v / 33.1)

	: time constant
	htau = (htau_min + htau_factor / (a + b)) / q

	hinf = a / (a + b)
}
