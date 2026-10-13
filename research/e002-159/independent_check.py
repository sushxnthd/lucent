"""Independent E002-159 checker: vectorized, does not import run.py."""
import pathlib,hashlib,json,math
import numpy as np
import pandas as pd
P=pathlib.Path("research/e002-159");SRC=pathlib.Path("research/e002-155/PAIRS.csv")
assert hashlib.sha256(SRC.read_bytes()).hexdigest()=="ec150e35dc84e120f1a0418a003989f4948595a8034ecbc68088954cfe0ce730"
x=pd.read_csv(SRC);r=json.loads((P/"RESULTS.json").read_text())
assert len(x)==r["n_pairs"]==17903
T=np.log(1.05);A=x.dPn.to_numpy()*.5;B=(x.dPn.to_numpy()-x.dD.to_numpy())*.5
C=(x.dPn.to_numpy()+x.dE.to_numpy()-x.dD.to_numpy())*.5
assert np.max(np.abs(B-x.dq.to_numpy()))<1e-10
def lab(v):return np.where(v>=T,1,np.where(v<=-T,-1,0))
a,b,c=lab(A),lab(B),lab(C)
for lag in (1,5,15,30):
 idx=x.lag.to_numpy()==lag;v=r["lags"][str(lag)]
 counts={"disagree":int(np.count_nonzero((a!=b)&idx)),
         "strong":int(np.count_nonzero((a*b==-1)&idx)),
         "signflip":int(np.count_nonzero((A*B<0)&idx)),
         "raw_disagree":int(np.count_nonzero((c!=b)&idx))}
 assert counts==v["counts"],(lag,counts,v["counts"])
 assert int(idx.sum())==v["n"]
 for g,t in v["groups"].items():
  ix=idx&(x.group.to_numpy()==g)
  assert int(ix.sum())==t["n"]
  assert int(np.count_nonzero((a!=b)&ix))==t["disagreement_n"]
  assert int(np.count_nonzero((a*b==-1)&ix))==t["strong_n"]
assert r["gates"]["G0"] and not r["gates"]["G1"] and not r["gates"]["G2"] and not r["gates"]["G3"] and r["gates"]["G4"]
print("PASS: pinned source; 17,903 vectorized reconstructions; all lag/group counts; negative gates preserved.")
