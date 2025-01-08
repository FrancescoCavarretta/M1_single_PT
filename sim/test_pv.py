from math import exp, pi, sqrt
import pickle
import numpy as np

with open('cells/cellDensity.pkl', 'rb') as fileObj:
  density = pickle.load(fileObj)['density']


RADIUS = 500

def calc_n_neuron(dens, height, radius=RADIUS):
  return (dens * 1e-9) * ((radius ** 2) * pi) * height

Ntot = calc_n_neuron(density[('M1','PV')][3], 190 + 190) 
#Ntot = calc_n_neuron(6788.0, 190 + 190) 
vol = ((RADIUS ** 2) * pi) * (190 + 190)

dens = Ntot / vol

dx = dens ** (- 1 / 3)
#l = 354.5

ke = 197
ne = 2.75

N1 = int(round(RADIUS / dx))
N2 = int(round(380 / 2 / dx))

s = 0
stot = 0
for i in range(N1 + 1):
  for j in range(N2 + 1):
    rc = i * dx
    h = j * dx
    dd = sqrt(i*i + j*j) * dx
    if dd <= 200:
      s += i * 2 * pi * 2 * exp(-dd / 124) #* ( 1 / ( 1 + ((dd / ke) ** ne) ) )
      stot += i * 2 * pi * 2
print('prob', s / stot)

for i in range(N1 + 1):
  for j in range(N2 + 1):
    rc = i * dx
    h = j * dx
    dd = sqrt(j*j + i*i) * dx
    if dd <= 400:
      s += i * 2 * pi * 2 * exp(-dd / 124) # * ( 1 / ( 1 + ((dd / ke) ** ne) ) )
      stot += i * 2 * pi * 2
print('prob', s / stot)

for i in range(N1 + 1):
  for j in range(N2 + 1):
    rc = i * dx
    h = j * dx
    dd = sqrt(j*j + i*i) * dx
    s += i * 2 * pi * 2 * exp(-dd / 124) #( 1 / ( 1 + ((dd / ke) ** ne) ) )
    stot += i * 2 * pi * 2
    
print('prob', s / stot)
print('prob', s / stot * calc_n_neuron(6788.0, 190 + 190) )
