"""Independent direct quadrature and LP checks; no human data."""
import json, math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import ndtr
from scipy.optimize import linprog
from model import identified_interval,weight,edge,smooth_event_times,triangular,triangular_peak_interval

p=Path(__file__).parent
f=json.loads((p/"FROZEN_PREDICTION.json").read_text())
T=f["exposure_s"]; D=f["displacement_px"]; sigma=f["blur_sigma_px"]
def image(x,v):
    a=quad(lambda z:weight(z,v)*ndtr((x-edge(z,v,D))/sigma),0,1,epsabs=2e-13)[0]
    b=quad(lambda z:weight(z,v),0,1)[0]
    return a/b
xs=np.linspace(-2,6,101)
pair_err=max(abs(image(float(x),"early")-image(float(x),"late")) for x in xs)
spatial_err=max(abs(image(float(x),"early")-quad(lambda s:ndtr((x-s)/sigma),0,D)[0]/D) for x in xs)
assert pair_err<1e-10 and spatial_err<1e-10
ta,tb=smooth_event_times(T)
assert abs((tb-ta)*1000-f["predicted_smooth_gap_ms"])<1e-10
assert abs(edge(.5,"early",D)-edge(.5,"late",D)-f["predicted_midpoint_gap_px"])<1e-12
lo,hi=identified_interval(.5,.5,T)
assert abs((hi-lo)*1000-f["predicted_sharp_width_ms"])<1e-10
rng=np.random.default_rng(20261020)
pass_in=pass_out=0
for _ in range(120):
    q=float(rng.uniform(.1,.9)); r=float(rng.uniform(.15,.95))
    a,b=identified_interval(q,r)
    for z,feasible in [(a+.05*(b-a),True),(b-.05*(b-a),True),(max(.0001,a-.05*(b-a)),False),(min(.9999,b+.05*(b-a)),False)]:
        n=160; widths=np.r_[np.repeat(z/(n//2),n//2),np.repeat((1-z)/(n//2),n//2)]
        eq=np.r_[(1-q)*widths[:n//2],-q*widths[n//2:]][None,:]
        sol=linprog(np.zeros(n),A_eq=eq,b_eq=[0],bounds=[(r,1)]*n,method="highs")
        assert sol.success==feasible,(q,r,z,sol.message)
        if feasible: pass_in+=1
        else: pass_out+=1
A=.15; L=25.; T2=1/60
pa,pb=triangular_peak_interval(A,L,T2)
def tri_image(x,zpeak):
    k=zpeak/T2
    return quad(lambda z:ndtr((x-triangular(z,k,A))/.03),0,k)[0]+quad(lambda z:ndtr((x-triangular(z,k,A))/.03),k,1)[0]
tri_err=max(abs(tri_image(float(x),pa)-tri_image(float(x),pb)) for x in np.linspace(-.08,.23,41))
assert tri_err<1e-10
print(json.dumps({"passed":True,"full_image_error":pair_err,"spatial_check_error":spatial_err,"lp_feasible":pass_in,"lp_infeasible":pass_out,"triangular_error":tri_err},indent=2))
