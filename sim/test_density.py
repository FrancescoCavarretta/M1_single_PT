from math import exp, pi
import pickle
import numpy as np

layers = {'L1': 128, 'L2': 141, 'L3': 149, 'L4': 170, 'L5A': 120, 'L5B': 182, 'L6': 264}
ninh = { 'L1':26, 'L2':107, 'L3':123, 'L4':140, 'L5A':90, 'L5B':131, 'L6':127}
nexc = {'L2':546,'L3':1145,'L4':1656,'L5A':454,'L5B':641,'L6':1288}

sst = {'L1':0.024, 'L2':0.352, 'L3':0.352, 'L4':0.199, 'L5A':0.268, 'L5B':0.10, 'L6':0.057}
pv = {'L1':0.00, 'L2':0.15, 'L3':0.15, 'L4':0.279, 'L5A':0.296, 'L5B':0.194, 'L6':0.081}
vip = {'L1':0.098, 'L2':0.393, 'L3':0.393, 'L4':0.344, 'L5A':0.098, 'L5B':0.066, 'L6':0.00}

S = 300 * 300
volumes = { l:(S * h * 1e-9) for l, h in layers.items() }

print('excitatory')
for l, n in sorted( nexc.items() ):
  print(l, n / volumes[l])

print()
print('inhibitory')
for l, n in sorted( ninh.items() ):
  print(l, n / volumes[l])


print()
print('inhibitory (pv vs som)')
for l, n in sorted( ninh.items() ):
  print(l, n / volumes[l] * pv[l], ' PV vs ', n / volumes[l] * pv[l] * sst[l], ' SST')


print()
print('SST+ inhibitory (Martinotti vs non-Martinotti)')
for l, n in sorted( ninh.items() ):
  if l in ['L2', 'L3']:
    p = 0.44
  else:
    p = 0.35
    
  print(l, n / volumes[l] * pv[l] * sst[l] * p, ' vs ', n / volumes[l] * pv[l] * sst[l] * (1 - p))

mc_tot = 0
nmc_tot = 0
print()
print('SST+ inhibitory (Martinotti vs non-Martinotti) connected')
for l, n in sorted( ninh.items() ):
  if l in ['L2', 'L3']:
    p = 0.44
  else:
    p = 0.35

  mc_tot += n / volumes[l] * pv[l] * sst[l] * p * 0.52
  nmc_tot += n / volumes[l] * pv[l] * sst[l] * (1 - p) * 0.03
  print(l, n / volumes[l] * pv[l] * sst[l] * p * 0.52, ' vs ', n / volumes[l] * pv[l] * sst[l] * (1 - p) * 0.03)
print(mc_tot, ' vs ', nmc_tot)
