# Exact E002-371 theorem

Assume aperture a(t) in [0,1], |a'(t)|<=V, endpoint apertures a0,a1, shutter gap H, threshold 0<theta<1. The exact compatible threshold-closed duration interval is

Tmin=min(H,((theta-a0)_+ +(theta-a1)_+)/V)
Tmax=max(0,H-((a0-theta)_+ +(a1-theta)_+)/V).

Proof: Every admissible trajectory lies between ell(t)=max(0,a0-Vt,a1-V(H-t)) and u(t)=min(1,a0+Vt,a1+V(H-t)). Both envelopes satisfy the speed and endpoint constraints. The duration where ell<=theta equals Tmax; the duration where u<=theta equals Tmin. Both extrema are attained.

For fully open endpoints, a positive-duration hidden threshold closure exists iff V>2(1-theta)/H. At equality there can only be a zero-duration threshold touch. Exact, conditional, not a human-calibrated limit.
