#!/usr/bin/env python3
"""E002-401: synthetic rolling-shutter, two-landmark temporal-skew instrument.

No physical camera or human landmark annotations. Frozen protocol: E002_401_FROZEN.md.
"""
from __future__ import annotations
import json
import random
from dataclasses import asdict
from e002_399_reference_adequacy import Frame, calibrated, certify

THETA = 0.2
EXPOSURE = 0.001
CENTERS = (-0.001, 0.001)
UPPER_OFFSET = -0.004
LOWER_OFFSET = +0.004
ROW_ERROR = (20.0 * abs(UPPER_OFFSET) + 20.0 * abs(LOWER_OFFSET))


def upper(t: float, aperture: float, velocity: float) -> float:
    return 0.35 + velocity * t


def lower(t: float, aperture: float, velocity: float) -> float:
    return 0.35 + aperture + velocity * t


def row_mean_linear(fn, center: float, offset: float, aperture: float,
                    velocity: float, exposure: float = EXPOSURE) -> float:
    """Exact shutter mean of a linear landmark at its own row time."""
    a = center + offset - exposure / 2
    b = center + offset + exposure / 2
    return (fn(a, aperture, velocity) + fn(b, aperture, velocity)) / 2


def row_measurement(center: float, aperture: float, velocity: float,
                    du: float = UPPER_OFFSET, dl: float = LOWER_OFFSET) -> float:
    return (row_mean_linear(lower, center, dl, aperture, velocity)
            - row_mean_linear(upper, center, du, aperture, velocity))


def decisions(aperture: float, velocity: float, du: float = UPPER_OFFSET,
              dl: float = LOWER_OFFSET, bound: float = 0.) -> dict:
    means = [row_measurement(t, aperture, velocity, du, dl) for t in CENTERS]
    frames = [Frame(t, m-bound, m+bound, EXPOSURE, 0.) for t, m in zip(CENTERS, means)]
    result = certify(frames, calibrated(0., THETA))
    return {'means': means, 'decision': result.decision,
            'min_lower': result.lower_min, 'witnessed_upper': result.witnessed_upper}


def wrong(decision: str, aperture: float) -> bool:
    return ((aperture < THETA and decision == 'CONFIRMED_NO_CROSSING')
            or (aperture > THETA and decision == 'CONFIRMED_CROSSING'))


def experiment(seed: int = 401, n: int = 1000) -> dict:
    assert n % 2 == 0
    witness_hidden = decisions(.19, +20.)
    witness_hidden_corrected = decisions(.19, +20., bound=ROW_ERROR)
    witness_open = decisions(.30, -20.)
    witness_open_corrected = decisions(.30, -20., bound=ROW_ERROR)
    assert witness_hidden['decision'] == 'CONFIRMED_NO_CROSSING', 'W1'
    assert witness_hidden_corrected['decision'] == 'UNRESOLVED', 'W2'
    assert witness_open['decision'] == 'CONFIRMED_CROSSING', 'W3a'
    assert witness_open_corrected['decision'] == 'UNRESOLVED', 'W3b'
    assert decisions(.19, +20., 0., 0.)['decision'] == 'CONFIRMED_CROSSING', 'W4a'
    assert decisions(.30, -20., 0., 0.)['decision'] == 'CONFIRMED_NO_CROSSING', 'W4b'
    rng = random.Random(seed)
    naive_wrong = corrected_wrong = 0
    naive_counts = {}
    corrected_counts = {}
    max_true_mean_error = 0.
    for i in range(n):
        aperture = .19 if i < n//2 else .30
        velocity = rng.choice((-1., 1.)) * rng.uniform(15., 20.)
        phase = rng.uniform(-.0002, .0002)
        du = UPPER_OFFSET + rng.uniform(-.00025, .00025)
        dl = LOWER_OFFSET + rng.uniform(-.00025, .00025)
        bound = (20. * .00425) * 2
        # A shifted center cancels from the linear common-mode measurement.
        assert abs(row_measurement(CENTERS[0]+phase, aperture, velocity, du, dl)
                   - row_measurement(CENTERS[0], aperture, velocity, du, dl)) < 1e-12
        naive = decisions(aperture, velocity, du, dl)
        safe = decisions(aperture, velocity, du, dl, bound)
        naive_counts[naive['decision']] = naive_counts.get(naive['decision'], 0) + 1
        corrected_counts[safe['decision']] = corrected_counts.get(safe['decision'], 0) + 1
        naive_wrong += wrong(naive['decision'], aperture)
        corrected_wrong += wrong(safe['decision'], aperture)
        max_true_mean_error = max(max_true_mean_error,
                                  max(abs(m-aperture) for m in naive['means']))
        assert max(abs(m-aperture) for m in naive['means']) <= bound + 1e-12
    assert naive_wrong >= 200, ('W5a', naive_wrong)
    assert corrected_wrong == 0, ('W5b', corrected_wrong)
    # Enlarging the row uncertainty cannot turn unresolved into a certificate.
    for aperture, velocity in ((.19,20.),(.30,-20.)):
        initial = decisions(aperture,velocity,bound=ROW_ERROR)['decision']
        enlarged = decisions(aperture,velocity,bound=ROW_ERROR+.1)['decision']
        assert initial == 'UNRESOLVED' and enlarged == 'UNRESOLVED', 'W7 monotonic'
    return {'experiment':'E002-401', 'evidence_tier':'synthetic two-landmark row-exposure instrument',
            'protocol':'E002_401_FROZEN.md', 'seed':seed, 'trials':n,
            'threshold':THETA, 'physical_aperture_speed_bound':0.,
            'row_offset_upper_s':UPPER_OFFSET, 'row_offset_lower_s':LOWER_OFFSET,
            'per_landmark_speed_upper_per_s':20., 'nominal_row_bound':ROW_ERROR,
            'jittered_row_bound':.17,
            'hidden_crossing_witness':{'physical_aperture':.19,
                'naive':witness_hidden,'corrected':witness_hidden_corrected},
            'open_witness':{'physical_aperture':.30,
                'naive':witness_open,'corrected':witness_open_corrected},
            'naive_wrong_certificates':naive_wrong,
            'corrected_wrong_certificates':corrected_wrong,
            'naive_decisions':naive_counts,'corrected_decisions':corrected_counts,
            'max_row_mean_bias':max_true_mean_error,
            'human_physical_aperture_validated':False,
            'product':'ABSTAIN_UNCALIBRATED'}


if __name__ == '__main__':
    print(json.dumps(experiment(),indent=2,sort_keys=True))
