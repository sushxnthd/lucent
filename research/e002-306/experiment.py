"""E002-306 reproducible synthetic fixed-chord arc minimax experiment."""
import math,json
import numpy as np
from scipy.optimize import brentq

def s(R,a): return a*a/(R+math.sqrt(R*R-a*a))
def f(R,a,x): return np.sqrt(R*R-x*x)-math.sqrt(R*R-a*a)
def inv(v,a): return (a*a+v*v)/(2*v)
def crit(R,eta,q):
    g=lambda al:s(R,R*math.sin(al))-s(R*(1+q),R*math.sin(al))-2*eta
    if g(math.pi/2)<=0: return None
    return brentq(g,1e-10,math.pi/2,xtol=1e-13)
def run():
    rng=np.random.default_rng(306);maxerr=0.
    for _ in range(2000):
        r1=float(rng.uniform(10,80));r2=r1*float(rng.uniform(.8,1.8))
        a=min(r1,r2)*float(rng.uniform(.05,.99))
        x=np.linspace(-a,a,201)
        d=float(np.max(abs(f(r1,a,x)-f(r2,a,x))))
        maxerr=max(maxerr,abs(d-abs(s(r1,a)-s(r2,a))))
        assert abs(d-abs(s(r1,a)-s(r2,a)))<2e-12
        assert abs(inv(s(r1,a),a)-r1)<2e-9
    R=25.;eta=.3;q=.1
    rows=[]
    for deg in [10,20,30,37,38.300201251982,40,45,60]:
        a=R*math.sin(math.radians(deg));v=s(R,a)
        lo=inv(min(a,v+2*eta),a)
        hi=None if v<=2*eta else inv(v-2*eta,a)
        gap=v-s(R*(1+q),a)
        rows.append(dict(half_arc_deg=deg,sagitta_px=v,distance_to_10pct_larger_radius_px=gap,distinguishable=gap>2*eta,compatible_radius_lower_px=lo,compatible_radius_upper_px=hi))
    return dict(kernel="E002-306",R_px=R,eta_px=eta,q=q,critical_half_arc_deg=math.degrees(crit(R,eta,q)),unbounded_half_arc_deg=math.degrees(math.acos(1-2*eta/R)),random_cases=2000,max_sup_error_px=maxerr,cases=rows,human_validation=False)
if __name__=="__main__":print(json.dumps(run(),indent=2))
