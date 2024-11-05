: Comment :
: : Large conductance calcium-dependent potassium channel of rat skeletal muscle
: :
: : Francesco Cavarretta
: : Jaeger lab, Emory University
: : e-mail: francesco.cavarretta.neuro@gmail.com; francesco.cavarretta@emory.edu
: : v. February 16th 2024
: :
: :
: References :
: : 1. Rothberg, Brad S., and Karl L. Magleby. "Voltage and Ca2+ activation of single large-conductance Ca2+-activated K+
: :   channels described by a two-tiered allosteric gating mechanism." The Journal of general physiology 116.1 (2000): 75-100.
: : 2. Rothberg, Brad S., and Karl L. Magleby. "Gating Kinetics of Single Large-Conductance Ca2+-Activated K+ Channels in High
: :   Ca2+ Suggest a Two-Tiered Allosteric Gating Mechanism." The Journal of general physiology 114.1 (1999): 93-124.
: : 3. Yang, Fan, and Jie Zheng. "High temperature sensitivity is intrinsic to voltage-gated potassium channels." 
: :   Elife 3 (2014): e03255. --- See Fig. 1

NEURON {
	SUFFIX kBK
	USEION k READ ek WRITE ik
	RANGE gbar, q10 
	GLOBAL vshift, mtau_factor, mtau_min
	RANGE minf, mtau, mvhalf

	USEION ca_hvaP READ ca_hvaPi
	USEION ca_hvaNL READ ca_hvaNLi
	USEION ca_lva READ ca_lvai
	USEION ca READ cai

	GLOBAL w_hvaP, w_hvaNL, w_lva
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
	gbar		= 0		(S/cm2)

	vshift		= 0		(mV)
	mtau_factor	= 1		(1)
	mtau_min 	= 0		(ms)

	q10			= 1.9	(1)		: see Ref. 3
	T0 			= 23	(degC)	: used for q10 calculation    

	w_hvaP		= 0		(1)
	w_hvaNL		= 1		(1)
	w_lva		= 0 	(1)
	mk_factor	= 1		(1)
  
}


ASSIGNED {
	v		(mV)
	ek		(mV)
	ik		(mA/cm2)
  
	minf	(1)
	mtau	(ms)

	celsius	(degC)
	q		(1)

	ca_hvaPi	(mM)  
	ca_hvaNLi	(mM)
	ca_lvai		(mM)
	cai			(mM)

	mvhalf		(mV)
}


STATE {
	m FROM 0 TO 1
}



BREAKPOINT {
	SOLVE states METHOD cnexp
	ik = gbar * m * (v - ek)
}
 

INITIAL {
	q = q10 ^ ((celsius - T0) / 10) 			: temperature dependence factor
  
	rates(v + vshift, w_hvaP * ca_hvaPi + w_hvaNL * ca_hvaNLi + w_lva * ca_lvai)
	m = minf

}


DERIVATIVE states {  
	rates(v + vshift, w_hvaP * ca_hvaPi + w_hvaNL * ca_hvaNLi + w_lva * ca_lvai)
	m' = (minf - m ) / mtau
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
		efun = -z
	} else {
		efun = z / (exp(z) - 1)
	}
}


FUNCTION alpha(v (mV), cai (uM)) { 
	: see Fig. 3 in Ref 1

	LOCAL vh

:	vh = -48.8 + 101.6 / (1 + ((20.0 / cai) ^ (-3.1)))
	vh = -48.8 + 101.6 / (1 + safe_exp((log(cai) + log(1000) - log(20)) / (1/3.1)))
	:alpha = -0.2 * (v - vh) / 2.7  / ( safe_exp(-(v - vh) / 2.7) - 1)
	alpha = -0.2 * 2.7 * efun(-(v - vh) / 2.7)
}


FUNCTION beta(v (mV), cai (uM)) {
 	: see Fig. 3 Ref 1 

	LOCAL vh

	:vh = -542.0 + 317.2 / (1 + ((2.5 / cai) ^ (-0.2)))
	vh = -542.0 + 317.2 / (1 + safe_exp((log(cai) + log(1000) - log(2.5)) / (1/0.2)))
	beta = 1550.2 * safe_exp(-(v - vh) / 57.9)
}


FUNCTION m_vh_calc(cai (uM)) { 
	: Upper and lower bounds estimated from bold line in Fig. 2D, Ref. 1
	: Linear component estimated from Fig. 2A, Ref. 2

	m_vh_calc = 40.5 * (log(11.1) - log(cai) - log(1000)) + 30.0

	if(m_vh_calc < -40) {
		m_vh_calc = -40
	} else if(m_vh_calc > 137.5) {
		m_vh_calc = 137.5
	}
}


PROCEDURE rates(v (mV), cai (mM)) { 
	: time constant
	mtau = 1 :(mtau_min + mtau_factor / (alpha(v, cai) + beta(v, cai))) / q
	
	: half value
	mvhalf = m_vh_calc(cai)

	: see Fig. 2, Ref. 1
	minf = 1 / (1 + safe_exp(-(v - mvhalf) / (11.5 * mk_factor) )) : activation
}








