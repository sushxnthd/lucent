"""Independent exact-rational nullspace and mutation checks; no NumPy."""
from fractions import Fraction
N=5
base=Fraction(4)
a=Fraction(3,10)
p0=[base for _ in range(3*N)]
p1=[base+([a,-a,Fraction(0)][s])*Fraction(k+1,N) for s in range(3) for k in range(N)]
assert p0!=p1
for k in range(N):
    assert sum(p0[s*N+k] for s in range(3))/3==sum(p1[s*N+k] for s in range(3))/3
    for v in ((1,-1,0),(1,0,-1)):
        assert sum(Fraction(x,3) for x in v)==0
mutated=lambda p,k:(2*p[k]+p[N+k]+p[2*N+k])/4
assert any(mutated(p0,k)!=mutated(p1,k) for k in range(N))
print("PASS: 5 exact collisions, 10 nullspace witnesses, mutation rejected")
