#!/usr/bin/env python3
"""E002-242 independent binomial-tail checker for frozen derived counts."""
import csv,math
from pathlib import Path
D=Path(__file__).resolve().parent
def upper(k,n,a):
    if k==n:return 1.
    lo,hi=0.,1.
    for _ in range(90):
        m=(lo+hi)/2
        cdf=sum(math.comb(n,j)*m**j*(1-m)**(n-j) for j in range(k+1))
        if cdf>a:lo=m
        else:hi=m
    return (lo+hi)/2
rows=list(csv.DictReader((D/'COUNTS.csv').open()))
assert len(rows)==16
assert {(x['condition'],x['gate'],int(x['iris_radius_px'])) for x in rows}=={(c,g,r) for c in ('nuisance','true_change') for g in ('base','dual') for r in (10,14,20,28)}
for x in rows:
    n,k,a,b=map(int,[x['n'],x['correct_admit'],x['accepted'],x['bad_admitted']])
    assert n==15 and k+a*0>=0 and k+b==a and a<=n
mx=max(upper(int(x['correct_admit']),15,.05/16) for x in rows)
assert abs(mx-0.5805954506987197)<1e-11
assert mx<.75
print('PASS 16-cell simultaneous 95% upper =',mx)
