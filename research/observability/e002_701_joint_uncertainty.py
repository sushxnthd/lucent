"""E002-701: exact-rational joint endpoint, clock and velocity uncertainty stress test."""
from fractions import Fraction as F
from itertools import product

def minimum(a,b,v,d):
    if abs(a-b)>v*d: return None
    return (a+b-v*d)/2

def run():
    theta=F(1,2); count=0; naive=0; naive_false=0; robust=0; robust_false=0; withdrawn=0
    examples=[]
    for ai,bi,ea,eb,vi,di in product(range(11),range(11),(-1,0,1),(-1,0,1),(1,2),(5,6,7)):
        a,b=F(ai,10),F(bi,10)
        am,bm=a+F(ea,10),b+F(eb,10)
        if not (0<=am<=1 and 0<=bm<=1): continue
        v=F(vi,2); d=F(di,10)
        m=minimum(a,b,v,d)
        if m is None:continue
        count+=1
        n=minimum(am,bm,F(1,2),F(1,2))
        nc=n is not None and n>theta
        rc=(am-F(1,10)+bm-F(1,10)-F(1)*F(7,10))/2>theta
        if nc:
            naive+=1
            if m<=theta:
                naive_false+=1
                if len(examples)<3:examples.append((str(a),str(b),str(am),str(bm),str(v),str(d),str(m)))
        if rc:
            robust+=1
            if m<=theta:robust_false+=1
        if nc and not rc:withdrawn+=1
    assert naive_false>0 and robust_false==0 and robust>0
    print('feasible',count,'nominal_certificates',naive,'nominal_false_exclusions',naive_false)
    print('joint_robust_certificates',robust,'joint_robust_false_exclusions',robust_false,'withdrawn_nominal',withdrawn)
    print('counterexamples',examples)
    print('PASS: exact-rational joint uncertainty stress')
if __name__=='__main__':run()
