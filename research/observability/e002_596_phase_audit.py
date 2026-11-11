#!/usr/bin/env python3
"""E002-596: exact-rational continuous phase audit, index-only; no human claims."""
from fractions import Fraction as F
import json

N = 19
R = F(95, 30)

def nearest(q):
    x = q + F(1, 2)
    return x.numerator // x.denominator

def signature(p):
    if not isinstance(p, F) or not 0 <= p < R:
        raise ValueError("INVALID_PHASE")
    out = []
    for k in range(N + 1):
        i = nearest(p + k * R)
        if i >= N:
            break
        out.append(i)
    assert len(out) == len(set(out))
    return tuple(out)

def misses(sig, w):
    if type(w) is not int or not 1 <= w <= N:
        raise ValueError("INVALID_WIDTH")
    return sum(not any(s <= i < s + w for i in sig)
               for s in range(N - w + 1))

def boundaries():
    points = {F(0), R}
    for k in range(N + 1):
        for i in range(N + 1):
            p = F(2*i + 1, 2) - k*R
            if 0 < p < R:
                points.add(p)
    return sorted(points)

def aggregate():
    bp = boundaries()
    phases = sorted(set(bp[:-1] + [(a+b)/2 for a,b in zip(bp,bp[1:])]))
    signatures = {signature(p) for p in phases}
    integer = {str(i): list(signature(F(i))) for i in range(4)}
    data = [{'indices':list(sig), 'n':len(sig),
             'misses':{str(w):misses(sig,w) for w in (1,2,3,4)}}
            for sig in sorted(signatures)]
    old = set().union(*(set(signature(F(i))) for i in range(3)))
    new = set().union(*(set(signature(F(i))) for i in range(4)))
    return {
        'experiment':'E002-596', 'evidence_tier':'EXACT_INDEX_ONLY',
        'native_fps':95, 'nominal_fps':30, 'window_native_frames':N,
        'integer_phases':integer,
        'three_phase_union':sorted(old),
        'three_phase_unseen':sorted(set(range(N))-old),
        'four_phase_union':sorted(new),
        'four_phase_unseen':sorted(set(range(N))-new),
        'boundary_count':len(bp),
        'distinct_continuous_signatures':len(signatures),
        'signature_sample_count_range':[min(map(len,signatures)),max(map(len,signatures))],
        'worst_missed_pulses_by_width':{str(w):max(misses(s,w) for s in signatures) for w in (1,2,3,4)},
        'best_missed_pulses_by_width':{str(w):min(misses(s,w) for s in signatures) for w in (1,2,3,4)},
        'critical_phases':[str(x) for x in bp],
        'signatures':data,
        'human_anatomical_labels':0, 'physical_shutter_calibrations':0,
        'product':'ABSTAIN_UNCALIBRATED', 'release':'BLOCKED'
    }

def test():
    a = aggregate()
    assert a['integer_phases']['0'] == [0,3,6,10,13,16]
    assert a['integer_phases']['1'] == [1,4,7,11,14,17]
    assert a['integer_phases']['2'] == [2,5,8,12,15,18]
    assert a['integer_phases']['3'] == [3,6,9,13,16]
    assert a['three_phase_unseen'] == [9]
    assert a['four_phase_unseen'] == []
    assert a['signature_sample_count_range'] == [5,6]
    for bad in (F(-1),R,F(4),0,1.0,None,True):
        try: signature(bad)
        except ValueError: pass
        else: raise AssertionError('BAD_PHASE_ACCEPTED')
    for bad in (-1,0,20,0.5,True):
        try: misses((0,3),bad)
        except ValueError: pass
        else: raise AssertionError('BAD_WIDTH_ACCEPTED')
    bp=boundaries()
    for l,r in zip(bp,bp[1:]):
        assert signature((3*l+r)/4)==signature((l+r)/2)==signature((l+3*r)/4)
    print(json.dumps(a,sort_keys=True,separators=(',',':')))

if __name__ == '__main__':
    test()
