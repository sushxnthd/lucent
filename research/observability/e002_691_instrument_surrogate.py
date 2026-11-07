"""E002-691: seeded piecewise-linear occluder surrogate; NOT physical/human evidence."""
from fractions import Fraction as F
import random

def minimum(a,b,v,h):
    if abs(a-b)>v*h: return None
    return max(F(0),(a+b-v*h)/2)

def simulate(seed=691,n=20000):
    rng=random.Random(seed)
    counts={'trials':0,'excluded':0,'hidden':0,'false_exclusion':0,'naive_false_exclusion':0,'uncertain_abstentions':0}
    for _ in range(n):
        h=F(rng.randint(2,20),10)
        v=F(rng.randint(1,6))
        a=F(rng.randint(2,20),10)
        b=F(rng.randint(2,20),10)
        if abs(a-b)>v*h: continue
        c=F(rng.randint(0,8),10)
        # A reachable midpoint at h/2, under |velocity| <= v.
        low=max(F(0),a-v*h/2,b-v*h/2)
        high=min(a+v*h/2,b+v*h/2)
        midpoint=low+(high-low)*F(rng.randint(0,10),10)
        actual_min=min(a,b,midpoint)
        # Nominal timestamp underestimates actual blind interval.
        h_nom=h*F(rng.randint(5,10),10)
        uncert=F(rng.randint(0,5),10)
        hplus=h+F(rng.randint(0,5),10)
        al=max(F(0),a-uncert); bl=max(F(0),b-uncert)
        robust=minimum(al,bl,v,hplus)
        naive=minimum(a,b,v,h_nom)
        assert robust is not None
        excluded=robust>c
        naive_excluded=naive is not None and naive>c
        closed=actual_min<=c
        counts['trials']+=1
        counts['excluded']+=int(excluded)
        counts['hidden']+=int(closed)
        counts['false_exclusion']+=int(excluded and closed)
        counts['naive_false_exclusion']+=int(naive_excluded and closed)
        counts['uncertain_abstentions']+=int(naive_excluded and not excluded)
    assert counts['false_exclusion']==0,counts
    assert counts['naive_false_exclusion']>0,counts
    return counts

if __name__=='__main__':
    print(simulate())
