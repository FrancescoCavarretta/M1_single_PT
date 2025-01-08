: kinetics from Kay & Wong 1987
: q10 from Allen, 1996
: Implemented by Francesco Cavarreta, Jaeger Lab, Emory University (03/2024)

NEURON {
	SUFFIX caL
	USEION ca_hvaNL READ ca_hvaNLi WRITE ica_hvaNL
	USEION ca READ cai, cao
	RANGE pbar, q10, minf, linf, iL

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
	pbar		= 0		(cm/s)
	vshift		= 0		(mV)
	mtau_factor	= 1		(1)
	mtau_min 	= 0		(ms)	

	mk_factor	= 1		(1)

	ltau_factor	= 1		(1)
	linf_min	= 1		(1)
	nlinf		= 1		(1)
	klinf		= 0.001	(mM)

	q10			= 2.3	(1)
	T0			= 21	(degC)		: used for q10 calculation  
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
	taul		(ms)
        iL	(mA/cm2)
}


STATE {
	m FROM 0 TO 1
	l FROM 0 TO 1
}


BREAKPOINT {
	SOLVE states METHOD cnexp
        iL = pbar * m*m * l * ghk(v, cai, cao)
	ica_hvaNL = pbar * m*m * l * ghk(v, cai, cao)
}


INITIAL {
	q = q10 ^ ((celsius - T0) / 10)

	rates(v + vshift + 3, ca_hvaNLi)
	m = minf
	l = linf
}


DERIVATIVE states {
	rates(v + vshift + 3, ca_hvaNLi)
	m' = (minf - m) / mtau
	l' = (linf - l) / taul
}


FUNCTION safe_exp(x) {
  if(x >= 700) {
    x = 700
  } else if (x <= -700) {
    x = -700
  }

  safe_exp = exp(x)
}

PROCEDURE rates(v (mV), cai (mM)) { LOCAL a, b

	a = 1.6 / (1 + safe_exp(-0.072 * (v + 5)))
	b = 0.1072 * efun((v + 8.69) / 5.36)

	mtau = (mtau_min + mtau_factor / (a + b)) / q

	minf = 1 / (1 + safe_exp(-(v + 19.48) / (9.6 * mk_factor) ))	

	: ca dependent inactivation
	taul = ltau_factor 

	linf = (1 - linf_min) / ( 1 + safe_exp((log(cai) - log(klinf)) / (-1/nlinf)) ) + linf_min :(1 - linf_min) / ( 1 + ((klinf / cai) ^ nlinf) ) + linf_min
}


FUNCTION ghk(v (mV), ci(mM), co(mM)) (.001 coul/cm3) { LOCAL z, eci, eco
	z = (1e-3) * 2 * FARADAY * v / (R * (celsius + 273.15))
	eco = co * efun(z)
	eci = ci * efun(-z)

	:high cao charge moves inward
	:negative potential charge moves inward

	ghk = (.001) * 2 * FARADAY * (eci - eco)
}


FUNCTION efun(z) {
	if (fabs(z) < 1e-5) {
		efun = 1
	} else if(z >= 700) {
		efun = 0
	} else {
		efun = z / (exp(z) - 1)
	}
}

