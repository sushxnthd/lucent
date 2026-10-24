#!/usr/bin/env python3
"""E002-411: sparse LED pulse scans do not identify an arbitrary shutter kernel.

Synthetic instrument only; no real camera, eyelid aperture, or human validation.
Preregistered in E002_411_FROZEN.md at commit 1726e08.
"""
from __future__ import annotations
import json
import math
import random

EXPOSURE_MS = 10.0
PULSE_MS = 0.2
SPARSE_PHASES_MS = tuple(float(j) for j in range(10))


def overlap(a, b, c, d):
    return max(0.0, min(b, d) - max(a, c))


def pulse_response(shutter, phases, pulse_ms=PULSE_MS, jitter_ms=0.0):
    """Exact normalized response of a rectangular shutter to rectangular pulses."""
    a, b = shutter
    if not (0 <= a < b <= EXPOSURE_MS):
        raise ValueError("Invalid shutter support")
    if pulse_ms <= 0 or jitter_ms < 0:
        raise ValueError("Invalid pulse width/jitter")
    return [overlap(a, b, p - jitter_ms, p + pulse_ms + jitter_ms) / (b - a)
            for p in phases]


def first_abs_moment_ms(shutter, center_ms=EXPOSURE_MS / 2):
    """Exact mean |t-center| for a normalized rectangular shutter."""
    a, b = shutter
    if a >= b:
        raise ValueError("Invalid shutter")
    if b <= center_ms:
        return center_ms - (a + b) / 2
    if a >= center_ms:
        return (a + b) / 2 - center_ms
    return ((center_ms-a)**2 + (b-center_ms)**2) / (2*(b-a))


def uncovered_support_ms(phases, pulse_ms, exposure_ms, jitter_ms=0.0):
    """Lebesgue length of exposure support not illuminated by any scanned pulse."""
    if (not phases or pulse_ms <= 0 or exposure_ms <= 0 or jitter_ms < 0
            or not all(math.isfinite(x) for x in phases)):
        raise ValueError("Missing/invalid calibrated phases")
    intervals = sorted((max(0., p-jitter_ms),
                        min(exposure_ms, p+pulse_ms+jitter_ms))
                       for p in phases)
    right = 0.
    uncovered = 0.
    for a, b in intervals:
        if b <= a:
            continue
        if a > right:
            uncovered += a - right
        right = max(right, b)
    return uncovered + max(0., exposure_ms - right)


def shutter_release_gate(*, phases, pulse_ms, exposure_ms, jitter_ms,
                         photodiode_verified, hardware_clock_verified,
                         row_response_verified, physical_moment_bound_verified):
    """Necessary instrument checks, NEVER sufficient for physical product release."""
    reasons = []
    try:
        blind = uncovered_support_ms(phases, pulse_ms, exposure_ms, jitter_ms)
        if blind > 1e-9:
            reasons.append("unilluminated_shutter_support")
    except (ValueError, TypeError):
        blind = None
        reasons.append("invalid_or_missing_phase_sweep")
    if not photodiode_verified:
        reasons.append("pulse_shape_not_independently_measured")
    if not hardware_clock_verified:
        reasons.append("camera_clock_not_independently_measured")
    if not row_response_verified:
        reasons.append("rolling_shutter_row_response_unknown")
    if not physical_moment_bound_verified:
        reasons.append("first_moment_not_physically_bounded")
    return dict(instrument_status="REJECT" if reasons else "NECESSARY_CHECKS_ONLY",
                product="ABSTAIN_UNCALIBRATED",
                uncovered_support_ms=blind, reasons=reasons,
                warning="Phase coverage cannot authenticate shutter kernel, eyelid geometry or physical velocity.")


def experiment(seed=4112026, trials=1000):
    center = (5.5, 5.7)
    edge = (9.5, 9.7)
    y_a = pulse_response(center, SPARSE_PHASES_MS)
    y_b = pulse_response(edge, SPARSE_PHASES_MS)
    m_a, m_b = first_abs_moment_ms(center), first_abs_moment_ms(edge)
    assert all(v == 0 for v in y_a+y_b) and abs(m_a-.6) < 1e-10
    assert abs(m_b-4.6) < 1e-10 and abs(m_b-m_a-4) < 1e-10  # P1
    assert pulse_response(center, SPARSE_PHASES_MS, jitter_ms=.05) == [0.]*10
    assert pulse_response(edge, SPARSE_PHASES_MS, jitter_ms=.05) == [0.]*10  # P2
    dense = [i/10 for i in range(99)]
    d_a, d_b = pulse_response(center, dense), pulse_response(edge, dense)
    assert d_a != d_b and max(d_a) > 0 and max(d_b) > 0  # P3
    rng = random.Random(seed)
    collisions = 0
    minimum_separation = float("inf")
    for _ in range(trials):
        a = rng.uniform(5.45, 5.65)
        b = rng.uniform(9.45, 9.65)
        k_a, k_b = (a, a+.10), (b, b+.10)
        if (pulse_response(k_a, SPARSE_PHASES_MS) ==
                pulse_response(k_b, SPARSE_PHASES_MS) == [0.]*10):
            collisions += 1
        minimum_separation = min(minimum_separation,
                                 first_abs_moment_ms(k_b)-first_abs_moment_ms(k_a))
    assert collisions == trials and minimum_separation >= 3.5  # P4
    # EXPLORATORY post-freeze robustness witness: measured pulse signals are
    # strictly positive, yet the two shutter moments remain nonidentifiable.
    # Each shutter is 50% uniform temporal response plus 50% hidden pulse.
    uniform_pulse_response = PULSE_MS / EXPOSURE_MS
    mixed_a = [.5*uniform_pulse_response + .5*y for y in y_a]
    mixed_b = [.5*uniform_pulse_response + .5*y for y in y_b]
    mixed_m_a = .5*(EXPOSURE_MS/4) + .5*m_a
    mixed_m_b = .5*(EXPOSURE_MS/4) + .5*m_b
    assert mixed_a == mixed_b and all(y > 0 for y in mixed_a)
    assert abs(mixed_m_b-mixed_m_a-2.) < 1e-10
    gate = shutter_release_gate(phases=SPARSE_PHASES_MS, pulse_ms=PULSE_MS,
        exposure_ms=EXPOSURE_MS, jitter_ms=.05,
        photodiode_verified=True, hardware_clock_verified=True,
        row_response_verified=True, physical_moment_bound_verified=False)
    assert gate["instrument_status"] == "REJECT"
    assert gate["product"] == "ABSTAIN_UNCALIBRATED"  # P6
    return dict(experiment="E002-411", evidence_tier="synthetic optical inverse problem",
        seed=seed, randomized_pairs=trials, indistinguishable_pairs=collisions,
        minimum_moment_separation_ms=minimum_separation,
        sparse_pulse_observations=y_a, dc_response_both=1,
        witness_moments_ms=dict(center=m_a, edge=m_b),
        moment_ratio=m_b/m_a,
        exploratory_positive_signal_mixture=dict(
            sparse_pulse_responses=mixed_a,
            center_moment_ms=mixed_m_a, edge_moment_ms=mixed_m_b,
            moment_separation_ms=mixed_m_b-mixed_m_a,
            preregistered=False),
        dense_scan_distinguishes=d_a != d_b,
        uncovered_sparse_ms=uncovered_support_ms(SPARSE_PHASES_MS, PULSE_MS,
                                                 EXPOSURE_MS, .05),
        gate=gate, human_aperture_validated=False,
        product="ABSTAIN_UNCALIBRATED")


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2, sort_keys=True))
