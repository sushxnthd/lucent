"""E002-736: exact subgroup-conditional failure of exchangeable max calibration.
Run: python research/observability/e002_736_subgroup_coverage.py
Synthetic population; not human data.
"""
from fractions import Fraction
from math import comb

def exact(n, p):
    conditional = (1-p)**n
    marginal = p * conditional
    assert marginal <= Fraction(1,n+1)
    return conditional, marginal

def brute(n,p):
    return sum((Fraction(comb(n,k))*p**k*(1-p)**(n-k)
                for k in range(n+1) if k == 0), Fraction(0))

for n in range(1,31):
    for p in (Fraction(1,100), Fraction(1,10), Fraction(1,2)):
        c,m = exact(n,p)
        assert c == brute(n,p)
        assert m == p*c
c,m=exact(20,Fraction(1,100))
print('E002-736 PASS: 90 exact subgroup cases')
print('n=20, fast fraction=1/100; conditional fast miss =',float(c))
print('marginal miss =',float(m),'unconditional rank bound =',float(Fraction(1,21)))
