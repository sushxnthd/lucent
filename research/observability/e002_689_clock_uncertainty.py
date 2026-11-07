"""E002-689: deterministic synthetic clock-gap uncertainty falsification."""
from fractions import Fraction as F
from itertools import product
def lower(a,b,v,h):
    assert h>0 and v>=0
    if abs(a-b)>v*h: return None
    return max(F(0),(a+b-v*h)/2)
def robust(left,right,v,hlo,hhi):
    assert hlo>0 and hhi>=hlo and v>=0
    al,ah=left; bl,bh=right
    if al>ah or bl>bh: return None
    if al>bh+v*hhi or bl>ah+v*hhi: return None
    a=max(al,bl-v*hhi); b=max(bl,al-v*hhi)
    return lower(a,b,v,hhi)
def oracle(left,right,v,hlo,hhi):
    best=None
    for h in [hlo+(hhi-hlo)*F(k,8) for k in range(9)]:
        for i,j in product(range(9),repeat=2):
            a=left[0]+(left[1]-left[0])*F(i,8)
            b=right[0]+(right[1]-right[0])*F(j,8)
            q=lower(a,b,v,h)
            if q is not None and (best is None or q<best): best=q
    return best
def run():
    n=0; contradictions=0; false_certificates=0
    for al,bl in product([F(0),F(1,2),F(1)],repeat=2):
      for aw,bw in product([F(0),F(1,2)],repeat=2):
       for v,hlo,hhi in product([F(1,2),F(1),F(2)],[F(1,2),F(1)],[F(1),F(2)]):
        if hhi<hlo: continue
        left=(al,al+aw); right=(bl,bl+bw)
        exact=robust(left,right,v,hlo,hhi)
        sample=oracle(left,right,v,hlo,hhi)
        if exact is not None and sample is not None and sample<exact: contradictions+=1
        if exact is None and sample is not None: contradictions+=1
        nominal=lower((left[0]+left[1])/2,(right[0]+right[1])/2,v,hlo)
        if nominal is not None and exact is not None and nominal>F(1,4) and exact<=F(1,4):
            false_certificates+=1
        n+=1
    assert contradictions==0 and false_certificates>0
    assert lower(F(1),F(1),F(1),F(1))==F(1,2)
    assert robust((F(1),F(1)),(F(1),F(1)),F(1),F(1),F(2))==F(0)
    print('cases',n,'grid_contradictions',contradictions,'nominal_false_certificates',false_certificates)
if __name__=='__main__':run()
