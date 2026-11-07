"""E002-642 exact-rational synthetic shutter surrogate. NOT human evidence."""
from fractions import Fraction as F
from itertools import product
from collections import Counter

def predict(a,b,c,vc,vo,g):
    return 'EXCLUDE' if (a-c)/vc+(b-c)/vo>g else 'ABSTAIN_REACHABLE'

def main():
    outcomes=Counter()
    for a,b,c,vc,vo,g in product([F(1),F(2),F(3)],[F(1),F(2)],[F(0),F(1,2)],[F(50),F(100)],[F(50),F(100)],[F(1,100),F(1,50),F(3,100)]):
        if min(a,b)<=c: continue
        t=max(F(0),min(g,(a-b+vo*g)/(vc+vo)))
        minimum=max(F(0),a-vc*t,b-vo*(g-t))
        label='CLOSURE' if minimum<=c else 'NO_CLOSURE'
        verdict=predict(a,b,c,vc,vo,g)
        outcomes[(verdict,label)]+=1
        assert not (verdict=='EXCLUDE' and label=='CLOSURE')
    assert sum(outcomes.values())==144
    assert outcomes[('EXCLUDE','NO_CLOSURE')]==121
    assert outcomes[('ABSTAIN_REACHABLE','CLOSURE')]==23
    print('SYNTHETIC ONLY',dict(outcomes))
if __name__=='__main__': main()
