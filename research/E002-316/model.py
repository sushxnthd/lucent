"""E002-316 1-D linear lid-band instrument model; not human evidence."""
import numpy as np

def observed_profile(width, contrast, kernel):
    kernel=np.asarray(kernel,dtype=float)
    assert width>=1 and 0<contrast<=1
    assert np.all(kernel>=0) and np.isclose(kernel.sum(),1)
    return contrast*np.convolve(np.ones(width),kernel,mode="full")

def moments(y):
    y=np.asarray(y,dtype=float); x=np.arange(len(y)); S=y.sum()
    mu=(x*y).sum()/S
    return float(S),float(mu),float(((x-mu)**2*y).sum()/S)

def anatomical_ratio_interval(S0,D0,S1,D1,r):
    assert min(S0,D0,S1,D1,r)>0 and r<=1
    q=(S1/D1)/(S0/D0)
    return q*r,q/r

def variance_width_necessary(V,vmin,vmax):
    assert 0<=vmin<=vmax<=V
    return np.sqrt(12*max(0,V-vmax)),np.sqrt(12*(V-vmin))
