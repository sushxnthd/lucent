"""E002-740: exact row-timing exclusion certificate and adversarial checks.
Synthetic mathematical instrument model only; no physiological calibration.
Run: python E002_740_ROW_TIME_VALIDATION.py
"""
from fractions import Fraction as F
from itertools import product

def certificate(a, b, nominal_gap, velocity_ceiling, row_time_uncertainty):
    """Point observations with actual gap <= nominal_gap + uncertainty.
    If a+b > L*Tmax, a zero aperture between points is impossible.
    Equality is deliberately inconclusive. Inputs are exact rationals.
    """
    assert 0 <= a <= 1 and 0 <= b <= 1
    assert nominal_gap >= 0 and velocity_ceiling > 0 and row_time_uncertainty >= 0
    return a+b > velocity_ceiling*(nominal_gap+row_time_uncertainty)

def hidden_zero_witness(a,b,gap,L):
    """Construct feasible full closure by maximal descent, zero dwell, ascent.
    Returns rational (time_of_zero, time_end_of_zero) or None.
    """
    if a+b > L*gap:
        return None
    return (a/L, gap-b/L)

def run():
    cases=0; reversals=0; witnesses=0
    for a,b,L,gap,u in product([F(1,4),F(1,2),F(3,4),F(1)],
                               [F(1,4),F(1,2),F(3,4),F(1)],
                               [F(25),F(50),F(100),F(200)],
                               [F(0),F(1,1000),F(1,200),F(1,100)],
                               [F(0),F(1,1000),F(1,200),F(1,100)]):
        cert=certificate(a,b,gap,L,u)
        actual=gap+u
        witness=hidden_zero_witness(a,b,actual,L)
        assert cert == (witness is None)
        if cert:
            for k in range(21):
                t=actual*F(k,20)
                lower=max(a-L*t,b-L*(actual-t),F(0))
                assert lower>0
        else:
            assert witness is not None
            assert F(0)<=witness[0]<=witness[1]<=actual
            witnesses+=1
        if certificate(a,b,gap,L,F(0)) and not cert:
            reversals+=1
        cases+=1
    a=b=F(1,2); L=F(100); nominal=F(0); u=F(1,100)
    assert certificate(a,b,nominal,L,F(0))
    assert not certificate(a,b,nominal,L,u)
    assert hidden_zero_witness(a,b,u,L)==(F(1,200),F(1,200))
    print(f'PASS {cases} exact configurations; {witnesses} feasible hidden closures; {reversals} timing-uncertainty reversals')
    print('EVIDENCE TIER: synthetic exact arithmetic; no physical/human validation')

if __name__=='__main__':
    run()
