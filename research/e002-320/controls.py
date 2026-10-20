"""Synthetic nuisance controls: expected failures, not real-camera robustness."""
from fractions import Fraction as F
import json,math
from pathlib import Path
P=F(1,30);E=F(1,100);d=F(1,25)
G=P-E;dropped=2*P-E
s=E+(dropped-d)/2
def ov(s,d,l,r): return max(F(0),min(s+d,r)-max(s,l))
assert G<d<dropped
assert ov(s,d,F(0),E)==0 and ov(s,d,2*P,2*P+E)==0
def bump(x,mid,radius):
    u=(x-mid)/radius
    return math.exp(-1/(1-u*u)) if abs(u)<1 else 0.
mid=float(E+P)/2
radius=float(P-E)*.45
assert bump(mid,mid,radius)>0
assert bump(float(E),mid,radius)==0 and bump(float(P),mid,radius)==0
out={
 "geometry_only":{"anatomical_event":False,"apparent_event":0.30,"error_budget":0.05,"gate":"FAIL: geometry residual exceeds error budget"},
 "brightness_only":{"anatomical_event":False,"apparent_event":0.25,"gate":"FAIL: unconstrained gain/bias mimics closure"},
 "missingness_only":{"nominal_gap_ms":float(G*1000),"dropped_gap_ms":float(dropped*1000),"invisible_event_ms":float(d*1000),"gate":"EXACT_COLLISION"},
 "smoothness_only":{"gate":"FAIL","counterexample":"C-infinity positive bump supported entirely inside shutter gap"}
}
Path(__file__).with_name("controls_results.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
