from math import sqrt, exp, pi
import numpy as np

def f(x, y, z):
  return exp(-sqrt(x * x + y * y + z * z) / 124)

def integrate(X=250, Y=250, Z=250, d=2.5):
  S = 0.0
  for x in np.linspace(-X, X, 2 * int(X / d) + 1):
    for y in np.linspace(-Y, Y, 2 * int(Y / d)  + 1):
      for z in np.linspace(-Z, Z, 2 * int(Z / d)  + 1 ):
        S += (d ** 3) / 8 * (f(x, y, z) + \
                             f(x + d, y, z) + \
                             f(x, y + d, z) + \
                             f(x + d, y + d, z) + \
                             f(x, y, z + d) + \
                             f(x + d, y, z + d) + \
                             f(x, y + d, z + d) + \
                             f(x + d, y + d, z + d))
  return S

##S = integrate()
##    
##dens = 40000 * 0.2 * 0.25 * 1e-9
##
##print(S * dens)
##
##
##
##def integrate_2(X=250, Y=250, Z=250, d=2.5):
##  S = 0.0
##  Stot = 0.0
##  for x in np.linspace(-X, X, 2 * int(X / d) + 1):
##    for y in np.linspace(-Y, Y, 2 * int(Y / d)  + 1):
##      for z in np.linspace(-Z, Z, 2 * int(X / d)  + 1 ):
##        if sqrt(x * x + y * y + z * z) <= 200:
##          S += (d ** 3) / 8 * (f(x, y, z) + \
##                               f(x + d, y, z) + \
##                               f(x, y + d, z) + \
##                               f(x + d, y + d, z) + \
##                               f(x, y, z + d) + \
##                               f(x + d, y, z + d) + \
##                               f(x, y + d, z + d) + \
##                               f(x + d, y + d, z + d))
##          Stot += d ** 3
##  return S / Stot
##      #print(x,y,z)
##
##print(integrate_2() )


print( 1152 * 1e-9 * integrate(553, 553, 137.5) )



