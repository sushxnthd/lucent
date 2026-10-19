"""E002-308 conditional shutter-mean observability. No human calibration."""
def area(z,L,h):
    if L == 0: return z*h
    m=min(h,z/L)
    return z*m-L*m*m/2

def min_mean(z,Lc,Lo,T):
    h=T/2
    return (area(z,Lc,h)+area(z,Lo,h))/T

def max_mean(z,Lc,Lo,T):
    return 1-min_mean(1-z,Lc,Lo,T)

def center_interval(y,eta,Lc,Lo,T):
    low=max(0,y-eta)
    high=min(1,y+eta)
    if low>high: return None
    def inverse(fn,target):
        a,b=0.0,1.0
        for _ in range(70):
            m=(a+b)/2
            if fn(m)<target: a=m
            else: b=m
        return (a+b)/2
    return (inverse(lambda z:max_mean(z,Lc,Lo,T),low),
            inverse(lambda z:min_mean(z,Lc,Lo,T),high))

def threshold_bound(theta,eta,Lc,Lo,T):
    return min_mean(theta,Lc,Lo,T)-eta,max_mean(theta,Lc,Lo,T)+eta

if __name__=="__main__":
    a,b=threshold_bound(.8,.05,25,8,1/60)
    assert abs(a-.68125)<1e-12
    assert abs(b-.9186666666666667)<1e-12
    print(a,b)
