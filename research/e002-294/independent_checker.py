"""Independent LP/quadrature checker for E002-294."""
import json,random
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq,linprog
from pathlib import Path
from experiment import case,CASES

def numerical(T,G,V,r,p):
    def mean(x):
        return quad(lambda t:max(0.,x-V*min(t,T-t))**p,0,T,points=[T/2],epsabs=1e-12)[0]/T
    x=1. if mean(1.)<=r else brentq(lambda x:mean(x)-r,0,1,xtol=1e-12)
    U=quad(lambda t:min(1.,x+V*min(t,G-t)),0,G,points=[G/2],epsabs=1e-12)[0]
    return x,U

def independent_lp(T,G,V,r,n=64):
    ts=np.r_[np.linspace(0,T,n+1),T+np.linspace(G/n,G,n)]
    m=len(ts);A=[];b=[]
    for i in range(m-1):
        row=np.zeros(m);row[i]=-1;row[i+1]=1
        A.extend([row,-row]);b.extend([V*(ts[i+1]-ts[i])]*2)
    w=np.zeros(m);objective=np.zeros(m)
    for i in range(n):
        d=ts[i+1]-ts[i];w[i]+=d/2;w[i+1]+=d/2
    for i in range(n,m-1):
        d=ts[i+1]-ts[i];objective[i]+=d/2;objective[i+1]+=d/2
    A.append(w);b.append(r*T)
    eq=np.zeros((1,m));eq[0,0]=1;eq[0,-1]=-1
    res=linprog(-objective,A_ub=np.array(A),b_ub=np.array(b),
                A_eq=eq,b_eq=[0],bounds=(0,1),method="highs")
    assert res.success,res.message
    return -res.fun

def run():
    results=[case(*args) for args in CASES]
    for x in results:
        edge,dose=numerical(x["T"],x["G"],x["V"],x["collision_mean_ceiling"],x["response_power"])
        assert abs(edge-x["edge_ceiling"])<3e-8
        assert abs(dose-x["hidden_gap_dose_seconds"])<3e-8
    rng=random.Random(294);gaps=[]
    for _ in range(100):
        T=rng.uniform(.008,.12);G=rng.uniform(.005,.12);V=rng.uniform(1,25);r=rng.uniform(.002,.25)
        analytic=case("random",T,G,V,r/2,1)["hidden_gap_dose_seconds"]
        lp=independent_lp(T,G,V,r)
        assert lp<=analytic+2e-7
        assert analytic-lp<.0005
        gaps.append(analytic-lp)
    for p,eta in [(1,1/32),(2,1/192)]:
        x,U=numerical(1,1,1,2*eta,p)
        assert abs(x-.25)<1e-10 and abs(U-.5)<1e-10
        m=quad(lambda t:max(0.,.25-min(t,1-t))**p,0,1,points=[.25,.5,.75])[0]
        assert abs(m-2*eta)<1e-10
    h=next(x for x in results if x["name"]=="24fps_unseen_synthetic_quadratic")
    assert h["hidden_gap_fraction_of_period"]>.13 and h["peak_ceiling"]<.65
    x=results[0]
    for field,offset in [("edge_ceiling",.01),("hidden_gap_dose_seconds",.002),("peak_ceiling",.03)]:
        modified=dict(x);modified[field]+=offset
        a,U=numerical(x["T"],x["G"],x["V"],x["collision_mean_ceiling"],x["response_power"])
        assert not (abs(modified["edge_ceiling"]-a)<1e-8 and abs(modified["hidden_gap_dose_seconds"]-U)<1e-8 and abs(modified["peak_ceiling"]-min(1.,a+x["V"]*x["G"]/2))<1e-8)
    summary={"status":"passed","numerical_quadrature_cases":len(results),"linear_program_cases":len(gaps),
             "max_lp_inner_approx_gap":max(gaps),"exact_rational_collisions":2,
             "mutations_rejected":3,"unseen_synthetic_holdout":"passed"}
    Path(__file__).with_name("verification.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(summary)
if __name__=="__main__":run()
