"""Sharp asymmetric shutter-gap bound. Standard library only."""
from math import sqrt

def endpoint(E,V,m):
    assert E>0 and V>0 and m>=0
    return min(1.,sqrt(2*V*E*m) if m<=V*E/2 else m+V*E/2)

def peak(E0,E1,G,U,D,m0,m1):
    assert G>=0 and U>0 and D>0
    b0,b1=endpoint(E0,U,m0),endpoint(E1,D,m1)
    t=max(0.,min(G,(b1+D*G-b0)/(U+D)))
    return min(1.,b0+U*t,b1+D*(G-t)),t

def occupancy(E0,E1,G,U,D,m0,m1,theta):
    b0,b1=endpoint(E0,U,m0),endpoint(E1,D,m1)
    return max(0.,G-max(0.,theta-b0)/U-max(0.,theta-b1)/D)
