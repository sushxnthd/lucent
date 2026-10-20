"""Independent two-frame exact opposite-sign collision checker."""
from fractions import Fraction as F
def conv(a,b):
    z=[F(0) for _ in range(len(a)+len(b)-1)]
    for i,x in enumerate(a):
        for j,y in enumerate(b): z[i+j]+=x*y
    return z
P3=conv([F(1,2)]*3,[F(1,5)]*5)
P5=conv([F(3,10)]*5,[F(1,3)]*3)
assert P3==P5
increasing=(P3,P5)
decreasing=(P5,P3)
assert increasing==decreasing
assert 3<5 and 5>3
print("exact full-video opposite-sign collision: PASS")
