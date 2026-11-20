#!/usr/bin/env python3
"""E002-524 exact high-speed reference-witness phase boundaries.

Pure sampling geometry. Not an anatomical observation or shutter calibration.
"""
import argparse
from fractions import Fraction as F
import json


def validate(period, exposure, uncertainty=F(0)):
    for v in (period, exposure, uncertainty):
        if not isinstance(v, F):
            raise TypeError('EXACT_RATIONAL_INPUT_REQUIRED')
    if period <= 0 or exposure <= 0 or exposure >= period or uncertainty < 0:
        raise ValueError('INVALID_REFERENCE_ACQUISITION_MODEL')


def bounds(period, exposure, uncertainty=F(0), verified_gap=None):
    """Exact periodic boundaries; robust full-witness sufficient condition."""
    validate(period, exposure, uncertainty)
    if verified_gap is not None and (not isinstance(verified_gap, F) or verified_gap <= 0):
        raise ValueError('INVALID_VERIFIED_GAP')
    G = period if verified_gap is None else verified_gap
    return {
        'ideal_positive_overlap_strict_gt': period - exposure,
        'ideal_full_witness_strict_gt': period + exposure,
        'robust_full_witness_strict_gt': G + exposure + 2 * uncertainty,
        'ideal_blind_gap': period - exposure,
    }


def phase_without_overlap(period, exposure, duration):
    """Phase placing a closure inside the reference blind gap."""
    validate(period, exposure)
    if not isinstance(duration, F) or duration < 0 or duration > period - exposure:
        raise ValueError('NO_OVERLAP_PHASE_NOT_AVAILABLE')
    return period - exposure


def phase_without_strict_full(period, exposure, duration):
    """Phase with no exposure strictly contained in the closure interval."""
    validate(period, exposure)
    if not isinstance(duration, F) or duration < 0 or duration > period + exposure:
        raise ValueError('NO_FULL_WITNESS_PHASE_NOT_AVAILABLE')
    if duration <= exposure:
        return F(0)
    window = duration - exposure
    if window == period:
        return F(0)  # exposures touch only the event boundaries
    return (window + period) / 2


def has_positive_overlap(period, exposure, duration, phase):
    validate(period, exposure)
    if not isinstance(duration, F) or duration < 0 or not isinstance(phase, F) or not 0 <= phase < period:
        raise ValueError('INVALID_EVENT_OR_PHASE')
    for k in range(-2, int(duration // period) + 3):
        a, b = phase + k * period, phase + k * period + exposure
        if max(F(0), a) < min(duration, b):
            return True
    return False


def has_strict_full(period, exposure, duration, phase, uncertainty=F(0)):
    validate(period, exposure, uncertainty)
    if not isinstance(duration, F) or duration < 0 or not isinstance(phase, F) or not 0 <= phase < period:
        raise ValueError('INVALID_EVENT_OR_PHASE')
    for k in range(-2, int(duration // period) + 3):
        a, b = phase + k * period, phase + k * period + exposure
        if a - uncertainty > 0 and b + uncertainty < duration:
            return True
    return False


def gate_reference_claim(period, exposure, duration, uncertainty=F(0),
                         *, verified_gap=None, native_indices_authenticated=False,
                         shutter_calibrated=False, clock_calibrated=False,
                         anatomy_two_independent_raters=False,
                         cross_camera_transport_calibrated=False,
                         duration_independently_attested=False):
    """All flags are external attestations; program cannot authenticate them."""
    b = bounds(period, exposure, uncertainty, verified_gap)
    flags = (native_indices_authenticated, shutter_calibrated, clock_calibrated,
             anatomy_two_independent_raters, cross_camera_transport_calibrated,
             duration_independently_attested)
    if not all(type(x) is bool for x in flags):
        raise ValueError('INVALID_EVIDENCE_FLAG')
    if not isinstance(duration, F) or duration <= 0:
        raise ValueError('INVALID_DURATION')
    if not all(flags) or verified_gap is None:
        return 'ABSTAIN_UNCALIBRATED'
    return ('CONDITIONAL_FULL_WITNESS_OPPORTUNITY' if duration > b['robust_full_witness_strict_gt']
            else 'REFERENCE_CENSORED_OR_PHASE_DEPENDENT')


def f(x):
    return {'fraction': str(x), 'decimal': float(x)}


def case(label, period, exposure, uncertainty=F(0), verified_gap=None):
    b = bounds(period, exposure, uncertainty, verified_gap)
    return {'name': label, 'period_ms': f(period), 'exposure_ms': f(exposure),
            'uncertainty_each_endpoint_ms': f(uncertainty),
            'verified_max_start_gap_ms': f(period if verified_gap is None else verified_gap),
            'ideal_positive_overlap_guarantee_if_duration_strictly_gt_ms': f(b['ideal_positive_overlap_strict_gt']),
            'ideal_strict_full_witness_guarantee_if_duration_strictly_gt_ms': f(b['ideal_full_witness_strict_gt']),
            'robust_strict_full_witness_guarantee_if_duration_strictly_gt_ms': f(b['robust_full_witness_strict_gt'])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', default='-')
    args = ap.parse_args()
    out = {'experiment': 'E002-524', 'evidence_tier': 'exact prospective instrument geometry; no human measurements',
           'cases': [case('240Hz_1ms', F(25, 6), F(1)),
                     case('240Hz_1ms_0p1ms_clock', F(25, 6), F(1), F(1, 10)),
                     case('1000Hz_0p5ms', F(1), F(1, 2)),
                     case('240Hz_one_missing_native_frame', F(25, 6), F(1), verified_gap=F(25, 3))],
           'independent_human_ratings': 0, 'authenticated_physical_captures': 0,
           'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}
    data = json.dumps(out, indent=2) + '\n'
    if args.output == '-':
        print(data, end='')
    else:
        with open(args.output, 'w', encoding='utf-8') as h:
            h.write(data)


if __name__ == '__main__':
    main()
