"""Conditional equal-bin EyeDentify reference-folding instrument model."""
import numpy as np
N=90
def fold_reference(x):
    x=np.asarray(x,dtype=float)
    if x.shape!=(270,): raise ValueError("requires 270 native samples")
    return (x[:N]+x[N:2*N]+x[2*N:])/3
def wave(f_hz,amplitude=.2,baseline=3.0,phase=0):
    t=np.arange(270)/90
    return baseline+amplitude*np.sin(2*np.pi*f_hz*t+phase)
def bias_coefficient(j):
    if not 0<=j<90: raise ValueError(j)
    return sum(abs(k-2*j/90) for k in range(3))/3
