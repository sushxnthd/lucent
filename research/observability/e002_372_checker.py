"""E002-372: independent LP checker for the resting-endpoint hidden-blink law.
Only synthetic instrument tests; no human validation.
Requires numpy, scipy.
"""
import math
import numpy as np
from scipy.optimize import linprog

def analytic_critical_time(L, V, A):
    assert L > 0 and V > 0 and A > 0
    one_leg = 2 * math.sqrt(L/A) if L <= V*V/A else L/V + V/A
    return 2 * one_leg

def lp_minimum_aperture(H, V, A, N=120):
    dt = H/N
    j = np.arange(N)
    k = np.arange(N+1)[:,None]
    W = dt*dt*np.maximum(k-j-.5,0)  # aperture = 1 + W@u
    U = dt*(j[None,:] < k)          # velocity = U@u
    Aub = np.vstack((W[1:-1],-W[1:-1],U[1:-1],-U[1:-1]))
    bub = np.r_[np.zeros(N-1),np.ones(N-1),
                np.full(N-1,V),np.full(N-1,V)]
    out = linprog(W[N//2],A_ub=Aub,b_ub=bub,
                  A_eq=np.vstack((W[-1],U[-1])),b_eq=np.zeros(2),
                  bounds=[(-A,A)]*N,method="highs")
    assert out.success, out.message
    a = 1+W@out.x
    v = U@out.x
    assert min(a) >= -1e-6 and max(a) <= 1+1e-6
    assert max(abs(v)) <= V+1e-6
    assert abs(a[-1]-1) < 1e-6 and abs(v[-1]) < 1e-6
    return float(min(a))

if __name__ == "__main__":
    H=1/30-0.010; theta=.2; L=1-theta; V=100.
    Acrit=2*V/(H-2*L/V)
    print("Acrit",Acrit)
    for A in [16000.,20000.,25000.,27000.,Acrit,28000.,30000.,40000.]:
        amin=lp_minimum_aperture(H,V,A)
        pred=H>analytic_critical_time(L,V,A)
        obs=amin<theta-1e-5
        if abs(A-Acrit)>1e-3: assert pred==obs,(A,pred,obs)
        print(A,round(amin,8),pred,obs)
