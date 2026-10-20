"""Independent sharp-bound and full-image checker, not importing instrument."""
from fractions import Fraction as F
import json,math
import numpy as np
def lo(y,k):return y/(k*(1-y)+y)
def hi(y,k):return k*y/(1-y+k*y)
def main():
    d=F('1.26')/F('42');theta=F('0.5')
    assert theta+d==F('0.53')
    assert F('0.529')-d<=theta<F('0.531')-d
    ylo=F('0.52')-F('0.01');t=F('0.48')
    kc=ylo*(1-t)/(t*(1-ylo))
    assert kc==F(221,196)
    assert lo(ylo,F('1.12'))>t>lo(ylo,F('1.14'))
    count=0
    for kn in range(1,101):
        k=F(kn+100,100)
        for yn in range(1,100):
            y=F(yn,100);a=lo(y,k);b=hi(y,k)
            assert k*a/(k*a+1-a)==b/(b+k*(1-b))==y
            count+=1
    rng=np.random.default_rng(1337)
    for _ in range(5000):
        k=float(rng.uniform(1.00001,10));w=rng.uniform(1,k,200);q=rng.uniform(0,1,200)
        y=float((w*q).sum()/w.sum());f=float(q.mean())
        assert lo(y,k)-1e-12<=f<=hi(y,k)+1e-12
        assert abs(y-f)<=(math.sqrt(k)-1)/(math.sqrt(k)+1)+1e-12
    a=[4,5,6,7,8,7,6,5,4,3,2,1,0,1,2,3];b=a[8:]+a[:8]
    def img(rs):
        return [[sum(10 if x*x+y*y<=r*r else 100 for r in rs) for x in range(-10,11)] for y in range(-10,11)]
    assert img(a)==img(b) and a[4]!=b[4]
    print(json.dumps(dict(status="PASS",exact_rational_extremizers=count,weighted_checks=5000,independent_rgb_collision=True,human="NOT RUN")))
if __name__=="__main__":main()
