"""Independent numerical audit; does not import model.py. Requires numpy/scipy."""
import json,math,random
import numpy as np
from pathlib import Path
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

ROOT=Path(__file__).resolve().parent
def B(E,V,m):return min(1.,math.sqrt(2*V*E*m) if m<=V*E/2 else m+V*E/2)
def closed(E0,E1,G,U,D,m0,m1):
 a,b=B(E0,U,m0),B(E1,D,m1)
 t=max(0.,min(G,(b+D*G-a)/(U+D)))
 return min(1.,a+U*t,b+D*(G-t)),t
def witness(E0,E1,G,U,D,m0,m1):
 h,t=closed(E0,E1,G,U,D,m0,m1)
 v0=max(0.,h-U*t);v1=max(0.,h-D*(G-t))
 def area(v,E,s):return v*v/(2*s*E) if v<=s*E else v-s*E/2
 return area(v0,E0,U),area(v1,E1,D)
def lp(E0,E1,G,U,D,m0,m1,n=240):
 x=np.r_[np.linspace(-E0,0,n+1),np.linspace(0,G,n+1)[1:],np.linspace(G,G+E1,n+1)[1:]]
 N=len(x);rr=[];cc=[];vv=[];bb=[]
 def add(dic,lim):
  k=len(bb);bb.append(lim)
  for j,v in dic.items():rr.append(k);cc.append(j);vv.append(v)
 for j in range(N-1):
  dt=x[j+1]-x[j]
  add({j:-1,j+1:1},U*dt);add({j:1,j+1:-1},D*dt)
 add({j:(.5 if j in (0,n) else 1.)/n for j in range(n+1)},m0)
 add({2*n+j:(.5 if j in (0,n) else 1.)/n for j in range(n+1)},m1)
 A=coo_matrix((vv,(rr,cc)),shape=(len(bb),N)).tocsr()
 b0,b1=B(E0,U,m0),B(E1,D,m1)
 guess=max(0,min(G,(b1+D*G-b0)/(U+D)))
 mid=n+int(round(guess*n/G)) if G else n
 vals=[]
 for j in sorted(set([n,2*n,*[max(n,min(2*n,mid+d)) for d in (-2,-1,0,1,2)]])):
  c=np.zeros(N);c[j]=-1
  s=linprog(c,A_ub=A,b_ub=bb,bounds=(0,1),method='highs')
  assert s.success,s.message
  vals.append(-s.fun)
 return max(vals)
def run():
 f=json.loads((ROOT/'FROZEN_PREDICTION.json').read_text())
 args=(f['left_exposure_seconds'],f['right_exposure_seconds'],f['dark_gap_seconds'],f['rise_speed_U_per_s'],f['fall_speed_D_per_s'],f['left_exposure_mean_upper'],f['right_exposure_mean_upper'])
 pred,t=closed(*args);assert abs(pred-f['predicted_sharp_peak'])<1e-13
 cases=[args,(.01,.01,1/30-.01,12,4,.01,.01),(.006,.014,.023,9.5,4,.008,.02),(.008,.016,.024,8,3,.02,.005),(.012,.008,.02,4,11,.03,.01),(.009,.009,.015,5,5,.02,.02)]
 random.seed(322)
 for _ in range(8):
  cases.append((random.uniform(.005,.016),random.uniform(.005,.016),random.uniform(.008,.035),random.uniform(3,16),random.uniform(2,14),random.uniform(.002,.03),random.uniform(.002,.03)))
 gaps=[]
 for a in cases:
  h,_=closed(*a);v=lp(*a)
  assert abs(h-v)<.0008,(a,h,v)
  means=witness(*a);assert means[0]<=a[-2]+1e-12 and means[1]<=a[-1]+1e-12
  gaps.append(abs(h-v))
 for _ in range(500):
  a=(random.uniform(.001,.05),random.uniform(.001,.05),random.uniform(0,.1),random.uniform(.3,25),random.uniform(.3,25),random.uniform(0,.6),random.uniform(0,.6))
  means=witness(*a);assert means[0]<=a[-2]+1e-12 and means[1]<=a[-1]+1e-12
 assert .095<pred<.100
 assert closed(*args[:2],args[2]+.04,*args[3:])[0]>pred
 assert closed(*args[:3],15,15,*args[-2:])[0]>pred
 result={'pass':True,'n_lp_cases':len(cases),'n_witness_cases':500,'holdout_peak':pred,'holdout_lp':lp(*args),'max_lp_gap':max(gaps),'human_evidence':False}
 (ROOT/'checker_results.json').write_text(json.dumps(result,indent=2)+'\n')
 print(result)
if __name__=='__main__':run()
