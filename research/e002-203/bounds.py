#!/usr/bin/env python3
"""E002-203 sharp validity bounds. Source-defined metadata; NOT pupil/RGB evidence."""
import csv,json
from pathlib import Path
P=Path(__file__).resolve().parent
def bino(n,l,r,w):return max(0,l+r-2*n+w),min(w,l,r)
def mono(n,k,w):return max(0,k-(n-w)),min(w,k)
def run():
 rows=list(csv.DictReader((P/"selected_trial_marginals.csv").open()))
 out={}
 for kind in ("binocular","left","right","oracle_fixed_eye"):
  vals=[]
  for x in rows:
   n,l,r=[int(x[k]) for k in ("n","left_valid","right_valid")]
   low,high=bino(n,l,r,600) if kind=="binocular" else mono(n,{"left":l,"right":r,"oracle_fixed_eye":max(l,r)}[kind],600)
   vals.append({"participant":x["participant"],"lower":low,"upper":high,"decision":"guaranteed" if low>=570 else ("possible" if high>=570 else "impossible")})
  out[kind]={"guaranteed":sum(v["decision"]=="guaranteed" for v in vals),"max_possible":sum(v["decision"]!="impossible" for v in vals),"records":vals}
 return out
if __name__=="__main__":
 a=run()
 assert [(a[k]["guaranteed"],a[k]["max_possible"]) for k in ("binocular","left","right","oracle_fixed_eye")]==[(4,10),(9,11),(8,10),(10,11)]
 print(json.dumps(a,indent=2))
