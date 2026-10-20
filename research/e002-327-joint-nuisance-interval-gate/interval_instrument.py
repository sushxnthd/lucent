import numpy as np
from scipy.optimize import linprog

def interval(y,h,nuisance,lower,upper,error):
    """Sharp alpha interval for y=alpha*h+N*beta+e, beta bounded, |e|<=eta."""
    y=np.asarray(y,float).reshape(-1);h=np.asarray(h,float).reshape(-1)
    N=np.asarray(nuisance,float)
    if N.ndim==1:N=N.reshape(-1,1)
    lo=np.asarray(lower,float);hi=np.asarray(upper,float)
    eta=np.broadcast_to(np.asarray(error,float),y.shape)
    assert N.shape==(len(y),len(lo)) and len(lo)==len(hi)
    A=np.column_stack((h,N))
    aub=np.vstack((A,-A));bub=np.r_[y+eta,-y+eta]
    bounds=[(None,None)]+list(zip(lo,hi))
    c=np.zeros(1+len(lo));c[0]=1
    low=linprog(c,A_ub=aub,b_ub=bub,bounds=bounds,method="highs")
    high=linprog(-c,A_ub=aub,b_ub=bub,bounds=bounds,method="highs")
    if low.status==3 or high.status==3:return dict(status="unbounded")
    if not low.success or not high.success:return dict(status="infeasible")
    a=float(low.x[0]);b=float(high.x[0])
    return dict(lower=a,upper=b,status=("certify_positive" if a>1e-9 else "certify_negative" if b< -1e-9 else "abstain"),witness_lower=low.x.tolist(),witness_upper=high.x.tolist())
