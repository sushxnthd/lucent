#!/usr/bin/env python3
"""E002-612: conditional observed-span velocity envelopes from point samples.

Research-only. An independently certified acceleration cap, point-aperture
measurements, timestamp bounds, and measurement error are prerequisites.
Nothing here certifies a human physiological speed limit.
"""
import argparse
import csv
import json
from fractions import Fraction as F
from itertools import product

FPS = (30, 120, 240, 1000)
ERROR_MM = (F('0.05'), F('0.1'), F('0.5'))
M_ILLUSTRATIVE = F(5000)
ATTESTATIONS = (
    'independent_acceleration_bound', 'instantaneous_anatomical_aperture',
    'independent_error_bounds', 'independent_clock_bounds',
    'contiguous_coverage', 'independent_geometry_calibration',
    'ethics_data_provenance',
)
NUISANCES = (
    'geometry', 'brightness', 'missingness', 'blur', 'gaze', 'glasses',
    'sampling', 'clock_error', 'occlusion', 'saturation', 'rolling_shutter',
)

def rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, str, F)):
        raise ValueError('numeric values must be exact decimal strings or integers')
    try:
        v = F(value)
    except (ValueError, ZeroDivisionError, TypeError) as exc:
        raise ValueError('invalid rational') from exc
    return v

def interval_bound(z0, z1, eps0, eps1, dt_lower, dt_upper, accel):
    z0, z1, e0, e1, lo, hi, m = map(rational, (z0, z1, eps0, eps1, dt_lower, dt_upper, accel))
    if not (e0 >= 0 and e1 >= 0 and 0 < lo <= hi and m >= 0):
        raise ValueError('invalid error, time or acceleration bounds')
    return (abs(z1-z0) + e0 + e1)/lo + m*hi/2

def certify_observed_span(data):
    """Returns a conditional mathematical bound, never a human certificate."""
    if not isinstance(data, dict) or data.get('experiment') != 'E002-612':
        raise ValueError('wrong experiment')
    obs, intervals = data.get('observations'), data.get('intervals')
    if not isinstance(obs, list) or len(obs) < 2 or not isinstance(intervals, list) or len(intervals) != len(obs)-1:
        raise ValueError('need contiguous observations and intervals')
    attest, nuis = data.get('attestations'), data.get('nuisances')
    if not isinstance(attest, dict) or not isinstance(nuis, dict):
        return {'status':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}
    if any(attest.get(k) is not True for k in ATTESTATIONS) or any(nuis.get(k) is not False for k in NUISANCES):
        return {'status':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}
    if any(not isinstance(o, dict) or o.get('point_observation') is not True or o.get('missing') is not False for o in obs):
        return {'status':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}
    if any(not isinstance(i, dict) for i in intervals):
        raise ValueError('bad interval')
    try:
        m = rational(data['acceleration_upper_mm_s2'])
        if m < 0:
            raise ValueError('negative acceleration')
        bounds = [interval_bound(obs[j]['z_mm'],obs[j+1]['z_mm'],
                  obs[j]['error_mm'],obs[j+1]['error_mm'],
                  intervals[j]['dt_lower_s'],intervals[j]['dt_upper_s'],m)
                  for j in range(len(intervals))]
    except KeyError as exc:
        raise ValueError('missing numeric field') from exc
    return {'status':'CONDITIONAL_OBSERVED_SPAN_VELOCITY_BOUND',
            'upper_mm_s':str(float(max(bounds))),
            'upper_exact':str(max(bounds)),
            'scope':'ONLY_CONTIGUOUS_OBSERVED_SPAN_AND_STIPULATED_PREMISES',
            'human_speed_certified':False,
            'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}

def scenario_rows():
    for f,e in product(FPS,ERROR_MM):
        u=interval_bound(0,0,e,e,F(1,f),F(1,f),M_ILLUSTRATIVE)
        yield dict(fps=f,error_mm=str(float(e)),
                   illustrative_acceleration_mm_s2=int(M_ILLUSTRATIVE),
                   conditional_speed_upper_mm_s=f'{float(u):.9f}',
                   exact=str(u),evidence='SYNTHETIC_NOT_HUMAN',
                   product='ABSTAIN_UNCALIBRATED',release='BLOCKED')

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--grid',action='store_true')
    p.add_argument('--input')
    args=p.parse_args()
    if args.input:
        with open(args.input,encoding='utf-8') as fh:
            data=json.load(fh)
        print(json.dumps(certify_observed_span(data),indent=2))
    elif args.grid:
        rows=list(scenario_rows())
        writer=csv.DictWriter(__import__('sys').stdout,fieldnames=list(rows[0]),lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)
    else:
        print(json.dumps({'scenario_count':len(list(scenario_rows())),
                          'physical_validation':'NOT_PERFORMED',
                          'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}))

if __name__ == '__main__':
    main()
