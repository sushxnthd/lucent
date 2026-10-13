import hashlib, math, pathlib
import numpy as np, pandas as pd
p=pathlib.Path('research/e002-155/PAIRS.csv')
assert hashlib.sha256(p.read_bytes()).hexdigest()=='ec150e35dc84e120f1a0418a003989f4948595a8034ecbc68088954cfe0ce730'
d=pd.read_csv(p);d['x']=abs((d.dE-d.dD)/2);d['event']=abs(d.dD)>-2*math.log(.95)
for lag in (1,5,15,30):
 s=d[d.lag==lag];pairs=[]
 for g in sorted(s.group.unique()):
  tr=s[s.group!=g];te=s[s.group==g]
  cutoff=np.quantile(tr.x,.8)
  pairs.extend(zip(te.event.tolist(),(te.x<=cutoff).tolist()))
 n=len(pairs);keep=[int(e) for e,k in pairs if k]
 base=sum(int(e) for e,k in pairs)/n
 risk=sum(keep)/len(keep)
 print(lag,n,len(keep),round(len(keep)/n,6),round(base,6),round(risk,6))
