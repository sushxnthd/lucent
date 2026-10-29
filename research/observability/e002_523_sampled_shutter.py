#!/usr/bin/env python3
"""E002-523 exact finite-sampling shutter-response counterexample.

Instrument-model falsification only. Not an optical measurement or human result.
"""
import argparse
from fractions import Fraction as F
import json

T = F(10)
ALPHA = F(1, 50)
DIP_WIDTH = F(4, 5)
THETA = F(1, 5)
OPEN = F(201, 1000)
A_CENTER = F(3, 2)
B_CENTER = F(11, 2)
SAMPLE_TIMES = tuple(F(i) for i in range(11))


def tent(t, center, width, area):
    """Piecewise-linear nonnegative triangular pulse with integral area."""
    d = abs(t - center)
    if d >= width / 2:
        return F(0)
    return (2 * area / width) * (1 - 2 * d / width)


def q0(t):
    return 1 / T if 0 <= t <= T else F(0)


def q1(t, width):
    if not 0 <= t <= T:
        return F(0)
    return 1 / T + tent(t, A_CENTER, width, ALPHA) - tent(t, B_CENTER, DIP_WIDTH, ALPHA)


def closure_mean(width):
    if not 0 < width < F(1):
        raise ValueError('INVALID_UNSAMPLED_TENT_WIDTH')
    mass_closed = width / T + ALPHA
    return OPEN * (1 - mass_closed)


def lower_duration(mean, cap):
    if cap is None:
        return None  # never derive cap from finite point samples
    if not isinstance(cap, F) or cap < 1 or mean < 0:
        raise ValueError('INVALID_INDEPENDENT_CAP')
    return max(F(0), T * (1 - mean / THETA) / cap)


def sampled_response_cap(samples, delta=None, lipschitz=None, independently_attested=False):
    """Conditional cap from external Lipschitz and sample-error bounds.

    This program cannot authenticate independently_attested.
    """
    if not independently_attested or delta is None or lipschitz is None:
        return None
    if not samples or delta < 0 or lipschitz < 0:
        raise ValueError('INVALID_CALIBRATION_INPUT')
    times = [t for t, _ in samples]
    values = [y for _, y in samples]
    if (times[0] < 0 or times[-1] > T or
            any(b <= a for a, b in zip(times, times[1:])) or
            any(y < 0 for y in values)):
        raise ValueError('INVALID_SAMPLES')
    h = max([times[0], T - times[-1]] + [(b - a) / 2 for a, b in zip(times, times[1:])])
    R = T * (max(values) + delta + lipschitz * h)
    if R < 1:
        raise ValueError('CALIBRATION_INCONSISTENT_WITH_NORMALIZATION')
    return R


def fmt(x):
    return {'fraction': str(x), 'decimal': float(x)}


def evaluate(width):
    m = closure_mean(width)
    observed = tuple((t, q0(t), q1(t, width)) for t in SAMPLE_TIMES)
    if not all(a == b for _, a, b in observed):
        raise AssertionError('SAMPLES_NOT_IDENTICAL')
    if 2 * ALPHA / DIP_WIDTH > 1 / T:
        raise AssertionError('NEGATIVE_RESPONSE')
    integral = T / T + ALPHA - ALPHA
    if integral != 1:
        raise AssertionError('NOT_NORMALIZED')
    if not m < THETA:
        raise AssertionError('FROZEN_MEAN_NOT_BELOW_THRESHOLD')
    true_R = 1 + 2 * ALPHA * T / width
    naive_R = T * max(q0(t) for t in SAMPLE_TIMES)
    naive = lower_duration(m, naive_R)
    true = lower_duration(m, true_R)
    if not naive > width or not true <= width:
        raise AssertionError('FALSIFICATION_DID_NOT_HOLD')
    return {
        'width_ms': fmt(width), 'sampled_response_values_equal': True,
        'sample_count': len(observed), 'integral_q0_q1': fmt(integral),
        'min_q1_ms_inverse': fmt(1 / T - 2 * ALPHA / DIP_WIDTH),
        'world0_weighted_mean': fmt(m), 'world1_weighted_mean': fmt(m),
        'world0_closed_duration_ms': fmt(T),
        'world1_closed_duration_ms': fmt(width),
        'sampled_peak_R_hat': fmt(naive_R), 'actual_R1': fmt(true_R),
        'unsafe_naive_lower_ms': fmt(naive), 'valid_true_cap_lower_ms': fmt(true),
        'point_samples_only_decision': 'ABSTAIN_UNCALIBRATED',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='-')
    args = parser.parse_args()
    out = {
        'experiment': 'E002-523', 'evidence_tier': 'exact synthetic instrument falsification',
        'not_measured': ['human anatomy', 'camera shutter', 'photodiode', 'human eyelid speed'],
        'frozen_worlds': [evaluate(F(1, 100)), evaluate(F(1, 10000))],
        'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED',
    }
    rendered = json.dumps(out, indent=2)
    if args.output == '-':
        print(rendered)
    else:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(rendered + '\n')


if __name__ == '__main__':
    main()
