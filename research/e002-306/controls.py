"""Nuisance controls for E002-306; all synthetic."""
import numpy as np,math,json
R=25.;R2=27.5;eta=.3;a=R*.5
x=np.linspace(-a,a,5001)
f=lambda r:np.sqrt(r*r-x*x)-math.sqrt(r*r-a*a)
y1=f(R);y2=f(R2);obs=(y1+y2)/2
assert max(abs(obs-y1))<=eta and max(abs(obs-y2))<=eta
pts=np.stack([x,y1],axis=1)
A=np.array([[1.2,.15],[-.07,.88]]);b=np.array([11.,-7.])
warped=pts@A.T+b
geomerr=float(np.max(abs((warped-b)@np.linalg.inv(A).T-pts)))
assert geomerr<1e-12
full=float(max(abs(y1-y2)));masked=float(max(abs((y1-y2)[abs(x)>=.6*a])))
assert masked<full
t=np.linspace(0,4,401);Ra=25+.25*np.sin(2*np.pi*1.3*t);Rb=1.1*Ra
s=lambda r:a*a/(r+np.sqrt(r*r-a*a))
smoothmax=float(max(abs(s(Ra)-s(Rb))))
assert smoothmax<=2*eta
print(json.dumps({"geometry_only_error_px":geomerr,"brightness_only_zero_contrast_unobservable":True,"missingness_only_full_gap_px":full,"missingness_only_masked_gap_px":masked,"temporal_smoothness_two_smooth_histories_indistinguishable":True,"temporal_max_gap_px":smoothmax,"human_validation":False},indent=2))
