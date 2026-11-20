"""E002-371 prospective reference-video evaluation. No human data bundled.

Input CSV columns:
participant_id,split,mean0_lower_mm,mean1_lower_mm,exposure0_upper_s,
exposure1_upper_s,gap_upper_s,velocity_upper_mm_s,threshold_mm,
reference_min_aperture_upper_mm,reference_adjudicable,calibration_authenticated,
linear_exposure_verified,timing_verified,geometry_verified

The reference minimum UPPER bound <= threshold establishes a closure;
a lower bound is insufficient. Uncertain reference labels are excluded
from the safety denominator and reported separately. Velocity bounds
must originate outside the confirmatory participant/session.
"""
import csv, json, sys
from decimal import Decimal, InvalidOperation
from collections import Counter

REQUIRED = ("participant_id split mean0_lower_mm mean1_lower_mm "
            "exposure0_upper_s exposure1_upper_s gap_upper_s "
            "velocity_upper_mm_s threshold_mm reference_min_aperture_upper_mm "
            "reference_adjudicable calibration_authenticated "
            "linear_exposure_verified timing_verified geometry_verified").split()
FLAGS = ("calibration_authenticated", "linear_exposure_verified",
         "timing_verified", "geometry_verified")
def number(row, name):
    v = Decimal(row[name])
    if not v.is_finite() or v < 0: raise ValueError(name)
    return v

def evaluate(rows):
    stats=Counter()
    participants=set()
    for row in rows:
        stats["total"]+=1
        if any(k not in row for k in REQUIRED): raise ValueError("missing columns")
        if row["split"] != "holdout":
            stats["non_holdout"]+=1
            continue
        participants.add(row["participant_id"])
        try:
            m0=number(row,"mean0_lower_mm"); m1=number(row,"mean1_lower_mm")
            e0=number(row,"exposure0_upper_s"); e1=number(row,"exposure1_upper_s")
            g=number(row,"gap_upper_s"); v=number(row,"velocity_upper_mm_s")
            c=number(row,"threshold_mm")
            ref=number(row,"reference_min_aperture_upper_mm")
        except (ValueError,InvalidOperation,KeyError):
            stats["invalid"]+=1
            continue
        adjudicable=row["reference_adjudicable"]=="1"
        if not adjudicable: stats["reference_uncertain"]+=1
        closure=adjudicable and ref<=c
        if closure: stats["reference_closures"]+=1
        if any(row[k]!="1" for k in FLAGS):
            stats["abstain_provenance"]+=1
            continue
        edge0=m0-v*e0/2
        edge1=m1-v*e1/2
        exclude=(edge0>c and edge1>c and
                 (edge0-c)+(edge1-c)>v*g)
        if exclude:
            stats["mathematical_exclusions"]+=1
            if not adjudicable: stats["exclusions_without_reference"]+=1
            elif closure: stats["false_exclusions"]+=1
        else: stats["not_excluded"]+=1
    stats["holdout_participants"]=len(participants)
    stats["safety_adjudication_incomplete"]=bool(stats["exclusions_without_reference"])
    # Not a population-level risk estimate. For zero failures in n
    # independently sampled closure opportunities, one-sided 95% bound
    # is 1 - 0.05**(1/n); clustered participants invalidate this shortcut.
    stats["independence_warning"]="Within-participant clustering: no binomial CI reported"
    return dict(stats)

if __name__=="__main__":
    if len(sys.argv)!=2: raise SystemExit("usage: python e002_371_reference_evaluator.py heldout.csv")
    with open(sys.argv[1],newline="",encoding="utf-8") as f:
        result=evaluate(csv.DictReader(f))
    print(json.dumps(result,sort_keys=True,indent=2))
    if result.get("false_exclusions",0): raise SystemExit(2)
