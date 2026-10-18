"""Minimal E002-290 exact conditional LP experiment; synthetic only."""
import json
import numpy as np
from scipy.optimize import linprog
S=np.array([1.,0,0,0,0,0])
N=np.array([[1,.4,1,0,1],[1,0,0,0,0],[1,1,1,0,0],
            [0,0,0,1,1],[0,0,0,1,0],[0,1,0,0,0]],float)
def dist(s,n):
    m,p=n.shape
    U=np.vstack([np.column_stack([-n,-np.ones(m)]),np.column_stack([n,-np.ones(m)])])
    r=linprog(np.r_[np.zeros(p),1.],A_ub=U,b_ub=np.r_[-s,s],
              bounds=[(None,None)]*p+[(0,None)],method='highs')
    assert r.success
    return float(r.fun)
def dual(s,n):
    m,p=n.shape
    r=linprog(np.r_[-s,s],A_eq=np.hstack([n.T,-n.T]),b_eq=np.zeros(p),
              A_ub=np.ones((1,2*m)),b_ub=[1.],bounds=[(0,None)]*(2*m),method='highs')
    assert r.success
    return float(-r.fun)
def main():
    d0=dist(S[:5],N[:5]); d=dist(S,N)
    dh=N.copy();dh[0,1]=.62;dh[3,4]=1.35
    dhold=dist(S,dh)
    assert d0<1e-9 and abs(d-5/23)<1e-9 and abs(dhold-1350/5213)<1e-9
    assert dist(S,np.column_stack([N,S]))<1e-9
    assert abs(d-dual(S,N))<1e-9 and abs(dhold-dual(S,dh))<1e-9
    rng=np.random.default_rng(2902026);gaps=[]
    for i in range(200):
        m=int(rng.integers(3,9));p=int(rng.integers(1,m+2))
        a=rng.normal(size=m);b=rng.normal(size=(m,p))
        gaps.append(abs(dist(a,b)-dual(a,b)))
    assert max(gaps)<1e-8
    eta=.01;optical_b=.03
    out={'human_data':False,'five_feature_d':d0,'six_feature_d':d,
         'unbounded_optical_d':dist(S,np.column_stack([N,S])),
         'calibrated_critical_amplitude':2*optical_b+2*eta/d,
         'heldout_d':dhold,'heldout_critical_amplitude':2*optical_b+2*eta/dhold,
         'randomized_primal_dual_checks':len(gaps),'max_primal_dual_gap':max(gaps),
         'holdout_below':'ambiguous','holdout_above':'distinguishable'}
    open('results.json','w').write(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
