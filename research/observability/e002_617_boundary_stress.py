#!/usr/bin/env python3
"""E002-617: frozen ±1-frame bilateral FC boundary uncertainty stress.

Published-human categorical labels + virtual point selection only.
No physical shutter, velocity, or anatomical-rating certification.
"""
import json
import statistics
import sys
from decimal import Decimal
from e002_616_bilateral_alias import bilateral_runs
from e002_615_timestamp_stress import paired_sources, time_nearest_samples
from e002_582_silesian5_fc import retained_indices
from e002_582_source_probe import retrieve

PHASES = 10
SOURCE_SHA256 = "a73bf84981b84f626a3cc7b3b3d1962360354740bc6cf3de5d9c92d6d380c223"
PROTOCOL_COMMIT = "cb9b1504ed541955177e446dac3fb1718a7be087"

def omitted(kept, a, b):
    return not any(x in kept for x in range(a, b + 1))

def analyze_sequence(rows, ts):
    ids = [r[0] for r in rows]
    times = [ts[x] for x in ids]
    deltas = [times[i] - times[i-1] for i in range(1, len(ids))
              if ids[i] == ids[i-1] + 1]
    if len(deltas) < 2 or any(x <= 0 for x in deltas):
        raise ValueError("INVALID_SOURCE_CADENCE")
    d = statistics.median(deltas)
    selectors = {
        "index": [retained_indices(ids[0], ids[-1], p) for p in range(PHASES)],
        "timestamp": [time_nearest_samples(ids, times, d, p) for p in range(PHASES)]
    }
    runs, exclusions = bilateral_runs(rows)
    hist = {"1":0, "2":0, "3":0, "4+":0}
    out = {key: {
        "baseline_pairs":0, "outward_robust_pairs":0,
        "outward_robust_distinct_events":0,
        "inward_surviving_baseline_pairs":0,
        "two_sided_stable_pairs":0, "two_sided_stable_distinct_events":0,
        "outward_robust_by_phase":[0]*PHASES
    } for key in selectors}
    pair_changes = 0
    for a,b in runs:
        length = b-a+1
        hist[str(length) if length <= 3 else "4+"] += 1
        flags = {}
        for key, phases in selectors.items():
            st = out[key]
            any_outward = any_stable = False
            flags[key] = []
            for p, kept in enumerate(phases):
                baseline = omitted(kept, a, b)
                outward = omitted(kept, a-1, b+1)
                survives = length >= 3
                stable = survives and outward
                if outward and not baseline:
                    raise AssertionError("OUTWARD_NOT_SUBSET_BASELINE")
                if stable and not outward:
                    raise AssertionError("STABLE_NOT_SUBSET_OUTWARD")
                st["baseline_pairs"] += int(baseline)
                st["outward_robust_pairs"] += int(outward)
                st["outward_robust_by_phase"][p] += int(outward)
                st["inward_surviving_baseline_pairs"] += int(survives and baseline)
                st["two_sided_stable_pairs"] += int(stable)
                any_outward |= outward
                any_stable |= stable
                flags[key].append(stable)
            st["outward_robust_distinct_events"] += int(any_outward)
            st["two_sided_stable_distinct_events"] += int(any_stable)
        pair_changes += sum(a != b for a,b in zip(flags["index"], flags["timestamp"]))
    if out["index"]["outward_robust_pairs"] != hist["1"]:
        raise ValueError("INDEX_OUTWARD_PHASE_LAW_FALSIFIED")
    if out["index"]["two_sided_stable_pairs"] != 0:
        raise ValueError("INDEX_TWO_SIDED_PREDICTION_FALSIFIED")
    for key in selectors:
        s = out[key]
        if not (0 <= s["two_sided_stable_pairs"] <= s["outward_robust_pairs"] <= s["baseline_pairs"]):
            raise AssertionError("MONOTONICITY")
        if sum(s["outward_robust_by_phase"]) != s["outward_robust_pairs"]:
            raise AssertionError("PHASE_SUM_MISMATCH")
    return {"eligible_bilateral_runs":len(runs), "excluded":exclusions,
            "length_histogram":hist, "erased_by_inward_trim":hist["1"]+hist["2"],
            "index":out["index"], "timestamp":out["timestamp"],
            "two_sided_selector_disagreements":pair_changes}

