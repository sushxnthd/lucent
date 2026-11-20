"""Independent exact-rational replay of selected E002-483 synthetic predictions."""
from fractions import Fraction as F
from json import dumps

KNOTS = [(F(0), F(0)), (F(5), F(1)), (F(15), F(-1)), (F(20), F(0))]

def dev(t):
    if t < 0 or t > 20:
        return F(0)
    for (a, fa), (b, fb) in zip(KNOTS, KNOTS[1:]):
        if a <= t <= b:
            return fa + (fb-fa)*(t-a)/(b-a)
    raise AssertionError('invalid knot')

def avg(a,b):
    xs=sorted({a,b,*[x for x,_ in KNOTS if a<x<b]})
    return F(1)+sum(((y-x)*(dev(x)+dev(y))/2 for x,y in zip(xs,xs[1:])),F(0))/(b-a)

def interval(pair,d=F(1,10),q=F(3,100)):
    a,b=pair
    xlo=(1-d)*a-q; xhi=(1+d)*a+q
    ylo=(1-d)*b-q; yhi=(1+d)*b+q
    assert min(xlo,xhi,ylo,yhi)>0
    return (xlo-yhi)/(xlo+yhi),(xhi-ylo)/(xhi+ylo)

rows=[]
for phase in [-5,-2,0,2,5]:
    s=F(phase)
    means=(avg(s,s+10),avg(s+10,s+20))
    moving=interval(means)
    stationary=interval((F(1),F(1)))
    margin=max(moving[0]-stationary[1],stationary[0]-moving[1])
    rows.append(dict(phase_ms=phase,means=[str(v) for v in means],margin=str(margin),certified=margin>0))
assert rows[2]['means']==['3/2','1/2']
assert rows[2]['margin']==str(F(493,1900))
assert all(row['certified'] for row in rows[1:4])
assert not rows[0]['certified'] and not rows[4]['certified']
print(dumps({'experiment':'E002-483','method':'independent_fraction_exact','cases':rows,'physical_validation':False},indent=2))
