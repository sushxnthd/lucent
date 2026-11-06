"""E002-687: interval-endpoint robust velocity exclusion; exact rational self-test."""
from fractions import Fraction as F
from itertools import product

def bound(a,b,v,h):
    if abs(a-b)>v*h: return None
    return max(F(0),(a+b-v*h)/2)

def robust(al,au,bl,bu,v,h):
    if al>au or bl>bu or min(au,bu+v*h)<max(al,bl-v*h): return None
    a=max(al,bl-v*h)
    b=max(bl,al-v*h)
    assert a<=au and b<=bu and abs(a-b)<=v*h
    return bound(a,b,v,h)

def oracle(al,au,bl,bu,v,h):
    candidates={al,au,bl-v*h,bu+v*h}
    candidates.update({max(al,bl-v*h),min(au,bu+v*h)})
    vals=[]
    for a in candidates:
        if al<=a<=au:
            for b in [max(bl,a-v*h),min(bu,a+v*h)]:
                if bl<=b<=bu and abs(a-b)<=v*h: vals.append(bound(a,b,v,h))
    return min(vals) if vals else None

if __name__=='__main__':
    grid=[F(x,2) for x in range(5)]
    n=0
    for al,au,bl,bu,v,h in product(grid,repeat=6):
        if al>au or bl>bu: continue
        x=robust(al,au,bl,bu,v,h)
        y=oracle(al,au,bl,bu,v,h)
        assert x==y,(al,au,bl,bu,v,h,x,y)
        n+=1
    assert bound(F(1),F(1),F(1),F(1))==F(1,2)
    assert robust(F(1,2),F(1),F(1,2),F(1),F(1),F(1))==F(0)
    print(f'PASS {n} interval configurations; exact rational oracle agreement; uncertainty reversal witness')
