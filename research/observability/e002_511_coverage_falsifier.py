#!/usr/bin/env python3
"""E002-511: frozen synthetic 299-person certificate-coverage falsification.

No human data, source images, or product claims. Two explicitly different
estimands: unconditional session failure vs conditional failure given coverage.
"""
import argparse
import json
import math
from e002_509_participant_power import evaluate

N = 299
COVERED = (0, 1, 8, 298, 299)


def independent_bound(k):
    return -math.expm1(math.log(0.05) / k) if k else None


def synthetic_cohort(k):
    return [
        dict(participant_id=f'synthetic_{i:03}', eligible_windows=5,
             certificates=int(i < k), false_exclusions=0,
             unresolved_certificates=0, reference_resolved=True)
        for i in range(N)
    ]


def experiment(phase):
    if phase not in ('prepatch', 'patched'):
        raise ValueError('INVALID_PHASE')
    rows = []
    for k in COVERED:
        actual = evaluate(synthetic_cohort(k))
        expected_gate = ('NO_USEFUL_COVERAGE' if k == 0 else
                         'PASSES_STATISTICAL_ZERO_EVENT_GATE_ONLY' if phase == 'prepatch' or k == N else
                         'INSUFFICIENT_COVERED_PARTICIPANTS')
        assert actual['risk_gate'] == expected_gate, (k, actual['risk_gate'], expected_gate)
        assert actual['participants_with_certificate'] == k
        assert actual['participants'] == N
        assert actual['release'] == 'BLOCKED'
        assert actual['product'] == 'ABSTAIN_UNCALIBRATED'
        bound = independent_bound(k)
        if phase == 'patched':
            assert actual['conditional_zero_failure_upper'] is None if k == 0 else (
                abs(actual['conditional_zero_failure_upper'] - bound) < 1e-13)
            assert abs(actual['unconditional_zero_failure_upper'] - independent_bound(N)) < 1e-13
            assert actual['conditional_risk_denominator'] == k
            assert actual['unconditional_risk_denominator'] == N
            assert abs(actual['certificate_participant_coverage'] - k / N) < 1e-13
        rows.append({
            'covered_participants': k,
            'all_enrolled': N,
            'observed_gate': actual['risk_gate'],
            'independent_conditional_95pct_upper': bound,
            'independent_unconditional_95pct_upper': independent_bound(N),
        })
    return {
        'experiment': 'E002-511',
        'phase': phase,
        'evidence': 'SYNTHETIC_COUNTS_ONLY',
        'rows': rows,
        'human_anatomical_ratings': 0,
        'physical_clock_authenticated': False,
        'continuous_speed_bound_certified': False,
        'product': 'ABSTAIN_UNCALIBRATED',
        'release': 'BLOCKED',
    }


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--phase', choices=('prepatch', 'patched'), required=True)
    args = ap.parse_args()
    print(json.dumps(experiment(args.phase), sort_keys=True, indent=2, allow_nan=False))
