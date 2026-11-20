"""E002-697: independent finite-grid exposure-integral adversarial oracle.
Synthetic only. Requires numpy/scipy; no human or camera evidence.
A piecewise-linear, 1-Lipschitz aperture is bounded in [0,1].
Trapezoidal integration is exact for these piecewise-linear segments.
"""
import numpy as np
from scipy.optimize import linprog

def solve(means=(.9,.9), step=.05):
    n=int(round(3/step))+1
    t=np.linspace(-1,2,n)
    A=[]; b=[]
    for i in range(n-1):
        row=np.zeros(n); row[i+1]=1; row[i]=-1
        A.extend((row,-row)); b.extend((step,step))
    eq=np.zeros((2,n))
    for k,(lo,hi) in enumerate(((-1,0),(1,2))):
        ix=np.flatnonzero((t>=lo-1e-10)&(t<=hi+1e-10))
        eq[k,ix]=step
        eq[k,ix[0]]*=.5; eq[k,ix[-1]]*=.5
    solutions=[]
    for j in np.flatnonzero((t>=-1e-10)&(t<=1+1e-10)):
        c=np.zeros(n);c[j]=1
        z=linprog(c,A_ub=A,b_ub=b,A_eq=eq,b_eq=means,bounds=(0,1),method="highs")
        if z.success: solutions.append((z.fun,float(t[j]),z.x))
    if not solutions: raise ValueError("infeasible input")
    val,at,x=min(solutions,key=lambda q:q[0])
    assert max(abs(eq@x-np.asarray(means)))<1e-7
    assert max(abs(np.diff(x)))<=step+1e-7
    return val,at

if __name__=="__main__":
    for step in (.1,.05,.025):
        value,at=solve(step=step)
        conservative=max(0,(.9+.9-(1+1))/2)
        print(f"step={step}: grid_min={value:.9f}, time={at:.3f}, E002-694_lower={conservative:.9f}")
        assert value>0.04
    print("PASS: positive grid minimum where conservative bound is zero; finite-grid only")
