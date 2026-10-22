"""Exact one-box-exposure optimal recovery of a calibrated ocular proxy."""
import math
def L(a,b):
    if not (0<=a<=1 and b>=0): raise ValueError
    if b==0: return a
    return a*a/b if 2*a<=b else a-b/4
def U(a,b): return 1-L(1-a,b)
def Linv(y,b):
    if b<0 or not 0<=y<=1: raise ValueError
    if b==0: return y
    if y>=L(1.,b): return 1.
    if y<=b/4: return math.sqrt(b*y)
    return y+b/4
def interval(m,V,w,eta=0):
    if not (0<=m<=1 and V>=0 and w>0 and eta>=0): raise ValueError
    b=V*w
    return (1-Linv(1-max(0.,m-eta),b),Linv(min(1.,m+eta),b))
def witness(a,V,w,mean,t):
    b=V*w; lo=L(a,b);hi=U(a,b)
    if not lo-1e-12<=mean<=hi+1e-12: raise ValueError
    lam=0 if hi-lo<1e-14 else max(0,min(1,(mean-lo)/(hi-lo)))
    return (1-lam)*max(0,a-V*abs(t))+lam*min(1,a+V*abs(t))
def optimum_exposure(V,k):
    if V<=0 or k<=0: raise ValueError
    return (2*k/V)**(2/3)
