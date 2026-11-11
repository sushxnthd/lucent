#!/usr/bin/env python3
"""E002-747: frozen-label prospective certificate scorer; stdlib only.

Input CSV columns: participant,condition,lower0,lower1,velocity_ceiling,
gap_upper,truth. truth is CLOSED, OPEN, or UNCERTAIN.
Outputs aggregate only; never prints participant IDs.
"""
import argparse, csv, json, math
from collections import defaultdict

REQUIRED = ("participant","condition","lower0","lower1","velocity_ceiling","gap_upper","truth")

def score(rows):
    seen=set(); groups=defaultdict(lambda: {"total":0,"excluded":0,"false_exclusions":0,"uncertain":0,"abstained":0})
    for index,row in enumerate(rows,1):
        if not all(k in row for k in REQUIRED): raise ValueError("missing required column")
        identity=(row["participant"],row["condition"],row.get("interval_id",str(index)))
        if identity in seen: raise ValueError("duplicate interval")
        seen.add(identity)
        truth=row["truth"].upper()
        if truth not in ("CLOSED","OPEN","UNCERTAIN"): raise ValueError("invalid truth")
        vals=[float(row[k]) for k in ("lower0","lower1","velocity_ceiling","gap_upper")]
        if not all(math.isfinite(x) and x>=0 for x in vals): raise ValueError("nonfinite or negative measurement")
        l0,l1,v,d=vals
        # A physical timing interval of zero needs a separate point-observation model.
        exclude = d>0 and v>0 and l0+l1>v*d
        for name in ("ALL",) if row["condition"]=="ALL" else ("ALL",row["condition"]):
            g=groups[name];g["total"]+=1
            if truth=="UNCERTAIN": g["uncertain"]+=1
            if exclude:
                g["excluded"]+=1
                if truth=="CLOSED":g["false_exclusions"]+=1
            else:g["abstained"]+=1
    out={}
    for name,g in sorted(groups.items()):
        # Error denominator is *adjudicated EXCLUDE decisions*, not number of closures.
        # Uncertain exclusions cannot be silently counted as correct.
        out[name]=dict(g)
    return out

def evaluate(rows):
    buckets=defaultdict(list)
    for r in rows:
        buckets["ALL"].append(r)
        if r["condition"] != "ALL": buckets[r["condition"]].append(r)
    result={}
    for name,subset in buckets.items():
        g=score(subset)["ALL"]
        uncertain_exclusions=sum(
            1 for r in subset
            if r["truth"].upper()=="UNCERTAIN" and
            float(r["gap_upper"])>0 and float(r["velocity_ceiling"])>0 and
            float(r["lower0"])+float(r["lower1"])>float(r["velocity_ceiling"])*float(r["gap_upper"])
        )
        n=g["excluded"]-uncertain_exclusions
        k=g["false_exclusions"]
        # For k=0, exact one-sided upper 95% bound. Other counts: no misleading interval.
        result[name]={**g,"adjudicated_exclusions":n,"uncertain_exclusions":uncertain_exclusions,
                      "false_exclusion_rate":k/n if n else None,
                      "zero_error_upper_95_one_sided":1-0.05**(1/n) if n and k==0 else None,
                      "release_blocked":bool(k or uncertain_exclusions or not n)}
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument("csv_path");a=p.parse_args()
    with open(a.csv_path,newline="",encoding="utf-8") as f: rows=list(csv.DictReader(f))
    print(json.dumps(evaluate(rows),indent=2,sort_keys=True))
if __name__=="__main__":main()
