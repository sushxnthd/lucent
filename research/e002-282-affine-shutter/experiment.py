#!/usr/bin/env python3
"""E002-282: deterministic conditional boundary and shutter phase sweep."""
import json
from pathlib import Path
N=4096
CASES=[("C1",1/30,1/60,.2,.7,.01,.6,1.4),("C2",1/30,1/60,.2,.7,.01,1.,1.),("C3",1/60,1/120,.2,.7,.01,.6,1.4),("C4",1/10,1/60,.2,.7,.01,.6,1.4),("C5",1/30,1/60,.06,.5,.015,.6,1.4),("C6",1/24,.01,.13,.65,.008,.75,1.25)]
def overlap(s,d,P,T):
 return max(max(0,min(s+d,k*P+T)-max(s,k*P))/T for k in range(-2,8))
out=[]
for name,P,T,D,delta,eta,m,M in CASES:
 q=4*eta/(D*delta)
 if q>=1:out.append(dict(case=name,no_go=True,qcrit=q));continue
 lam=q*M/(m*(1-q)+q*M);dcrit=P-T+2*T*lam
 counts={}
 for side,factor in (("below",.98),("above",1.02)):
  n=0
  for i in range(N):
   lam_geom=overlap(i*P/N,dcrit*factor,P,T)
   eff=m*lam_geom/(m*lam_geom+M*(1-lam_geom)) if lam_geom else 0
   n+=int(D*delta*eff<=4*eta+1e-13)
  counts[side]=n
 assert counts["below"]>0 and counts["above"]==0
 out.append(dict(case=name,dcrit_ms=1000*dcrit,qcrit=q,ambiguous=counts))
p=Path(__file__).resolve().parent
(p/"results_generated.json").write_text(json.dumps(out,indent=2)+"\n")
print("PASS",[(x["case"],x.get("dcrit_ms"),x.get("ambiguous")) for x in out])
