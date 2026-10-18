"""Synthetic E002-276 aperture observability; no human data."""
import json,math
from pathlib import Path
import numpy as np
N,SIGMA,R,TOL,REPS=60,.5,20.,1.,4000
DEV=[.12,.20,.35,.50,.65,.80,1.,1.2,1.57]
HOLD=[.58,.93]
def design(a):
 t=np.linspace(-a,a,N)
 return np.column_stack((np.ones(N),np.cos(t),np.sin(t)))
def analytic(a):
 X=design(a)
 sd=float(SIGMA*np.sqrt(np.linalg.inv(X.T@X)[0,0]))
 return sd,math.erf(TOL/(math.sqrt(2)*sd))
def run():
 rng=np.random.default_rng(2762026)
 rows=[]
 for a in DEV+HOLD:
  X=design(a)
  y=(X@np.array([R,2.5,-1.7]))[:,None]+rng.normal(0,SIGMA,size=(REPS,N)).T
  rr=np.linalg.lstsq(X,y,rcond=None)[0][0]
  sd,p=analytic(a)
  rows.append(dict(alpha=a,arc_degrees=2*a*180/math.pi,sd_px=sd,p_pred=p,p_observed=float(np.mean(abs(rr-R)<=TOL)),sd_observed=float(np.std(rr,ddof=1)),split='holdout' if a in HOLD else 'development'))
 lo,hi=.05,math.pi
 for _ in range(70):
  mid=(lo+hi)/2
  if analytic(mid)[1]>=.75:hi=mid
  else:lo=mid
 half=np.linspace(-.15,.15,N//2)
 t=np.r_[half,half+math.pi]
 X=np.column_stack((np.ones(N),np.cos(t),np.sin(t)))
 result=dict(metadata=dict(seed=2762026,n=N,sigma_px=SIGMA,radius_px=R,tolerance_px=TOL,repetitions=REPS,human_data=False),transition=dict(alpha_rad=hi,total_arc_degrees=2*hi*180/math.pi),rows=rows,wildcard=dict(antipodal_sd=float(SIGMA*np.sqrt(np.linalg.inv(X.T@X)[0,0])),single_arc_sd=analytic(.15)[0]),exact_gauge=dict(r1=20,b1=0,r2=19,b2=1,same_apparent_radius=True))
 Path(__file__).with_name('RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
 print(result['transition'])
 print([(r['alpha'],r['p_pred'],r['p_observed']) for r in rows if r['split']=='holdout'])
if __name__=='__main__':run()
