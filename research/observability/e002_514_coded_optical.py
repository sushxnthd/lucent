#!/usr/bin/env python3
"""E002-514: exhaustive set-valued inverse shutter timing, synthetic only.

A bounded-noise coded-optical *instrument feasibility* test. The external
optical clock, photodiode, radiometric model and camera geometry are assumed,
not authenticated. Never output a physical clearance or eyelid claim.
"""
import argparse
import json
import random
import statistics

CHANNELS = 8
TICKS = 1600
FRAMES = 40
EXPOSURE_TICKS = 10
DURATIONS = tuple(range(8, 13))
NOISE_MAX = 0.004
ENVELOPE = 0.010
HELD_OUT = (101, 103, 107, 109, 113)


def optical_code(seed):
    rng = random.Random(seed + 99173)
    return [[rng.getrandbits(1) for _ in range(TICKS)] for _ in range(CHANNELS)]


def cumulative(code):
    result = []
    for channel in code:
        sums = [0]
        for bit in channel:
            if bit not in (0, 1):
                raise ValueError('NONBINARY_OPTICAL_CODE')
            sums.append(sums[-1] + bit)
        result.append(sums)
    if len(result) != CHANNELS or len(set(map(len, result))) != 1:
        raise ValueError('INVALID_CHANNEL_GEOMETRY')
    return result


def integrate(sums, start, duration):
    if type(start) is not int or type(duration) is not int or start < 0 or duration <= 0 or start + duration > len(sums[0]) - 1:
        raise ValueError('EXPOSURE_OUT_OF_RANGE')
    return tuple((channel[start + duration] - channel[start]) / duration for channel in sums)


def compatible_intervals(sums, observation, envelope=ENVELOPE):
    """All feasible [start,end] ticks; never choose an MLE as a certificate."""
    if len(observation) != CHANNELS or not 0 <= envelope <= 1 or any(type(x) not in (float, int) or not -envelope <= x <= 1 + envelope for x in observation):
        raise ValueError('INVALID_OPTICAL_OBSERVATION')
    feasible = []
    for start in range(len(sums[0]) - 1):
        for duration in DURATIONS:
            if start + duration > len(sums[0]) - 1:
                break
            predicted = integrate(sums, start, duration)
            if all(abs(x-y) <= envelope + 1e-12 for x,y in zip(predicted, observation)):
                feasible.append((start, start + duration))
    return feasible


def blind_gap_upper(left, right):
    if not left or not right:
        return None
    return max(0, max(start for start, _ in right) - min(end for _, end in left))


def synthetic_trial(seed):
    rng = random.Random(seed)
    sums = cumulative(optical_code(seed))
    records = []
    for i in range(FRAMES):
        # Nominal period is used only to generate a truth world, never by solver.
        nominal = round(20 + i * (100/3))
        start = nominal + rng.randint(-2, 2)
        truth = (start, start + EXPOSURE_TICKS)
        observation = tuple(x + rng.uniform(-NOISE_MAX, NOISE_MAX)
                            for x in integrate(sums, start, EXPOSURE_TICKS))
        feasible = compatible_intervals(sums, observation)
        records.append((truth, feasible))
    valid = []
    for (a,fa), (b,fb) in zip(records, records[1:]):
        upper = blind_gap_upper(fa, fb)
        if upper is not None:
            true_gap = max(0, b[0] - a[1])
            valid.append((true_gap, upper))
    return {
        'seed': seed, 'frames': len(records),
        'true_exposures_contained': sum(truth in feasible for truth,feasible in records),
        'uniquely_identified_frames': sum(len(feasible) == 1 for _,feasible in records),
        'empty_feasible_frames': sum(not feasible for _,feasible in records),
        'evaluated_gaps': len(valid),
        'unsafe_gap_underbounds': sum(upper < truth for truth,upper in valid),
        'median_conservatism_ms': statistics.median(upper-truth for truth,upper in valid) if valid else None,
        'maximum_conservatism_ms': max((upper-truth for truth,upper in valid), default=None)
    }


def physical_gate(metadata):
    """Explicitly reject absent nuisance controls; no software attestation."""
    required = ('independent_photodiode_clock', 'measured_optical_code',
                'bounded_radiometric_response', 'bounded_gain_offset',
                'verified_exposure_geometry', 'verified_scanline_mapping',
                'verified_frame_continuity', 'bounded_clock_error',
                'bounded_missingness_blur', 'bounded_ambient_brightness')
    missing = [key for key in required if metadata.get(key) is not True]
    return {'status': 'ABSTAIN_UNCALIBRATED' if missing else 'INPUTS_REPORTED_NOT_INDEPENDENTLY_VERIFIED',
            'missing_controls': missing, 'physical_validation_by_code': False,
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}


def run():
    trials = [synthetic_trial(seed) for seed in HELD_OUT]
    total_frames = sum(t['frames'] for t in trials)
    total_gaps = sum(t['evaluated_gaps'] for t in trials)
    median = statistics.median(t['median_conservatism_ms'] for t in trials if t['median_conservatism_ms'] is not None)
    passed = (sum(t['true_exposures_contained'] for t in trials) == total_frames
              and sum(t['unsafe_gap_underbounds'] for t in trials) == 0
              and total_gaps >= 0.8 * len(HELD_OUT) * (FRAMES-1)
              and median <= 2)
    return {'experiment':'E002-514','evidence':'HELD_OUT_SYNTHETIC_INSTRUMENT_FEASIBILITY_ONLY',
            'pre_registered_seeds':list(HELD_OUT),'held_out_simulation_gate':'PASS' if passed else 'FAIL',
            'trials':trials,'total_frames':total_frames,'total_evaluated_gaps':total_gaps,
            'median_of_trial_medians_ms':median,
            'nominal_fps_used_by_solver':False,'real_physical_instrument_used':False,
            'real_human_labels_obtained':False,'certified_human_speed_bound':False,
            'physical_calibration_gate':physical_gate({}),
            'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true', help='Print JSON report (default)')
    parser.parse_args()
    print(json.dumps(run(), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
