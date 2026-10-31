#!/usr/bin/env python3
"""E002-542: frozen crossed-stimulus optical preflight. SYNTHETIC ONLY.

Uses the existing E002-541 timing estimator unchanged. This is not a camera,
photodiode, anatomical, physiological, or deployment calibration.
"""
from __future__ import annotations
import argparse
import json
import math

from e002_541_coded_light import (
    N_FRAMES, PERIOD_MS, TRUTH, exposure_average, estimate, light, simulate,
)

GAIN, OFFSET = 0.65, 0.20
AMPLITUDES = (0.25, 0.50)
GAMMA = 1.6
TAPS = (0.25, 0.50, 0.25)
RADIOMETRY_FAIL = 0.025
EDGE_FAIL = 0.015


def rms(errors: list[float]) -> float:
    return math.sqrt(sum(e * e for e in errors) / len(errors))


def blur(signal: list[float]) -> list[float]:
    return [
        TAPS[0] * signal[max(0, i - 1)] +
        TAPS[1] * signal[i] +
        TAPS[2] * signal[min(len(signal) - 1, i + 1)]
        for i in range(len(signal))
    ]


def frozen_fit(signal: list[int], sensor_signal: list[float] | None = None,
               *, gamma: float = 1.0) -> dict:
    samples = simulate(signal if sensor_signal is None else sensor_signal, gamma=gamma)
    fit = estimate(signal, samples)
    if fit['decision'] != 'SYNTHETIC_IDENTIFIED' or fit['best'] != list(TRUTH):
        raise AssertionError('frozen timing estimator did not recover synthetic truth')
    return fit


def radiometry_challenge(signal: list[int], gamma: float) -> dict:
    fit = frozen_fit(signal, gamma=gamma)
    phase, duration, delay = fit['best']
    errors = []
    by_amplitude = {}
    for amplitude in AMPLITUDES:
        current = []
        for frame in range(N_FRAMES):
            for row in (0, 1):
                x = exposure_average(signal, frame * PERIOD_MS + phase + row * delay, duration)
                predicted = fit['offset_fit'] + fit['gain_fit'] * amplitude * x
                observed = OFFSET + GAIN * (amplitude * x) ** gamma
                current.append(observed - predicted)
        errors.extend(current)
        by_amplitude[str(amplitude)] = round(rms(current), 8)
    return {
        'training': fit, 'amplitude_rmse': by_amplitude,
        'heldout_rmse': round(rms(errors), 8),
        'heldout_max_abs': round(max(map(abs, errors)), 8),
        'heldout_falsified': rms(errors) > RADIOMETRY_FAIL,
    }


def edge_pulses() -> list[float]:
    signal = [0.0] * 800
    for frame in range(N_FRAMES):
        start = frame * PERIOD_MS + TRUTH[0]
        signal[start - 1] = 1.0
        signal[start + TRUTH[1]] = 1.0
    return signal


def edge_challenge(training_signal: list[int], *, response_blur: bool) -> dict:
    sensor_training = blur(training_signal) if response_blur else None
    fit = frozen_fit(training_signal, sensor_training)
    challenge = edge_pulses()
    physical_light = blur(challenge) if response_blur else challenge
    phase, duration, delay = fit['best']
    errors = []
    by_row = {0: [], 1: []}
    for frame in range(N_FRAMES):
        for row in (0, 1):
            start = frame * PERIOD_MS + phase + row * delay
            expected = fit['offset_fit'] + fit['gain_fit'] * exposure_average(challenge, start, duration)
            observed = OFFSET + GAIN * exposure_average(physical_light, start, duration)
            delta = observed - expected
            errors.append(delta)
            by_row[row].append(delta)
    return {
        'training': fit,
        'heldout_rmse': round(rms(errors), 8),
        'heldout_max_abs': round(max(map(abs, errors)), 8),
        'row0_max_abs': round(max(map(abs, by_row[0])), 8),
        'row1_max_abs': round(max(map(abs, by_row[1])), 8),
        'heldout_falsified': max(map(abs, errors)) > EDGE_FAIL,
    }


def run() -> dict:
    signal = light('coded')
    linear = radiometry_challenge(signal, 1.0)
    gamma = radiometry_challenge(signal, GAMMA)
    instantaneous = edge_challenge(signal, response_blur=False)
    temporal_blur = edge_challenge(signal, response_blur=True)
    wrong_source = estimate(light('coded', 20261031), simulate(signal))
    invalid = simulate(signal)
    duplicate = estimate(signal, invalid + [invalid[0]])
    missing = estimate(signal, simulate(signal, keep=tuple(range(15))))
    saturated = estimate(signal, simulate(signal, gain=1.4, offset=0.2, clip=True))
    return {
        'protocol': 'E002-542_FROZEN.md',
        'evidence_tier': 'SYNTHETIC_INSTRUMENT_ONLY',
        'linear': linear, 'gamma': gamma,
        'instantaneous': instantaneous, 'temporal_blur': temporal_blur,
        'wrong_source': wrong_source['decision'],
        'duplicate_frame': duplicate['decision'],
        'missing_frames': missing['decision'],
        'saturated': saturated['decision'],
        'frozen_predictions': {
            'linear_heldout_pass': not linear['heldout_falsified'],
            'gamma_heldout_falsified': gamma['heldout_falsified'],
            'instantaneous_heldout_pass': not instantaneous['heldout_falsified'],
            'blur_heldout_falsified': temporal_blur['heldout_falsified'],
        },
        'physical_capture_count': 0,
        'human_anatomical_rating_count': 0,
        'continuous_time_human_motion_bounds': 0,
        'product': 'ABSTAIN_UNCALIBRATED',
        'release': 'BLOCKED',
    }


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', default='-')
    args = p.parse_args()
    payload = json.dumps(run(), indent=2, sort_keys=True) + '\n'
    if args.output == '-':
        print(payload, end='')
    else:
        with open(args.output, 'w', encoding='utf-8') as handle:
            handle.write(payload)
