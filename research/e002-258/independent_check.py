#!/usr/bin/env python3
"""Independent direct centered-moment checker."""
import csv,sys
from fractions import Fraction as F
from pathlib import Path
def check(p):
    with open(p,newline="") as f: a=list(csv.DictReader(f))
    totals=[]; trends=[]
    for w in ("same_direction","opposite_direction"):
        z=[r for r in a if r["world"]==w]
        assert len(z)==4
        x=[F(r["rgb"]) for r in z]; y=[F(r["reference"]) for r in z]
        mx=sum(x)/4;my=sum(y)/4
        totals.append((mx,my,sum((v-mx)**2 for v in x),
                       sum((v-my)**2 for v in y),
                       sum((u-mx)*(v-my) for u,v in zip(x,y)),
                       sum((u-v)**2 for u,v in zip(x,y))/4))
        trends.append([1 if (x[j+1]-x[j])*(y[j+1]-y[j])>0 else -1 for j in (0,2)])
    assert totals[0]==totals[1], "aggregate mismatch"
    assert totals[0][2:]==(404,10100,1616,1818), "moment mismatch"
    assert trends==[[1,1],[-1,-1]], "session mismatch"
    print("INDEPENDENT_PASS")
if __name__=="__main__":check(sys.argv[1] if len(sys.argv)>1 else Path(__file__).with_name("WITNESS.csv"))
