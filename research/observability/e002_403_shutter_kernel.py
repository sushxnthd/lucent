#!/usr/bin/env python3
"""E002-403: prospectively frozen nonuniform shutter-response counterexample.

This is a synthetic temporal-instrument falsification, not human validation.
"""
from __future__ import annotations
from dataclasses import asdict
import json
import random
from e002_399_reference_adequacy import Frame, calibrated, certify


def trial(v, exposure, pulse_fraction, minimum):
    """Two outer-edge temporal pulses; actual aperture valley at midpoint."""
    dt = exposure
    pulse = exposure * pulse_fraction
    # Both pulses sample the same distance e - pulse/2 from the physical valley.
    observed_mean = minimum + v * (exposure - pulse / 2)
    first_moment = exposure / 2 - pulse / 2
    uniform_mean = minimum + v * exposure / 2
    t = (0.0, dt)
    naive = certify([Frame(s, observed_mean, observed_mean, exposure, 0.)
                     for s in t], calibrated(v))
    corrected = certify([Frame(s, observed_mean, observed_mean, exposure, 0.,
                               first_moment) for s in t], calibrated(v))
    uniform = certify([Frame(s, uniform_mean, uniform_mean, exposure, 0.,
                             exposure / 4) for s in t], calibrated(v))
    return naive, corrected, uniform, first_moment


def experiment(seed=403, n=1000):
    v, e, p, minimum = 20., .010, .02, .19
    naive, corrected, uniform, moment = trial(v, e, p, minimum)
    assert naive.decision == 'CONFIRMED_NO_CROSSING', 'P1'
    assert corrected.decision == 'UNRESOLVED', 'P2'
    assert uniform.decision == 'UNRESOLVED', 'P3'
    rng = random.Random(seed)
    false_naive = false_corrected = false_uniform = 0
    for i in range(n):
        v = rng.uniform(10., 40.)
        e = rng.uniform(.005, .020)
        p = rng.uniform(.01, .03)
        minimum = .2 - .06 * v * e
        naive_i, corrected_i, uniform_i, _ = trial(v, e, p, minimum)
        false_naive += naive_i.decision == 'CONFIRMED_NO_CROSSING'
        false_corrected += corrected_i.decision == 'CONFIRMED_NO_CROSSING'
        false_uniform += uniform_i.decision == 'CONFIRMED_NO_CROSSING'
    assert false_naive >= .90 * n, ('P4', false_naive)
    assert false_corrected == 0 and false_uniform == 0, 'P4'
    return {
        'experiment': 'E002-403', 'evidence_tier': 'adversarial synthetic instrument',
        'seed': seed, 'trials': n, 'threshold': .2,
        'witness': {
            'true_minimum': .19, 'true_crossing_time_s': .005,
            'naive_uniform_assumption': asdict(trial(20., .010, .02, .19)[0]),
            'moment_aware': asdict(trial(20., .010, .02, .19)[1]),
            'true_uniform_shutter': asdict(trial(20., .010, .02, .19)[2]),
            'actual_first_absolute_moment_s': moment,
            'uniform_assumed_first_absolute_moment_s': .010 / 4
        },
        'false_no_crossing_certificates': {
            'naive_uniform': false_naive,
            'moment_aware': false_corrected,
            'actual_uniform': false_uniform
        },
        'human_physical_aperture_validated': False,
        'product': 'ABSTAIN_UNCALIBRATED unless independent temporal-kernel calibration'
    }


if __name__ == '__main__':
    print(json.dumps(experiment(), indent=2, sort_keys=True))
