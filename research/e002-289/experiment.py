"""Lucent E002-289: synthetic projective conic and arc identifiability study.
No human or real-camera data. Wang et al. (2019) already prove the conic invariant.
"""
import math,json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
SEED=2892026
def conic(r): return np.diag([1.,1.,-r*r])
def warp(C,H):
    J=np.linalg.inv(H)
    return J.T@C@J
def ratio(Cp,Ci):
    v=np.linalg.eigvals(np.linalg.solve(Ci,Cp))
    assert max(abs(v.imag))<1e-7
    v=v.real
    pairs=sorted((abs(v[i]-v[j]),i,j) for i in range(3) for j in range(i+1,3))
    _,i,j=pairs[0]
    k=next(k for k in range(3) if k not in (i,j))
    return math.sqrt(v[k]/((v[i]+v[j])/2))
def delta(a,b,L):
    return a-math.sqrt(a*a-L*L)-b+math.sqrt(b*b-L*L)
def critical(a,b,eps,u):
    target=min(4*eps,2*eps+2*u)
    if target>=delta(a,b,a*(1-1e-12)): return None
    c=target+b-a
    v=(b*b-a*a-c*c)/(2*c)
    return math.sqrt(max(0.,a*a-v*v))
def minimax(a,b,L,u):
    d=delta(a,b,L)
    return max(d/2,d-2*u)
def independent_lp(a,b,L,u):
    ys=np.linspace(0,L,111)
    d=(a-np.sqrt(a*a-ys*ys))-(b-np.sqrt(b*b-ys*ys))
    n=len(d)
    A=np.vstack((np.column_stack((np.ones(n),-np.ones(n))),np.column_stack((-np.ones(n),-np.ones(n)))))
    sol=linprog([0,1],A_ub=A,b_ub=np.r_[-d,d],bounds=[(-2*u,2*u),(0,None)],method="highs")
    assert sol.success
    return float(sol.x[1])
def run():
    rng=np.random.default_rng(SEED)
    errs=[]
    for _ in range(300):
        H=np.eye(3)
        H[:2,:2]=rng.normal(size=(2,2))*.15+np.eye(2)
        H[:2,2]=rng.uniform(-.4,.4,size=2)
        H[2,:2]=rng.uniform(-.3,.3,size=2)
        if abs(np.linalg.det(H))<.25: continue
        r=float(rng.uniform(.22,.65))
        errs.append(abs(ratio(warp(conic(r),H),warp(conic(1.),H))-r))
    assert len(errs)>200 and max(errs)<1e-10
    cases=[]
    for name,a,b,eps,u in [
        ("no_translation",20.,22.,.3,0.),
        ("moderate_translation",20.,22.,.3,.15),
        ("free_translation",20.,22.,.3,.6),
        ("high_pixel_noise",20.,22.,.7,.3),
        ("synthetic_holdout_not_human",17.,20.,.25,.2)]:
        L=critical(a,b,eps,u)
        lo=None if L is None else independent_lp(a,b,.97*L,u)
        hi=None if L is None else independent_lp(a,b,1.03*L,u)
        if L is not None: assert lo<=2*eps and hi>2*eps
        cases.append(dict(name=name,radius_a=a,radius_b=b,epsilon=eps,u=u,critical_half_arc_px=L,below_margin=lo,above_margin=hi))
    maxdiff=0.
    for _ in range(300):
        a=float(rng.uniform(8,35));b=a+float(rng.uniform(.2,5))
        L=float(rng.uniform(.01,.95*a));u=float(rng.uniform(0,1))
        d=abs(minimax(a,b,L,u)-independent_lp(a,b,L,u))
        maxdiff=max(maxdiff,d)
        assert d<1e-7
    out=dict(study="E002-289",synthetic_only=True,prior_art_replication_count=len(errs),max_conic_ratio_error=max(errs),arc_cases=cases,independent_LP_cases=300,max_LP_disagreement=maxdiff,human_evidence=False,field_level_novelty=False)
    (HERE/"results.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
if __name__=="__main__":run()
