#!/usr/bin/env python3
"""Independent verification of frozen E002-264 exact and numeric outputs."""
import json
from fractions import Fraction as Q
from pathlib import Path
from math import isclose
o=json.loads(Path(__file__).with_name("RESULTS.json").read_text())
v=o["exact_counterexample"]
a,b,c,d=[Q(x) for x in v["identical_image_quadruple"]]
q=(b-a)*(d-c)/((c-a)*(d-b))
r0=Q(v["interpretation_A_radius"])
r1=Q(v["interpretation_B_radius"])
shift=Q(v["interpretation_B_decentration"])
assert q==Q(v["exact_cross_ratio"])
assert q==((1-r0)/(1+r0))**2
assert q==((1-r1)**2-shift**2)/((1+r1)**2-shift**2)
assert 0<r1<r0 and 0<shift<1-r1
for row in o["identified_intervals"]:
    L=row["true_radius_lower"]
    U=row["true_radius_upper"]
    D=row["max_decentration_over_iris_radius"]
    assert L<=U
    assert isclose(((1-L)**2-D**2)/((1+L)**2-D**2),float(q),abs_tol=2e-10)
assert len({x["true_radius"] for x in o["wildcard_constant_q_varying_radius"]})>1
assert len({x["cross_ratio"] for x in o["wildcard_constant_q_varying_radius"]})==1
assert q!=((1-Q(1,2))**2-shift**2)/((1+Q(1,2))**2-shift**2)
print("E002-264 independent checker passed")
