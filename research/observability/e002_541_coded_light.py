#!/usr/bin/env python3
"""E002-541: synthetic coded-LED shutter timing identifiability bench.

No physical camera, human physiology, or production certification.
"""
from __future__ import annotations
import argparse
import json
import math
import random

N_FRAMES = 20
PERIOD_MS = 33
PHASES = tuple(range(21))
EXPOSURES = (4, 8, 12)
ROW_DELAYS = (0, 5, 10)
TRUTH = (7, 8, 5)
MAX_RMSE = 0.025
MIN_MARGIN = 0.004


def light(kind: str, seed: int = 20261030) -> list[int]:
    if kind == 'coded':
        state = seed & 0xffffffff
        out = []
        for _ in range(800):
            state = (1664525 * state + 1013904223) & 0xffffffff
            out.append((state >> 31) & 1)
        return out
    if kind == 'periodic':
        return [int(i % 4 >= 2) for i in range(800)]
    if kind == 'constant':
        return [1] * 800
    raise ValueError('unknown source kind')


def exposure_average(signal: list[float], start: int, duration: int) -> float:
    if start < 0 or duration <= 0 or start + duration > len(signal):
        raise ValueError('exposure outside reference signal')
    return sum(signal[start:start + duration]) / duration


def simulate(signal: list[int], *, truth: tuple[int, int, int] = TRUTH,
             gain: float = 0.65, offset: float = 0.2, noise: float = 0.,
             seed: int = 9, period_ms: int = PERIOD_MS,
             keep: tuple[int, ...] | None = None,
             clip: bool = False, row_gain_factor: float = 1.,
             gamma: float = 1., phase_jitter: bool = False) -> list[tuple[int, int, float]]:
    rng = random.Random(seed)
    phase, exposure, row_delay = truth
    samples = []
    for frame in range(N_FRAMES):
        if keep is not None and frame not in keep:
            continue
        for row in (0, 1):
            x = exposure_average(signal, frame * period_ms + phase + row * row_delay + (frame % 3 if phase_jitter else 0), exposure)
            y = offset + gain * (row_gain_factor if row else 1.) * (x ** gamma) + rng.uniform(-noise, noise)
            if clip:
                y = min(1., max(0., y))
            samples.append((frame, row, y))
    return samples


def affine_rmse(xs: list[float], ys: list[float]) -> tuple[float, float, float]:
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    vx = sum((x - mx)**2 for x in xs)
    if vx < 1e-12:
        return math.inf, math.nan, math.nan
    gain = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / vx
    offset = my - gain * mx
    rmse = math.sqrt(sum((y - gain*x - offset)**2 for x, y in zip(xs, ys)) / n)
    if gain <= 0:
        return math.inf, gain, offset
    return rmse, gain, offset


