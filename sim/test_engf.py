from math import exp, pi
import pickle
import numpy as np

with open('cells/cellDensity.pkl', 'rb') as fileObj:
  density = pickle.load(fileObj)['density']


RADIUS = 150

def calc_n_neuron(dens, height, radius=RADIUS):
  return (dens * 1e-9) * ((radius ** 2) * pi) * height

Ntot = calc_n_neuron(density[('M1','I')][0], 740 - 620)
                     
vol = ((RADIUS ** 2) * pi) * (740 - 620)

dens = Ntot / vol

dx = dens ** (- 1 / 3)
#l = 354.5

l = 94.5
#r = exp(-dx/ l)
N = int(round(RADIUS / dx))
vh = 9
s = 0
stot = 0
for i in range(N + 1):
  n = (740 - 620) / dx * (2 * i * dx * pi) / dx
  s += i / (1 + exp( (i * dx-vh) / l))
  stot += i
print('prob', s / stot)

RADIUS = 150
N = int(round(RADIUS / dx))
s = 0
stot = 0
for i in range(int(round(150 / dx)) + 1, int(round(400 / dx)) + 1):
  n = (740 - 620) / dx * (2 * i * dx * pi) / dx
  #s += i * exp( -i * dx / l)
  s += i / (1 + exp( (i * dx-vh) / l))
  stot += i
print('prob', s / stot)
#print(2 * ((810 / dx) + 1) * (1 - r ** (N + 1)) / (1 - r) / Ntot)

#s = 0
for i in range(N):
#  s += 2 * (620 + 190) / dx * i * pi / ( 1 + exp(i * dx / l) )
  s += 2 * (740 - 620) / dx * i * pi / (1 + exp( (i * dx-vh) / l))
  #print(i, 2 * (620 + 190) / dx * i * pi , exp(- i * dx / l))
print(s)
