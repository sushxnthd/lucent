"""Independent exact rational checker: no model.py import."""
from fractions import Fraction as F
import numpy as np
def conv(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out
def main():
    a=conv([F(1,2)]*3,[F(1,5)]*5)
    b=conv([F(3,10)]*5,[F(1,3)]*3)
    assert a==b==[F(k,10) for k in [1,2,3,3,3,2,1]]
    assert sum(a)==F(3,2)
    for c in [F(3,5),F(2,5),F(1,5)]:
        assert conv([c]*3,[F(1,5)]*5)==conv([c*F(3,5)]*5,[F(1,3)]*3)
    rng=np.random.default_rng(316)
    for _ in range(1200):
        n=int(rng.integers(1,45));m=int(rng.integers(1,45))
        C=float(rng.uniform(.05,.98))
        K=rng.dirichlet(np.ones(m)*rng.uniform(.4,3))
        y=np.zeros(n+m-1)
        for i in range(n):
            for j in range(m):y[i+j]+=C*K[j]
        x=np.arange(len(y));S=y.sum();mu=(x*y).sum()/S
        kmu=(np.arange(m)*K).sum()
        v=((x-mu)**2*y).sum()/S
        kv=((np.arange(m)-kmu)**2*K).sum()
        assert abs(S-C*n)<2e-12
        assert abs(mu-((n-1)/2+kmu))<2e-12
        assert abs(v-((n*n-1)/12+kv))<2e-12
    q=1.1
    assert q*.90<=1<q/.90 and 1<q*.92<=q/.92
    assert 2.4/.5<=1.5/.3 and 2.55/.5>1.5/.3
    print("E002-316 exact collision + 1200 independent moment trials + frozen gates: PASS")
if __name__=="__main__":main()
