#!/usr/bin/env python3
"""E002-266 conditional pupil-change observability. Stdlib only; no human data."""
from fractions import Fraction as F
import json,random,hashlib
def bound(q,k,e):
    q,k,e=F(q),F(k),F(e)
    assert q>0 and k>=1 and e>=1
    B=k*e*e
    return q/B,q*B
def gate(q,k,e):
    a,b=bound(q,k,e)
    return "increase" if a>1 else ("decrease" if b<1 else "abstain")
def fmt(x): return str(x.numerator)+"/"+str(x.denominator)
Q=F(26,25)
wide=(F(53,50),F(101,100))
narrow=(F(203,200),F(201,200))
assert gate(Q,*wide)=="abstain"
assert gate(Q,*narrow)=="increase"
# Same RGB observation in two physically different worlds.
worlds=[(Q,F(1),F(1),F(1)),(F(1),Q,F(1),F(1))]
assert all(r*m*e2/e1==Q for r,m,e1,e2 in worlds)
rng=random.Random(2662026)
counts={"increase":0,"decrease":0,"abstain":0}
trials=[]
for i in range(2400):
    k=F(rng.randint(100,125),100)
    e=F(rng.randint(100,105),100)
    R=F(rng.randint(60,150),100)
    m=F(rng.randint(1000,int(1000*k)),1000)
    if rng.randint(0,1):m=1/m
    e1=F(rng.randint(1000,int(1000*e)),1000)
    e2=F(rng.randint(1000,int(1000*e)),1000)
    if rng.randint(0,1):e1=1/e1
    if rng.randint(0,1):e2=1/e2
    q=R*m*e2/e1
    a,b=bound(q,k,e)
    assert a<=R<=b
    d=gate(q,k,e)
    assert not(d=="increase" and R<=1)
    assert not(d=="decrease" and R>=1)
    counts[d]+=1
    trials.append(dict(i=i,q=fmt(q),R=fmt(R),k=fmt(k),e=fmt(e),decision=d,covered=True))
assert counts=={"increase":856,"decrease":659,"abstain":885}
digest=hashlib.sha256(json.dumps(trials,sort_keys=True,separators=(",",":")).encode()).hexdigest()
assert digest=="0281d1836b225d4a06515959b406bb381dae0c9f732f545648a35cee54880945"
print(json.dumps({"run":"E002-266","n":len(trials),"counts":counts,"digest":digest,"human":"NOT_TESTED"},sort_keys=True))
