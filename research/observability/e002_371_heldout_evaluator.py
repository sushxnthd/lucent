#!/usr/bin/env python3
"""E002-371 preregistered held-out CSV evaluator. Not evidence without real input.

CSV columns: subject_id,split,sequence_id,left_low_mm,left_high_mm,
right_low_mm,right_high_mm,closure_threshold_low_mm,closure_threshold_high_mm,
gap_low_s,gap_high_s,velocity_ceiling_low_mm_s,velocity_ceiling_high_mm_s,
reference_hidden_closure,reference_quality_ok
One row per independently synchronized ordinary-camera gap. velocity ceilings
must be independently certified (not maxima from the held-out sequence).
Reference labels must be from high-frame-rate adjudication, not interpolation.
"""
import argparse
import csv
import json
from collections import Counter

FIELDS = ("left_low_mm left_high_mm right_low_mm right_high_mm "
          "closure_threshold_low_mm closure_threshold_high_mm gap_low_s gap_high_s "
          "velocity_ceiling_low_mm_s velocity_ceiling_high_mm_s").split()

def classify(r):
    try:
        a,b,c,d,e,f,t0,t1,v0,v1 = (float(r[k]) for k in FIELDS)
    except (KeyError,ValueError) as exc:
        return "INVALID",str(exc)
    if not (0<=a<=b and 0<=c<=d and 0<=e<=f and
            0<t0<=t1 and 0<v0<=v1):
        return "INVALID","invalid intervals or nonpositive gap/speed"
    if a<=f or c<=f:
        return "ABSTAIN","endpoint could already be closed"
    # If ANY nuisance-compatible endpoint pair is inconsistent with the
    # assumed speed model, model applicability is not established.
    if max(abs(a-d),abs(b-c)) > v0*t0:
        return "ABSTAIN","endpoint compatibility not certified"
    if (a-f)+(c-f)>v1*t1:
        return "EXCLUDE","closure unreachable for all admissible parameters"
    return "ABSTAIN","hidden closure remains possible"

def evaluate(rows):
    counts=Counter()
    false_exclusions=[]
    subjects={}
    for n,r in enumerate(rows,2):
        key=(r.get("subject_id"),r.get("split"))
        if not all(key) or r.get("split") not in ("calibration","heldout"):
            raise ValueError(f"line {n}: missing subject or invalid split")
        if key[0] in subjects and subjects[key[0]]!=key[1]:
            raise ValueError(f"line {n}: subject leakage across splits")
        subjects[key[0]]=key[1]
        if r.get("split")!="heldout": continue
        verdict,reason=classify(r)
        counts[verdict]+=1
        if verdict=="INVALID": raise ValueError(f"line {n}: {reason}")
        if r.get("reference_quality_ok")!="1":
            counts["UNADJUDICATED"]+=1
            continue
        label=r.get("reference_hidden_closure")
        if label not in ("0","1"): raise ValueError(f"line {n}: invalid reference label")
        if verdict=="EXCLUDE" and label=="1":
            false_exclusions.append({"line":n,"sequence_id":r.get("sequence_id")})
    return {"tier":"held-out evaluation; validity depends on independently verified inputs",
            "heldout_decisions":dict(counts),"false_exclusions":false_exclusions,
            "release_gate":"FAIL" if false_exclusions else "NOT_VALIDATED_BY_ZERO_ERRORS",
            "limitations":"Zero observed failures is not a certified physiological speed bound; adjudication and calibration provenance require external audit."}

def selftest():
    base=dict(zip(FIELDS,["2","2","2","2","0","0","0.01","0.01","100","100"]))
    assert classify(base)[0]=="EXCLUDE"
    base["gap_high_s"]="0.04"
    assert classify(base)[0]=="ABSTAIN"
    base["gap_high_s"]="0.01"
    base["left_low_mm"]="-1"
    assert classify(base)[0]=="INVALID"
    row=dict(zip(FIELDS,["2","2","2","2","0","0","0.01","0.01","100","100"]))
    row.update(subject_id="A",split="heldout",sequence_id="s1",
               reference_hidden_closure="1",reference_quality_ok="1")
    assert len(evaluate([row])["false_exclusions"])==1
    assert evaluate([dict(row,reference_hidden_closure="0")])["release_gate"]=="NOT_VALIDATED_BY_ZERO_ERRORS"
    try: evaluate([row,dict(row,split="calibration")])
    except ValueError: pass
    else: raise AssertionError("subject leakage undetected")
    print("PASS: 6 protocol checks (synthetic fixtures, not human validation)")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--csv",help="preregistered, independently acquired gap table")
    a=p.parse_args()
    if not a.csv: selftest()
    else:
        with open(a.csv,newline="",encoding="utf-8") as f:
            print(json.dumps(evaluate(csv.DictReader(f)),indent=2))