def estimate(signal: list[int], samples: list[tuple[int, int, float]],
             *, phases=PHASES, exposures=EXPOSURES, row_delays=ROW_DELAYS,
             period_ms: int = PERIOD_MS) -> dict:
    """Conditional synthetic fit; never authenticate physical timing."""
    if len(signal) < 800 or len(samples) < 2:
        return {'decision': 'ABSTAIN', 'reason': 'incomplete_signal_or_samples'}
    seen = set()
    frames = set()
    for f, r, y in samples:
        if type(f) is not int or type(r) is not int or not 0 <= f < N_FRAMES or r not in (0, 1) or (f, r) in seen or not math.isfinite(y):
            return {'decision': 'ABSTAIN', 'reason': 'invalid_sample_identity'}
        seen.add((f, r))
        frames.add(f)
        if y <= 0.001 or y >= 0.999:
            return {'decision': 'ABSTAIN', 'reason': 'clipped_or_saturated'}
    if len(frames) < math.ceil(.8*N_FRAMES) or len(samples) != 2*len(frames):
        return {'decision': 'ABSTAIN', 'reason': 'missing_frames_or_rows'}
    ys = [s[2] for s in samples]
    if max(ys) - min(ys) < .01:
        return {'decision': 'ABSTAIN', 'reason': 'uninformative_brightness'}
    scores = []
    for phase in phases:
        for exposure in exposures:
            for row_delay in row_delays:
                try:
                    xs = [exposure_average(signal, f*period_ms + phase + r*row_delay, exposure) for f, r, _ in samples]
                except ValueError:
                    return {'decision': 'ABSTAIN', 'reason': 'reference_signal_coverage'}
                rmse, gain, offset = affine_rmse(xs, ys)
                scores.append((rmse, (phase, exposure, row_delay), gain, offset))
    scores.sort(key=lambda x: (x[0], x[1]))
    best, second = scores[:2]
    margin = second[0] - best[0]
    result = {'best': list(best[1]), 'rmse': round(best[0], 8),
              'runner_up': list(second[1]), 'runner_rmse': round(second[0], 8),
              'margin': round(margin, 8), 'samples': len(samples),
              'gain_fit': round(best[2], 6), 'offset_fit': round(best[3], 6)}
    if not math.isfinite(best[0]) or best[0] > MAX_RMSE:
        result.update(decision='ABSTAIN', reason='model_mismatch')
    elif margin < MIN_MARGIN:
        result.update(decision='ABSTAIN', reason='nonidentifiable_timing')
    else:
        result.update(decision='SYNTHETIC_IDENTIFIED', reason='model_conditional_only')
    return result


def run() -> dict:
    coded = light('coded')
    periodic = light('periodic')
    clean = estimate(coded, simulate(coded))
    noisy = estimate(coded, simulate(coded, noise=.01))
    alias = estimate(periodic, simulate(periodic))
    wrong_rows = estimate(coded, simulate(coded), row_delays=(0,))
    wrong_clock = estimate(coded, simulate(coded, period_ms=34))
    constant = estimate(light('constant'), simulate(light('constant')))
    missing = estimate(coded, simulate(coded, keep=tuple(range(15))))
    saturated = estimate(coded, simulate(coded, gain=1.4, offset=.2, clip=True))
    row_gain = estimate(coded, simulate(coded, row_gain_factor=.75))
    gamma = estimate(coded, simulate(coded, gamma=1.6))
    phase_jitter = estimate(coded, simulate(coded, phase_jitter=True))
    blurred = [(.25*coded[max(i-1, 0)] + .5*coded[i] + .25*coded[min(i+1, len(coded)-1)]) for i in range(len(coded))]
    temporal_blur = estimate(coded, simulate(blurred))
    periodic_alias_equal = all(exposure_average(periodic, f*PERIOD_MS + 7 + r*5, 8) == exposure_average(periodic, f*PERIOD_MS + 11 + r*5, 8) for f in range(N_FRAMES) for r in (0, 1))
    sweep = []
    for seed in range(40):
        s = light('coded', seed)
        out = estimate(s, simulate(s))
        sweep.append({'seed': seed, 'decision': out['decision'],
                      'correct': out.get('best') == list(TRUTH),
                      'margin': out.get('margin')})
    return {'truth': list(TRUTH), 'clean': clean, 'noisy': noisy, 'periodic': alias,
            'wrong_rows': wrong_rows, 'wrong_clock': wrong_clock,
            'constant': constant, 'missing': missing, 'saturated': saturated,
            'row_gain': row_gain, 'gamma': gamma, 'phase_jitter': phase_jitter, 'temporal_blur': temporal_blur,
            'periodic_phase_7_vs_11_exactly_equal': periodic_alias_equal,
            'sweep': {'correct_identified': sum(x['correct'] and x['decision'] == 'SYNTHETIC_IDENTIFIED' for x in sweep),
                      'total': len(sweep), 'failed_seeds': [x for x in sweep if not x['correct'] or x['decision'] != 'SYNTHETIC_IDENTIFIED']},
            'evidence_tier': 'SYNTHETIC_ONLY', 'physical_validation': False,
            'human_anatomical_ratings': 0, 'product': 'ABSTAIN_UNCALIBRATED'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='-')
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output == '-':
        print(payload, end='')
    else:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(payload)
