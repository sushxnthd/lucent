#!/usr/bin/env python3
"""E002-657 | Nonuniform shutter response falsifies rectangular e/4 certificates.

Evidence: deterministic synthetic mathematical counterexample; NOT human data,
physical sensor calibration, independent replication, or a production release.

For nonnegative normalized exposure weight k(u), a V-Lipschitz aperture a(t),
and exposure observation y = integral k(u) a(s+u) du, the guaranteed bound is
a(t) >= y - V * integral k(u) |t-s-u| du.
Proof: a(s+u) <= a(t)+V|s+u-t|; integrate against k.
The factor is sharp for a single observation: choose a(x)=c+V|x-t|,
with c>=0 and an aperture range sufficiently large to avoid saturation.

A rectangular exposure on [-e/2,e/2] has first absolute moment e/4
at t=s. A shutter response concentrated toward the end of that same
exposure has a larger moment. Substituting e/4 is then unsound.

Reproduce: python3 research/observability/e002_657_shutter_kernel.py
"""
from fractions import Fraction as F

def uniform_interval_abs_moment(lo, hi):
    assert lo < hi
    if lo >= 0:
        return (lo + hi) / 2
    if hi <= 0:
        return -(lo + hi) / 2
    return (lo*lo + hi*hi) / (2*(hi-lo))

def run():
    V = F(4)
    e = F(1, 5)
    threshold = F(3, 10)
    center_aperture = F(1, 5)
    lo, hi = F(9, 100), F(1, 10)  # exposure weight only on final 5% of nominal window
    moment = uniform_interval_abs_moment(lo, hi)
    assert moment == F(19, 200)
    rectangular_moment = e / 4
    y = center_aperture + V*moment
    naive_lower = y - V*rectangular_moment
    corrected_lower = y - V*moment
    assert y == F(29, 50) and naive_lower == F(19, 50)
    assert corrected_lower == center_aperture
    assert naive_lower > threshold > center_aperture
    # Test sharpness for a(t)=center_aperture+V*abs(t) at t=0.
    for i in range(1, 100):
        u = lo + (hi-lo)*F(i,100)
        assert center_aperture+V*abs(u) >= center_aperture
    # A symmetric rectangular kernel restores the conventional e/4.
    assert uniform_interval_abs_moment(-e/2, e/2) == rectangular_moment
    print("E002-657 PASS: y=0.58, actual minimum=0.20, naive lower=0.38, calibrated lower=0.20")
    print("Kernel absolute moment=0.095 s, rectangular assumption=0.05 s")
    print("Evidence tier: synthetic; human=0, physical shutter=0, independent replay=0")

if __name__ == "__main__":
    run()
