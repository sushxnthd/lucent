#!/usr/bin/env python3
"""Independent discretized exposure-integral adversary for E002-540.

Does not import the analytic evaluator or witness. Piecewise-linear aperture
values have exact trapezoidal exposure integrals. Synthetic evidence only.
"""
import argparse
import json
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix


def optimize(steps_per_300th: int, speed: float):
    if steps_per_300th not in (10,20):
        raise ValueError("frozen grids: 10 or 20 steps per 1/300 second")
    if speed not in (40.0,45.0):
        raise ValueError("frozen speeds: 40 or 45")
    q=steps_per_300th
    n=13*q
    dt=1/(300*q)
    first_end=3*q
    second_start=10*q
    mid=(first_end+second_start)//2
    assert (first_end+second_start)%2==0
    a_ub=lil_matrix((2*n,n+1),dtype=float)
    b_ub=np.full(2*n,speed*dt)
    for i in range(n):
        a_ub[2*i,i]=-1; a_ub[2*i,i+1]=1
        a_ub[2*i+1,i]=1; a_ub[2*i+1,i+1]=-1
    a_eq=lil_matrix((2,n+1),dtype=float)
    for row,start,end in [(0,0,first_end),(1,second_start,n)]:
        for j in range(start,end+1):
            a_eq[row,j]=(0.5 if j in (start,end) else 1)/(end-start)
    c=np.zeros(n+1)
    c[mid]=1
    res=linprog(c,A_ub=a_ub.tocsr(),b_ub=b_ub,A_eq=a_eq.tocsr(),b_eq=[.9,.9],
                bounds=(0,1),method="highs")
    if not res.success:
        raise RuntimeError(res.message)
    means=a_eq.tocsr()@res.x
    speed_violation=max(0,max(abs(np.diff(res.x))/dt)-speed)
    return {
        "grid_intervals":n,"speed_ceiling":speed,"minimum_aperture":float(res.fun),
        "exposure_means":[float(v) for v in means],
        "max_speed_violation":float(speed_violation),
        "midpoint_time_seconds":mid*dt,
        "synthetic_only":True,
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--q",type=int,choices=(10,20),default=10)
    parser.add_argument("--speed",type=float,choices=(40.0,45.0),default=45.0)
    args=parser.parse_args()
    result=optimize(args.q,args.speed)
    target=0.175 if args.speed==45.0 else 0.2504906208587144
    assert abs(result["minimum_aperture"]-target) < 0.025, "FROZEN LP DISAGREEMENT"
    assert max(abs(v-.9) for v in result["exposure_means"]) < 1e-8
    assert result["max_speed_violation"] < 1e-8
    assert (result["minimum_aperture"]<.2) == (args.speed==45.0)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__": main()
