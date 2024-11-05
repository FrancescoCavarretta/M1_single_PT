:Comment : The transient component of the K current
:Reference : :		Voltage-gated K+ channels in layer 5 neocortical pyramidal neurones from young rats:subtypes and gradients,Korngreen and Sakmann, J. Physiology, 2000


NEURON	{
	SUFFIX kT
	USEION k READ ek WRITE ik

	RANGE gbar, q10
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

	q10		= 2			(1)
	T0		= 21		(degC)	: used for q10 calculation  	

	mk_factor	= 1		(1)
	hk_factor	= 1		(1)
}


ASSIGNED {
	celsius	(degC)
	q		(1)
  
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
	ik = gbar * m*m*m*m * h * (v - ek)
}


INITIAL {
	q = q10 ^ ((celsius - T0) / 10) : temperature dependence factor

	rates(v + 2.7 + vshift)

	m = minf
	h = hinf
}


DERIVATIVE states {
	rates(v + 2.7 + vshift)
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
	mtau =  (mtau_min + mtau_factor * ( 0.34	+ 0.92	* safe_exp(-((v + 71) / 59) ^ 2))) / q
	htau =  (htau_min + htau_factor * ( 8		+ 49	* safe_exp(-((v + 73 + wshift) / 23) ^ 2))) / q

	minf =  1 / (1 + safe_exp(-(v + 0) / (19 * mk_factor) ))
	hinf =  1 / (1 + safe_exp( (v + 66 + wshift) / (10 * hk_factor) ))
}
