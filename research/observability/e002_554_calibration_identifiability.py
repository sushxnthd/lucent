"""E002-554 exact-rational shutter-kernel calibration non-identifiability.

Research-only: no human, optical, photodiode or device measurements.
"""
from fractions import Fraction as F
import json

ONE = F(1)
HALF = F(1, 2)
THETA = F(3, 1000)
SEGMENTS = (
    (F(0), F(1, 10), 1),
    (F(1, 10), F(1, 5), -1),
    (F(1, 5), F(4, 5), 0),
    (F(4, 5), F(9, 10), -1),
    (F(9, 10), F(1), 1),
)


def kernel(sign):
    """Return piecewise-constant K=1+sign*q/2, sign=+1 or -1."""
    if sign not in (-1, 1):
        raise ValueError("kernel sign must be +/-1")
    return tuple((a, b, ONE + F(sign * q, 2)) for a, b, q in SEGMENTS)


def integral(k, power=0, lo=F(0), hi=F(1)):
    if not (F(0) <= lo <= hi <= ONE):
        raise ValueError("invalid pulse support")
    total = F(0)
    for a, b, w in k:
        left, right = max(a, lo), min(b, hi)
        if right > left:
            total += w * (right ** (power + 1) - left ** (power + 1)) / (power + 1)
    return total


def moments(k):
    mass = integral(k)
    if mass != ONE or any(w <= 0 for _, _, w in k):
        raise ValueError("not a positive normalized shutter kernel")
    center = integral(k, 1)
    variance = integral(k, 2) - center * center
    return mass, center, variance


def exposure_variance(k, width):
    return moments(k)[2] * width * width


def measured_quadratic(k, exposure_start, width):
    """Exact integral of f(t)=(t-1/2)^2 for t=start+width*x."""
    _, center, variance = moments(k)
    tcenter = exposure_start + width * center
    return (tcenter - HALF) ** 2 + width * width * variance


def exclusion_bound(observed0, observed1, claimed_kernel, width=HALF):
    """E002-553 midpoint envelope for equal exposures and A=2."""
    c0 = -F(1, 2) + width * moments(claimed_kernel)[1]
    c1 = ONE + width * moments(claimed_kernel)[1]
    assert (c0, c1) == (-F(1, 4), F(5, 4))
    d = c1 - c0
    variance = exposure_variance(claimed_kernel, width)
    return (observed0 + observed1) / 2 - variance - d * d / 4


def experiment():
    high, low = kernel(1), kernel(-1)
    highmom, lowmom = moments(high), moments(low)
    m0 = measured_quadratic(high, -HALF, HALF)
    m1 = measured_quadratic(high, ONE, HALF)
    assert m0 == m1
    bad = exclusion_bound(m0, m1, low)
    good = exclusion_bound(m0, m1, high)
    assert highmom[0] == lowmom[0] == ONE
    assert highmom[1] == lowmom[1] == HALF
    assert highmom[2] - lowmom[2] == F(2, 125)
    assert bad == F(1, 250) and good == 0
    assert bad > THETA > good
    for lo, hi in ((F(1, 4), F(3, 10)), (F(9, 20), F(11, 20)), (F(7, 10), F(3, 4))):
        assert integral(high, lo=lo, hi=hi) == integral(low, lo=lo, hi=hi)
    assert integral(high, lo=F(1, 20), hi=F(1, 10)) != integral(low, lo=F(1, 20), hi=F(1, 10))
    return {
        "evidence_tier": "EXACT_SYNTHETIC_ONLY",
        "kernel_mass": "1",
        "kernel_center": "1/2",
        "high_variance_normalized": str(highmom[2]),
        "low_variance_normalized": str(lowmom[2]),
        "variance_difference_normalized": str(highmom[2] - lowmom[2]),
        "observed_aperture_mean_each": str(m0),
        "wrong_kernel_lower_bound": str(bad),
        "correct_kernel_lower_bound": str(good),
        "closure_threshold": str(THETA),
        "actual_minimum": "0",
        "center_pulse_calibration_distinguishes": False,
        "edge_pulse_calibration_distinguishes": True,
        "physical_capture_count": 0,
        "human_rater_count": 0,
        "product": "ABSTAIN_UNCALIBRATED",
    }


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2, sort_keys=True))
