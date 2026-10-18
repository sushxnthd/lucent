"""E002-278: exact set separation for a known log-radius response template.
All data synthetic; limits L and eps are hypothetical and uncalibrated.
"""
import json, math, pathlib, hashlib
import numpy as np

L=0.012; EPS=0.0015; A=0.0048; DURATION=5.0
CASES=[
 ("10fps_0p4Hz",10,.4,1/30,0.),
 ("24fps_1p2Hz",24,1.2,1/60,0.),
 ("30fps_1p2Hz",30,1.2,1/60,0.),
 ("60fps_1p2Hz",60,1.2,1/120,0.),
 ("10fps_5Hz_alias",10,5.,1/60,0.),
 ("24fps_4Hz_half_exposure",24,4.,1/48,0.),
 ("24fps_4Hz_full_exposure",24,4.,1/24,0.),
 ("10fps_5Hz_phase_shift",10,5.,1/60,.37)
]
def signal(fs,f,te,phase):
 t=np.arange(round(fs*DURATION))/fs
 return t,np.sinc(f*te)*np.sin(2*np.pi*f*t+phase)
def critical(t,s):
 d=t[None,:]-t[:,None]; h=s[None,:]-s[:,None]
 good=np.triu(np.ones_like(d,dtype=bool),1)&(np.abs(h)>1e-12)
 if not good.any():return None,None
 q=np.full(d.shape,np.inf);q[good]=(2*L*d[good]+4*EPS)/np.abs(h[good])
 i,j=np.unravel_index(np.argmin(q),q.shape)
 return float(q[i,j]),(int(i),int(j))
def witness(t,s,a):
 w=a*s
 # Existence is equivalent to pairwise Lipschitz interval feasibility.
 d=np.abs(t[:,None]-t[None,:])
 assert np.max(np.abs(w[:,None]-w[None,:])-2*L*d-4*EPS)<=1e-10
 g=np.max(w[None,:]-2*EPS-2*L*d,axis=1)
 b0=g/2;b1=-g/2;e0=(w-g)/2;e1=-e0
 y0=b0+e0;y1=w+b1+e1
 assert np.max(np.abs(y0-y1))<1e-10
 assert np.max(np.abs(np.diff(b0)/np.diff(t)))<=L+1e-10
 assert np.max(np.abs(e0))<=EPS+1e-10
 return dict(t=t.tolist(),template=s.tolist(),b0=b0.tolist(),b1=b1.tolist(),
             e0=e0.tolist(),e1=e1.tolist(),y0=y0.tolist(),y1=y1.tolist())
def run():
 result=[];raw={}
 for name,fs,f,te,phase in CASES:
  t,s=signal(fs,f,te,phase);crit,pair=critical(t,s)
  separated=crit is not None and A>crit*(1+1e-10)
  row=dict(name=name,fps=fs,frequency_hz=f,exposure_s=te,phase_rad=phase,
           critical_log_amplitude=crit,critical_pair=pair,
           test_amplitude=A,guaranteed_separation=separated)
  result.append(row)
  if name in ("24fps_4Hz_half_exposure","24fps_4Hz_full_exposure"):
   if separated:
    i,j=pair
    raw[name]=dict(pair=pair,signal_difference=float(abs(A*(s[j]-s[i]))),
                   artifact_plus_noise_budget=float(2*L*(t[j]-t[i])+4*EPS))
   else:raw[name]=witness(t,s,A)
  if crit is not None:
   assert witness(t,s,crit*.95) is not None
   assert np.max(np.abs((crit*1.05)*(s[:,None]-s[None,:]))-2*L*np.abs(t[:,None]-t[None,:])-4*EPS)>0
  else:assert np.max(np.abs(s-s[0]))<1e-12
 p=pathlib.Path(__file__).resolve().parent
 (p/"RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
 (p/"RAW_SYNTHETIC.json").write_text(json.dumps(raw,indent=2)+"\n")
 print(json.dumps([dict(name=x["name"],Acrit=x["critical_log_amplitude"],separable=x["guaranteed_separation"]) for x in result],indent=2))
if __name__=="__main__":run()
