#!/usr/bin/env python3
"""E002-616: frozen bilateral FC human-source virtual alias test; aggregate-only."""
import json
import sys
import statistics
from e002_615_timestamp_stress import paired_sources, time_nearest_samples
from e002_582_silesian5_fc import retained_indices
from e002_582_source_probe import retrieve
from decimal import Decimal

N_PHASE = 10

def bilateral_runs(rows):
    runs = []
    reasons = {"boundary":0, "missing_index":0, "nuisance":0}
    i = 0
    while i < len(rows):
        if rows[i][2] != "C" or rows[i][4] != "C":
            i += 1
            continue
        a = i
        while (i+1 < len(rows) and rows[i+1][0] == rows[i][0]+1
               and rows[i+1][2] == "C" and rows[i+1][4] == "C"):
            i += 1
        b = i
        if a == 0 or b == len(rows)-1:
            reasons["boundary"] += 1
        else:
            seg = rows[a-1:b+2]
            if any(seg[k+1][0] != seg[k][0]+1 for k in range(len(seg)-1)):
                reasons["missing_index"] += 1
            elif any(r[1] == "N" or r[3] == "N" or r[5] == "N" for r in seg):
                reasons["nuisance"] += 1
            else:
                runs.append((rows[a][0], rows[b][0]))
        i += 1
    return runs, reasons

def analyze_sequence(rows, ts):
    ids = [r[0] for r in rows]
    times = [ts[x] for x in ids]
    intervals = [times[i]-times[i-1] for i in range(1,len(ids))
                 if ids[i] == ids[i-1]+1]
    if len(intervals) < 2:
        raise ValueError("INSUFFICIENT_TIMING")
    d = statistics.median(intervals)
    if d <= 0:
        raise ValueError("INVALID_CADENCE")
    index = [retained_indices(ids[0],ids[-1],p) for p in range(N_PHASE)]
    actual = [time_nearest_samples(ids,times,d,p) for p in range(N_PHASE)]
    runs, reasons = bilateral_runs(rows)
    per_index = [0]*N_PHASE
    per_actual = [0]*N_PHASE
    any_index = any_actual = changed = both = long_omitted = checked = 0
    hist = {"1":0,"2":0,"3":0,"4+":0}
    for a,b in runs:
        length = b-a+1
        hist[str(length) if length <= 3 else "4+"] += 1
        mi,ma = [],[]
        for p in range(N_PHASE):
            xi = not any(x in index[p] for x in range(a,b+1))
            xa = not any(x in actual[p] for x in range(a,b+1))
            mi.append(xi)
            ma.append(xa)
            per_index[p] += int(xi)
            per_actual[p] += int(xa)
            changed += int(xi != xa)
            both += int(xi and xa)
            long_omitted += int(length >= 4 and (xi or xa))
        any_index += int(any(mi))
        any_actual += int(any(ma))
        if a >= ids[0]+10 and b <= ids[-1]-10:
            checked += 1
            expected = {1:7,2:4,3:1}.get(length,0)
            if sum(mi) != expected:
                raise ValueError("EXACT_INDEX_PHASE_LAW_FALSIFIED")
    return {"eligible_bilateral_runs":len(runs),"excluded":reasons,
            "length_histogram":hist,"index_omissions_by_phase":per_index,
            "actual_omissions_by_phase":per_actual,
            "index_any_phase":any_index,"actual_any_phase":any_actual,
            "paired_event_phase_changes":changed,
            "jointly_omitted_event_phase_pairs":both,
            "long_run_omission_event_phase_pairs":long_omitted,
            "interior_phase_law_checked":checked}

def analyze(data):
    out = []
    for rows,ts,status in paired_sources(data):
        if status != "ELIGIBLE":
            raise ValueError("SOURCE_TIMESTAMP_ABSTAIN:"+status)
        out.append(analyze_sequence(rows,ts))
    total = lambda k:sum(x[k] for x in out)
    keys = ("eligible_bilateral_runs","index_any_phase","actual_any_phase",
            "paired_event_phase_changes","jointly_omitted_event_phase_pairs",
            "long_run_omission_event_phase_pairs","interior_phase_law_checked")
    totals = {k:total(k) for k in keys}
    totals["index_omissions_by_phase"] = [
        sum(x["index_omissions_by_phase"][p] for x in out) for p in range(N_PHASE)]
    totals["actual_omissions_by_phase"] = [
        sum(x["actual_omissions_by_phase"][p] for x in out) for p in range(N_PHASE)]
    totals["length_histogram"] = {k:sum(x["length_histogram"][k] for x in out)
                                   for k in ("1","2","3","4+")}
    if sum(totals["length_histogram"].values()) != totals["eligible_bilateral_runs"]:
        raise AssertionError("HISTOGRAM_MISMATCH")
    # Preserve any long-run timestamp-selector surprise as a measured falsifier.
    h = totals["length_histogram"]
    if sum(totals["index_omissions_by_phase"]) != 7*h["1"]+4*h["2"]+h["3"]:
        raise ValueError("FROZEN_PHASE_LAW_TOTAL_FALSIFIED")
    return {"experiment":"E002-616",
            "evidence":"PUBLISHED_HUMAN_BILATERAL_FC_LABEL_VIRTUAL_POINT_SAMPLING",
            "source_archive_sha256":"a73bf84981b84f626a3cc7b3b3d1962360354740bc6cf3de5d9c92d6d380c223",
            "source_sequences":len(out),"totals":totals,"per_sequence":out,
            "physical_shutter_validated":False,"hard_velocity_ceiling_validated":False,
            "independent_anatomical_raters":0,
            "product":"ABSTAIN_UNCALIBRATED","release":"BLOCKED"}

def self_test():
    mk = lambda i,l="X",r="X",nf="X",lnv="X",rnv="X":(i,nf,l,lnv,r,rnv)
    rows = [mk(i) for i in range(30)]
    for i in (10,11,12): rows[i] = mk(i,"C","C")
    runs,reasons = bilateral_runs(rows)
    assert runs == [(10,12)] and sum(reasons.values()) == 0
    times = {i:Decimal(i)*10 for i in range(30)}
    z = analyze_sequence(rows,times)
    assert z["eligible_bilateral_runs"] == 1 and z["length_histogram"]["3"] == 1
    assert sum(z["index_omissions_by_phase"]) == 1
    assert z["interior_phase_law_checked"] == 1
    assert z["long_run_omission_event_phase_pairs"] == 0
    one = rows[:]; one[11] = mk(11,"C","X")
    assert bilateral_runs(one)[0] == [(10,10),(12,12)]
    nuisance = rows[:]; nuisance[11] = mk(11,"C","C","N")
    rr,why = bilateral_runs(nuisance)
    assert rr == [] and why["nuisance"] == 1
    boundary = rows[:]; boundary[0] = mk(0,"C","C")
    assert bilateral_runs(boundary)[1]["boundary"] == 1
    missing = [r for r in rows if r[0] != 11]
    rr,why = bilateral_runs(missing)
    assert rr == [] and why["missing_index"] == 2
    print(json.dumps({"experiment":"E002-616","synthetic_self_test":"PASS",
                      "test_groups":6}))

if __name__ == "__main__":
    self_test()
    if "--source" in sys.argv:
        print(json.dumps(analyze(retrieve()),sort_keys=True))
