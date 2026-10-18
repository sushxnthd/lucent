"""E002-279. Synthetic RGB ocular response vs photometric nuisance-span collision.
No real human data. Re-run: python experiment.py
"""
import json, numpy as np
from pathlib import Path
from scipy.optimize import linprog
FS=30; T=np.arange(120)/FS; EPS=.001; A=.020
HERE=Path(__file__).resolve().parent

def stim(name):
    if name=="step": return (T>=.8).astype(float)
    if name=="double": return (((T>=.6)&(T<1.2))|((T>=2.1)&(T<2.7))).astype(float)
    return np.repeat(np.random.default_rng(279).integers(0,2,12),10).astype(float)

def filter_lag(b,lag):
    u=np.interp(T-lag,T,b,left=0.,right=float(b[-1]))
    v=np.zeros(len(T)); k=np.exp(-1/(FS*.32))
    for i in range(1,len(T)):v[i]=k*v[i-1]+(1-k)*u[i]
    return v

def primal(s,X):
    n=len(s); p=X.shape[1]
    G=np.r_[np.c_[X,-np.ones(n)],np.c_[-X,-np.ones(n)]]
    r=linprog(np.r_[np.zeros(p),1.],A_ub=G,b_ub=np.r_[s,-s],
              bounds=[(None,None)]*p+[(0,None)],method="highs")
    assert r.success,r.message
    d=np.max(np.abs(s-X@r.x[:p]))
    assert abs(d-r.x[-1])<1e-7
    return float(d),r.x[:p]

def dual(s,X):
    n=len(s)
    r=linprog(np.r_[-s,s],A_ub=np.ones((1,2*n)),b_ub=[1.],
              A_eq=np.c_[X.T,-X.T],b_eq=np.zeros(X.shape[1]),
              bounds=(0,None),method="highs-ds")
    assert r.success,r.message
    w=r.x[:n]-r.x[n:]
    return float(w@s),w

def one(name,lag,raw=False):
    b=stim(name); s=filter_lag(b,.24);s/=max(abs(s))
    x=filter_lag(b,lag)
    X=np.c_[np.ones(len(T)),T-T.mean(),b,x]
    d,beta=primal(s,X);dd,w=dual(s,X)
    assert abs(d-dd)<2e-7
    crit=None if d<1e-10 else 2*EPS/d
    out={"schedule":name,"artifact_lag_s":lag,"d_inf":d,"dual_d_inf":dd,
         "Acrit":crit,"test_A":A,"separable":bool(A*d>2*EPS+1e-9),
         "dual_orthogonality":float(max(abs(X.T@w))),"dual_l1":float(sum(abs(w)))}
    if raw:
        out["raw"]={"t":T.tolist(),"brightness":b.tolist(),"response":s.tolist(),
                    "artifact":x.tolist(),"nuisance_coefficients":beta.tolist(),
                    "dual_witness":w.tolist()}
    return out

def main():
    rows=[one(name,lag,raw=(name=="double" and lag in (0.,.24)))
          for name in ("step","double","random") for lag in (0.,.12,.24)]
    # Wildcard: hypothetical blink aperture pulse, not a measured human blink.
    b=stim("double");X=np.c_[np.ones(len(T)),T-T.mean(),b,filter_lag(b,.24)]
    blink=np.exp(-.5*((T-1.6)/.1)**2);blink_d,_=primal(blink,X)
    r={"kernel":"E002-279","type":"synthetic_only","epsilon":EPS,"fps":FS,
       "n_frames":len(T),"physiological_lag_s":.24,"tau_s":.32,
       "model":"z=X beta+A s+e, max|e|<=epsilon","rows":rows,
       "adversarial":{"truth":"no physiology; brightness artifact follows s",
          "reduced_nuisance_false_positive":rows[3]["separable"],
          "full_nuisance_certificate":rows[5]["separable"]},
       "wildcard":{"blink_like_d_inf":blink_d,"Acrit":2*EPS/blink_d},
       "human_result":None}
    (HERE/"results.json").write_text(json.dumps(r,indent=2)+"\n")
    print([(x["schedule"],x["artifact_lag_s"],x["Acrit"]) for x in rows])
if __name__=="__main__":main()
