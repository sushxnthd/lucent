"""E002-297 minimal runnable independent synthetic instrument check."""
import numpy as np
from fractions import Fraction as F
rng=np.random.default_rng(20261019)
def random_psf():
    h=rng.uniform(.01,1,15);return h/h.sum()
def area_trial():
    x=np.zeros(256); a=0
    for k in range(16):
        width=int(rng.integers(8,44));center=int(rng.integers(115,141))
        mask=np.zeros(256);mask[center-width//2:center-width//2+width]=1
        x+=np.convolve(mask,random_psf(),mode="same")/16;a+=width/16
    return x,a
def rolling_area(A,v,tau,T):
    d=1-v*tau
    xs=np.linspace(-40,40,30001)
    if v==0:return A
    if v>0:
        low=(d*xs-A/2)/v;high=(d*xs+A/2)/v
    else:
        low=(d*xs+A/2)/v;high=(d*xs-A/2)/v
    y=np.maximum(0,np.minimum(T,high)-np.maximum(0,low))/T
    return np.trapezoid(y,xs)
def run():
    errs=[]; ratios=[]
    for _ in range(400):
        x,a=area_trial();y,b=area_trial();c=float(rng.uniform(.3,2))
        sx=(c*x).sum();sy=(c*y).sum()
        errs.append(abs(sx/c-a));ratios.append(abs(sy/sx-b/a))
    print("global shutter max mass error",max(errs))
    print("global shutter max ratio error",max(ratios))
    A,v,tau,T=11.7,1125,27e-6,.013
    print("rolling predicted",A/(1-v*tau),"numerical",rolling_area(A,v,tau,T))
if __name__=="__main__":run()
