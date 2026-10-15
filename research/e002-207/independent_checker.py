#!/usr/bin/env python3
"""Independent recomputation of source metadata counts and all participant denominators."""
import csv,hashlib,json,math
from collections import defaultdict
from pathlib import Path
P=Path(__file__).resolve().parent
raw=(P/"source_data_loss_per_trial.csv").read_bytes()
o=json.loads((P/"results/FRONTIER.json").read_text())
assert hashlib.md5(raw).hexdigest()=="369d9446b62fd00888a6d51e152697bd"
assert hashlib.sha256(raw).hexdigest()==o["source"]["sha256"]
assert len(raw)==o["source"]["bytes"]
with (P/"source_data_loss_per_trial.csv").open(encoding="utf-8-sig",newline="") as f:
    rows=list(csv.DictReader(f))
assert len(rows)==o["n_source_rows"]
groups=defaultdict(list)
for r in rows:
    groups[r["pid"]].append((r["trial"],r["eye"].lower(),
      int(r["n_trial_samples"]),int(r["n_valid_trial_samples"])))
assert len(groups)==15
assert {p["pid"] for p in o["participants"]}==set(groups)
assert len(o["participants"])==15
total=0; possible=0
for person in o["participants"]:
    group=groups[person["pid"]]
    names={x[0] for x in group};total+=len(names)
    assert person["n_trials"]==len(names)
    eligibility=defaultdict(set)
    for trial,eye,n,v in group:
        if n>=600 and v>=570:eligibility[trial].add(eye)
    assert person["left_candidate_trials"]==sum("left" in s for s in eligibility.values())
    assert person["right_candidate_trials"]==sum("right" in s for s in eligibility.values())
    assert person["either_candidate_trials"]==len(eligibility)
    assert person["both_candidate_trials"]==sum(len(s)==2 for s in eligibility.values())
    chosen=person["first_candidate"]
    if eligibility:
        assert chosen and chosen["trial"] in eligibility
        assert chosen["eye"] in eligibility[chosen["trial"]]
        if "left" in eligibility[chosen["trial"]]:assert chosen["eye"]=="left"
        possible+=1
    else:assert chosen is None
assert total==o["n_complete_trials"]
s=o["summary"]
assert s["n_participants"]==15 and s["needed"]==math.ceil(0.75*15)
assert s["possible_participants"]==possible and s["impossible_participants"]==15-possible
assert abs(s["ceiling"]-possible/15)<1e-12
assert s["marginal_feasible"]==(possible>=12)
assert o["rgb_waveform"]=="NOT_TESTED" and o["actual_window_admission"]=="NOT_MEASURED"
print("PASS independent source hashes, participant denominators, and marginal eligibility")
