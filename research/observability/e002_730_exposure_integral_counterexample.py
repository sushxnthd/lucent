"""E002-730: exposure integration is not a pointwise aperture certificate.

Evidence: exact-rational synthetic counterexample, NOT human or physical data.
A normalized aperture a(t)=min(1,V*abs(t-1/2)) on [0,1] has
a(0)=a(1)=1, a(1/2)=0, and box-exposure mean 1-1/V for V>=2.
At V=4/s, mean=0.75 despite a full hidden closure.

Product consequence: never substitute an exposure-integrated mean or
frame-level brightness proxy for a pointwise aperture lower bound in
E002-371. Without a calibrated inverse exposure/geometry model,
ABSTAIN_UNCALIBRATED. This is a falsification of that substitution,
not an empirical test of E002-371 itself.

Physical follow-up: record an independently timestamped occluder moving
through a calibrated aperture at controlled velocities; simultaneously
collect short- and long-exposure camera observations, blind the
certificate algorithm to the high-rate reference, and compare false
exclusions under brightness, blur, rolling shutter, missingness, gaze
proxy, clock jitter, and optical geometry perturbations.
"""
from fractions import Fraction as F


def aperture(t, velocity=F(4), center=F(1, 2)):
    return min(F(1), velocity * abs(t - center))


def integrated_aperture(velocity=F(4)):
    # Exact area for the triangular deficit, provided velocity >= 2.
    assert velocity >= 2
    return F(1) - F(1) / velocity


def main():
    v = F(4)
    assert aperture(F(0), v) == aperture(F(1), v) == 1
    assert aperture(F(1, 2), v) == 0
    assert integrated_aperture(v) == F(3, 4)
    for v in (F(2), F(4), F(8), F(16)):
        assert integrated_aperture(v) == 1 - F(1) / v
        assert aperture(F(1, 2), v) == 0
    print("PASS: exact synthetic counterexample V=4/s, mean=3/4, min=0")


if __name__ == "__main__":
    main()
