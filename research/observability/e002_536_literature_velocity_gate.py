#!/usr/bin/env python3
"""E002-536: literature velocity priors are not hard eyelid-aperture certificates.

Research-only exact-rational stress test; no physical or human measurements.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import json

REQUIRED = (
    'continuous_time_hard_bound',
    'same_session_paired_aperture_scale',
    'independent_anatomical_reference',
    'photodiode_authenticated_exposure',
    'authenticated_frame_clock',
    'native_missingness_audited',
    'nuisance_envelope_verified',
)
SPEED_TYPES = ('aperture_derivative', 'upper_lid_only', 'cohort_mean', 'sampled_peak')


def ratio(value):
    if isinstance(value, bool) or value is None:
        raise ValueError('invalid rational')
    try:
        out = Q(str(value))
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise ValueError('invalid rational') from exc
    return out


def evaluate(case):
    if not isinstance(case, dict):
        raise ValueError('case must be an object')
    v = ratio(case.get('speed_mm_s'))
    aperture = ratio(case.get('aperture_mm'))
    b, c = ratio(case.get('endpoint_aperture')), ratio(case.get('closure_threshold'))
    t, e = ratio(case.get('period_s')), ratio(case.get('exposure_s'))
    if v <= 0 or aperture <= 0 or not 0 <= c < b <= 1 or not 0 < e <= t:
        raise ValueError('invalid speed, scale, endpoint, threshold, period or exposure')
    if case.get('speed_observable') not in SPEED_TYPES:
        raise ValueError('unknown speed observable')
    evidence = case.get('attestations')
    if not isinstance(evidence, dict) or any(type(evidence.get(k)) is not bool for k in REQUIRED):
        raise ValueError('all attestation fields must be explicit booleans')
    dwell = case.get('dwell_evidence')
    if dwell not in ('none', 'group_mean', 'eventwise_hard_minimum'):
        raise ValueError('invalid dwell evidence')
    normalized = v / aperture
    r = normalized * (t - e) / (2 * (b - c))
    hard = case['speed_observable'] == 'aperture_derivative' and all(evidence[k] for k in REQUIRED)
    blockers = []
    if case['speed_observable'] != 'aperture_derivative':
        blockers.append('SPEED_OBSERVABLE_NOT_HARD_APERTURE_DERIVATIVE')
    blockers.extend('MISSING_'+k.upper() for k in REQUIRED if not evidence[k])
    if dwell == 'group_mean':
        blockers.append('GROUP_MEAN_DWELL_NOT_EVENTWISE_MINIMUM')
    decision = 'CONDITIONAL_BOUND_ONLY' if hard else 'ILLUSTRATIVE_NOT_CERTIFIED'
    return {
        'experiment': 'E002-536',
        'evidence_tier': 'PRIMARY_LITERATURE_STRESS_NOT_PHYSICAL_VALIDATION',
        'normalized_speed_s_inverse': str(normalized),
        'dimensionless_gap_ratio': str(r),
        'geometric_condition_if_hard_bound': 'NO_HIDDEN_CROSSING' if r < 1 else 'HIDDEN_CROSSING_NOT_EXCLUDED',
        'decision': decision,
        'blockers': blockers,
        'group_mean_dwell_is_minimum': False,
        'physical_validated': False,
        'can_certify_product_hidden_closure_exclusion': False,
        'product': 'ABSTAIN_UNCALIBRATED',
        'release': 'BLOCKED',
    }


def frozen_case(fps):
    return dict(speed_mm_s='243', aperture_mm='49/5',
                endpoint_aperture='1', closure_threshold='1/5',
                period_s=f'1/{fps}', exposure_s='1/1000',
                speed_observable='cohort_mean',
                dwell_evidence='group_mean',
                attestations={k: False for k in REQUIRED})


def run_frozen():
    return {'15fps': evaluate(frozen_case(15)),
            '30fps': evaluate(frozen_case(30))}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--frozen', action='store_true')
    p.add_argument('--input', type=str)
    a = p.parse_args()
    if a.frozen == bool(a.input):
        p.error('choose exactly one of --frozen or --input')
    data = run_frozen() if a.frozen else evaluate(json.loads(open(a.input, encoding='utf-8').read()))
    print(json.dumps(data, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
