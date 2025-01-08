TITLE Low threshold calcium current
:
:   Ca++ current responsible for low threshold spikes (LTS)
:   Differential equations
:
:   Model of Huguenard & McCormick, J Neurophysiol 68: 1373-1383, 1992.
:   The kinetics is described by Goldman-Hodgkin-Katz equations,
:   using a m2h format, according to the voltage-clamp data
:   (whole cell patch clamp) of Huguenard & Prince, J. Neurosci. 
:   12: 3804-3817, 1992.
:
:   This model is described in detail in:
:   Destexhe A, Neubig M, Ulrich D and Huguenard JR.  
:   Dendritic low-threshold calcium currents in thalamic relay cells.  
:   Journal of Neuroscience 18: 3574-3588, 1998.
:   (a postscript version of this paper, including figures, is available on
:   the Internet at http://cns.fmed.ulaval.ca)
:
:    - shift parameter for screening charge
:    - empirical correction for contamination by inactivation (Huguenard)
:    - GHK equations
:
:
:   Written by Alain Destexhe, Laval University, 1995
:

: From ModelDB, accession no. 279, modified qm and qh


NEURON {
	SUFFIX caT
	USEION ca_lva READ ca_lvai WRITE ica_lva
	USEION ca READ cai, cao
	RANGE pbar, q10m, q10h
	GLOBAL vshift, mtau_factor, htau_factor, mtau_min, htau_min, wshift
	GLOBAL mk_factor, hk_factor
	RANGE vhm, vhh
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
	wshift		= 0		(mV)
	mtau_factor	= 1		(1)
	mtau_min 	= 0		(ms)
	htau_factor	= 1		(1)
	htau_min 	= 0		(ms)

	mk_factor	= 1		(1)
	hk_factor	= 1		(1)

	q10m		= 5		(1)
	q10h		= 3.1	(1)
	T0			= 24	(degC)	

	vhm			= 23.53	(mV)
	vhh			= 3 	(mV)
}


ASSIGNED {
	celsius		(degC)
	qm			(1)
	qh			(1)

	v			(mV)

	cai			(mA/cm2)
	cao			(mA/cm2)

	ica_lva		(mA/cm2)
	ca_lvai		(mA/cm2)
	ca_lvao		(mA/cm2)

	minf		(1)
	mtau		(ms)
	hinf		(1)
	htau		(ms)
}


STATE {
	m FROM 0 TO 1
	h FROM 0 TO 1
}


BREAKPOINT {
	SOLVE states METHOD cnexp
	ica_lva = pbar * m*m * h * ghk(v, cai, cao)
}


INITIAL {
	qm = q10m ^ ((celsius - T0) / 10)
	qh = q10h ^ ((celsius - T0) / 10)

	rates(v + vshift)
	m = minf
	h = hinf
}


DERIVATIVE states {
	rates(v + vshift)
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


FUNCTION efun(z) {
	if (fabs(z) < 1e-5) {
		efun = 1
	} else if(z >= 700) {
		efun = 0
	} else {
		efun = z / (exp(z) - 1)
	}
}

PROCEDURE rates(v (mV)) {

:
:   The kinetic functions are taken as described in the model of 
:   Huguenard & McCormick, and corresponds to a temperature of 23-25 deg.
:   Transformation to 36 deg assuming Q10 of 5 and 3 for m and h
:   (as in Coulter et al., J Physiol 414: 587, 1989).
:
:   The activation functions were estimated by John Huguenard.
:   The V_1/2 were of -57 and -81 in the vclamp simulations, 
:   and -60 and -84 in the current clamp simulations.
:
:   The activation function were empirically corrected in order to account
:   for the contamination of inactivation.  Therefore the simulations 
:   using these values reproduce more closely the voltage clamp experiments.
:   (cfr. Huguenard & McCormick, J Neurophysiol, 1992).
:


	mtau = (mtau_min + mtau_factor * ( 0.612 + 1 / ( safe_exp(-(v + 134 - vhm) / 16.7) + safe_exp((v + 18.8 - vhm) / 18.2) ) )) / qm


	if (v < (-82 + vhh - wshift)) {
		htau = (htau_min + htau_factor * safe_exp((v + 469 - vhh + wshift) / 66.6)          ) / qh
	} else {
		htau = (htau_min + htau_factor * ( 28 + safe_exp(-(v + 24 - vhh + wshift) / 10.5) ) ) / qh
	}

	minf = 1 / ( 1 + safe_exp(-(v + 59 - vhm) / (6.2 * mk_factor) ) )
	hinf = 1 / ( 1 + safe_exp( (v + 83 - vhh + wshift) / (4 * hk_factor) ) )
}


FUNCTION ghk(v(mV), ci(mM), co(mM)) (.001 coul/cm3) { LOCAL z, eci, eco
	z = (1e-3) * 2 * FARADAY * v / (R * (celsius + 273.15))
	eco = co * efun(z)
	eci = ci * efun(-z)

	:high cao charge moves inward
	:negative potential charge moves inward

	ghk = (.001) * 2 * FARADAY * (eci - eco)
}



