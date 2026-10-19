"""Conditional full-image observability law; synthetic model only."""
import math
from scipy.special import ndtr

def identified_interval(q, r, T=1.0):
    if not (0<=q<=1 and 0<r<=1 and T>0): raise ValueError("bad domain")
    return T*r*q/(1-q+r*q), T*q/(r*(1-q)+q)

def weight(z, variant):
    return 1-z/2 if variant=="early" else .5+z/2

def edge(z, variant, D=1.):
    return D*(4*z-z*z)/3 if variant=="early" else D*(2*z+z*z)/3

def smooth_event_times(T):
    return T*(2-math.sqrt(2.5)),T*(math.sqrt(2.5)-1)

def triangular(z, peak, A=1.):
    return A*z/peak if z<=peak else A*(1-z)/(1-peak)

def triangular_peak_interval(A,L,T):
    return (A/L,T-A/L) if L*T>=2*A else None
