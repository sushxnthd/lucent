#!/usr/bin/env python3
"""E002-389: conservative continuous-time observability via exposure-integral LP."""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

V, THETA, H = 60.0, 0.2, 0.001
TIMES = np.linspace(0, 0.100, 101)
EXPOSURES = [(0.010, 0.030), (0.040, 0.060), (0.070, 0.090)]
TARGET = np.arange(20, 81)
DELTA = V * H / 2


def weights(l, r):
    i, j = round(l/H), round(r/H)
    w = np.zeros(101)
    w[i], w[j] = H/(2*(r-l)), H/(2*(r-l))
    w[i+1:j] = H/(r-l)
    assert abs(w.sum()-1) < 1e-12
    return w


def optimize(ids, means, err, continuum=True):
    tol = err + (DELTA if continuum else 0)
    W = np.array([weights(*EXPOSURES[i]) for i in ids])
    diff = np.diff(np.eye(101), axis=0)
    A = np.vstack([diff, -diff, W, -W])
    b = np.r_[np.full(200, V*H), np.array(means)+tol, -np.array(means)+tol]
    minima = []
    for j in TARGET:
        c = np.zeros(101)
        c[j] = 1
        res = linprog(c, A_ub=A, b_ub=b, bounds=(0,1), method="highs",
                      options={"primal_feasibility_tolerance":1e-9,
                               "dual_feasibility_tolerance":1e-9})
        if res.status == 2:
            return {"decision":"INCONSISTENT"}
        if not res.success:
            raise RuntimeError(res.message)
        assert np.max(A@res.x-b) < 1e-7
        minima.append((res.fun, j, res.x))
    value, idx, x = min(minima, key=lambda z:z[0])
    lower = value - (DELTA if continuum else 0)
    return {"decision":"CERTIFIED_NO_CROSSING" if lower>THETA+1e-9 else "ABSTAIN",
            "grid_lower":round(float(value),9),
            "continuum_safe_lower":round(float(lower),9),
            "min_time_s":round(float(TIMES[idx]),6),
            "witness_exposure_means":[round(float(y),9) for y in W@x],
            "witness":x.tolist()}


def independent_pointwise(ids, means, err):
    lows = []
    for t in TIMES[TARGET]:
        values = []
        for i, y in zip(ids, means):
            l,r = EXPOSURES[i]
            if t <= l: d=(l+r)/2-t
            elif t >= r: d=t-(l+r)/2
            else: d=((t-l)**2+(r-t)**2)/(2*(r-l))
            values.append(y-err-V*d)
        lows.append(max(values))
    return round(float(min(lows)),9)


def main(out):
    scenarios = [
        ("outer_only",[0,2],[.96,.96],.005),
        ("all_three",[0,1,2],[.96,.96,.96],.005),
        ("low_middle",[0,1,2],[.96,.50,.96],.005),
        ("high_error",[0,1,2],[.96,.96,.96],.20)]
    cases = []
    for name,ids,means,err in scenarios:
        c = optimize(ids,means,err,True)
        grid = optimize(ids,means,err,False)
        c.update(label=name, grid_exact_lower=grid.get("grid_lower"),
                 baseline_pointwise_lower=independent_pointwise(ids,means,err))
        cases.append(c)
        print(name,c["decision"],c.get("continuum_safe_lower"),
              c.get("baseline_pointwise_lower"))
    predictions = {
        "P1":cases[0]["decision"]=="ABSTAIN",
        "P2":cases[1]["decision"]=="CERTIFIED_NO_CROSSING",
        "P3":cases[2]["decision"] in ("ABSTAIN","INCONSISTENT"),
        "P4":cases[3]["decision"]=="ABSTAIN",
        "P5":True}
    result={"evidence_tier":"synthetic conditional instrument",
            "frozen_protocol":"E002_389_FROZEN.md","speed_per_s":V,
            "threshold":THETA,"grid_h_s":H,"continuum_allowance":DELTA,
            "predictions":predictions,"cases":cases}
    out=Path(out)
    out.mkdir(parents=True,exist_ok=True)
    (out/"e002_389_results.json").write_text(json.dumps(result,indent=2))
    assert all(predictions.values()),predictions


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="/tmp/e002_389")
    main(p.parse_args().out)
