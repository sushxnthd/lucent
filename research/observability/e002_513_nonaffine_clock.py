#!/usr/bin/env python3
"""E002-513: exact two-world clock counterexample; no physical certification.

Tests inference from long-span optical anchors WITHOUT an independently
validated affine clock. Does not falsify E002-506's explicitly affine model.
"""
from decimal import Decimal, localcontext
from fractions import Fraction
import json

N = 300
TARGET = 150
SPIKE = Fraction(1, 500)  # 2 ms; frozen before execution
PERIOD = Fraction(1, 30)
EXPOSURE = Fraction(1, 100)


def build_world(*, n=N, target=TARGET, spike=SPIKE):
    if type(n) is not int or n < 2 or type(target) is not int or not 0 <= target < n:
        raise ValueError('INVALID_FRAME_GEOMETRY')
    if not isinstance(spike, Fraction) or spike < 0:
        raise ValueError('INVALID_CLOCK_SPIKE')
    baseline = Fraction(10, n)
    others = baseline - spike / (n-1)
    if others < EXPOSURE or baseline + spike < EXPOSURE:
        raise ValueError('INVALID_EXPOSURE_SEPARATION')
    intervals = [others] * n
    intervals[target] = baseline + spike
    starts = [Fraction(0)]
    for period in intervals:
        starts.append(starts[-1] + period)
    if starts[-1] != Fraction(10):
        raise AssertionError('ANCHOR_MISMATCH')
    return starts


def decimal_of(x):
    return Decimal(x.numerator) / Decimal(x.denominator)


def risk_at_local_gap(gap, *, threshold='0.2'):
    if not isinstance(gap, Fraction) or gap < EXPOSURE:
        raise ValueError('INVALID_LOCAL_GAP')
    with localcontext() as ctx:
        ctx.prec = 70
        v, w, b, err, th = Decimal('60'), decimal_of(EXPOSURE), Decimal('0.999'), Decimal('0.001'), Decimal(threshold)
        if not 0 < th < 1:
            raise ValueError('INVALID_THRESHOLD')
        eta = 1-b+err
        d = min(Decimal(1), (2*v*w*eta).sqrt()) if eta <= v*w/2 else min(Decimal(1), eta+v*w/2)
        h = decimal_of(gap) - w
        risk = d + v*h/2
        return {'risk_upper': str(+risk), 'blind_gap_seconds': str(+h),
                'conditional_scalar_result': 'CONDITIONAL_EXCLUSION' if 1-th-risk > Decimal('1e-20') else 'NOT_EXCLUDED_OR_BOUNDARY'}


def maximum_local_period(span, count, minimum_period):
    """Sharp envelope from total span and certified minimum of OTHER intervals.

    For zero minimum, this is a supremum under strict monotonicity.
    Does not calibrate a physical clock.
    """
    if type(count) is not int or count < 2 or not isinstance(span, Fraction) or not isinstance(minimum_period, Fraction):
        raise ValueError('INVALID_ENVELOPE_INPUT')
    if span <= 0 or minimum_period < 0 or count*minimum_period > span:
        raise ValueError('INFEASIBLE_ENVELOPE')
    return span - (count-1)*minimum_period


def falsify():
    a = build_world(spike=Fraction(0))
    b = build_world()
    if a[0] != b[0] or a[-1] != b[-1] or len(a) != len(b):
        raise AssertionError('OBSERVATIONS_DIFFER')
    ga, gb = a[TARGET+1]-a[TARGET], b[TARGET+1]-b[TARGET]
    ra, rb = risk_at_local_gap(ga), risk_at_local_gap(gb)
    if not (ra['conditional_scalar_result'] == 'CONDITIONAL_EXCLUSION'
            and rb['conditional_scalar_result'] == 'NOT_EXCLUDED_OR_BOUNDARY'):
        raise AssertionError('FROZEN_PREDICTION_NOT_REPRODUCED')
    return {'experiment': 'E002-513', 'evidence_tier': 'EXACT_SYNTHETIC_NONAFFINE_CLOCK_COUNTEREXAMPLE',
            'optical_anchor_frames': [0, N], 'optical_anchor_times_seconds': ['0', '10'],
            'all_frames_present_in_both_worlds': True,
            'world_a_target_period_seconds': str(ga), 'world_b_target_period_seconds': str(gb),
            'target_gap_inflation_seconds': str(gb-ga),
            'world_a': ra, 'world_b': rb,
            'intermediate_frame_timing_distinguishes_worlds': a[TARGET+1] != b[TARGET+1],
            'long_span_anchors_certify_local_gap': False,
            'affine_model_falsified': False,
            'independent_physical_clock_authenticated': False,
            'physical_shutter_calibrated': False,
            'continuous_time_human_speed_certified': False,
            'human_anatomical_ratings_obtained': False,
            'physical_hidden_closure_certified': False,
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}


if __name__ == '__main__':
    print(json.dumps(falsify(), sort_keys=True, indent=2))
