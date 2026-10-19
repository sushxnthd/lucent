import json
from math import sqrt
from pathlib import Path
from scipy.optimize import brentq

def exposure_min(x,T,V,p=1):
    return 2*(x**(p+1)-max(0.,x-V*T/2)**(p+1))/((p+1)*V*T)

def edge_ceiling(r,T,V,p=1):
    r=max(0.,min(1.,r))
    if p==1:
        return min(1.,sqrt(r*V*T) if r<=V*T/4 else r+V*T/4)
    if r>=exposure_min(1.,T,V,p): return 1.
    if r==0: return 0.
    return brentq(lambda x:exposure_min(x,T,V,p)-r,0.,1.,xtol=1e-14)

def gap_ceiling(x,G,V):
    if x+V*G/2<=1:return x*G+V*G*G/4
    return G-(1-x)**2/V

def case(name,T,G,V,eta,p):
    r=min(1.,2*eta); x=edge_ceiling(r,T,V,p); U=gap_ceiling(x,G,V)
    return dict(name=name,T=T,G=G,V=V,eta=eta,response_power=p,collision_mean_ceiling=r,
                edge_ceiling=x,peak_ceiling=min(1.,x+V*G/2),
                hidden_gap_dose_seconds=U,hidden_gap_fraction_of_period=U/(T+G))

CASES=[
 ("30fps_half_shutter_linear",1/60,1/60,20,.025,1),
 ("10hz_loader_60fps_shutter_linear",1/60,1/12,20,.025,1),
 ("30fps_half_shutter_quadratic",1/60,1/60,20,.025,2),
 ("10hz_loader_60fps_shutter_quadratic",1/60,1/12,20,.025,2),
 ("30fps_noiseless",1/60,1/60,20,0,1),
 ("10hz_noiseless",1/60,1/12,20,0,1),
 ("30fps_low_noise_linear",1/60,1/60,20,.005,1),
 ("30fps_slow_eyelid_linear",1/60,1/60,8,.025,1),
 ("24fps_unseen_synthetic_quadratic",.012,1/24-.012,18,.008,2),
 ("rational_witness_linear",1.,1.,1.,1/32,1),
 ("rational_witness_quadratic",1.,1.,1.,1/192,2)]
if __name__=="__main__":
    Path(__file__).with_name("results.json").write_text(json.dumps({"cases":[case(*args) for args in CASES]},indent=2)+"\n")
