#!/usr/bin/env python3
"""E002-545 reproducible synthetic stress: correlated positions, arbitrary drift."""
import json
import random
from e002_545_paired_randomization import exact_p

SEED = 5452026
REPS = 1000
PAIRS = 8
POSITIONS = 20
ALPHA = 0.05
rng = random.Random(SEED)


def trial(effect):
    # Arbitrary fixed block differences (time drift and position correlation),
    # with a fair randomized flash assignment in each pair.
    rows = []
    for i in range(PAIRS):
        common = rng.gauss(0, 1.25) + 0.1 * i
        pattern = [common + 0.35 * rng.gauss(0, 1) + 0.05*j for j in range(POSITIONS)]
        sign = 1 if rng.randrange(2) else -1
        rows.append([sign*x + (effect if j == 0 else 0.0) for j, x in enumerate(pattern)])
    return exact_p(rows)[0] <= ALPHA

null = sum(trial(0) for _ in range(REPS))
positive = sum(trial(4) for _ in range(REPS))
result = {'evidence': 'synthetic_only', 'seed': SEED, 'replications_per_condition': REPS,
          'pairs': PAIRS, 'positions': POSITIONS, 'alpha': ALPHA,
          'null_rejections': null, 'null_rate': null/REPS,
          'injected_effect_at_one_position': 4,
          'effect_rejections': positive, 'effect_rate': positive/REPS,
          'physical_measurements': 0, 'human_measurements': 0}
print(json.dumps(result, indent=2, sort_keys=True))
