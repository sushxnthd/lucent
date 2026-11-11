#!/usr/bin/env python3
"""E002-606: exact rational-rate ideal point-sampling falsifier.

Synthetic piecewise-constant native-frame bins only. Not human, shutter or velocity data.
"""
import json
from fractions import Fraction
from math import lcm


def positive_int(x):
    if type(x) is not int or x <= 0 or x > 100000:
        raise ValueError('POSITIVE_BOUNDED_INTEGER_REQUIRED')
    return x


def exact_miss(f_high, f_low, bins):
    h, l, m = map(positive_int, (f_high, f_low, bins))
    return max(Fraction(0), Fraction(1) - Fraction(m*l, h))


def independent_lattice_miss(f_high, f_low, bins):
    h, l, m = map(positive_int, (f_high, f_low, bins))
    tick = lcm(h, l)
    period, width = tick // l, m * (tick // h)
    if period > 100000:
        raise ValueError('PHASE_GRID_TOO_LARGE')
    missed = 0
    for phase in range(period):
        # Enumerate actual low-camera sample times, not the closed-form expression.
        sample_times = (phase + k*period for k in range(-1, width//period + 2))
        seen = any(0 <= t < width for t in sample_times)
        missed += not seen
    return Fraction(missed, period)


def three_phase_index_miss(bins):
    m = positive_int(bins)
    return Fraction(max(0, 3-m), 3)


def frac(f):
    return f'{f.numerator}/{f.denominator}'


def experiment():
    rows=[]
    for h in (100,110):
        for m in (1,2,3,4):
            a=exact_miss(h,30,m)
            b=independent_lattice_miss(h,30,m)
            if a != b:
                raise AssertionError(f'INDEPENDENT_ENUMERATION_MISMATCH:{h}:{m}')
            naive=three_phase_index_miss(m)
            rows.append({'native_hz':h,'target_hz':30,'closed_native_bins':m,
                         'ideal_30fps_miss':frac(a),'three_phase_index_miss':frac(naive),
                         'index_minus_ideal':frac(naive-a),
                         'independent_lattice_miss':frac(b)})
    keyed={(r['native_hz'],r['closed_native_bins']):r for r in rows}
    for key,expected in { (100,3):'1/10',(110,3):'2/11',(110,2):'5/11',(110,4):'0/1'}.items():
        if keyed[key]['ideal_30fps_miss'] != expected:
            raise AssertionError(f'FROZEN_PREDICTION_FAILED:{key}')
    return {'experiment':'E002-606','evidence_tier':'EXACT_SYNTHETIC_IDEAL_POINT_SAMPLING',
            'precommitted_predictions_passed':True,'independent_enumeration_passed':True,
            'rows':rows,'human_closure_events_measured':0,
            'physical_shutter_calibrated':False,'continuous_velocity_certified':False,
            'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}

if __name__=='__main__':
    print(json.dumps(experiment(),sort_keys=True,indent=2))
