:: Comment
: Kinetics extracted from Li et al, 2007 - Mossy fibers N-calcium channel
: q10 from 
: written by Francesco Cavarretta (Jaeger lab, Emory University)
: on 03/08/2024 

NEURON {
	SUFFIX caN
	USEION ca_hvaNL READ ca_hvaNLi WRITE ica_hvaNL
	USEION ca READ cai, cao
	RANGE pbar, q10, minf
	GLOBAL vshift, mtau_factor, mtau_min, ltau_factor, linf_min, nlinf, klinf
	GLOBAL mk_factor
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
	pbar	= 0			(cm/s)
	vshift	= 0			(mV)
	mtau_factor	= 1		(1)
	mtau_min 	= 0		(ms)	

	mk_factor	= 1		(1)

	ltau_factor	= 1		(1)
	linf_min	= 1		(1)
	nlinf		= 1		(1)
	klinf		= 0.001	(mM)

	q10			= 5.9	(1)
	T0			= 23	(degC)		: used for q10 calculation  
}


ASSIGNED {
	celsius		(degC)
	q			(1)

	v			(mV)

	cai			(mA/cm2)
	cao			(mA/cm2)

	ica_hvaNL	(mA/cm2)
	ca_hvaNLi	(mA/cm2)
	ca_hvaNLo	(mA/cm2)

	minf		(1)
	mtau		(ms)

	linf		(1)
	ltau		(ms)
}


STATE {
	m FROM 0 TO 1
	l FROM 0 TO 1
}


BREAKPOINT {
	SOLVE states METHOD cnexp
	ica_hvaNL = pbar * m * l * ghk(v, cai, cao)
}


INITIAL {
	q = q10 ^ ((celsius - T0) / 10)

	rates(v + vshift + 5.9, ca_hvaNLi)
	m = minf
	l = linf
}


DERIVATIVE states {
	rates(v + vshift + 5.9, ca_hvaNLi)
	m' = (minf - m) / mtau
	l' = (linf - l) / ltau
}


FUNCTION safe_exp(x) {
  if(x >= 700) {
    x = 700
  } else if (x <= -700) {
    x = -700
  }

  safe_exp = exp(x)
}

FUNCTION efun(z) {
	if (fabs(z) < 1e-5) {
		efun = 1
	} else if(z >= 700) {
		efun = 0
	} else if(z <= -700) {
		efun = -1
	} else {
		efun = z / (exp(z) - 1)
	}
}


PROCEDURE rates(v (mV), cai (mM)) { 
	: time constant
	if (v <= -2.5) {
		mtau = (mtau_min + mtau_factor * safe_exp((v + 2.5) / 17.1) + 0.1) / q
	} else {
		mtau = (mtau_min + mtau_factor * safe_exp(-(v + 2.5) / 28.2) + 0.1) / q
	}

	: voltage-dependent activation
	minf = 1 / (1 + safe_exp(-(v + 1) / (5 * mk_factor) ))	

	: time constant for ca dependent inactivation
	ltau = ltau_factor 

	: ca dependent inactivation
	:linf = (1 - linf_min) / ( 1 + ((klinf / cai) ^ nlinf) ) + linf_min
	linf = (1 - linf_min) / ( 1 + safe_exp((log(cai) - log(klinf)) / (-1/nlinf)) ) + linf_min

}


FUNCTION ghk(v(mV), ci(mM), co(mM)) (.001 coul/cm3) { LOCAL z, eci, eco
	z = (1e-3) * 2 * FARADAY * v / (R * (celsius + 273.15))
	eco = co * efun(z)
	eci = ci * efun(-z)

	:high cao charge moves inward
	:negative potential charge moves inward

	ghk = (.001) * 2 * FARADAY * (eci - eco)
}



