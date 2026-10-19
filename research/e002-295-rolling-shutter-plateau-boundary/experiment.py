import json,math,random
from pathlib import Path
P=Path(__file__).resolve().parent
def width(v,T,tau):return v*T/(1-v*tau)
def inverse(w,T,tau):return w/(T+tau*w)
def threshold(H,T,tau):return H/(T+tau*H)
def pix(y,H,v,T,tau,A,B):
 k=1-v*tau;h=k*H/2
 q=max(0,min(1,.5+(k*y-h)/(v*T)))
 return A+B*q
def case(name,H,T,tau,v):
 w=width(v,T,tau);m=(H-w)/2
 return dict(name=name,H=H,T=T,tau=tau,v=v,width=w,plateaus=m>0,margin=m,critical=threshold(H,T,tau),recovered=inverse(w,T,tau) if m>0 else None)
cases=[case('30fps_short',40,1/120,2e-5,1600),case('30fps_long',40,.02,2e-5,1600),case('fast_motion',40,.02,2e-5,3000),case('10hz_loader_same_exposure',40,.02,2e-5,1600),case('frozen_low',48,1/90,14e-6,3500),case('frozen_high',48,1/90,14e-6,4500)]
H=40;T=.02;tau=2e-5;v1=3000;v2=4000;w1=width(v1,T,tau);w2=width(v2,T,tau)
A1=.3;B1=.4;B2=B1*w2/w1;A2=A1+(B1-B2)/2
diff=max(abs(pix(i*H/400,H,v1,T,tau,A1,B1)-pix(i*H/400,H,v2,T,tau,A2,B2)) for i in range(401))
assert diff<1e-12 and cases[4]['plateaus'] and not cases[5]['plateaus']
r=dict(cases=cases,collision_max_abs_pixel_diff=diff,reference_humans=0)
(P/'results.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))