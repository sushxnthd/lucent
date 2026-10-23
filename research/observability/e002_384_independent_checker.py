"""Independent exact-integration and Lipschitz-envelope checker for E002-384."""
import json
from pathlib import Path
import numpy as np
from e002_384_clip_calibration import aperture, V, W, FPS

rng=np.random.default_rng(384382)
max_abs=0.0
for _ in range(500):
    c=float(rng.uniform(.01,1.9)); p=float(rng.uniform(.004,.055))
    l=float(rng.uniform(0,1.98)); r=l+W
    breaks=[l,r,c-p/2-.95/V,c-p/2,c+p/2,c+p/2+.95/V]
    knots=np.array(sorted(set(x for x in breaks if l<=x<=r)))
    exact=float(np.trapezoid(aperture(knots,[c],[p]),knots)/W)
    fine=np.linspace(l,r,4001)
    dense=float(np.trapezoid(aperture(fine,[c],[p]),fine)/W)
    max_abs=max(max_abs,abs(exact-dense))
assert max_abs<2e-6,max_abs

max_env=0.0
H=1/FPS-W
for _ in range(2000):
    l=float(rng.uniform(0,1));r=float(rng.uniform(max(0,l-V*H),min(1,l+V*H)))
    tstar=(l-r+V*H)/(2*V)
    t=np.array([0,H,min(H,max(0,tstar))])
    # Independently evaluate the two Lipschitz cones at their intersection and boundaries.
    lower_path=np.maximum.reduce([np.zeros_like(t),l-V*t,r-V*(H-t)])
    numerical=float(lower_path.min())
    closed=max(0,l-V*H,r-V*H,(l+r-V*H)/2)
    max_env=max(max_env,abs(numerical-closed))
assert max_env<1e-12,max_env
result={'piecewise_linear_exact_integration_checks':500,'max_integral_difference':max_abs,'independent_envelope_checks':2000,'max_envelope_difference':max_env,'status':'PASS'}
Path(__file__).with_name('e002_384_independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
