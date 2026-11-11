"""Independent exhaustive rational oracle for E002-685 conditional scalar gap rule.
Synthetic verification only, not physical or human validation.
"""
from fractions import Fraction as F
from itertools import product
import json

def oracle(a,b,v,h,c):
    # Pointwise Lipschitz cone intersection; independently minimize in time.
    if abs(a-b)>v*h: return 'INFEASIBLE'
    if v==0: return 'EXCLUDE' if min(a,b)>c else 'ABSTAIN'
    t=(a-b+v*h)/(2*v)
    assert 0<=t<=h
    minimum=max(F(0),a-v*t)
    return 'EXCLUDE' if minimum>c else 'ABSTAIN'

def implementation(a,b,v,h,c):
    if abs(a-b)>v*h: return 'INFEASIBLE'
    return 'EXCLUDE' if max(F(0),(a+b-v*h)/2)>c else 'ABSTAIN'

def main():
    vals=[F(x,4) for x in range(9)]
    total=feasible=0
    for a,b,v,h,c in product(vals,repeat=5):
        total+=1
        actual=implementation(a,b,v,h,c)
        expected=oracle(a,b,v,h,c)
        assert actual==expected,(a,b,v,h,c,actual,expected)
        feasible+=expected!='INFEASIBLE'
    mono=0
    for a,b,c in product(vals,repeat=3):
        for v in vals:
            previous=None
            for h in vals:
                outcome=oracle(a,b,v,h,c)
                if outcome=='INFEASIBLE': continue
                if previous=='ABSTAIN': assert outcome!='EXCLUDE'
                previous=outcome
                mono+=1
    print(json.dumps(dict(experiment='E002-686',evidence='synthetic exact rational independent oracle',grid_cases=total,feasible_cases=feasible,mismatches=0,monotonicity_checks=mono,physical_trials=0,human_trials=0)))
if __name__=='__main__':main()
