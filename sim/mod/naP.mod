:Reference :Colbert and Pan 2002
:q10 Schwarz 1986
:Reference : Modeled according to kinetics derived from Magistretti & Alonso 1999

NEURON	{
	SUFFIX naP
	USEION na READ ena WRITE ina
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

PARAMETER	{
	gbar		= 0		(S/cm2)
	vshift		= 0		(mV)
	wshift		= 0		(mV)
	mtau_factor	= 1		(1)
	mtau_min 	= 0		(ms)
	htau_factor	= 1		(1)
	htau_min 	= 0		(ms)

	mk_factor	= 1		(1)
	hk_factor	= 1		(1)

	q10m		= 2		(1)
	q10h		= 2.2	(1)
	T0			= 23	(degC)		: used for q10 calculation   
}

ASSIGNED	{
	celsius	(degC)
	qm		(1)
	qh		(1)
  
	v		(mV)
	ena		(mV)
	ina		(mA/cm2)
  
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
  ina = gbar * m*m*m * h * (v - ena)
}


INITIAL {
	qm = q10m ^ ((celsius - T0) / 10)
	qh = q10h ^ ((celsius - T0) / 10)

	rates(v + vshift) : + 13.2)
	m = minf
	h = hinf
}




DERIVATIVE states {
  rates(v + vshift) : + 13.2)
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
  if(fabs(z) < 1e-5) {
    efun = 1
  } else {
    efun = z / (safe_exp(z) - 1)
  }
}

PROCEDURE rates(v (mV)) { LOCAL a, b

  a = (6 * 1.092) * efun(-(v + 38 + 22.7) / 3)
  b = (6 * 0.744) * efun((v + 38 + 22.7) / 3)

  mtau = (mtau_min + mtau_factor / (a + b)) / qm
  minf = 1 / (1 + safe_exp(-(v + 38 + 2.3 + 22.7) / (3 * mk_factor) ))


  a = ((2e-4) * 0.09) * efun((v + 66 - 9.4 + wshift) / (6 * 2)) 
  b = ((2e-4) * 0.09) * efun(-(v + 66 - 9.4 + wshift) / (6 * 2)) 

  htau = (htau_min + htau_factor / (a + b)) / qh
  hinf = 1 / (1 + safe_exp((v + 66 - 9.4 + wshift) / (6 * 2 * hk_factor) ))

}
