from math import sqrt, exp, pi
import numpy as np

llambda = 77

def f(x, y):
  return 2 * pi * x * exp(-sqrt(x * x + y * y) / llambda)


d = 0.5
S = 0.0
for x in np.linspace(0, 500, int(500 / d)  + 1):
  for y in np.linspace(-60, 60, 2 * int(120 / d)  + 1):
    S += (f(x, y) + f(x + d, y) + f(x, y + d) + f(x + d, y + d)) * (d ** 2) / 4

print(S)
    
dens = 1579.86 * 1e-9

print(S * dens)


def integrate_2(d=2.5):
  S = 0.0
  Stot = 0.0
  for x in np.linspace(0, 500, int(500 / d)  + 1):
    for y in np.linspace(-60, 60, 2 * int(120 / d)  + 1):
      if sqrt(x * x + y * y) <= 200:
        S += (f(x, y) + f(x + d, y) + f(x, y + d) + f(x + d, y + d)) * (d ** 2) / 4
        Stot += 2 * pi * (x + (x + d)) * d / 2 * d
        
  return S / Stot

print(integrate_2() )

