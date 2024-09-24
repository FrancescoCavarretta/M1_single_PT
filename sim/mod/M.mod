: Comment :
: : M-type potassium current from L5 pyramidal neurons of neocortex
: :
: : Modeled by Francesco Cavarretta
: : Jaegelab, Emory University
: : e-mail: francesco.cavarretta.neuro@gmail.com; francesco.cavarretta@emory.edu
: : written on 03/01/2024
: :
: :
: References :
: : 1. Battefeld, Arne, et al. "Heteromeric Kv7. 2/7.3 channels differentially regulate action potential initiation and conduction in neocortical myelinated axons." 
: : Journal of Neuroscience 34.10 (2014): 3719-3732.
: : 2. Guan, Dongxu, et al. "Contributions of Kv7-mediated potassium current to sub-and suprathreshold responses of rat layer II/III neocortical pyramidal neurons." 
: : Journal of Neurophysiology 106.4 (2011): 1722-1733.

NEURON {
	SUFFIX kM
	USEION k READ ek WRITE ik
  
	RANGE gbar, q10
	GLOBAL vshift, mtau_factor, mtau_min
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
	gbar	= 0		(S/cm2)
	vshift	= 0		(mV)
	mtau_factor	= 1
	mtau_min	= 0	(ms)

	q10		= 2.5			: see Ref. 2
	T0		= 35	(degC)	: used for q10 calculation    
	mk_factor	= 1	(1)
  
}


ASSIGNED {
	celsius	(degC)
	q
  
	v		(mV)
	ek		(mV)
	ik		(mA/cm2)
  
	minf
	mtau	(ms)
}


STATE {
	m FROM 0 TO 1
}



BREAKPOINT {
        SOLVE states METHOD cnexp
        ik = m * gbar * (v - ek)
}
 

INITIAL {
	q = q10 ^ ((celsius - T0) / 10) : temperature dependence factor, see ref. 2
  
	rates(v + vshift)

	m = minf

}


DERIVATIVE states {  
	rates(v + vshift)
	m' = (minf - m ) / mtau
}


PROCEDURE rates(v (mV)) {
	: see ref 2 for both

	: time constant
	mtau = (mtau_min + mtau_factor * (13.4 + 26.3 * exp(-((v + 29.7) / 30.3) ^ 2))) / q
		          
	: see Fig. 2, Ref. 1
	minf = 1 / (1 + exp(-(v + 36.7) / (9.48 * mk_factor) )) : activation
}








