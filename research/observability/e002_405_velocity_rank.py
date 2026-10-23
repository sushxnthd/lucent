#!/usr/bin/env python3
"""E002-405: finite-sample velocity maxima are not deterministic physical bounds.

Exact rank law plus a synthetic aperture trajectory. No human validation.
"""
from __future__ import annotations
import json
import random
from dataclasses import asdict

from e002_399_reference_adequacy import Frame, calibrated, certify

COHORTS = ((20, 10), (100, 100), (1000, 100))
SEED = 405
REPLICATES = 5000


def sample(rng, kind):
    return rng.random() if kind == 'uniform' else rng.expovariate(1.0)


def rank_experiment(seed=SEED, replicates=REPLICATES):
    rng = random.Random(seed)
    results = []
    for kind in ('uniform', 'exponential'):
        for n, m in COHORTS:
            exceeded = 0
            for _ in range(replicates):
                ceiling = max(sample(rng, kind) for _ in range(n))
                exceeded += any(sample(rng, kind) > ceiling for _ in range(m))
            expected = m / (n + m)
            observed = exceeded / replicates
            assert abs(observed - expected) < .03, (kind, n, m, expected, observed)
            results.append({'distribution': kind, 'calibration_n': n,
                            'future_m': m, 'exact_exceedance_risk': expected,
                            'observed_exceedance_frequency': observed,
                            'absolute_error': abs(observed-expected),
                            'replicates': replicates})
    return results


def aperture(t):
    return .18 + 6.0 * abs(t - .02)


def exposure_mean(center, width):
    # Endpoint exposure intervals do not cross the triangle's kink.
    return (aperture(center-width/2) + aperture(center+width/2))/2


def physical_witness():
    width = 1e-6
    times = (0., .04)
    means = [exposure_mean(t, width) for t in times]
    frames = [Frame(t, a, a, width, 0.) for t, a in zip(times, means)]
    wrong = certify(frames, calibrated(speed=4., threshold=.20))
    correct = certify(frames, calibrated(speed=6., threshold=.20))
    assert aperture(.02) < .20
    assert all(abs(a-.30)<1e-12 for a in means)
    assert wrong.decision == 'CONFIRMED_NO_CROSSING', wrong
    assert correct.decision == 'UNRESOLVED', correct
    return {'times_s': times, 'exposure_s': width, 'means': means,
            'true_minimum': aperture(.02), 'threshold': .20,
            'empirical_speed_claim': 4., 'actual_speed': 6.,
            'incorrect_empirical_certificate': asdict(wrong),
            'correct_hard_speed_certificate': asdict(correct)}


def main():
    result = {'experiment': 'E002-405',
              'evidence_tier': 'exact order-statistic law and synthetic physical witness',
              'seed': SEED,
              'rank_law': 'P(max future > max calibration)=m/(n+m), jointly exchangeable and no ties',
              'rank_experiments': rank_experiment(),
              'physical_witness': physical_witness(),
              'human_physical_aperture_validated': False,
              'product': 'ABSTAIN_UNCALIBRATED'}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
