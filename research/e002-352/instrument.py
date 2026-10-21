"""Lucent E002-352: analytic shutter-peak boundary (standard library only)."""
from math import sqrt

def peak(t, t0, A, V):
    if not (V > 0 and A >= 0): raise ValueError("A>=0, V>0")
    return max(0.0, A-V*abs(t-t0))

def shutter_mean(offset, A, V, w):
    if not (V>0 and w>0 and A>=0): raise ValueError("bad arguments")
    q=A/V
    def P(x):
        r=min(abs(x),q)
        s=A*r-.5*V*r*r
        return s if x>=0 else -s
    return (P(offset+w/2)-P(offset-w/2))/w

def guarantee(A, V, F, w):
    if not (V>0 and F>0 and 0<w<=F and A>=0): raise ValueError("bad arguments")
    q=A/V
    l=(F-w)/2
    u=(F+w)/2
    return V/(2*w)*(max(q-l,0)**2-max(q-u,0)**2)

def observable(A, V, F, w, epsilon):
    if epsilon<0: raise ValueError("epsilon>=0")
    return guarantee(A,V,F,w)>2*epsilon

def speed_boundary(A,F,w,epsilon):
    if not (A>0 and 0<=epsilon<A/2): return None
    lo=1e-12
    hi=max(4*A/(F-w) if F>w else 4*A/F,1.0)
    while guarantee(A,hi,F,w)>2*epsilon: hi*=2
    for _ in range(120):
        mid=(lo+hi)/2
        if guarantee(A,mid,F,w)>2*epsilon: lo=mid
        else: hi=mid
    return (lo+hi)/2

def collision(A,V,F,w,epsilon,frames=15):
    """Exact same observed samples for a tent event and no event."""
    rows=[]
    for k in range(-frames//2,frames//2+1):
        m=shutter_mean(k*F-F/2,A,V,w)
        if m>2*epsilon+1e-10: raise ValueError("not in collision region")
        rows.append((k,m,-m/2,m/2,m/2))
    return rows

if __name__=="__main__":
    assert abs(guarantee(1,60,1/30,.01)-.075)<1e-12
    assert abs(speed_boundary(1,1/30,.01,.05)-56.819636113594925)<1e-8
    print("E002-352: analytic checks passed")
