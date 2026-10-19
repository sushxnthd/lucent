"""Independent arithmetic checks of E002-302 (no human data)."""
from fractions import Fraction
from math import ceil
from cert_core import threshold,sign_certificate
for n in range(3,31):
    for alpha in (Fraction(1,20),Fraction(1,10),Fraction(1,4)):
        k=ceil((n+1)*(1-float(alpha))-1e-12)
        guaranteed=Fraction(min(k,n+1),n+1)
        assert guaranteed>=1-alpha
assert sign_certificate(1,1.1,.05)==1
assert sign_certificate(1,1.02,.05)==0
assert sign_certificate(1,1/.9,.05)==1
# If the true log change is zero, a sign certificate implies residual > d.
import math
s=math.log(1.1)
assert s>.05 and abs(s-0)>.05
assert threshold(list(range(18)),.05)==float("inf")
print("independent rank and sharp-sign checks passed")
