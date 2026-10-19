"""Independent high-precision and LP verification; Python scipy, numpy, mpmath."""
import math, json
import numpy as np
import mpmath as mp
from scipy.special import ndtr
from scipy.optimize import brentq,linprog

def highprecision(T,r,v,sigma):
    mp.mp.dps=50
    T,r,v,sigma=map(lambda z:mp.mpf(str(z)),(T,r,v,sigma))
    k=v/sigma;h=T/2
    def G(z):
        a=k*z
        return z*mp.erf(a/mp.sqrt(2))/2+(mp.exp(-a*a/2)-1)/(k*mp.sqrt(2*mp.pi))
    return float(mp.findroot(lambda u:r*G(h+u)-G(h-u),(mp.mpf(0),h/3)))

def independent_LP(T,r,v,sigma,N=601):
    t=np.linspace(-T/2,T/2,N)
    def f(x):
        c=ndtr((x-v*t)/sigma)-.5
        c[0]*=.5;c[-1]*=.5
        z=linprog(c,bounds=[(r,1)]*N,method='highs')
        assert z.success
        return z.fun
    return brentq(f,0,v*T/2,xtol=1e-12)/v

def run():
    rng=np.random.default_rng(311)
    worst=0.
    for j in range(50):
        T=float(rng.uniform(.006,.035));r=float(rng.uniform(.08,.96))
        v=float(rng.uniform(40,250));sigma=float(rng.uniform(.3,2.8))
        a=highprecision(T,r,v,sigma)
        b=independent_LP(T,r,v,sigma)
        worst=max(worst,abs(a-b))
        assert abs(a-b)<4e-7,(j,a,b)
    p=(.013,.37,170.,.9)
    frozen=.0017549665698877767
    assert abs(highprecision(*p)-frozen)<1e-11
    assert abs(independent_LP(*p,N=1201)-frozen)<1.5e-7
    print(json.dumps({'status':'PASS','cases':50,'worst_error_s':worst,'frozen_prediction_s':frozen}))
if __name__=='__main__':run()
