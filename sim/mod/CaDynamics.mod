: Dynamics that track inside calcium concentration
: modified from Destexhe et al. 1994

NEURON	{
	SUFFIX CaDynamics
	USEION ca READ ica WRITE cai VALENCE 2
	USEION ca_hvaP READ ica_hvaP WRITE ca_hvaPi VALENCE 2
	USEION ca_hvaNL READ ica_hvaNL WRITE ca_hvaNLi VALENCE 2
    USEION ca_lva READ ica_lva WRITE ca_lvai VALENCE 2
	RANGE depth_hvaP, depth_hvaNL, depth_lva, decay_hvaP, decay_hvaNL, decay_lva, decay, minCai 
	RANGE gamma_hvaP, gamma_hvaNL, gamma_lva
}

UNITS	{
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
	gamma_hvaP	=	0.05	(1)		: percent of free calcium (not buffered)
	gamma_hvaNL	=	0.05	(1)		: percent of free calcium (not buffered)
	gamma_lva	=	0.05	(1)		: percent of free calcium (not buffered)

	decay_hvaP	=	80		(ms)	: rate of removal of calcium
	decay_hvaNL	=	80		(ms)	: rate of removal of calcium
	decay_lva	=	80		(ms)	: rate of removal of calcium
	decay		=	80		(ms)	: rate of removal of calcium

	depth_hvaP	=	0.1		(um)	: depth of shell
	depth_hvaNL	=	0.1		(um)	: depth of shell
	depth_lva	=	0.1		(um)	: depth of shell

	minCai		=	8e-5	(mM)	
	
	cao 		= 2			(mM)
	ca_lvao		= 2			(mM)
	ca_hvaPo	= 2			(mM)
	ca_hvaNLo	= 2			(mM)
}

ASSIGNED	{
  ica			(mA/cm2)
  ica_lva		(mA/cm2)
  ica_hvaP		(mA/cm2)
  ica_hvaNL		(mA/cm2)
}

STATE	{
	ca_lvai		(mM)
	ca_hvaPi	(mM)
	ca_hvaNLi	(mM)
	cai			(mM)
}

BREAKPOINT	{ 
	SOLVE states METHOD cnexp
}

INITIAL {
  cai 		= minCai
  ca_lvai	= minCai
  ca_hvaPi	= minCai
  ca_hvaNLi	= minCai
}

DERIVATIVE states	{ LOCAL drive_channel

        drive_channel = - 10000 / (2*FARADAY) * ( gamma_lva*ica_lva/depth_lva + gamma_hvaP*ica_hvaP/depth_hvaP + gamma_hvaNL*ica_hvaNL/depth_hvaNL )
        if (drive_channel < 0) { drive_channel = 0 }        : cannot pump inward  
		cai' =  drive_channel - (ca_lvai - minCai) / decay

        drive_channel =  - 10000 / (2*FARADAY) * (1-gamma_lva)*ica_lva/depth_lva
        if (drive_channel < 0) { drive_channel = 0 }        : cannot pump inward  
		ca_lvai' =  drive_channel - (ca_lvai - minCai) / decay_lva

        drive_channel =  - 10000 / (2*FARADAY) * (1-gamma_hvaP)*ica_hvaP/depth_hvaP 
        if (drive_channel < 0) { drive_channel = 0 }        : cannot pump inward 
		ca_hvaPi' =  drive_channel - (ca_hvaPi - minCai) / decay_hvaP

        drive_channel =  - 10000 / (2*FARADAY) * (1-gamma_hvaNL)*ica_hvaNL/depth_hvaNL 
        if (drive_channel < 0) { drive_channel = 0 }        : cannot pump inward 
		ca_hvaNLi' =  drive_channel - (ca_hvaNLi - minCai) / decay_hvaNL
}
