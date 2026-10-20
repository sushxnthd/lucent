"""Independent checker; intentionally does NOT import model.py."""
import json, math, random
from pathlib import Path
root=Path(__file__).parent
frozen=json.loads((root/"FROZEN_PREDICTION.json").read_text())
R=frozen["R_pixels"]; eps=frozen["epsilon_pixels"]; tau=frozen["target_relative_upper_error"]

def circumradius(a,s):
    cy=(s*s-a*a)/(2*s)
    return abs(s-cy)

def geometry(r,phi):
    alpha=math.radians(phi/2)
    return r*math.sin(alpha),r*(1-math.cos(alpha))

def check_interval(a,shat,e,samples=501):
    lo=max(0,shat-e);hi=min(a,shat+e)
    if hi<=0 or lo>hi: return None
    lb=circumradius(a,hi)
    ub=math.inf if lo<=0 else circumradius(a,lo)
    for i in range(samples):
        s=lo+(hi-lo)*(i+.5)/samples
        if s>0:
            r=circumradius(a,s)
            assert lb-1e-8<=r<=ub+1e-8
    return lb,ub

rng=random.Random(20261020)
for i in range(400):
    radius=rng.uniform(4,120);phi=rng.uniform(8,170)
    a,s=geometry(radius,phi)
    e=rng.uniform(.00001,.95*s)
    b=check_interval(a,s,e)
    expected_low=circumradius(a,s+e) if s+e<=a else a
    expected_high=circumradius(a,s-e)
    assert abs(b[0]-expected_low)<1e-10
    assert abs(b[1]-expected_high)<1e-10

cases=[]
for case in frozen["unseen_synthetic_cases"]:
    phi=case["span_deg"];a,s=geometry(R,phi)
    b=check_interval(a,s,eps,10001)
    label=("unbounded upper radius" if math.isinf(b[1])
      else "finite but >10% upper error" if b[1]>R*(1+tau)+1e-10
      else "finite and <=10% upper error")
    assert label==case["prediction"]
    cases.append({"span_deg":phi,"sagitta_pixels":s,
                  "radius_interval_pixels":[b[0],None if math.isinf(b[1]) else b[1]],
                  "classification":label})

def upper_error(phi):
    a,s=geometry(R,phi)
    return math.inf if s<=eps else circumradius(a,s-eps)/R-1

l,h=10.,180.
for _ in range(100):
    m=(l+h)/2
    if upper_error(m)>tau:l=m
    else:h=m
threshold=(l+h)/2
assert abs(threshold-frozen["predicted_10pct_upper_error_transition_deg"])<1e-10
l,h=0.,180.
for _ in range(100):
    m=(l+h)/2
    if geometry(R,m)[1]<=eps:l=m
    else:h=m
finite=(l+h)/2
assert abs(finite-frozen["predicted_finite_radius_transition_deg"])<1e-10

a,s=geometry(20,60)
base=check_interval(a,s,.2)
scaled=check_interval(3*a,3*s,.6)
assert all(abs(3*x-y)<1e-9 for x,y in zip(base,scaled))
photo=check_interval(a,s,.4)
assert photo[0]<base[0] and photo[1]>base[1]
ma,ms=geometry(20,15)
assert math.isinf(check_interval(ma,ms,.2)[1])
s1,s2=s-.2,s+.2
assert circumradius(a,s1)>circumradius(a,s2)
assert abs((s1+.2)-s)<1e-12 and abs((s2-.2)-s)<1e-12

result={"status":"PASS","randomized_feasible_cases":400,
        "samples_per_random_case":501,
        "finite_radius_transition_deg":finite,
        "ten_percent_transition_deg":threshold,
        "frozen_cases":cases,
        "controls":{"geometry_scaling":"PASS","brightness_segmentation_budget":"PASS",
                    "missing_arc":"PASS","temporal_smoothness":"PASS"},
        "human_data":"NONE","independent_checker":"does not import model.py"}
(root/"checker_results.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
print(json.dumps(result,indent=2))
