from statistics import NormalDist
from scipy.optimize import brentq
N=NormalDist()
for s in (0.8,1.5,2.5):
 for g in (1.2,1.6,2.2):
  root=brentq(lambda x:N.cdf(x/s)**g-0.5,-4*s,4*s)
  assert abs(root-s*N.inv_cdf(0.5**(1/g)))<1e-9
print('Independent gamma-root checks PASS')
