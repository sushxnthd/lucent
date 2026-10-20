"""E002-321 conditional shutter-gap bound (synthetic only)."""
from math import sqrt

def endpoint_bound(E,L,mu):
    assert E>0 and L>0 and 0<=mu<=1
    if mu<=L*E/2:
        b=sqrt(2*L*E*mu)
    else:
        b=mu+L*E/2
    return min(1.,b)

def hidden_peak(P,E,L,mu):
    assert P>=E>0 and L>0
    return min(1.,endpoint_bound(E,L,mu)+L*(P-E)/2)

def max_hidden_threshold_duration(P,E,L,mu,theta):
    assert 0<theta<1
    return max(0.,P-E-2*max(0.,theta-endpoint_bound(E,L,mu))/L)

def witness(t,P,E,L,mu):
    b=endpoint_bound(E,L,mu);G=P-E
    if -E<=t<=0:return max(0.,b+L*t)
    if 0<=t<=G:return min(1.,b+L*min(t,G-t))
    if G<=t<=P:return max(0.,b-L*(t-G))
    raise ValueError("outside domain")
