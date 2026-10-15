#!/usr/bin/env python3
"""Independent exhaustive small-n proof-check and 15-record cross-check."""
import csv,itertools
from pathlib import Path
P=Path(__file__).resolve().parent
for n in range(1,7):
 for w in range(1,n+1):
  S=set(range(w))
  for l in range(n+1):
   L=list(itertools.combinations(range(n),l))
   for r in range(n+1):
    R=list(itertools.combinations(range(n),r))
    v=[len(set(a)&set(b)&S) for a in L for b in R]
    assert (min(v),max(v))==(max(0,l+r-2*n+w),min(w,l,r))
rows=list(csv.DictReader((P/"selected_trial_marginals.csv").open()))
assert len(rows)==15
counts=[]
for kind in ("binocular","left","right","oracle_fixed_eye"):
 g=p=0
 for row in rows:
  n,l,r=(int(row[x]) for x in ("n","left_valid","right_valid"))
  if kind=="binocular":lo,hi=max(0,l+r-2*n+600),min(600,l,r)
  else:
   c={"left":l,"right":r,"oracle_fixed_eye":max(l,r)}[kind]
   lo,hi=max(0,c-(n-600)),min(600,c)
  g+=lo>=570;p+=hi>=570
 counts.append((g,p))
assert counts==[(4,10),(9,11),(8,10),(10,11)]
print("PASS exhaustive n<=6 and source-derived 15-record bounds; physiological gates NOT TESTED")
