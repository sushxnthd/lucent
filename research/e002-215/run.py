#!/usr/bin/env python3
"""E002-215: source-pinned, calibration-aware NRMSE lower-bound audit.
No human raw video; no temporal waveform certification; stdlib only.
"""
import csv, hashlib, json, math, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
SRC=ROOT.parent/"e002-214"/"DERIVED_PARTICIPANT.csv"
EXPECTED="7c0e15e5ca1155d3dd0acd0915fcb699487694db"
def rows():
    raw=SRC.read_bytes()
    digest=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\\0"+raw).hexdigest()
    if digest!=EXPECTED: raise RuntimeError("SOURCE_HASH_MISMATCH "+digest)
    with SRC.open(newline="") as f: out=[{k:float(v) for k,v in row.items()} for row in csv.DictReader(f)]
    if len(out)!=51 or len({r["participant"] for r in out})!=51: raise RuntimeError("COHORT_INTEGRITY")
    return out
def nrmse(r,a,g=1.0):
    return math.sqrt(max(0.,1.+(g*a)**2-2*g*a*r))
def oracle(r):
    return math.sqrt(max(0.,1.-max(0.,r["left_r"],r["right_r"])**2))
def pass_ids(data,g):
    return [int(r["participant"]) for r in data if any(
        r[e+"_r"]>=.7 and .75-1e-12<=g*r[e+"_amp_ratio"]<=1.25+1e-12
        for e in ("left","right"))]
def compute(data):
    thresholds=(.25,.35,.5,.6,.7,.75,.8,1.)
    frontier=[dict(nrmse_threshold=t,
        positive_affine_oracle_count=sum(oracle(r)<=t+1e-12 for r in data),
        original_gain_offset_only_count=sum(min(nrmse(r["left_r"],r["left_amp_ratio"]),nrmse(r["right_r"],r["right_amp_ratio"]))<=t+1e-12 for r in data))
        for t in thresholds]
    gains=[1.]
    for r in data:
        for e in ("left","right"):
            if r[e+"_r"]>=.7:
                gains.extend((.75/r[e+"_amp_ratio"],1.25/r[e+"_amp_ratio"]))
    best=(-1,0.,[])
    for g in gains:
        ids=pass_ids(data,g)
        if len(ids)>best[0]: best=(len(ids),g,ids)
    return dict(frontier=frontier,posthoc_global_gain_r07_amp075_125=dict(count=best[0],gain=best[1],participants=best[2]),
       original_gain_r07_amp075_125=len(pass_ids(data,1.)),
       correlation_only_r07_oracle=sum(max(r["left_r"],r["right_r"])>=.7 for r in data),
       oracle_positive_affine_nrmse_min=min(map(oracle,data)),
       per_participant=[dict(participant=int(r["participant"]),positive_affine_oracle_nrmse=oracle(r),
           original_gain_offset_only_best_eye_nrmse=min(nrmse(r["left_r"],r["left_amp_ratio"]),nrmse(r["right_r"],r["right_amp_ratio"]))) for r in data])
if __name__=="__main__":
    print(json.dumps(compute(rows()),indent=2,sort_keys=True))
