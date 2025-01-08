from math import sqrt, exp, pi
import numpy as np

def f(x, y):
  return 2 * pi * x * exp(-sqrt(x * x + y * y) / 124)


def get_prob(depth0=0, depth1=137.5, radius=553, d=0.0625):
  S = 0.0
  for x in np.linspace(0, radius, int(radius / d)  + 1):
    for y in np.linspace(depth0, depth1, int((depth1 - depth0) / d)  + 1):
      S += (f(x, y) + f(x + d, y) + f(x, y + d) + f(x + d, y + d)) * (d ** 2) / 4
  return S

S0 = get_prob(depth0=(137.5+76), depth1=(137.5+76+315)) * 1321 * 1e-9
print('# PV+ connected neurons in layer 2/3', round(S0))
S1 = get_prob(depth0=137.5, depth1=(137.5+76)) * 2467 * 1e-9
print('# PV+ connected neurons in layer 5A', round(S1))
S2 = get_prob(depth0=-137.5, depth1=137.5) * 1152 * 1e-9
print('# PV+ connected neurons in layer 5B', round(S2))
S3 = get_prob(depth0=137.5, depth1=(137.5+265), d=0.0625) * 433 * 1e-9
print('# PV+ connected neurons in layer 6', round(S3))
print()
print('# PV+ connected neurons', round(S0+S1+S2+S3))
