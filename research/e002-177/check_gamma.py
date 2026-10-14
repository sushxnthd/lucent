import json, math, sys
from pathlib import Path
x=json.loads(Path(sys.argv[1]).read_text())
cdf=lambda z:(1+math.erf(z/math.sqrt(2)))/2
def root(g,s):
 lo,hi=-10*s,10*s
 for _ in range(80):
  mid=(lo+hi)/2
  if cdf(mid/s)**g<.5:lo=mid
  else:hi=mid
 return (lo+hi)/2
assert len(x['cases'])==18
assert len(x['gamma_cases'])==12
for a in x['cases']:
 assert a['pass'] and a['max_abs_residual']<1e-12 and a['monotonic']
for a in x['gamma_cases']:
 assert abs(root(a['gamma'],a['blur_px'])-a['edge_shift_px'])<2e-12
assert x['summary']['physiological_rgb_gate']=='NOT_TESTED'
print('INDEPENDENT_CHECK_PASSED')
