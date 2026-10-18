"""E002-286: exact Poisson blink-count ceiling; illustrative rates only."""
import json, math
from scipy.stats import poisson
from scipy.optimize import brentq

def tv(T, lam0, lam1, p=1., nu=0.):
    a,b=T*(p*lam0+nu),T*(p*lam1+nu)
    if a==b:return 0.
    if a==0:return float(1-poisson.pmf(0,b))
    k=math.floor((b-a)/math.log(b/a))+1
    return float(poisson.sf(k-1,b)-poisson.sf(k-1,a))

def acc(T,lam0,lam1,p=1.,nu=0.):
    return (1+tv(T,lam0,lam1,p,nu))/2

def crossing(target,p=1.,nu=0.):
    return brentq(lambda T:acc(T,.2,.4,p,nu)-target,.001,10000.)

if __name__=="__main__":
    rows=[dict(T_seconds=T,perfect_accuracy=acc(T,.2,.4),p80_fp1pm_accuracy=acc(T,.2,.4,.8,1/60)) for T in (2,3,5,10,30,60,120)]
    result=dict(rows=rows,perfect_T90=crossing(.9),perfect_T95=crossing(.95),imperfect_T90=crossing(.9,.8,1/60))
    assert acc(5,.2,.4)<.7
    assert abs((1*.2)-(.5*.4))<1e-15
    print(json.dumps(result,indent=2))
