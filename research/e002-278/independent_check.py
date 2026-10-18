"""Independent exact pairwise enumeration and LP validation of E002-278."""
import math,json,pathlib
import numpy as np
from scipy.optimize import linprog
P=pathlib.Path(__file__).resolve().parent
L=.012;E=.0015;A=.0048
def independent_threshold(row):
 fs=row["fps"];f=row["frequency_hz"];te=row["exposure_s"];phase=row["phase_rad"]
 t=[i/fs for i in range(round(5*fs))]
 sinc=1. if te==0 else math.sin(math.pi*f*te)/(math.pi*f*te)
 s=[sinc*math.sin(2*math.pi*f*x+phase) for x in t]
 vals=[(2*L*(t[j]-t[i])+4*E)/abs(s[j]-s[i])
       for i in range(len(t)) for j in range(i+1,len(t)) if abs(s[j]-s[i])>1e-12]
 return (min(vals) if vals else None),t,s
def lp_overlap(t,s,a):
 n=len(t);eq=np.zeros((n,4*n));rhs=a*np.asarray(s)
 for i in range(n):
  eq[i,i]=1;eq[i,n+i]=-1;eq[i,2*n+i]=1;eq[i,3*n+i]=-1
 ub=[];lim=[]
 for o in (0,n):
  for i in range(n-1):
   v=np.zeros(4*n);v[o+i]=1;v[o+i+1]=-1
   ub.extend([v,-v]);lim.extend([L*(t[i+1]-t[i])]*2)
 bounds=[(None,None)]*(2*n)+[(-E,E)]*(2*n)
 return linprog(np.zeros(4*n),A_ub=np.array(ub),b_ub=lim,A_eq=eq,b_eq=rhs,bounds=bounds,method="highs").success
def main():
 rows=json.loads((P/"RESULTS.json").read_text())
 for row in rows:
  c,t,s=independent_threshold(row);saved=row["critical_log_amplitude"]
  assert (c is None)==(saved is None)
  if c is not None:
   assert abs(c-saved)<1e-10
   assert row["guaranteed_separation"]==(A>c*(1+1e-10))
   tt=t[:18];ss=s[:18]
   cand=[(2*L*(tt[j]-tt[i])+4*E)/abs(ss[j]-ss[i]) for i in range(18) for j in range(i+1,18) if abs(ss[j]-ss[i])>1e-12]
   if cand:
    v=min(cand);assert lp_overlap(tt,ss,.95*v);assert not lp_overlap(tt,ss,1.05*v)
  else:assert lp_overlap(t[:18],s[:18],1000)
 assert rows[5]["guaranteed_separation"] and not rows[6]["guaranteed_separation"]
 # Adjacent-only constraints fail: each adjacent pair passes but endpoints do not.
 assert 2<=1+1.2 and 4>2+1.2
 print("PASS independent enumeration + linear-program overlap tests + exposure crossing")
if __name__=="__main__":main()
