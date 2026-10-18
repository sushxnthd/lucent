#!/usr/bin/env python3
"""Independent exact witness and alternate 8192-phase check for E002-282."""
import json
from fractions import Fraction as F
from pathlib import Path
cases=json.loads((Path(__file__).resolve().parent/"results_generated.json").read_text())
params={"C1":(1/30,1/60,.2,.7,.01,.6,1.4),"C2":(1/30,1/60,.2,.7,.01,1.,1.),"C3":(1/60,1/120,.2,.7,.01,.6,1.4),"C4":(1/10,1/60,.2,.7,.01,.6,1.4),"C6":(1/24,.01,.13,.65,.008,.75,1.25)}
def minoverlap(d,P,T):
 low=2.
 for i in range(8192):
  s=i*P/8192
  best=max(max(0,min(s+d,k*P+T)-max(s,k*P))/T for k in range(-1,7))
  low=min(low,best)
 return low
for c in cases:
 if c["case"]=="C5":assert c["no_go"];continue
 P,T,D,delta,eta,m,M=params[c["case"]]
 q=4*eta/(D*delta);lam=q*M/(m*(1-q)+q*M)
 assert abs(c["dcrit_ms"]/1000-(P-T+2*T*lam))<1e-10
 for side,factor,expected in (("below",.98,False),("above",1.02,True)):
  l=minoverlap(c["dcrit_ms"]/1000*factor,P,T)
  eff=m*l/(m*l+M*(1-l)) if l else 0
  assert (D*delta*eff>4*eta)==expected
  assert (c["ambiguous"][side]==0)==expected
q0,q1,D=F(1,5),F(4,5),F(1,5)
shift=D*(q1-q0)/2
assert max(map(abs,[D*q0-D*q1+shift,shift,shift]))==D*(q1-q0)/2
print("PASS: independent phase grid + exact rational witness")
