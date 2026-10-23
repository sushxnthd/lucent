"""E002-380 independent exact shutter-phase oracle. Synthetic, not human."""
from fractions import Fraction as Q
from random import Random

def overlap(a,b,c,d): return max(Q(0),min(b,d)-max(a,c))
def direct(s,F,w,D,offsets):
    best=Q(0)
    for delta in offsets:
        for n in range(-4,7):
            t=n*F+delta
            best=max(best,overlap(s,s+D,t,t+w))
    return best
def witness(F,w,D,m,offsets):
    knots={Q(0)}
    for d in offsets:
        knots.add((d+m-D)%F); knots.add((d+w-m)%F)
    knots=sorted(knots)
    tests=knots+[(a+b)/2 for a,b in zip(knots,knots[1:])]+[(knots[-1]+F)/2]
    return next((s for s in tests if direct(s,F,w,D,offsets)<m),None)
def theorem(F,w,D,m,offsets):
    if not offsets or not 0<m<=min(w,D):return False
    xs=sorted(set(d%F for d in offsets))
    G=max([b-a for a,b in zip(xs,xs[1:])]+[F+xs[0]-xs[-1]])
    return D+w-2*m>=G
def check():
    rng=Random(380)
    for _ in range(3000):
        F=Q(rng.randint(20,80),1000)
        w=F*Q(rng.randint(1,8),10)
        D=F*Q(rng.randint(1,16),10)
        m=min(D,w)*Q(rng.randint(1,10),10)
        offsets=[F*Q(rng.randrange(1000),1000) for j in range(rng.randint(1,8))]
        assert (witness(F,w,D,m,offsets) is None)==theorem(F,w,D,m,offsets)
    F=Q(1,30);w=Q(1,100);five=[Q(j,200) for j in range(5)]
    for D,m in [(Q(24,1000),w),(Q(15,1000),Q(4,1000))]:
        assert theorem(F,w,D,m,five)
        assert not theorem(F,w,D,m,five[1:4])
        assert witness(F,w,D,m,five[1:4]) is not None
    assert not theorem(F,w,Q(15,1000),Q(4,1000),[Q(j,4000) for j in range(5)])
    print('E002-380: 3000 exact randomized checks and frozen tests PASS')
if __name__=='__main__':check()
