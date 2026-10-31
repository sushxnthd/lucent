#!/usr/bin/env python3
"""E002-547: exact boxcar-integrated reference sensitivity counterexample.

Hypothetical aperture only. No human/camera data, no certified shutter model.
"""
import argparse
import json
from fractions import Fraction as F

B, C, T = F(9, 10), F(1, 5), F(1, 100)
V = 2 * B / T
APEX = T / 2
CRITICAL = 4 * C / V


def aperture(t):
    t = F(t)
    if t < 0 or t > T:
        return B
    return V * abs(t - APEX)


def primitive(t):
    """Integral of a(u) du from 0 to t, continuous at 0, apex and T."""
    t = F(t)
    if t < 0:
        return B * t
    if t <= APEX:
        return B * t - V * t * t / 2
    half_area = B * APEX / 2
    x = t - APEX
    if t <= T:
        return half_area + V * x * x / 2
    return B * T / 2 + B * (t - T)


def exposure_mean(center, duration):
    center, duration = F(center), F(duration)
    if duration <= 0:
        raise ValueError("exposure duration must be positive")
    return (primitive(center + duration / 2) - primitive(center - duration / 2)) / duration


def phase_positive_width_4ms():
    # Algebraic, not estimated by search; exact square-root in this fixture.
    length = F(1, 250)
    half = F(1, 1500)
    assert half * half == length * (C / V - length / 4)
    assert exposure_mean(APEX + half, length) == C
    assert exposure_mean(APEX - half, length) == C
    assert exposure_mean(APEX + half + F(1, 1000000), length) > C
    assert exposure_mean(APEX - half - F(1, 1000000), length) > C
    assert exposure_mean(APEX, length) < C
    return 2 * half


def uniform_phase_probability(fps, width):
    if fps <= 0 or width < 0:
        raise ValueError("invalid rate or interval width")
    return min(F(1), F(fps) * width)


def numerical_midpoint(center, duration, n=100000):
    # Independent approximate midpoint quadrature (no analytic primitive).
    center, duration = F(center), F(duration)
    lo = float(center - duration / 2)
    step = float(duration) / n
    return sum(float(aperture(F.from_float(lo + (i + .5) * step))) for i in range(n)) / n


def self_test():
    assert V == 180
    assert CRITICAL == F(1, 225)
    assert primitive(F(0)) == 0
    assert primitive(APEX) == F(9, 4000)
    assert primitive(T) == F(9, 2000)
    for x in [F(-1, 100), F(0), F(1, 1000), APEX, F(9, 1000), T, F(2, 100)]:
        assert F(0) <= aperture(x) <= B
    for length, center_mean in [(F(1, 250), F(9, 50)),
                                (F(1, 200), F(9, 40)),
                                (F(1, 100), F(9, 20))]:
        assert exposure_mean(APEX, length) == center_mean
        for offset in [F(1, 10000), F(1, 1000), F(1, 200)]:
            assert exposure_mean(APEX - offset, length) == exposure_mean(APEX + offset, length)
            assert exposure_mean(APEX + offset, length) >= center_mean
    assert exposure_mean(APEX, CRITICAL) == C
    assert exposure_mean(APEX, F(1, 200)) > C
    assert exposure_mean(APEX, F(1, 100)) > C
    width = phase_positive_width_4ms()
    assert width == F(1, 750)
    assert uniform_phase_probability(200, width) == F(4, 15)
    assert uniform_phase_probability(240, width) == F(8, 25)
    assert uniform_phase_probability(200, F(0)) == 0
    assert uniform_phase_probability(100, F(0)) == 0
    assert uniform_phase_probability(200, F(1, 450)) == F(4, 9)
    for length in [F(1, 250), F(1, 200), F(1, 100)]:
        for offset in [F(0), F(1, 1000), F(3, 1000)]:
            exact = float(exposure_mean(APEX + offset, length))
            assert abs(numerical_midpoint(APEX + offset, length, 20000) - exact) < 1e-7
    for bad in [F(0), F(-1, 1000)]:
        try:
            exposure_mean(APEX, bad)
        except ValueError:
            pass
        else:
            raise AssertionError("nonpositive exposure accepted")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        self_test()
    width = phase_positive_width_4ms()
    out = {
        'experiment': 'E002-547',
        'evidence': 'exact synthetic boxcar model, not human or calibrated camera',
        'critical_exposure_s': str(CRITICAL),
        'reference_cases': [
            {'fps': 200, 'exposure_s': '1/250', 'minimum_mean': str(exposure_mean(APEX, F(1,250))), 'detection_probability': str(uniform_phase_probability(200, width)), 'instantaneous_probability': '4/9'},
            {'fps': 240, 'exposure_s': '1/250', 'minimum_mean': str(exposure_mean(APEX, F(1,250))), 'detection_probability': str(uniform_phase_probability(240, width)), 'instantaneous_probability': '8/15'},
            {'fps': 200, 'exposure_s': '1/200', 'minimum_mean': str(exposure_mean(APEX, F(1,200))), 'detection_probability': '0', 'instantaneous_probability': '4/9'},
            {'fps': 100, 'exposure_s': '1/100', 'minimum_mean': str(exposure_mean(APEX, F(1,100))), 'detection_probability': '0', 'instantaneous_probability': '2/9'},
        ],
        'human_sequences_tested': 0,
        'release': 'BLOCKED',
        'product': 'ABSTAIN_UNCALIBRATED',
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
