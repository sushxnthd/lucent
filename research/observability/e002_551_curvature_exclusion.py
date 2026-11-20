"""E002-551: conditional local closure exclusion; no physiological certification.

Standard bounded-second-derivative interpolation inequality. All numerical
inputs are externally stipulated; this module cannot authenticate them.
"""
from __future__ import annotations
import json
import math
import random
from dataclasses import dataclass

REQUIRED_GATES = (
    'geometry', 'anatomy', 'brightness', 'missingness', 'blur', 'gaze',
    'glasses', 'sampling', 'clock', 'marker_identity', 'optical_transfer',
)

@dataclass(frozen=True)
class Result:
    decision: str
    lower_bound: float | None
    minimizer_fraction: float | None
    reason: str


def exclude(y0, y1, d, e, u, A, theta=0.2, *,
            instantaneous=False, gates=None) -> Result:
    if not instantaneous:
        return Result('ABSTAIN', None, None, 'endpoint exposure response not certified instantaneous')
    if not isinstance(gates, dict) or not all(gates.get(k) is True for k in REQUIRED_GATES):
        return Result('ABSTAIN', None, None, 'missing or failed independent nuisance gate')
    vals = (y0, y1, d, e, u, A, theta)
    if any(type(x) not in (int, float) or not math.isfinite(x) for x in vals):
        return Result('ABSTAIN', None, None, 'invalid or missing numerical certificate')
    if not (0 <= y0 <= 1 and 0 <= y1 <= 1 and 0 <= theta <= 1 and
            e >= 0 and u >= 0 and A >= 0 and d > 2*u):
        return Result('ABSTAIN', None, None, 'invalid physical range or clock interval')
    D = d + 2*u
    c = A * D * D
    a, b = y0 - e, y1 - e
    s = max(0., min(1., 0.5 - (b-a)/c)) if c > 0 else (0. if a <= b else 1.)
    lower = (1-s)*a + s*b - 0.5*c*s*(1-s)
    if lower > theta:
        return Result('CONDITIONAL_EXCLUSION_ONLY', lower, s, 'all stated assumptions required')
    return Result('POSSIBLE_CLOSURE_OR_UNRESOLVED', lower, s, 'sharp envelope intersects threshold')


def parabola_min(f0, f1, D, q):
    """Minimum of f=(1-s)f0+s*f1-q*D²*s*(1-s)/2, s in [0,1]."""
    c = q * D * D
    if c > 0:
        s = max(0., min(1., 0.5 - (f1-f0)/c))
        return (1-s)*f0+s*f1-0.5*c*s*(1-s)
    return min(f0, f1)


def simulation(n=10000, seed=551):
    rng = random.Random(seed)
    gates = {k: True for k in REQUIRED_GATES}
    stats = dict(seed=seed, target_trials=n, accepted=0, excluded=0,
                 true_closures=0, false_exclusions=0, discarded_out_of_range=0, speed_only_excluded=0)
    for _ in range(n):
        d = rng.uniform(.002, .02)
        u = rng.uniform(0., min(.0004, d/5))
        D = rng.uniform(d-2*u, d+2*u)
        A = rng.uniform(0., 10000.)
        q = rng.uniform(-A, A)
        f0, f1 = rng.uniform(.25,.9), rng.uniform(.25,.9)
        low = parabola_min(f0, f1, D, q)
        high = -parabola_min(-f0, -f1, D, -q)
        if low < 0 or high > 1:
            stats['discarded_out_of_range'] += 1
            continue
        e = rng.uniform(0., .025)
        y0 = f0 + rng.uniform(-e,e)
        y1 = f1 + rng.uniform(-e,e)
        if not (0 <= y0 <= 1 and 0 <= y1 <= 1):
            stats['discarded_out_of_range'] += 1
            continue
        r = exclude(y0,y1,d,e,u,A,instantaneous=True,gates=gates)
        assert r.decision != 'ABSTAIN'
        stats['accepted'] += 1
        closure = low <= .2
        stats['true_closures'] += int(closure)
        is_excluded = r.decision == 'CONDITIONAL_EXCLUSION_ONLY'
        stats['excluded'] += int(is_excluded)
        Dmax = d+2*u
        Vcert = (abs(y1-y0)+2*e)/(d-2*u) + A*Dmax/2
        speed_only_lower = ((y0-e)+(y1-e)-Vcert*Dmax)/2
        stats['speed_only_excluded'] += int(speed_only_lower > .2)
        stats['false_exclusions'] += int(is_excluded and closure)
    return stats


def run():
    gates = {k: True for k in REQUIRED_GATES}
    short = exclude(.25,.25,.005,0,0,8000,instantaneous=True,gates=gates)
    long = exclude(.25,.25,.01,0,0,8000,instantaneous=True,gates=gates)
    underdeclared = exclude(.25,.25,.01,0,0,1000,instantaneous=True,gates=gates)
    out = dict(evidence_tier='SYNTHETIC_CONDITIONAL_ONLY',
               short_ms_5=dict(decision=short.decision,lower=short.lower_bound),
               long_ms_10=dict(decision=long.decision,lower=long.lower_bound),
               sharp_witness_at_10ms=parabola_min(.25,.25,.01,8000),
               underdeclared_A_false_exclusion=dict(decision=underdeclared.decision,
                                                    true_min=parabola_min(.25,.25,.01,8000),
                                                    declared_A=1000,true_A=8000),
               simulation=simulation())
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__ == '__main__':
    run()
