"""Exact regression identity checked against explicit least squares on synthetic vectors."""
import math,statistics
def check(x,y):
    mx=statistics.mean(x);my=statistics.mean(y)
    vx=sum((z-mx)**2 for z in x);vy=sum((z-my)**2 for z in y)
    cov=sum((a-mx)*(b-my) for a,b in zip(x,y))
    r=cov/math.sqrt(vx*vy);slope=max(0.,cov/vx);intercept=my-slope*mx
    observed=math.sqrt(sum((v-intercept-slope*u)**2 for u,v in zip(x,y))/vy)
    predicted=math.sqrt(1-r*r) if r>0 else 1.
    assert abs(observed-predicted)<1e-12
for x,y in [([1,2,3,4],[1,3,2,5]),([1,2,3,4],[4,3,2,1]),([1,2,3,4],[2,4,6,8]),([1,2,3,4],[2,3,2,3])]:check(x,y)
print("SYNTHETIC IDENTITY CHECK PASSED")
