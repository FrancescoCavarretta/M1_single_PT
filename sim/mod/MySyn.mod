TITLE simple AMPA receptors

COMMENT
-----------------------------------------------------------------------------

	Simple model for glutamate AMPA receptors
	=========================================

  - FIRST-ORDER KINETICS, FIT TO WHOLE-CELL RECORDINGS

    Whole-cell recorded postsynaptic currents mediated by AMPA/Kainate
    receptors (Xiang et al., J. Neurophysiol. 71: 2552-2556, 1994) were used
    to estimate the parameters of the present model; the fit was performed
    using a simplex algorithm (see Destexhe et al., J. Computational Neurosci.
    1: 195-230, 1994).

  - SHORT PULSES OF TRANSMITTER (0.3 ms, 0.5 mM)

    The simplified model was obtained from a detailed synaptic model that
    included the release of transmitter in adjacent terminals, its lateral
    diffusion and uptake, and its binding on postsynaptic receptors (Destexhe
    and Sejnowski, 1995).  Short pulses of transmitter with first-order
    kinetics were found to be the best fast alternative to represent the more
    detailed models.

  - ANALYTIC EXPRESSION

    The first-order model can be solved analytically, leading to a very fast
    mechanism for simulating synapses, since no differential equation must be
    solved (see references below).



References

   Destexhe, A., Mainen, Z.F. and Sejnowski, T.J.  An efficient method for
   computing synaptic conductances based on a kinetic model of receptor binding
   Neural Computation 6: 10-14, 1994.

   Destexhe, A., Mainen, Z.F. and Sejnowski, T.J. Synthesis of models for
   excitable membranes, synaptic transmission and neuromodulation using a
   common kinetic formalism, Journal of Computational Neuroscience 1:
   195-230, 1994.

Modified by Penny under the instruction of M.L.Hines on Oct 03, 2017
	Change gmax

-----------------------------------------------------------------------------
ENDCOMMENT



NEURON {
	POINT_PROCESS MySyn
	RANGE R, gmax, g, Cdur, tau1, tau2, e
	NONSPECIFIC_CURRENT  i
	:GLOBAL Cdur, Erev
}
UNITS {
	(nA) = (nanoamp)
	(mV) = (millivolt)
	(uS) = (microsiemens)
	(mM) = (milli/liter)
}

PARAMETER {
:    Cmax	= 0.1	(mM)		: max transmitter concentration
:	Cdur	= 0.3	(ms)		: transmitter duration (rising phase)
:	Cdur	= 0.1	(ms)		: transmitter duration (rising phase)
:	Alpha	= 0.94	(/ms)	: forward (binding) rate
:	Alpha	= 1	(/ms)	: forward (binding) rate
:	Beta	= 0.018	(/ms)		: backward (unbinding) rate
:	Beta	= 0.5 (/ms)		: backward (unbinding) rate
	e	= 0	(mV)		:0 reversal potential
	gmax    = 1  (uS)

    tau1 = 0.05 (ms)
    tau2 = 5.3
}


ASSIGNED {
	v		(mV)		: postsynaptic voltage
	i 		(nA)		: current = g*(v - Erev)
	g 		(uS)		: conductance
	:Rinf				: steady state channels open
	:Rtau		(ms)		: time constant of channel binding
	synon
        Rmax
        R
        Cdur
}

STATE {Ron Roff}

INITIAL {
    :Rinf = Cmax*Alpha / (Cmax*Alpha + Beta)
    :Rtau = 1 / ((Alpha * Cmax) + Beta)
    Rmax = exp(-Cdur / tau1)
    synon = 0
    Cdur = tau1 / 2 * 3
}

BREAKPOINT {
	SOLVE release METHOD cnexp
        R = (Ron + Roff) / Rmax
	g = R * gmax
	i = g*(v - e)

}

DERIVATIVE release {
	Ron' = (synon - Ron) / tau1
	Roff' = -Roff / tau2
}

: following supports both saturation from single input and
: summation from multiple inputs
: if spike occurs during CDur then new off time is t + CDur
: ie. transmitter concatenates but does not summate
: Note: automatic initialization of all reference args to 0 except first

NET_RECEIVE(weight, on, nspike, r0, t0 (ms)) {
	: flag is an implicit argument of NET_RECEIVE and  normally 0
        if (flag == 0) { : a spike, so turn on if not already in a Cdur pulse
		nspike = nspike + 1
		if (!on) {
			r0 = r0 * exp(-(t - t0) / tau1)
			t0 = t
			synon = synon + weight
			state_discontinuity(Ron, Ron + r0)
			state_discontinuity(Roff, Roff - r0)
			on = 1
		}
                         
		: come again in Cdur with flag = current value of nspike
		net_send(Cdur, nspike)
        }
	if (flag == nspike) { : if this associated with last spike then turn off
		r0 = weight + (r0 - weight) * exp(-(t - t0)/tau1)
		t0 = t
		synon = synon - weight
		state_discontinuity(Ron, Ron - r0)
		state_discontinuity(Roff, Roff + r0)
		on = 0
	}
}
