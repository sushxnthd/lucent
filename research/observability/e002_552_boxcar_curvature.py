"""E002-552 exact exposure-integrated curvature envelope.

Mathematical instrument model only. No real shutter, human A, or anatomical
transfer certificates are authenticated by this executable.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
import json
import random

GATES = (
    'geometry', 'anatomy', 'brightness', 'missingness', 'blur', 'gaze',
    'glasses', 'sampling', 'clock', 'marker_identity', 'optical_transfer',
    'boxcar_aperture_response', 'global_shutter', 'hard_acceleration',
    'exposure_timing', 'independent_calibration',
)

@dataclass(frozen=True)
class Decision:
    label: str
    minimum: F | None
    argmin: F | None
    reason: str


def rational(x):
    if isinstance(x, bool) or not isinstance(x, (int, str, F)):
        raise ValueError('only exact integer, fraction or decimal-string inputs permitted')
    return F(x)


def exclude(m0, m1, d, h0, h1, A, theta, *, e0=0, e1=0,
            clock_error=0, gates=None):
    if not isinstance(gates, dict) or not all(gates.get(k) is True for k in GATES):
        return Decision('ABSTAIN_UNCALIBRATED', None, None, 'missing independent nuisance or transfer certificate')
    try:
        m0,m1,d,h0,h1,A,theta,e0,e1,clock_error = map(rational,
            (m0,m1,d,h0,h1,A,theta,e0,e1,clock_error))
    except (ValueError, TypeError, ZeroDivisionError):
        return Decision('ABSTAIN_UNCALIBRATED', None, None, 'invalid or inexact numeric certificate')
    if not (0 <= m0 <= 1 and 0 <= m1 <= 1 and 0 <= theta <= 1 and
            d > 0 and h0 > 0 and h1 > 0 and A >= 0 and
            0 <= e0 <= 1 and 0 <= e1 <= 1 and clock_error == 0):
        return Decision('ABSTAIN_UNCALIBRATED', None, None, 'invalid ranges or uncertified shutter timing support')
    c0, c1 = -h0/2, d+h1/2
    D = c1-c0
    left, right = -c0/D, (d-c0)/D
    b0 = m0-e0-A*h0*h0/24
    b1 = m1-e1-A*h1*h1/24
    curvature = A*D*D
    if curvature:
        s = max(left, min(right, F(1,2)-(b1-b0)/curvature))
    else:
        s = left if b0 <= b1 else right
    lower = (1-s)*b0+s*b1-curvature*s*(1-s)/2
    t = c0+s*D
    label = 'CONDITIONAL_INSTRUMENT_EXCLUSION_ONLY' if lower > theta else 'POSSIBLE_CLOSURE_OR_UNRESOLVED'
    return Decision(label, lower, t, 'synthetic/conditional only; no physiological release certificate')


def quadratic_mean(a, b, q, lo, hi):
    """Mean of a + b*t + q*t^2/2 on [lo,hi]."""
    return a+b*(lo+hi)/2+q*(lo*lo+lo*hi+hi*hi)/6


def quadratic_minmax(a,b,q,lo,hi):
    def f(t): return a+b*t+q*t*t/2
    vals = [f(lo),f(hi)]
    if q:
        vertex = -b/q
        if lo <= vertex <= hi:
            vals.append(f(vertex))
    return min(vals),max(vals)


def simulation(n=10000, seed=552):
    rng = random.Random(seed)
    gates = {k:True for k in GATES}
    counts = dict(seed=seed, generated=n, accepted=0, discarded_out_of_range=0,
                  true_closures=0, excluded=0, false_exclusions=0,
                  envelope_violations=0, sharp_equalities=0)
    for _ in range(n):
        d=F(rng.randint(2,20),1000)
        h0=F(rng.randint(1,8),1000)
        h1=F(rng.randint(1,8),1000)
        A=F(rng.randint(500,20000))
        q=F(rng.randint(-int(A),int(A)))
        a=F(rng.randint(20,80),100)
        b=F(rng.randint(-30,30))
        entire_min,entire_max=quadratic_minmax(a,b,q,-h0,d+h1)
        if entire_min<0 or entire_max>1:
            counts['discarded_out_of_range']+=1
            continue
        m0=quadratic_mean(a,b,q,-h0,F(0))
        m1=quadratic_mean(a,b,q,d,d+h1)
        e0=F(rng.randint(0,20),1000)
        e1=F(rng.randint(0,20),1000)
        y0=m0+F(rng.randint(-int(e0*1000),int(e0*1000)),1000)
        y1=m1+F(rng.randint(-int(e1*1000),int(e1*1000)),1000)
        if not (0<=y0<=1 and 0<=y1<=1):
            counts['discarded_out_of_range']+=1
            continue
        r=exclude(y0,y1,d,h0,h1,A,F(1,5),e0=e0,e1=e1,gates=gates)
        assert r.label!='ABSTAIN_UNCALIBRATED'
        true_min,_=quadratic_minmax(a,b,q,F(0),d)
        counts['accepted']+=1
        counts['true_closures']+=int(true_min<=F(1,5))
        counts['excluded']+=int(r.label=='CONDITIONAL_INSTRUMENT_EXCLUSION_ONLY')
        counts['false_exclusions']+=int(r.label=='CONDITIONAL_INSTRUMENT_EXCLUSION_ONLY' and true_min<=F(1,5))
        counts['envelope_violations']+=int(r.minimum>true_min)
        counts['sharp_equalities']+=int(r.minimum==true_min)
    return counts


def run():
    gates={k:True for k in GATES}
    d=F(1); h=F(1,5); A=F(2); theta=F(1,10)
    m=quadratic_mean(F(1,4),F(-1),F(2),-h,F(0))
    result=exclude(m,m,d,h,h,A,theta,gates=gates)
    naive=m-A*d*d/8
    assert m==F(109,300) and naive==F(17,150)
    assert result.minimum==0 and result.argmin==F(1,2)
    assert naive>theta and result.label=='POSSIBLE_CLOSURE_OR_UNRESOLVED'
    assert exclude(F(1,2),F(1,2),d,h,h,0,theta,gates=gates).label=='CONDITIONAL_INSTRUMENT_EXCLUSION_ONLY'
    return dict(evidence_tier='EXACT_SYNTHETIC_INSTRUMENT_ONLY',
        witness=dict(measured_mean=str(m),true_min='0',naive_instantaneous_lower=str(naive),
                     corrected_lower=str(result.minimum),naive_false_exclusion=True,
                     corrected_exclusion=False),simulation=simulation())

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
