"""Independent LP, witness quadrature, and random coverage tests."""
import json, numpy as np
from scipy.optimize import linprog
from instrument import interval,L,U,optimum_exposure
rng=np.random.default_rng(20261022361)
N=121;dt=1/(N-1);W=np.ones(N);W[0]=W[-1]=.5;W/=N-1
D=np.diff(np.eye(N),axis=0)
def lp_bounds(m,b,eta):
    A=np.vstack([D,-D,W,-W]); ub=np.r_[np.full(2*(N-1),b*dt),m+eta,-m+eta]
    c=np.zeros(N);c[N//2]=1
    l=linprog(c,A_ub=A,b_ub=ub,bounds=(0,1),method="highs")
    u=linprog(-c,A_ub=A,b_ub=ub,bounds=(0,1),method="highs")
    assert l.success and u.success
    return l.fun,-u.fun
max_lp=0.
for i in range(100):
    b=float(rng.uniform(.01,2.6));m=float(rng.uniform(.015,.985));eta=float(rng.uniform(0,.045))
    a=interval(m,b,1,eta);q=lp_bounds(m,b,eta)
    err=max(abs(a[j]-q[j]) for j in range(2));max_lp=max(max_lp,err)
    assert err<.00065
max_quad=0.
for i in range(700):
    b=float(rng.uniform(.001,3));m=float(rng.uniform(.001,.999));eta=float(rng.uniform(0,.07))
    for a in interval(m,b,1,eta):
        low=L(a,b);high=U(a,b);target=float(np.clip(m,low,high))
        assert abs(target-m)<=eta+1e-9
        lam=0 if high-low<1e-14 else (target-low)/(high-low)
        t=np.linspace(-.5,.5,10001)
        x=(1-lam)*np.maximum(0,a-b*np.abs(t))+lam*np.minimum(1,a+b*np.abs(t))
        err=abs(float(np.trapezoid(x,t))-target);max_quad=max(max_quad,err)
        assert err<1e-6
for i in range(5000):
    b=float(rng.uniform(0,2));eta=float(rng.uniform(0,.03))
    x=np.empty(101);x[50]=rng.uniform(0,1)
    for j in range(51,101): x[j]=np.clip(x[j-1]+rng.uniform(-b/100,b/100),0,1)
    for j in range(49,-1,-1): x[j]=np.clip(x[j+1]+rng.uniform(-b/100,b/100),0,1)
    m=float(np.clip(np.trapezoid(x,dx=.01)+rng.uniform(-eta,eta),0,1))
    lo,hi=interval(m,b,1,eta)
    assert lo-1e-8<=x[50]<=hi+1e-8
V=4.;k=.0015;pred=[]
for w in (.002,.008,.03):
    eta=k/np.sqrt(w);lo,hi=interval(.5,V,w,eta)
    pred.append(dict(exposure_ms=1000*w,halfwidth=(hi-lo)/2,certified=(hi-lo)/2<=.03))
assert [p["certified"] for p in pred]==[False,True,False]
out=dict(lp_trials=100,max_lp_discrepancy=max_lp,witnesses=1400,max_quadrature_error=max_quad,
         coverage_cases=5000,prediction=pred,optimum_exposure_ms=1000*optimum_exposure(V,k),
         human_trials=0,status="ALL_PASS")
open("RESULTS.json","w").write(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
