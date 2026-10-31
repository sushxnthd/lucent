#!/usr/bin/env python3
"""E002-546: exact, hypothetical reference-camera aliasing falsifier.

Not human physiology, a certified motion bound, or camera shutter calibration.
Only stdlib. No image/data download. Exact rational arithmetic.
"""
import argparse
import json
from fractions import Fraction as F

B = F(9, 10)
C = F(1, 5)
T = F(1, 100)
W = T * C / B
FREQUENCIES = (30, 100, 200, 240, 500)


def aperture(t):
    """Symmetric triangular closure, with open aperture outside [0,T]."""
    if t < 0 or t > T:
        return B
    if t <= T / 2:
        return B * (1 - 2 * t / T)
    return B * (2 * t / T - 1)


def min_sampled_aperture(fps, phase):
    period = F(1, fps)
    if not (0 <= phase < period):
        raise ValueError("phase outside one sample period")
    times = []
    t = phase
    while t <= T:
        times.append(t)
        t += period
    return min((aperture(t) for t in times), default=B)


def phase_detection_probability(fps):
    """Lebesgue phase fraction for ideal instantaneous periodic sampling."""
    return min(F(1), W * fps)


def as_record(fps):
    p = phase_detection_probability(fps)
    return {
        "fps": fps,
        "detection_probability_uniform_phase": str(p),
        "miss_probability_uniform_phase": str(1 - p),
        "worst_phase_can_miss": W < F(1, fps),
    }


def self_test():
    assert W == F(1, 450)
    assert 2 * B / T == 180
    expected = {30: F(1, 15), 100: F(2, 9),
                200: F(4, 9), 240: F(8, 15), 500: F(1)}
    for fps, p in expected.items():
        assert phase_detection_probability(fps) == p
        assert phase_detection_probability(fps) + (1-p) == 1
    assert aperture(F(0)) == B
    assert aperture(T / 2) == 0
    assert aperture(T) == B
    assert min_sampled_aperture(100, F(0)) == B
    assert min_sampled_aperture(200, F(1, 400)) == F(9, 20)
    assert min_sampled_aperture(200, F(1, 400)) > C
    assert min_sampled_aperture(200, F(0)) == 0
    assert not phase_detection_probability(500) < 1
    for bad in (-F(1, 1000), F(1, 100)):
        try:
            min_sampled_aperture(100, bad)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid phase accepted")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    result = {
        "experiment": "E002-546",
        "evidence_tier": "exact hypothetical sampling model; no human measurements",
        "aperture_open": str(B),
        "closure_threshold": str(C),
        "closure_duration_s": str(T),
        "constructed_max_speed_per_s": str(2 * B / T),
        "threshold_contact_width_s": str(W),
        "reference_rates": [as_record(f) for f in FREQUENCIES],
        "adversarial_100fps_phase_0_min_aperture": str(min_sampled_aperture(100, F(0))),
        "adversarial_200fps_phase_1_over_400_min_aperture": str(min_sampled_aperture(200, F(1, 400))),
        "human_sequences_tested": 0,
        "release": "BLOCKED",
        "product": "ABSTAIN_UNCALIBRATED",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
