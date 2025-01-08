from math import exp, pi
import pickle
import numpy as np

with open('cells/cellDensity.pkl', 'rb') as fileObj:
  density = pickle.load(fileObj)['density']


RADIUS = 200

def calc_n_neuron(dens, height, radius=RADIUS):
  return (dens * 1e-9) * ((radius ** 2) * pi) * height

Ntot = calc_n_neuron(density[('M1','SOM')][5]*0.44, 620 - 300) + \
       calc_n_neuron(density[('M1','SOM')][2]*0.34, 300 - 190) + \
       calc_n_neuron(density[('M1','SOM')][3]*0.34, 190 + 190) + \
       calc_n_neuron(density[('M1','SOM')][4]*0.34, -190 + 425)

vol = ((RADIUS ** 2) * pi) * (620 + 190)

dens = Ntot / vol

dx = dens ** (- 1 / 3)
#l = 354.5

l = 91.5
#r = exp(-dx/ l)
N = int(round(RADIUS / dx))
vh = 300
s = 0
stot = 0
for i in range(N + 1):
  n = (620 + 190) / dx * (2 * i * dx * pi) / dx
  s += i / (1 + exp( (i * dx-vh) / l))
  stot += i
print('prob', s / stot)

RADIUS = 400
N = int(round(RADIUS / dx))
s = 0
stot = 0
for i in range(N + 1):
  n = (620 + 190) / dx * (2 * i * dx * pi) / dx
  #s += i * exp( -i * dx / l)
  s += i / (1 + exp( (i * dx-vh) / l))
  stot += i
print('prob', s / stot)
#print(2 * ((810 / dx) + 1) * (1 - r ** (N + 1)) / (1 - r) / Ntot)

#s = 0
for i in range(N):
#  s += 2 * (620 + 190) / dx * i * pi / ( 1 + exp(i * dx / l) )
  s += 2 * (620 + 190) / dx * i * pi / (1 + exp( (i * dx-vh) / l))
  #print(i, 2 * (620 + 190) / dx * i * pi , exp(- i * dx / l))
print(s)
