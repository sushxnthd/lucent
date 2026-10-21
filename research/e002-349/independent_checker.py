"""Independent phase-enumeration oracle; requires NumPy."""
import numpy as np
from exposure_phase import minimax_overlap,sharp_boundary,detector_boundary
rng=np.random.default_rng(3492026)
def brute(D,F,w,n=3001):
    s=np.linspace(0,F,n); best=np.zeros_like(s)
    for k in range(-2,7):
        best=np.maximum(best,np.maximum(0,np.minimum(s+D,k*F+w)-np.maximum(s,k*F)))
    return float(best.min())
maxerr=0.
for _ in range(700):
    F=float(rng.uniform(.01,.15));w=float(rng.uniform(.04,1)*F);D=float(rng.uniform(0,2.5)*F)
    err=abs(brute(D,F,w)-minimax_overlap(D,F,w))/F
    assert err<.00025,(D,F,w,err)
    maxerr=max(maxerr,err)
collisions=0
for _ in range(400):
    F=float(rng.uniform(.015,.12));w=float(rng.uniform(.05,.95)*F);eps=float(rng.uniform(.001,.45))
    B=sharp_boundary(F,w,eps)
    for factor in (0,.5,1):
        D=F-w+factor*(B-F+w);s=w-(D-(F-w))/2
        h=np.array([max(0,min(s+D,k*F+w)-max(s,k*F))/w for k in range(-2,5)])
        y=h/2
        assert max(abs(y))<=eps+1e-10 and max(abs(y-h))<=eps+1e-10
        collisions+=1
    assert minimax_overlap(B+1e-5*w,F,w)/w>2*eps
F=1/30;w=.01;eps=.05
assert abs(sharp_boundary(F,w,eps)*1000-25.3333333333333)<1e-8
assert abs(detector_boundary(F,w,.5,eps)*1000-34.3333333333333)<1e-8
print({"random_phase_checks":700,"collision_checks":collisions,"max_normalized_phase_grid_error":maxerr,"human_evidence":"NOT RUN"})
