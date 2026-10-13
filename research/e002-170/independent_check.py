#!/usr/bin/env python3
"""Independent reimplementation of E002-170 event-window arithmetic."""
import json, math, pathlib, statistics
P=pathlib.Path(__file__).resolve().parent
r=json.loads((P/"RESULTS.json").read_text())
m=json.loads((P/"SOURCE_MANIFEST.json").read_text())
checks={"source_url_consistent": m["source_url"]=="https://www.blinkingmatters.com/files/upload/research/eyeblink8.zip",
        "frame_window_frozen":m["frame_window"]==150}
if r["status"]=="EVALUABLE":
    counts=[]
    pred_num=0.
    for name,v in r["videos"].items():
        starts=v["blink_onsets"]
        c=[]
        for w in v["windows"]:
            recomputed=sum(1 for onset in starts if w["start"]<=onset<w["end_exclusive"])
            assert recomputed==w["count"], (name,w)
            assert w["end_exclusive"]-w["start"]==150
            c.append(recomputed)
        mu=sum(c)/len(c) if c else None
        if mu is not None:
            assert math.isclose(mu,v["mean_count"],abs_tol=1e-12)
            var=sum((x-mu)**2 for x in c)/len(c)
            assert math.isclose(var,v["population_variance"],abs_tol=1e-12)
            assert math.isclose(c.count(0)/len(c),v["zero_fraction"],abs_tol=1e-12)
            pred_num+=len(c)*math.exp(-mu)
        counts.extend(c)
    pooled=r["pooled"]
    checks["all_window_counts_independently_recomputed"]=True
    checks["pooled_count_consistent"]=len(counts)==pooled["eligible_windows"]
    checks["pooled_zero_fraction_consistent"]=math.isclose(
        counts.count(0)/len(counts),pooled["observed_zero_fraction"],abs_tol=1e-12)
    checks["poisson_zero_prediction_consistent"]=math.isclose(
        pred_num/len(counts),pooled["poisson_predicted_zero_fraction"],abs_tol=1e-12)
else:
    checks["negative_gate_preserved"]=r["status"] in ("BLOCKED_DATA_ACCESS","NOT_EVALUABLE")
    checks["failure_not_misrepresented_as_scientific_falsification"]=r["scientific_gate"]=="NOT_RUN"
ok=all(checks.values())
(P/"INDEPENDENT_CHECK.json").write_text(json.dumps({"passed":ok,"checks":checks},indent=2,sort_keys=True)+"\n")
print(json.dumps({"passed":ok,"checks":checks},indent=2))
if not ok: raise SystemExit(1)
