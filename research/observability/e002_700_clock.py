"""E002-700 exact-rational clock-gap falsification; Python 3 standard library."""
from fractions import Fraction as F
from itertools import product

def lower(a,b,L,d):
    assert abs(a-b)<=L*d
    return (a+b-L*d)/2

def run():
    theta=F(1,2); L=F(1); nominal=F(1,2)
    results=[]
    for jitter in (F(0),F(1,20),F(1,10),F(1,5),F(2,5)):
        feasible=naive=unsafe=robust=0
        for ai,bi in product(range(11),repeat=2):
            a,b=F(ai,10),F(bi,10)
            actual=nominal+jitter
            if abs(a-b)>L*actual: continue
            feasible+=1
            n=lower(a,b,L,nominal) if abs(a-b)<=L*nominal else F(-1)
            r=lower(a,b,L,actual)
            if n>theta:
                naive+=1
                if r<=theta: unsafe+=1
            if r>theta: robust+=1
        results.append((str(jitter),feasible,naive,unsafe,robust))
    assert results[0][3]==0
    assert any(x[3]>0 for x in results[1:])
    print("jitter feasible naive_exclusions false_exclusions robust_exclusions")
    for x in results: print(*x)
    print("PASS: exact rational adversarial clock-gap falsification")
if __name__=="__main__":run()
