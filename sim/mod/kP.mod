:Comment : The persistent component of the K current
:Reference : :		Voltage-gated K+ channels in layer 5 neocortical pyramidal neurones from young rats:subtypes and gradients, Korngreen and Sakmann, J. Physiology, 2000


NEURON	{
	SUFFIX kP
	USEION k READ ek WRITE ik

	RANGE gbar, q10m, q10h
	GLOBAL vshift, mtau_factor, htau_factor, mtau_min, htau_min, wshift
	GLOBAL mk_factor, hk_factor
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
	wshift		= 0		(mV)
	mtau_factor	= 1		(1)
	mtau_min 	= 0		(ms)
	htau_factor	= 1		(1)
	htau_min 	= 0		(ms)

	q10m		= 2.9	(1)
	q10h		= 2.6	(1)
	T0			= 21	(degC)	: used for q10 calculation  

	mk_factor	= 1		(1)
	hk_factor	= 1		(1)
}


ASSIGNED {
	celsius	(degC)
	qm		(1)
	qh		(1)
  
	v		(mV)
	ek		(mV)
	ik		(mA/cm2)
  
	minf	(1)
	mtau	(ms)
	hinf	(1)
	htau	(ms)  
}


STATE {
	m FROM 0 TO 1
	h FROM 0 TO 1
}


BREAKPOINT {
	SOLVE states METHOD cnexp
	ik = gbar * m*m * h * (v - ek)
}


INITIAL {
	qm = q10m ^ ((celsius - T0) / 10) : temperature dependence factor
	qh = q10h ^ ((celsius - T0) / 10) : temperature dependence factor

	rates(v + 2.6 + vshift) : +2.6 mV correction for junction potential

	m = minf
	h = hinf
}


DERIVATIVE states {
	rates(v + 2.6 + vshift) : +2.6 mV correction for junction potential
	m' = (minf - m) / mtau
	h' = (hinf - h) / htau
}

FUNCTION safe_exp(x) {
  if(x >= 700) {
    x = 700
  } else if (x <= -700) {
    x = -700
  }

  safe_exp = exp(x)
}


PROCEDURE rates(v (mV)) {
	if (v < -50) {
		mtau =	(mtau_min + mtau_factor * (1.25 + 175.03	* safe_exp(	v * 0.026	)))  / qm
	} else {
		mtau =	(mtau_min + mtau_factor * (1.25 + 13		* safe_exp( -v * 0.026	)))  / qm
	}

	htau = (htau_min + htau_factor * ( 360 + (1010 + 24 * (v + 55 + wshift) ) * safe_exp(-( (v + 75 + wshift) / 48) ^ 2) )) / qh

	minf = 1 / (1 + safe_exp(-(v + 1 ) / (12 * mk_factor) ))
	hinf = 1 / (1 + safe_exp( (v + 54 + wshift) / (11 * hk_factor) ))
}
