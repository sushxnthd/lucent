#!/usr/bin/env python3
"""E002-389 independent primal/dual and strict-hidden-crossing checks."""
import json
import sys
import numpy as np
from scipy.optimize import linprog

H,V,N = .001,60.,101
WINDOWS=[(10,30),(40,60),(70,90)]
SPECS={
 "outer_only":([0,2],[.96,.96],.005),
 "all_three":([0,1,2],[.96,.96,.96],.005),
 "low_middle":([0,1,2],[.96,.50,.96],.005),
 "high_error":([0,1,2],[.96,.96,.96],.20)}


def mean(x,l,r):
    return float(np.trapezoid(x[l:r+1],dx=H)/((r-l)*H))


def independently_solve(ids,observed,err,target):
    rows=[]; rhs=[]
    for j in range(N-1):
        a=np.zeros(N);a[j]=-1;a[j+1]=1
        rows.extend([a.copy(),-a.copy()])
        rhs.extend([V*H,V*H])
    for i,y in zip(ids,observed):
        l,r=WINDOWS[i]
        a=np.zeros(N)
        for k in range(l,r):
            a[k]+=.5/(r-l)
            a[k+1]+=.5/(r-l)
        rows.extend([a.copy(),-a.copy()])
        rhs.extend([y+err,-y+err])
    A=np.array(rows);b=np.array(rhs)
    c=np.zeros(N);c[target]=1
    res=linprog(c,A_ub=A,b_ub=b,bounds=(0,1),method="highs",
                options={"primal_feasibility_tolerance":1e-9,
                         "dual_feasibility_tolerance":1e-9})
    assert res.success,res.message
    dual=float(b@res.ineqlin.marginals+res.upper.marginals.sum())
    stat=A.T@res.ineqlin.marginals+res.lower.marginals+res.upper.marginals
    assert abs(res.fun-dual)<1e-7
    assert np.max(np.abs(stat-c))<1e-7
    assert np.max(A@res.x-b)<1e-7
    return res.fun


def main(path):
    cases={c["label"]:c for c in json.load(open(path))["cases"]}
    checks=0
    for name,(ids,y,err) in SPECS.items():
        case=cases[name]
        x=np.array(case["witness"])
        assert np.min(x)>=-1e-9 and np.max(x)<=1+1e-9
        assert np.max(np.abs(np.diff(x)))<=V*H+1e-8
        for i,yy in zip(ids,y):
            assert abs(mean(x,*WINDOWS[i])-yy)<=err+V*H/2+1e-8
            checks+=1
        t=round(case["min_time_s"]/H)
        assert abs(independently_solve(ids,y,err+V*H/2,t)-case["grid_lower"])<1e-7
        checks+=1
    # Strict (<0.2) crossing, fully consistent with *original* outer-only measurements.
    t=np.linspace(0,.1,N)
    witness=.96-np.maximum(0,.77-V*np.abs(t-.05))
    assert witness[50]<.2 and abs(witness[50]-.19)<1e-10
    assert np.max(np.abs(np.diff(witness)))/H<=V+1e-9
    assert all(abs(mean(witness,*WINDOWS[i])-.96)<1e-10 for i in [0,2])
    checks+=3
    print(json.dumps({"status":"PASS","independent_checks":checks,
                      "strict_crossing_at_50ms":float(witness[50]),
                      "outer_means":[mean(witness,*WINDOWS[i]) for i in [0,2]]}))


if __name__=="__main__":
    main(sys.argv[1])
