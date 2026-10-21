"""Synthetic Lucent ocular instrument. No human validation."""
import numpy as np
from scipy.signal import lfilter
DT=1/300
T=np.arange(0,5+0.01,DT)
K=np.arange(150)
def probe(pos):
    return np.array([int(int(t*2) in pos) for t in T],float)
def expose(v):
    return np.array([v[i*10:i*10+3].mean() for i in K])
def design(pos,tau):
    u=probe(pos)
    t=np.arange(len(u))*DT
    lag=np.maximum(0,t-.22)
    g=np.where(t>=.22,lag*np.exp(-lag/.32)/(.32**2),0)
    s=expose(np.convolve(u,g)[:len(u)]*DT)
    a=np.exp(-DT/tau)
    ae=lfilter([1-a],[1,-a],u)
    n=np.column_stack((np.ones(150),expose(t),expose(t*t),expose(u),expose(ae)))
    return s,n
def qnorm(pos,tau,missing=()):
    s,n=design(pos,tau)
    if len(missing):
        keep=np.ones(len(s),bool)
        keep[list(missing)]=False
        s,n=s[keep],n[keep]
    return float(np.linalg.norm(s-n@np.linalg.lstsq(n,s,rcond=None)[0]))
