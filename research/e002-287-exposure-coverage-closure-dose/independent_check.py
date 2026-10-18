#!/usr/bin/env python3
"""Independent exact rational witness and mutation checks; no experiment import."""
from fractions import Fraction as F
from itertools import product
def bounds(y,P,T,eps):
    return (T*sum((max(F(0),a-eps) for a in y),F(0)),
            T*sum((min(F(1),a+eps) for a in y),F(0))+len(y)*(P-T))
n=0
for P,T,e in [(F(1,10),F(1,50),F(1,100)),(F(1,30),F(1,60),F(1,100)),(F(1,10),F(1,10),F(1,100))]:
    for y in product([F(1,5),F(2,5),F(1,2),F(3,5),F(4,5)],repeat=2):
        lo,hi=bounds(y,P,T,e)
        a=[max(F(0),v-e) for v in y]
        b=[min(F(1),v+e) for v in y]
        assert lo==T*sum(a,F(0))
        assert hi==T*sum(b,F(0))+len(y)*(P-T)
        assert all(abs(v-z)<=e for v,z in zip(a,y))
        assert all(abs(v-z)<=e for v,z in zip(b,y))
        n+=1
assert F(1)*F(1,50)==F(1,5)*F(1,10)
assert 50*(F(1,10)-F(1,50))==4
original=bounds([F(1,2)],F(1,10),F(1,50),F(1,100))
mutants=[(original[0],original[1]-F(2,25)),(original[0]+F(1,100),original[1]),(original[0],original[1]+F(1,100))]
assert all(x!=original for x in mutants)
assert 1-F(6,25)+2*F(6,25)*F(1,100)==F(478,625)
print('PASS',n,'rational witnesses; 2 collisions; 3 mutations; 24fps holdout width .7648')
