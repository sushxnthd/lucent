"""E002-670: frozen synthetic held-out exposure-certificate challenge.
Not human or physical evidence. Standard-library only; deterministic seed.
"""
import random
from fractions import Fraction as F

SEED=6702026
TAU=F(3,10)
WIDTH=F(1,30)
V=F(60)
ETA=F(1,100)

def closure_limit(w,v,tau):
    d=1-tau
    r=min(w,d/v)
    return 1-(d*r-v*r*r/2)/w

def integrate_piecewise(knots):
    """Exact trapezoid integral of a piecewise-linear aperture."""
    return sum((t1-t0)*(a0+a1)/2 for (t0,a0),(t1,a1) in zip(knots,knots[1:])) / (knots[-1][0]-knots[0][0])

def min_aperture(knots):
    return min(a for _,a in knots)

def lipschitz(knots):
    return max(abs((b-a)/(s-t)) for (t,a),(s,b) in zip(knots,knots[1:]))

def make_trajectory(rng):
    # 4 equal segments; constrained random walk, ground truth exact.
    t=[WIDTH*F(i,4) for i in range(5)]
    a=[F(rng.randrange(0,101),100)]
    for i in range(4):
        delta=V*(t[i+1]-t[i]); lo=max(F(0),a[-1]-delta); hi=min(F(1),a[-1]+delta)
        candidate=F(rng.randrange(0,101),100)
        a.append(min(hi,max(lo,candidate)))
    return list(zip(t,a))

def run():
    rng=random.Random(SEED)
    limit=closure_limit(WIDTH,V,TAU)
    assert limit==F(351,400)
    cases=5000
    certified=0; actual_closure=0; false_certificates=0; abstained=0
    for _ in range(cases):
        k=make_trajectory(rng)
        assert lipschitz(k)<=V
        true_mean=integrate_piecewise(k)
        err=F(rng.randrange(-100,101),10000)
        assert abs(err)<=ETA
        measured=true_mean+err
        cert=measured-ETA>limit
        closed=min_aperture(k)<=TAU
        certified+=cert; actual_closure+=closed; abstained+=not cert
        false_certificates+=bool(cert and closed)
    assert false_certificates==0
    reach=(1-TAU)/V
    witness=[(F(0),TAU),(reach,F(1)),(WIDTH,F(1))]
    assert integrate_piecewise(witness)==limit
    assert min_aperture(witness)==TAU
    assert not (limit-ETA>limit)
    print(f'E002-670 PASS seed={SEED} n={cases} certified={certified} abstained={abstained} closures={actual_closure} false_certificates={false_certificates} limit={limit}')
if __name__=='__main__':run()
