# Standalone exact-rational checker for E002-363; no third-party dependencies.
from fractions import Fraction as Q
F,w=Q(1,30),Q(1,100)
eps_over_rho=Q(9,100)
Dcrit=F-w+4*eps_over_rho*w
def overlap(a,b,n):
    return max(Q(0),min(b,n*F+w)-max(a,n*F))
def obs(intervals):
    return [sum((overlap(a,b,n) for a,b in intervals),Q(0)) for n in range(-7,8)]
# Exact long-bout collision: two 120ms closed bouts, 20ms gap vs merged 260ms.
g0,g1=Q(11,1000),Q(31,1000)
a,d=g0-Q(120,1000),g1+Q(120,1000)
assert obs([(a,g0),(g1,d)])==obs([(a,d)])
# Exactly at the noise boundary, each of two shutter overlaps is 2epsilon/rho.
x=(Dcrit-(F-w))/2
o=obs([(w-x,w-x+Dcrit)])
assert max(o)/w==2*eps_over_rho and o.count(x)==2
# An event fitting in shutter dead time is invisible.
assert max(obs([(w,w+(F-w)/2)]))==0
# G=F+w always admits a complete exposure for every tested rational phase.
for i in range(600):
    start=Q(i,600)*F
    assert any(start<=n*F and n*F+w<=start+F+w for n in range(-1,4))
assert Dcrit==Q(101,3750)
print("PASS: exact RGB-occupancy collision, exact noise boundary, 600 rational phases")
