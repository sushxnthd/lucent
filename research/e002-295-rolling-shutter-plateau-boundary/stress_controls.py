import numpy as np,json
from pathlib import Path
H=40.;T=.02;tau=20e-6;v=1600.;A=.25;B=.5
ys=np.linspace(0,H,801);ss=np.linspace(-T/2,T/2,2001);h=(1-v*tau)*H/2
def capture(accel=0.,glare=0.,shift=0.,gain=1.,offset=0.):
 t=tau*ys[:,None]+ss[None,:]
 x=A+B*(ys[:,None]>=h+shift+v*t+.5*accel*t*t).mean(axis=1)
 return gain*(x+glare*np.exp(-.5*((ys-14)/2)**2))+offset
def estimate(x,aa=A,bb=B):
 f=(x-aa)/bb;mid=(f>.2)&(f<.8)
 slope=np.polyfit(ys[mid],f[mid],1)[0];w=1/slope
 return w/(T+tau*w)
r=dict(base=estimate(capture()),geometry_only=estimate(capture(shift=2)),
 brightness_uncalibrated=estimate(capture(gain=1.1,offset=.05)),
 brightness_recalibrated=estimate(capture(gain=1.1,offset=.05),1.1*A+.05,1.1*B),
 acceleration=estimate(capture(accel=150000)),glasses_reflection=estimate(capture(glare=.12)),
 missingness_only='ABSTAIN: plateau cropped',temporal_smoothness_only='ABSTAIN: peak speed not identified')
Path(__file__).with_name('stress_results.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))