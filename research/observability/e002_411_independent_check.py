#!/usr/bin/env python3
"""Independent midpoint-quadrature oracle for E002-411 (no shared integration code)."""
from __future__ import annotations
import json
from e002_411_phase_identifiability import experiment, shutter_release_gate


def independent_integral(lo, hi, n=100000):
    """Numerically integrate shutter moment and sampled pulse responses."""
    exposure, step = 10.0, 10.0/n
    mass = moment = 0.
    signals = [0.]*10
    for i in range(n):
        t = (i+.5)*step
        if lo <= t < hi:
            density = 1/(hi-lo)
            mass += density*step
            moment += abs(t-5.)*density*step
            j = int(t)
            if j < 10 and j <= t <= j+.2:
                signals[j] += density*step
    return mass, moment, signals


def run():
    a = independent_integral(5.5, 5.7)
    b = independent_integral(9.5, 9.7)
    for numeric, expected in [(a, .6), (b, 4.6)]:
        assert abs(numeric[0]-1.) < .01
        assert abs(numeric[1]-expected) < .005
        assert max(numeric[2]) < .01
    assert abs((b[1]-a[1])-4.) < .005
    # Independent necessary-conditions controls; neither may release a product.
    dense = [i/10 for i in range(99)]
    checks = [
        dict(phases=range(10), pulse_ms=.2, exposure_ms=10., jitter_ms=.05,
             photodiode_verified=True, hardware_clock_verified=True,
             row_response_verified=True, physical_moment_bound_verified=True),
        dict(phases=dense, pulse_ms=.2, exposure_ms=10., jitter_ms=0.,
             photodiode_verified=False, hardware_clock_verified=True,
             row_response_verified=True, physical_moment_bound_verified=True),
        dict(phases=dense, pulse_ms=.2, exposure_ms=10., jitter_ms=0.,
             photodiode_verified=True, hardware_clock_verified=False,
             row_response_verified=True, physical_moment_bound_verified=True),
        dict(phases=dense, pulse_ms=.2, exposure_ms=10., jitter_ms=0.,
             photodiode_verified=True, hardware_clock_verified=True,
             row_response_verified=False, physical_moment_bound_verified=True),
        dict(phases=dense, pulse_ms=.2, exposure_ms=10., jitter_ms=0.,
             photodiode_verified=True, hardware_clock_verified=True,
             row_response_verified=True, physical_moment_bound_verified=False),
    ]
    gates = [shutter_release_gate(**kwargs) for kwargs in checks]
    assert all(g["instrument_status"] == "REJECT" for g in gates)
    assert all(g["product"] == "ABSTAIN_UNCALIBRATED" for g in gates)
    dense_all = shutter_release_gate(phases=dense, pulse_ms=.2,
        exposure_ms=10., jitter_ms=0., photodiode_verified=True,
        hardware_clock_verified=True, row_response_verified=True,
        physical_moment_bound_verified=True)
    assert dense_all["instrument_status"] == "NECESSARY_CHECKS_ONLY"
    assert dense_all["product"] == "ABSTAIN_UNCALIBRATED"
    report = experiment()
    assert report["indistinguishable_pairs"] == 1000
    return dict(oracle="independent midpoint quadrature",
        midpoint_bins=100000, center_moment_ms=a[1], edge_moment_ms=b[1],
        moment_separation_ms=b[1]-a[1], independent_controls_passed=len(gates)+1,
        product="ABSTAIN_UNCALIBRATED")


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
