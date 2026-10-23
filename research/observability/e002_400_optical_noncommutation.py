#!/usr/bin/env python3
"""E002-400: optical inversion and shutter averaging do not generally commute.

Synthetic instrument only. Imports the existing conditional E002-399 aperture
certificate; no human measurements or deployment validation are claimed.
"""
from __future__ import annotations
import json
import math
import random
from dataclasses import asdict
from e002_399_reference_adequacy import Frame, calibrated, certify


def optical_bias_bound(speed: float, exposure: float, curvature: float, slope_floor: float) -> float:
    """Upper bound on |inverse_f(E f(x)) - E x| for Lipschitz x and monotone C2 f.

    Taylor/Jensen gives K*V**2*e**2/(24*m). A distribution-free bound V*e/2
    also holds because inverse_f(E f(x)) lies in the observed aperture range.
    """
    if not all(math.isfinite(v) for v in (speed, exposure, curvature, slope_floor)):
        raise ValueError('Nonfinite calibration')
    if speed < 0 or exposure <= 0 or curvature < 0 or slope_floor <= 0:
        raise ValueError('Invalid calibration')
    return min(curvature*speed*speed*exposure*exposure/(24*slope_floor), speed*exposure/2)


def exp_optical_inverse_mean(center: float, exposure: float, speed: float, k: float) -> float:
    """Exact f^-1(E f(x)) for x(t)=center +/- V*t, f(x)=exp(k*(x-center))."""
    z = k*speed*exposure/2
    return center if z == 0 else center + math.log(math.sinh(z)/z)/k


def mean_quadratic_transfer(a: float, b: float) -> tuple[float, float]:
    """Exact physical and f(x)=x+x²/2 means over a linear trajectory segment."""
    mean=(a+b)/2
    return mean, mean+0.5*(a*a+a*b+b*b)/3


def piecewise_means(values: list[float]) -> tuple[float, float]:
    means=[mean_quadratic_transfer(a,b) for a,b in zip(values,values[1:])]
    return (sum(v[0] for v in means)/len(means),
            sum(v[1] for v in means)/len(means))


def experiment(seed: int=400, n: int=500) -> dict:
    theta=.2; speed=1.; exposure=.1; gap=.2; minimum=.199
    centers=[0.,gap]
    center_aperture=minimum+gap/2
    optical=exp_optical_inverse_mean(center_aperture,exposure,speed,120.)
    physical_mean=center_aperture
    naive=certify([Frame(t,optical,optical,exposure,0.) for t in centers],
                  calibrated(speed,theta))
    physical=certify([Frame(t,physical_mean,physical_mean,exposure,0.) for t in centers],
                     calibrated(speed,theta))
    k=120.
    m=k*math.exp(k*(0.-center_aperture))
    K=k*k*math.exp(k*(1.-center_aperture))
    bound=optical_bias_bound(speed,exposure,K,m)
    corrected=certify([Frame(t,optical-bound,optical+bound,exposure,0.) for t in centers],
                      calibrated(speed,theta))
    assert minimum<theta
    assert naive.decision=='CONFIRMED_NO_CROSSING', 'H1 failed'
    assert physical.decision=='UNRESOLVED', 'H2 failed'
    assert corrected.decision=='UNRESOLVED', 'H3 failed'
    rng=random.Random(seed)
    qbound=optical_bias_bound(1.,.1,1.,1.)
    worst=0.
    for i in range(n):
        values=[.5]
        for j in range(10):
            values.append(values[-1]+rng.uniform(-1,1)*.01)
        assert all(0<=v<=1 for v in values)
        pm,sm=piecewise_means(values)
        recovered=math.sqrt(1+2*sm)-1
        bias=abs(recovered-pm)
        assert bias<=qbound+1e-12, ('H5 failed',i,bias,qbound)
        worst=max(worst,bias)
    assert all(abs(piecewise_means([a,b])[0]-(a+b)/2)<1e-14
               for a,b in ((.2,.4),(.9,.8),(.3,.3))), 'H6 failed'
    return {
        'experiment':'E002-400','evidence_tier':'synthetic optical transfer counterexample',
        'physical_minimum':minimum,'threshold':theta,'centers_s':centers,
        'exposure_s':exposure,'speed_bound_per_s':speed,
        'physical_shutter_mean':physical_mean,
        'inverse_optical_shutter_mean':optical,
        'noncommutation_bias':optical-physical_mean,
        'calibrated_optical_error_bound':bound,
        'naive_decision':asdict(naive),'physical_mean_decision':asdict(physical),
        'corrected_decision':asdict(corrected),
        'quadratic_random_trials':n,'quadratic_bound':qbound,
        'quadratic_max_bias':worst,'human_physical_aperture_validated':False,
        'product':'ABSTAIN_UNCALIBRATED'
    }


if __name__=='__main__':
    print(json.dumps(experiment(),indent=2,sort_keys=True))
