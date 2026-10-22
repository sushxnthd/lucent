"""E002-376: phase-coverage checker, independent of interval-length formula.
Only shutter geometry; no human data or RGB model.
"""
from fractions import Fraction as Q
import random

def overlap(a,b,c,d):
    return max(Q(0),min(b,d)-max(a,c))

def measured(D,F,w,m,phase):
    return any(overlap(Q(0),D,phase+k*F,phase+k*F+w)>=m
               for k in range(-3,int(D//F)+5))

def law(D,F,w,m):
    if D<m or m>w: return Q(0)
    return min(Q(1),max(Q(0),(D+w-2*m)/F))

def sweep(D,F,w,m,n):
    return sum(measured(D,F,w,m,F*Q(2*i+1,2*n)) for i in range(n))/n

def run():
    D=Q(58,1000); w=Q(10,1000)
    frozen=[(10,10,Q(48,100)),(20,10,Q(96,100)),(25,10,Q(1)),
            (30,10,Q(1)),(10,5,Q(58,100)),(20,5,Q(1))]
    checks=0
    for fps,ms,expected in frozen:
        F=Q(1,fps);m=Q(ms,1000)
        assert law(D,F,w,m)==expected
        assert abs(sweep(D,F,w,m,2000)-float(expected))<=1/2000+1e-12
        checks+=2001
    F=Q(1,20);phase=Q(49,1000)
    assert not measured(D,F,w,w,phase)
    assert overlap(Q(0),D,phase,phase+w)==Q(9,1000)
    assert overlap(Q(0),D,phase-F,phase-F+w)==Q(9,1000)
    assert measured(D,Q(1,25),w,w,phase%Q(1,25))
    assert law(Q(2,1000),Q(1,10),w,Q(5,1000))==0
    checks+=5
    rng=random.Random(376)
    for _ in range(300):
        F=Q(rng.randrange(20,151),1000)
        w=F*Q(rng.randrange(1,100),100)
        m=w*Q(rng.randrange(1,101),100)
        D=F*Q(rng.randrange(1,301),100)
        assert abs(sweep(D,F,w,m,400)-float(law(D,F,w,m)))<=1/400+1e-10
        checks+=400
    print('PASS',checks,'synthetic phase checks; human validation: NONE')
if __name__=='__main__':run()
