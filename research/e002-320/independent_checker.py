"""Independent exact-rational minimax phase search. Does not import model.py."""
from fractions import Fraction as F
import random
def overlap(s,d,l,r): return max(F(0),min(s+d,r)-max(s,l))
def phase_minimax(P,E,d):
    intervals=[(k*P,k*P+E) for k in range(-2,4)]
    breaks={F(0),P}
    for l,r in intervals:
        breaks.update(x for x in (l-d,r-d,l,r) if 0<x<P)
    breaks=sorted(breaks)
    candidates=set(breaks)
    for left,right in zip(breaks[:-1],breaks[1:]):
        lines=[]
        for l,r in intervals:
            yl=overlap(left,d,l,r);yr=overlap(right,d,l,r)
            m=(yr-yl)/(right-left);lines.append((m,yl-m*left))
        for i,(m,b) in enumerate(lines):
            for n,c in lines[i+1:]:
                if m!=n:
                    x=(c-b)/(m-n)
                    if left<=x<=right: candidates.add(x)
    return min((max(overlap(s,d,l,r) for l,r in intervals),s) for s in candidates)
if __name__=="__main__":
    rng=random.Random(3202026)
    for i in range(600):
        P=F(rng.randint(6,80),rng.randint(1,20))
        E=P*F(rng.randint(1,19),20)
        d=P*F(rng.randint(1,20),20)
        observed,phase=phase_minimax(P,E,d)
        expected=max(F(0),d-(P-E))/2
        assert observed==expected,(P,E,d,observed,expected)
    P,E,eta=F(1,24),F(1,80),F(7,100)
    assert P-E+4*eta*E==F(49,1500)
    assert phase_minimax(P,E,F(31,1000))[0]<=2*eta*E
    assert phase_minimax(P,E,F(35,1000))[0]>2*eta*E
    print("PASS: 600 exact rational geometries and frozen synthetic crossing")
