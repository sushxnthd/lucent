"""Exact row-propagation shutter certificate. Synthetic, not human evidence."""
from fractions import Fraction as Q

def arcs(F,w,m,rows):
    F,w,m=map(Q,(F,w,m))
    if not (F>0 and 0<m<=w<=F): raise ValueError("invalid shutter")
    out=[]
    for r in rows:
        d,t,D=map(Q,(r["delta"],r["tau"],r["D"]))
        if D<m:continue
        L=D+w-2*m
        if L>=F:return [(Q(0),F)]
        if L<0:continue
        left=(d-t+m-D)%F
        right=left+L
        if right<=F:out.append((left,right))
        else:out.extend([(left,F),(Q(0),right-F)])
    return sorted(out)

def certify(F,w,m,rows):
    F=Q(F);reach=Q(0)
    for a,b in arcs(F,w,m,rows):
        if a>reach:return False,(reach+a)/2
        reach=max(reach,b)
    return (True,None) if reach>=F else (False,(reach+F)/2)

def whole_eye_duration(rows):
    return max(Q(0),min(Q(r["tau"])+Q(r["D"]) for r in rows)-max(Q(r["tau"]) for r in rows))

def frozen(alpha):
    return [dict(delta=Q(i,200),tau=Q(alpha)*Q(i,200),D=Q(15,1000)) for i in range(5)]

def run():
    F,w,m=Q(1,30),Q(1,100),Q(4,1000)
    expect={Q(0):True,Q(18,100):True,Q(11,60):True,Q(19,100):False,Q(20,100):False,Q(1):False}
    for alpha,yes in expect.items():
        actual,witness=certify(F,w,m,frozen(alpha))
        assert actual==yes,(alpha,actual)
        print(alpha,actual,float(witness) if witness is not None else None,float(whole_eye_duration(frozen(alpha))))
    assert whole_eye_duration(frozen(Q(1)))==0
    print("E002-381 frozen boundary PASS")
if __name__=="__main__":run()
