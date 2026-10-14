#!/usr/bin/env python3
"""Independent count/gate checker; cannot validate physiological RGB."""
import json,sys
r=json.load(open(sys.argv[1] if len(sys.argv)>1 else "research/e002-176/results/RESULTS.json"))
assert r["run"]=="E002-176" and r["source_md5"]=="5e04a7b5e50f7508775e1daea527246b"
p=list(r["participants"].values());s=r["summary"];w=[x for a in p for x in a["windows"]]
assert len(p)==s["participants_parsed"]
assert len(w)==s["accepted_windows"]
assert sum(a["total_windows"] for a in p)==s["total_windows"]
if w:
 assert abs(sum(x["pass"] for x in w)/len(w)-s["pass_fraction"])<1e-12
 for x in w:
  assert len(x["r_phases"])==4 and abs(min(x["r_phases"])-x["worst_r"])<1e-12
  assert x["pass"]==(x["worst_r"]>=.90)
  assert 0<=x["low5_power_fraction"]<=1.00000001
assert s["physiological_rgb_gate"]=="NOT_TESTED" and s["primary_paired_data_gate"]=="NOT_TESTED"
print("PASS independent structure/gates; windows",len(w),"participants",len(p))
