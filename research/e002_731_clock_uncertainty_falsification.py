"""E002-731: adversarial timing falsification of endpoint-only hidden-closure exclusion.

Self-contained Python 3 script; no external dependencies. Synthetic, not human evidence.
An aperture a(t) is L-Lipschitz. For exact point samples at times t0,t1,
a(t)>=max(a0-L(t-t0), a1-L(t1-t)); thus a hidden zero is impossible
when a0+a1>L*(t1-t0). Equality permits a piecewise-linear zero.

When endpoint clock timestamps each have independent error <=eps,
the actual interval may be nominal_gap+2*eps. Therefore exclusion
requires a0+a1 > L*(nominal_gap+2*eps), NOT L*nominal_gap.
The construction below exhibits a false exclusion by the naive rule.
Exposure-averaged samples are NOT point samples; this rule cannot be
applied to them (see E002-730).
"""
from fractions import Fraction as F

def exclude(a0, a1, L, nominal_gap, eps=F(0)):
    assert min(a0,a1,L,nominal_gap,eps)>=0
    return a0+a1 > L*(nominal_gap+2*eps)

def aperture(t, t0, t1, a0, a1, L):
    # Feasible piecewise-linear trajectory reaching zero at t0+a0/L.
    assert L>0 and t1-t0 >= (a0+a1)/L
    z=t0+a0/L
    return a0-L*(t-t0) if t<=z else min(a1,L*(t-z))

def test():
    L=F(1); a0=a1=F(3,5); nominal=F(1); eps=F(1,10)
    assert exclude(a0,a1,L,nominal)
    assert not exclude(a0,a1,L,nominal,eps)
    t0=-eps; t1=nominal+eps
    z=t0+a0/L
    assert aperture(t0,t0,t1,a0,a1,L)==a0
    assert aperture(z,t0,t1,a0,a1,L)==0
    assert aperture(t1,t0,t1,a0,a1,L)==a1
    assert t1-t0==nominal+2*eps
    # At equality the exclusion MUST abstain, not assert impossibility.
    assert not exclude(F(1,2),F(1,2),F(1),F(1))
    # Boundary holds for rational sweep, including adversarial clock shifts.
    for n in range(1,101):
        gap=F(n,100)
        for k in range(0,11):
            e=F(k,100)
            a=F(3,5)
            predicted=exclude(a,a,L,gap,e)
            feasible=(2*a <= L*(gap+2*e))
            assert predicted == (not feasible)
    print("PASS: 1,100 exact-rational boundary cases; explicit hidden-zero witness")
    print("SYNTHETIC ONLY: no shutter integration, physiological L, or human validation")

if __name__=="__main__":
    test()
