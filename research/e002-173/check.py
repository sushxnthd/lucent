"""Independent 16-corner proof checks, no human data required."""
import itertools,math
from certificate import certificate
T=math.log(1.05)
def category(x):
 return 1 if x>=T else (-1 if x<=-T else 0)
for v in (-.5,-.1,-.02,0,.02,.1,.5):
 for e in (0,.005,.01,.02,.05):
  vals=[]
  for signs in itertools.product((-1,1),repeat=4):
   p0,p1,d0,d1=[a*(1+s*e) for a,s in zip((1,math.exp(v),1,1),signs)]
   vals.append(math.log((p1/d1)/(p0/d0)))
  h=2*math.log((1+e)/(1-e))
  assert abs(min(vals)-(v-h))<1e-12
  assert abs(max(vals)-(v+h))<1e-12
  classes=set(map(category,vals))
  expected=next(iter(classes)) if len(classes)==1 else None
  assert certificate(v,e)==expected
print("PASS: 35 cases, 560 independent error-box corners")
