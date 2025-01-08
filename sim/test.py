from neuron import h
import numpy as np
h.load_file("nrngui.hoc")
h.load_file("cells/PTcell_orig.hoc")
h.cvode_active(1)
c = h.PTcell()



def convert():
  global tvec, vvec
  tvec1 = np.array([x for x in tvec])
  vvec1 = np.array([x for x in vvec])
  tvec = np.linspace(0.0, h.tstop, 14000)
  vvec = np.interp(tvec, tvec1, vvec1)
  
def ap_threshold(t, v, thresh=20):
  idx = np.argwhere((v[1:] - v[:-1]) / (t[1:] - t[:-1]) >= thresh)[0, 0]
  return t[idx], v[idx]

def ap_peak(t, v, thresh=20):
  tap = ap_threshold(t, v, thresh)[0]
  idx = np.argwhere(t >= tap)[:,0]
  imax = np.argmax(v[idx])
  return t[idx[imax]], v[idx[imax]]


def ap_amplitude(t, v, thresh=20):
  return ap_peak(t, v, thresh)[1] - ap_threshold(t, v, thresh)[1]


def get_ap_chunk(t, v, thresh=20):
  tap, vap = ap_threshold(t, v, thresh)
  idx = np.argwhere(v >= vap)[:, 0]
  try:
    idx2 = np.argwhere((idx[1:] - idx[:-1]) > 1)[0, 0]+1
  except IndexError:
    idx2 = idx.size
  return t[idx[:idx2]], v[idx[:idx2]]
  
  
def ap_half_width(t, v, thresh=20):
  t, v = get_ap_chunk(t, v, thresh=20)
  ipk = np.argmax(v)
  tpk, vpk = t[ipk], v[ipk]
  vamp = vpk - v[0]
  vamp_h = vamp * 0.5 + v[0]
  ihalf = np.argmin(np.abs(v[ipk:] - vamp_h)) + ipk
  th = t[ihalf]
  return th - tpk


def ap_fahp(t, v, thresh=20, dt=5):
  tap1, vth = ap_threshold(t, v, thresh)
  tap2 = tap1 + dt
##  import matplotlib.pyplot as plt
##  plt.plot(v[np.argwhere((t >= tap1) & (t <= tap2))[:, 0]])
##  plt.show()
  vmin = np.min(v[np.argwhere((t >= tap1) & (t <= tap2))[:, 0]])
  return abs(vmin - vth)


def ap_rise(t, v, thresh=20):
  tap = ap_threshold(t, v, thresh)[0]
  tpk = ap_peak(t, v, thresh)[0]
  return abs(tpk - tap)


def ap_decay(t, v, thresh=20):
  tap, vap = ap_threshold(t, v, thresh)
  tpk = ap_peak(t, v, thresh)[0]
  
  tap2 = t[np.argwhere((t >= tap) & (v >= vap))[-1, 0]]
  

  return abs(tap2 - tpk)

ic = h.IClamp(0.5, sec=c.soma)
ic.delay = 5000
ic.dur = 1000
h.tstop = 7000
ic.amp = .12+0.04

def run():
  global tvec, vvec
  vvec = h.Vector()
  vvec.record(c.soma(0.5)._ref_v)
  tvec = h.Vector()
  tvec.record(h._ref_t)
  
  h.run()
  convert()

  for f in [ap_threshold, ap_amplitude, ap_half_width, ap_fahp, ap_rise, ap_decay]:
    print(f.__name__, f(tvec, vvec))


if __name__ == '__main__':
  apc = h.APCount(0.5, sec=c.soma)
  
####  h('forall for(x,0) gbar_naP(x)*=2')
####  ic.amp = 0.08
####  while ic.amp <= 0.4:
####    h.run()
####    print(ic.amp, '\t', apc.n)
####    ic.amp += 0.08
####
####  print()
####  h('forall gbar_naP=0')
####  #h('forall gbar_kBK=0')
####  #h('forall for(x,0) gbar_naT(x)*=0.2')
####  ic.amp = 0.08
####  while ic.amp <= 0.4:
####    h.run()
####    print(ic.amp, '\t', apc.n)
####    ic.amp += 0.08
