"""Independent linear-feasibility replay of E002-279, with exact rational anchor."""
import json,numpy as np
from fractions import Fraction
from pathlib import Path
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
rows=json.loads((HERE/"results.json").read_text())["rows"]
T=np.arange(120)/30

def sample(name,lag):
    if name=="step": b=(T>=.8).astype(float)
    elif name=="double": b=(((T>=.6)&(T<1.2))|((T>=2.1)&(T<2.7))).astype(float)
    else:b=np.repeat(np.random.default_rng(279).integers(0,2,12),10).astype(float)
    def filt(d):
        u=np.interp(T-d,T,b,left=0.,right=float(b[-1]))
        x=np.zeros(len(T));a=np.exp(-1/(30*.32))
        for i in range(1,len(T)):x[i]=a*x[i-1]+(1-a)*u[i]
        return x
    s=filt(.24);s/=max(abs(s))
    return s,np.c_[np.ones(len(T)),T-T.mean(),b,filt(lag)]

def overlap(a,s,X):
    r=linprog(np.zeros(X.shape[1]),A_ub=np.r_[X,-X],
              b_ub=np.r_[a*s+.002,-a*s+.002],
              bounds=[(None,None)]*X.shape[1],method="highs-ipm")
    return bool(r.success)

assert 2*Fraction(1,10)/Fraction(1,2)==Fraction(2,5)
for row in rows:
    s,X=sample(row["schedule"],row["artifact_lag_s"])
    c=row["Acrit"]
    if c is None: assert overlap(1e6,s,X)
    else:
        assert overlap(.95*c,s,X)
        assert not overlap(1.05*c,s,X)
    assert overlap(0,s,X)
    if "raw" in row:
        w=np.array(row["raw"]["dual_witness"])
        assert abs(w@s-row["dual_d_inf"])<1e-8
        assert max(abs(X.T@w))<1e-8
        assert sum(abs(w))<1+1e-8
# Three independent adversarial mutation guards.
a=next(x for x in rows if x["Acrit"] is not None)
s,X=sample(a["schedule"],a["artifact_lag_s"])
assert a["separable"] != overlap(.020,s,X)
r=next(x for x in rows if "raw" in x)
s,X=sample(r["schedule"],r["artifact_lag_s"])
w=np.array(r["raw"]["dual_witness"]);w[0]+=.1
assert max(abs(X.T@w))>1e-4
c=next(x for x in rows if x["Acrit"] is None)
s,X=sample(c["schedule"],c["artifact_lag_s"])
assert overlap(1e6,s,X)
print("9 independent LP replays, 3 mutation guards, exact rational anchor PASS")
