#!/usr/bin/env python3
"""E002-264: exact one-chord projective ambiguity. Synthetic/algebraic, not human data."""
from fractions import Fraction as F
from math import sqrt
from pathlib import Path
import json, hashlib

R0=F(7,20)
T=F(1,4)

def h(x,t): return (x+t)/(1+t*x)
def cross_ratio(a,b,c,d): return ((b-a)*(d-c))/((c-a)*(d-b))
def q_rd(r,d):
    assert 0<r<1 and abs(d)+r<1
    return ((1-r)**2-d*d)/((1+r)**2-d*d)
def r_centered(q): return (1-sqrt(q))/(1+sqrt(q))
def r_min(q,D):
    assert 0<q<1 and 0<=D<1
    A=(1+q)/(1-q)
    return (1-D*D)/(A+sqrt(A*A-1+D*D))
def r_dec_from_projectivity(r,t):
    return (r*(1-t*t)/(1-t*t*r*r),t*(1-r*r)/(1-t*t*r*r))

# Exact rational counterexample: different true radii, identical image quadruple.
a,b,c,z=(h(x,T) for x in (-F(1),-R0,R0,F(1)))
r1,d1=r_dec_from_projectivity(R0,T)
assert (a,z)==(-1,1)
assert b==d1-r1 and c==d1+r1
assert r1!=R0 and d1!=0
assert cross_ratio(a,b,c,z)==q_rd(R0,F(0))==q_rd(r1,d1)
assert cross_ratio(a,b,c,z)==((1-R0)/(1+R0))**2

q=float(q_rd(R0,F(0)))
Ds=[0,.05,.10,.20,.30,.50]
rows=[]
for D in Ds:
    lo=r_min(q,D)
    # The observed cross ratio has the same value at both interval endpoints.
    assert abs(q_rd(lo,D)-q)<1e-12
    assert lo<=float(R0)+1e-12
    rows.append(dict(max_decentration_over_iris_radius=D,
                     true_radius_lower=round(lo,12),true_radius_upper=float(R0),
                     maximal_relative_overstatement_percent=round(100*(float(R0)-lo)/float(R0),6)))

# Wildcard: varying physical pupil radius plus co-varying decentration can yield a flat cross-ratio.
# This is an admissible synthetic trajectory, not a claim about actual eye dynamics.
trajectory=[]
for D in [0,.04,.08,.12,.16,.20]:
    r=r_min(q,D)
    trajectory.append(dict(decentration=round(D,4),true_radius=round(r,9),
                           measured_centered_radius=round(r_centered(q),9),
                           cross_ratio=round(q_rd(r,D),12)))

out={"run":"E002-264","data_type":"exact algebra and deterministic synthetic examples only",
     "human_data_evaluated":False,"source_parent":"E002-263",
     "formula_q":"((1-r)^2-d^2)/((1+r)^2-d^2)",
     "centered_inversion_upper_bound":float(R0),"q":round(q,15),
     "exact_counterexample":{
       "perspective_parameter":str(T),"interpretation_A_radius":str(R0),
       "interpretation_A_decentration":"0","interpretation_B_radius":str(r1),
       "interpretation_B_decentration":str(d1),
       "identical_image_quadruple":[str(x) for x in (a,b,c,z)],
       "exact_cross_ratio":str(cross_ratio(a,b,c,z))},
     "identified_intervals":rows,"wildcard_constant_q_varying_radius":trajectory,
     "failure_gate":"single-chord cross ratio cannot identify radius without a decentration bound",
     "product_gate":"reject quantitative radius claim if independent decentration bound unavailable"}
path=Path(__file__).with_name('RESULTS.json')
path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({"q":q,"exact_example":out['exact_counterexample'],"rows":rows,"wildcard":trajectory},indent=2))
