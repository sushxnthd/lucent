"""Conditional Poisson occupancy falsification; recordings are not people."""
import random
from count import expected_zero
SEED=20261014
def summarize(groups,reps=20000):
    g=[x for x in groups if x]
    w=sum(map(len,g))
    if not w: return {"status":"NO_WINDOWS"}
    observed=sum(c==0 for x in g for c in x)/w
    expected=sum(expected_zero(x) for x in g)/w
    rng=random.Random(SEED)
    extreme=0
    for _ in range(reps):
        z=0
        for x in g:
            bins=[0]*len(x)
            for i in range(sum(x)):
                bins[rng.randrange(len(x))]+=1
            z+=bins.count(0)
        if abs(z/w-expected)>=abs(observed-expected):
            extreme+=1
    p=(extreme+1)/(reps+1)
    return {"recordings":len(g),"windows":w,"observed_zero":observed,
            "conditional_expected_zero":expected,"delta":observed-expected,
            "monte_carlo_reps":reps,"p_two_sided":p,
            "discrepancy_gate":"PASS" if len(g)>=4 and abs(observed-expected)>=0.10 and p<=0.01 else "NOT_MET"}
