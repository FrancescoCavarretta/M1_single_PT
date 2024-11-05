: SK-type calcium-activated potassium current from CA1 hippocampal pyramidal neurons
: Reference : Hirschberg et al, 1999
: : Modeled by Francesco Cavarretta
: : Jaegelab, Emory University
: : e-mail: francesco.cavarretta.neuro@gmail.com; francesco.cavarretta@emory.edu
: : v. February 29th 2024

NEURON {
  SUFFIX kSK
  USEION k READ ek WRITE ik

	USEION ca_hvaP READ ca_hvaPi
	USEION ca_hvaNL READ ca_hvaNLi
	USEION ca_lva READ ca_lvai
	USEION ca READ cai

    RANGE gbar, q10
	GLOBAL mtau_factor, mtau_min
	GLOBAL w_hvaP, w_hvaNL, w_lva
	GLOBAL mk_factor, cshift
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
	gbar		= 0	(S/cm2)
	mtau_factor	= 1	(1)
	mtau_min 	= 0	(ms)

	w_hvaP		= 1		(1)
	w_hvaNL		= 0		(1)
	w_lva		= 0 	(1)

	q10		= 1		(1)
	T0		= 37	(degC)
	mk_factor	= 1	(1)
	cshift		= 0	(1)	
}


ASSIGNED {
	celsius	(degC)
	v       (mV)
	ik      (mA/cm2)
	ek      (mV)
	q

	minf	(1)
	mtau	(ms)

	ca_hvaPi	(mM)  
	ca_hvaNLi	(mM)
	ca_lvai		(mM)
	cai			(mM)
}


STATE {
  m FROM 0 TO 1
}


BREAKPOINT {
  SOLVE states METHOD cnexp
  ik = gbar * m * (v - ek)
}


INITIAL {
	q = q10 ^ ((celsius - T0) / 10)
	rates(w_hvaP * ca_hvaPi + w_hvaNL * ca_hvaNLi + w_lva * ca_lvai)
	m = minf
}


DERIVATIVE states {
	rates(w_hvaP * ca_hvaPi + w_hvaNL * ca_hvaNLi + w_lva * ca_lvai)
	m' = (minf - m) / mtau
}


FUNCTION safe_exp(x) {
  if(x >= 700) {
    x = 700
  } else if (x <= -700) {
    x = -700
  }

  safe_exp = exp(x)
}



FUNCTION alpha(cai (uM)) { LOCAL ps
  ps = 0.74 / (1 + safe_exp((log10(cai) + 3.34) / 0.11)) + 0.26
  alpha = 1 / (1.091 * ps + 7.694 * (1 - ps))
}


FUNCTION beta(cai (uM)) { LOCAL pl, ps, tau_long
  ps = 0.75 / (1 + safe_exp(-(log10(cai) + 3.44) / 0.1)) 
  pl = 0.97 / (1 + safe_exp((log10(cai) + 3.52) / 0.09)) + 0.03
  tau_long =  765.39 * safe_exp(-(cai * 1000 - 0.31) / 0.01) + 89.42
  beta = 1 / (0.847 * ps + tau_long * pl + 4.59 * (1 - ps - pl))
}

PROCEDURE rates(ca (mM)) { 
	: time constant
	mtau = (mtau_min + mtau_factor * 1 / (alpha(ca) + beta(ca))) / q

    : activation
	minf = 1 / (1 + safe_exp(-(log(ca) + 3.58 + cshift) / (0.217 * mk_factor) ))
}