def analyze(data):
    results = []
    for rows, ts, status in paired_sources(data):
        if status != "ELIGIBLE":
            raise ValueError("SOURCE_TIMESTAMP_ABSTAIN:" + status)
        results.append(analyze_sequence(rows,ts))
    totals = {"eligible_bilateral_runs":sum(r["eligible_bilateral_runs"] for r in results),
              "erased_by_inward_trim":sum(r["erased_by_inward_trim"] for r in results),
              "two_sided_selector_disagreements":sum(r["two_sided_selector_disagreements"] for r in results),
              "length_histogram":{k:sum(r["length_histogram"][k] for r in results)
                                  for k in ("1","2","3","4+")}}
    for selector in ("index","timestamp"):
        totals[selector] = {}
        for k in ("baseline_pairs","outward_robust_pairs",
                  "outward_robust_distinct_events",
                  "inward_surviving_baseline_pairs",
                  "two_sided_stable_pairs","two_sided_stable_distinct_events"):
            totals[selector][k] = sum(r[selector][k] for r in results)
        totals[selector]["outward_robust_by_phase"] = [
            sum(r[selector]["outward_robust_by_phase"][p] for r in results)
            for p in range(PHASES)]
    if totals["eligible_bilateral_runs"] != 279:
        raise ValueError("E002_616_BASELINE_COUNT_CHANGED")
    if totals["length_histogram"] != {"1":4,"2":14,"3":21,"4+":240}:
        raise ValueError("E002_616_LENGTH_HISTOGRAM_CHANGED")
    if totals["index"]["baseline_pairs"] != 105 or totals["timestamp"]["baseline_pairs"] != 105:
        raise ValueError("E002_616_BASELINE_PAIRS_CHANGED")
    return {"experiment":"E002-617", "protocol_commit":PROTOCOL_COMMIT,
            "source_archive_sha256":SOURCE_SHA256,
            "evidence":"PUBLISHED_HUMAN_CATEGORICAL_BOUNDARY_UNCERTAINTY_STRESS",
            "hypothetical_frame_boundary_uncertainty":1,
            "source_sequences":len(results),"per_sequence":results,"totals":totals,
            "physical_shutter_validated":False,"velocity_ceiling_validated":False,
            "independent_anatomical_raters":0,
            "product":"ABSTAIN_UNCALIBRATED","release":"BLOCKED"}

def self_test():
    def mk(i,l="X",r="X",nf="X",lnv="X",rnv="X"):
        return (i,nf,l,lnv,r,rnv)
    rows=[mk(i) for i in range(80)]
    rows[20]=mk(20,"C","C")
    for i in range(40,43): rows[i]=mk(i,"C","C")
    ts={i:Decimal(i)*10 for i in range(80)}
    result=analyze_sequence(rows,ts)
    assert result["eligible_bilateral_runs"]==2
    assert result["erased_by_inward_trim"]==1
    assert result["index"]["baseline_pairs"]==8
    assert result["index"]["outward_robust_pairs"]==1
    assert result["index"]["inward_surviving_baseline_pairs"]==1
    assert result["index"]["two_sided_stable_pairs"]==0
    jitter=ts.copy()
    jitter[20]+=Decimal(2)
    jittered=analyze_sequence(rows,jitter)
    assert jittered["eligible_bilateral_runs"]==2
    bad=rows[:]
    bad[20]=mk(20,"C","C","N")
    assert analyze_sequence(bad,ts)["eligible_bilateral_runs"]==1
    missing=[r for r in rows if r[0]!=19]
    assert analyze_sequence(missing,ts)["eligible_bilateral_runs"]==1
    assert omitted({0,1,2},4,5) and not omitted({0,1,2},2,5)
    print(json.dumps({"experiment":"E002-617","synthetic_self_test":"PASS","groups":6},
                     sort_keys=True))

if __name__=="__main__":
    self_test()
    if "--source" in sys.argv:
        print(json.dumps(analyze(retrieve()),sort_keys=True))
