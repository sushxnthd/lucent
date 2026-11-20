#!/usr/bin/env python3
"""E002-517: frozen exact coded-optical shutter-code collisions.

An ideal-model identifiability falsification. No physical camera or human data.
The random seeds and decision criteria were frozen in E002_517_FROZEN.md.
"""
import argparse
from collections import defaultdict
from fractions import Fraction
from itertools import accumulate
import json
import random

SEEDS = (211, 223, 227, 229, 233)
DURATIONS = (8, 9, 10, 11, 12)
CHANNELS = 8
TICKS = 1600
MIN_SEPARATION_MS = 50


def optical_code(seed):
    rng = random.Random(seed + 99173)
    return [[rng.getrandbits(1) for _ in range(TICKS)] for _ in range(CHANNELS)]


def prefix_sums(code):
    return [[0, *accumulate(channel)] for channel in code]


def signature(sums, start, duration):
    """Exact rational eight-channel exposure means, not approximate floats."""
    return tuple(Fraction(s[start + duration] - s[start], duration) for s in sums)


def collision_scan(seed):
    sums = prefix_sums(optical_code(seed))
    by_duration = {}
    collisions = []
    for d in DURATIONS:
        groups = defaultdict(list)
        for s in range(TICKS - d + 1):
            groups[signature(sums, s, d)].append(s)
        pairs = []
        for starts in groups.values():
            for i, s in enumerate(starts):
                for t in starts[i + 1:]:
                    if t - s >= MIN_SEPARATION_MS:
                        pairs.append((s, t))
        pairs.sort()
        by_duration[str(d)] = {
            'collision_pairs': len(pairs),
            'first_pair': list(pairs[0]) if pairs else None,
            'max_separation_ms': max((t - s for s, t in pairs), default=None),
        }
        collisions.extend((d, s, t) for s, t in pairs)
    collisions.sort()
    return by_duration, collisions, sums


def run():
    per_seed = []
    witness = None
    all_collisions = 0
    for seed in SEEDS:
        by_duration, collisions, sums = collision_scan(seed)
        all_collisions += len(collisions)
        per_seed.append({
            'seed': seed, 'by_duration': by_duration,
            'exact_same_duration_distant_collision_pairs': len(collisions),
            'first_collision': list(collisions[0]) if collisions else None,
        })
        if witness is None:
            choices = [(s, t) for d, s, t in collisions if d == 10 and s >= 30]
            if choices:
                s1, s2 = min(choices)
                left_start, left_end = s1 - 30, s1 - 20
                left = signature(sums, left_start, 10)
                right_a = signature(sums, s1, 10)
                right_b = signature(sums, s2, 10)
                assert right_a == right_b
                assert s1 - left_end == 20 and s2 - left_end >= 70

                # Import the *existing* E002-514 exhaustive inverse. It must
                # retain both truths and conservatively bound the larger gap.
                from e002_514_coded_optical import (
                    cumulative, compatible_intervals, blind_gap_upper
                )
                original_sums = cumulative(optical_code(seed))
                fa = compatible_intervals(
                    original_sums, tuple(float(x) for x in left), envelope=0.)
                fb = compatible_intervals(
                    original_sums, tuple(float(x) for x in right_a), envelope=0.)
                upper = blind_gap_upper(fa, fb)
                assert (s1, s1 + 10) in fb and (s2, s2 + 10) in fb
                assert (left_start, left_end) in fa
                assert upper >= s2 - left_end

                perturbed = list(right_a)
                perturbed[0] += Fraction(1, 1000)
                assert signature(sums, s1, 10) != tuple(perturbed)
                assert signature(sums, s2, 10) != tuple(perturbed)
                witness = {
                    'seed': seed, 'duration_ms': 10,
                    'left_exposure_ms': [left_start, left_end],
                    'world_a_right_exposure_ms': [s1, s1 + 10],
                    'world_b_right_exposure_ms': [s2, s2 + 10],
                    'right_observation_exact': [str(x) for x in right_a],
                    'world_a_true_blind_gap_ms': s1 - left_end,
                    'world_b_true_blind_gap_ms': s2 - left_end,
                    'hypothetical_timing_budget_ms': 50,
                    'world_a_within_budget': s1 - left_end <= 50,
                    'world_b_within_budget': s2 - left_end <= 50,
                    'inverse_feasible_right_intervals': len(fb),
                    'conservative_gap_upper_ms': upper,
                    'inverse_never_underbounds_either_world': upper >= s2 - left_end,
                }
    return {
        'experiment': 'E002-517',
        'evidence_tier': 'EXACT_SYNTHETIC_CODEBOOK_IDENTIFIABILITY_ONLY',
        'seeds': list(SEEDS), 'duration_ms': list(DURATIONS),
        'minimum_start_separation_ms': MIN_SEPARATION_MS,
        'collision_pairs_total': all_collisions,
        'primary_prediction': 'PASS' if all_collisions else 'FAIL',
        'two_world_10ms_witness': witness, 'per_seed': per_seed,
        'human_labels': 0, 'physical_camera_verified': False,
        'certified_speed_limit': False,
        'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED',
    }


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
