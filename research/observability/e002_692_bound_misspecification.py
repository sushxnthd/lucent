"""E002-692: exact-rational sensitivity to underestimating eyelid speed.
Synthetic adversarial trajectories, NOT human physiology. Python standard library.
"""
from fractions import Fraction as F
from itertools import product

def certificate(a,b,h,v,c):
    return abs(a-b)<=v*h and (a+b-v*h)/2>c

def run():
    counts=dict(feasible=0,nominal_exclusions=0,false_exclusions=0,robust_exclusions=0,robust_false_exclusions=0)
    example=None
    for a,b,h,v,c,k in product(
        [F(i,4) for i in range(2,9)], [F(i,4) for i in range(2,9)],
        [F(1,2),F(1),F(3,2)], [F(1,2),F(1),F(2)],
        [F(i,8) for i in range(9)], [F(1),F(5,4),F(3,2),F(2)]):
        actual=v*k
        if abs(a-b)>actual*h: continue
        counts["feasible"]+=1
        # Sharp attainable V-shaped trajectory with speed actual.
        hidden=(a+b-actual*h)/2<=c
        nominal=certificate(a,b,h,v,c)
        robust=certificate(a,b,h,2*v,c)
        counts["nominal_exclusions"]+=int(nominal)
        counts["false_exclusions"]+=int(nominal and hidden)
        counts["robust_exclusions"]+=int(robust)
        counts["robust_false_exclusions"]+=int(robust and hidden)
        if example is None and nominal and hidden and k>1:
            example=tuple(map(str,(a,b,h,v,c,k,(a+b-actual*h)/2)))
    assert counts["false_exclusions"]>0
    assert counts["robust_false_exclusions"]==0
    print(counts)
    print("counterexample",example)
    return counts

if __name__=="__main__": run()
