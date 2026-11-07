#!/usr/bin/env python3
"""E002-538 sharp acceleration-only aperture bound. Research only."""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
import json

ATTESTATIONS = (
    'independent_continuous_time_acceleration_bound',
    'pointwise_anatomical_endpoints',
    'blinded_anatomical_reference',
    'photodiode_authenticated_shutter',
    'authenticated_clock_and_gap',
    'native_missingness_audited',
    'nuisance_envelope_verified',
)

def rational(x):
    if isinstance(x, bool) or x is None:
        raise ValueError('rational must not be bool/null')
    try:
        return Q(str(x))
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise ValueError('invalid rational') from exc

def lower(t, b0, b1, gap, accel):
    return b0 + (b1-b0)*t/gap - accel*t*(gap-t)/2

def exact_minimum(b0, b1, gap, accel):
    if accel == 0:
        return (Q(0), b0) if b0 <= b1 else (gap, b1)
    vertex = gap/2 - (b1-b0)/(accel*gap)
    t = max(Q(0), min(gap, vertex))
    return t, lower(t, b0, b1, gap, accel)

def evaluate(case):
    if not isinstance(case, dict):
        raise ValueError('case must be object')
    b0 = rational(case.get('b0'))
    b1 = rational(case.get('b1'))
    c = rational(case.get('threshold'))
    gap = rational(case.get('max_unobserved_gap_s'))
    accel = rational(case.get('max_abs_aperture_accel_s2'))
    if not (0 <= c < b0 <= 1 and 0 <= c < b1 <= 1 and gap > 0 and accel >= 0):
        raise ValueError('invalid geometry, gap or acceleration')
    evidence = case.get('attestations')
    if not isinstance(evidence, dict) or any(type(evidence.get(k)) is not bool for k in ATTESTATIONS):
        raise ValueError('attestations must be explicit booleans')
    if case.get('endpoint_observable') not in ('pointwise_anatomical_aperture', 'exposure_average', 'raw_pixel_brightness'):
        raise ValueError('unknown endpoint observable')
    if case.get('acceleration_source') not in ('independent_continuous_envelope', 'sampled_second_difference', 'literature_cohort'):
        raise ValueError('unknown acceleration source')
    t, minval = exact_minimum(b0,b1,gap,accel)
    delta = min(b0,b1)-c
    q = accel*gap*gap/(8*delta) if b0 == b1 else None
    admissible = (case['endpoint_observable'] == 'pointwise_anatomical_aperture'
                  and case['acceleration_source'] == 'independent_continuous_envelope'
                  and all(evidence[k] for k in ATTESTATIONS))
    blockers = []
    if case['endpoint_observable'] != 'pointwise_anatomical_aperture':
        blockers.append('EXPOSURE_AVERAGE_NOT_POINTWISE_ANATOMY')
    if case['acceleration_source'] != 'independent_continuous_envelope':
        blockers.append('ACCELERATION_NOT_CONTINUOUS_HARD_BOUND')
    blockers.extend('MISSING_'+k.upper() for k in ATTESTATIONS if not evidence[k])
    return {
        'experiment': 'E002-538',
        'evidence_tier': 'EXACT_MATH_SYNTHETIC_NOT_PHYSICAL_VALIDATION',
        'minimum_lower_envelope': str(minval),
        'minimizer_time_s': str(t),
        'equal_endpoint_dimensionless_Q': str(q) if q is not None else None,
        'conditional_geometry': 'NO_HIDDEN_CROSSING' if minval > c else 'HIDDEN_CROSSING_FEASIBLE',
        'threshold_touch_is_excluded': False,
        'evidence_decision': 'CONDITIONAL_BOUND_ONLY' if admissible else 'ILLUSTRATIVE_NOT_CERTIFIED',
        'blockers': blockers,
        'physical_validated': False,
        'human_acceleration_certified': False,
        'product': 'ABSTAIN_UNCALIBRATED',
        'release': 'BLOCKED',
    }

def frozen_case(accel, fps, b0='9/10', b1='9/10'):
    return dict(b0=b0,b1=b1,threshold='1/5',
                max_unobserved_gap_s=f'1/{fps}',
                max_abs_aperture_accel_s2=str(accel),
                endpoint_observable='pointwise_anatomical_aperture',
                acceleration_source='sampled_second_difference',
                attestations={k:False for k in ATTESTATIONS})

def run_frozen():
    cases = {'30fps_A3000': frozen_case(3000,30),
             '30fps_A5040': frozen_case(5040,30),
             '30fps_A6000': frozen_case(6000,30),
             '240fps_A6000': frozen_case(6000,240),
             '30fps_asymmetric_A6000': frozen_case(6000,30,'4/5','9/10')}
    return {name:evaluate(case) for name,case in cases.items()}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument('--frozen',action='store_true')
    group.add_argument('--input')
    a=p.parse_args()
    result=run_frozen() if a.frozen else evaluate(json.loads(open(a.input,encoding='utf-8').read()))
    if a.frozen:
        assert ([result[k]['equal_endpoint_dimensionless_Q'] for k in
                 ('30fps_A3000','30fps_A5040','30fps_A6000','240fps_A6000')] ==
                ['25/42','1','25/21','25/1344'])
        assert ([result[k]['conditional_geometry'] for k in
                 ('30fps_A3000','30fps_A5040','30fps_A6000','240fps_A6000')] ==
                ['NO_HIDDEN_CROSSING','HIDDEN_CROSSING_FEASIBLE','HIDDEN_CROSSING_FEASIBLE','NO_HIDDEN_CROSSING'])
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
