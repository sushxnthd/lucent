"""E002-481: exact rational width-class optical detection (SYNTHETIC ONLY).

A finite pulse scan can certify only a *calibrated response class*, never
exact zero shutter sensitivity or human anatomical nonclosure.
"""
from __future__ import annotations
import json
from fractions import Fraction as F

T = F(1000, 240)
W = F(6, 1000)
U = F(4, 1000)
A = F(1, 5)
EPS = F(2, 1000)
THETA = F(4, 100)
ABSTAIN = 'ABSTAIN_UNCALIBRATED'


def rational(x):
    if isinstance(x, bool):
        raise ValueError('boolean is not a physical measurement')
    if isinstance(x, float):
        import math
        if not math.isfinite(x):
            raise ValueError('nonfinite input')
        return F(str(x))
    if isinstance(x, (int, str, F)):
        return F(x)
    raise ValueError('unsupported quantity')


def validate(period, width, uncertainty, island_width, amplitude, noise, threshold):
    t, w, u, l, a, eps, theta = map(rational, (period,width,uncertainty,island_width,amplitude,noise,threshold))
    if t <= 0 or w <= 0 or u < 0 or l < 0 or a < 0 or eps < 0 or theta < 0:
        raise ValueError('invalid measurement geometry')
    if w + l + 2*u >= t:
        raise ValueError('requires isolated island, no multi-period pulse overlap')
    return t,w,u,l,a,eps,theta


def guaranteed_overlap(width=W, uncertainty=U, island_width=W):
    w,u,l = map(rational, (width,uncertainty,island_width))
    if w <= 0 or u < 0 or l < 0:
        raise ValueError('invalid width or uncertainty')
    return max(F(0), min(w,l,(w+l)/2-u))


def guaranteed_grid_overlap(n, period=T, width=W, uncertainty=U, island_width=W):
    if type(n) is not int or n <= 0:
        raise ValueError('invalid phase count')
    t,w,u,l,_,_,_ = validate(period,width,uncertainty,island_width,A,EPS,THETA)
    return max(F(0),min(w,l,(w+l)/2-u-t/(2*n)))


def robust_contrast(n, island_width, amplitude=A, period=T, width=W, uncertainty=U, noise=EPS, threshold=THETA):
    t,w,u,l,a,eps,theta = validate(period,width,uncertainty,island_width,amplitude,noise,threshold)
    q = guaranteed_grid_overlap(n,t,w,u,l)
    worst = a*q/w-eps
    return {'guaranteed_overlap_ms':str(q), 'worst_case_contrast':str(worst),
            'detectable_strict':worst>theta, 'physical_claim':ABSTAIN}


def min_phase_count(island_width, amplitude=A, period=T, width=W, uncertainty=U, noise=EPS, threshold=THETA):
    t,w,u,l,a,eps,theta=validate(period,width,uncertainty,island_width,amplitude,noise,threshold)
    if a == 0:
        return None
    required=(theta+eps)*w/a
    max_overlap=guaranteed_overlap(w,u,l)
    if max_overlap <= required:
        return None
    gap=w+l-2*u-2*required
    if gap <= 0:
        return None
    n=int(t//gap)+1
    assert guaranteed_grid_overlap(n,t,w,u,l)>required
    if n>1:
        assert guaranteed_grid_overlap(n-1,t,w,u,l)<=required
    return n


def overlap(a,b,c,d):
    return max(F(0),min(b,d)-max(a,c))


def brute_worst_phase(n, island_width, period=T, width=W, uncertainty=U):
    """Independent endpoint-overlap enumeration at the grid midpoint.

    For a single isolated interval, overlap versus start is unimodal, so
    its minimum over the allowed timing interval is at one endpoint.
    The two nearest grid centers are worst at their common midpoint.
    """
    t,w,u,l,_,_,_=validate(period,width,uncertainty,island_width,A,EPS,THETA)
    if type(n) is not int or n<=0:
        raise ValueError('invalid n')
    island_center=t/(2*n)
    lo=island_center-l/2
    hi=island_center+l/2
    best=F(0)
    for i in range(n):
        nominal=F(i)*t/n-w/2
        per_pulse=[]
        for e in (-u,u):
            start=nominal+e
            per_pulse.append(sum((overlap(start,start+w,lo+k*t,hi+k*t) for k in (-1,0,1)),F(0)))
        best=max(best,min(per_pulse))
    return best


def experiment():
    cases={}
    for label,l in [('narrow',F(5,10000)),('geometric_only',F(3,1000)),('detectable_class',F(6,1000))]:
        n=min_phase_count(l)
        cases[label]={'island_width_ms':str(l),'infinite_grid_overlap_ms':str(guaranteed_overlap(W,U,l)),
                      'minimum_detectable_phase_count':n,
                      'at_668':robust_contrast(668,l),
                      'at_2815':robust_contrast(2815,l),
                      'at_2816':robust_contrast(2816,l)}
    exact_threshold=2*(U+(THETA+EPS)*W/A)-W
    return {'experiment':'E002-481', 'evidence_tier':'SYNTHETIC_WIDTH_RESTRICTED_OPTICAL_MODEL',
            'pointwise_guaranteed_pulse_core_ms':str(max(F(0),W-2*U)),
            'infinite_grid_strict_minimum_island_width_ms':str(exact_threshold),
            'cases':cases,
            'independent_brute_overlap_n2815':str(brute_worst_phase(2815,W)),
            'independent_brute_overlap_n2816':str(brute_worst_phase(2816,W)),
            'physical_shutter_acquisitions':0,'new_human_sequences':0,
            'physical_claim':ABSTAIN,'e002_371_physical_validation':'NOT_ESTABLISHED'}

if __name__=='__main__':
    print(json.dumps(experiment(),indent=2,sort_keys=True))
