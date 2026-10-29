#!/usr/bin/env python3
"""E002-515: offline, reference-blind replay of measured optical timing.

Consumes independently collected waveform, camera observation and reference
files. No acquisition metadata, no inferred fps, no hardware attestation.
All outputs are audit diagnostics; no physical or human certificate.
"""
import argparse
import csv
import json
import math
from pathlib import Path

CHANNELS = tuple(f'ch{i}' for i in range(8))
DURATION_RANGE_MS = (8., 12.)
MAX_RECORDS = 20000


def finite_float(value, name):
    try:
        v = float(value)
    except (TypeError, ValueError):
        raise ValueError('NONNUMERIC_' + name) from None
    if not math.isfinite(v):
        raise ValueError('NONFINITE_' + name)
    return v


def read_csv(path, columns):
    with open(path, newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or set(reader.fieldnames) != set(columns):
            raise ValueError('SCHEMA_MISMATCH')
        rows = []
        for row in reader:
            if len(rows) >= MAX_RECORDS:
                raise ValueError('TOO_MANY_RECORDS')
            if None in row or any(x is None or x == '' for x in row.values()):
                raise ValueError('INCOMPLETE_RECORD')
            rows.append(row)
    if not rows:
        raise ValueError('EMPTY_RECORDS')
    return rows


def waveform(path):
    rows = read_csv(path, ('start_ms', 'end_ms', *CHANNELS))
    out = []
    last_end = None
    for row in rows:
        a, b = finite_float(row['start_ms'], 'TIME'), finite_float(row['end_ms'], 'TIME')
        if not a >= 0 or not b > a or (last_end is not None and abs(a-last_end) > 1e-8):
            raise ValueError('WAVEFORM_CLOCK_DISCONTINUITY')
        levels = tuple(finite_float(row[c], 'LEVEL') for c in CHANNELS)
        if any(not 0 <= x <= 1 for x in levels):
            raise ValueError('INVALID_WAVEFORM_LEVEL')
        out.append((a, b, levels))
        last_end = b
    return out


def observations(path):
    rows = read_csv(path, ('frame_id', *CHANNELS))
    result = []
    for row in rows:
        name = row['frame_id']
        if not name or len(name) > 80 or any(ch not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for ch in name):
            raise ValueError('INVALID_FRAME_ID')
        obs = tuple(finite_float(row[c], 'CAMERA_VALUE') for c in CHANNELS)
        if any(not 0 <= x <= 1 for x in obs):
            raise ValueError('INVALID_CAMERA_VALUE')
        result.append((name, obs))
    ids = [x[0] for x in result]
    if len(set(ids)) != len(ids):
        raise ValueError('DUPLICATE_FRAME_ID')
    return result


def reference(path):
    rows = read_csv(path, ('frame_id', 'start_ms', 'end_ms', 'uncertainty_ms'))
    result = {}
    last_start = -1
    for row in rows:
        name = row['frame_id']
        if name in result:
            raise ValueError('DUPLICATE_REFERENCE_ID')
        a, b, u = (finite_float(row[k], k.upper()) for k in ('start_ms', 'end_ms', 'uncertainty_ms'))
        if not 0 <= a < b or not 0 <= u <= 5 or a <= last_start:
            raise ValueError('INVALID_REFERENCE_TIME')
        result[name] = (a, b, u)
        last_start = a
    return result


def native_sequence(path):
    """Read a claimed native-index ledger. This is NOT hardware attestation."""
    rows = read_csv(path, ('frame_id', 'native_index'))
    ledger = []
    seen_ids = set()
    seen_indices = set()
    for row in rows:
        name, raw = row['frame_id'], row['native_index']
        if (not name or len(name) > 80 or
                any(ch not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for ch in name)):
            raise ValueError('INVALID_NATIVE_FRAME_ID')
        if not raw.isascii() or not raw.isdecimal():
            raise ValueError('INVALID_NATIVE_INDEX')
        index = int(raw)
        if index > 10**12:
            raise ValueError('INVALID_NATIVE_INDEX')
        if name in seen_ids or index in seen_indices:
            raise ValueError('DUPLICATE_NATIVE_SEQUENCE_ENTRY')
        seen_ids.add(name)
        seen_indices.add(index)
        ledger.append((name, index))
    return ledger


def validate_native_sequence(camera, truth, ledger):
    """Fail closed for an explicitly claimed contiguous native segment."""
    if ledger is None:
        return False
    ids = [name for name, _ in camera]
    if [name for name, _ in ledger] != ids:
        raise ValueError('NATIVE_SEQUENCE_ORDER_MISMATCH')
    if any(b != a+1 for (_, a), (_, b) in zip(ledger, ledger[1:])):
        raise ValueError('NATIVE_SEQUENCE_GAP')
    if any(truth[nb][0] <= truth[na][0] for na, nb in zip(ids, ids[1:])):
        raise ValueError('REFERENCE_CAMERA_ORDER_MISMATCH')
    return True


def candidates(wave, obs, residual_max):
    """Search measured optical boundaries, not synthetic nominal frame times."""
    if not 0 <= residual_max <= 1:
        raise ValueError('INVALID_RESIDUAL_ENVELOPE')
    accum = [[0.] for _ in CHANNELS]
    for a, b, levels in wave:
        for k, level in enumerate(levels):
            accum[k].append(accum[k][-1] + (b-a)*level)
    found = []
    for i in range(len(wave)):
        for j in range(i+1, len(wave)+1):
            start, end = wave[i][0], wave[j-1][1]
            duration = end-start
            if duration > DURATION_RANGE_MS[1]+1e-9:
                break
            if duration < DURATION_RANGE_MS[0]-1e-9:
                continue
            predicted = tuple((a[j]-a[i])/duration for a in accum)
            if all(abs(x-y) <= residual_max + 1e-12 for x, y in zip(predicted, obs)):
                found.append((start, end))
    return found


def replay(wave, camera, truth, residual_max, timing_envelope_ms, native_ledger=None):
    """Truth is accessed only after all optical candidate sets are frozen."""
    if not 0 <= timing_envelope_ms <= 5:
        raise ValueError('INVALID_TIMING_ENVELOPE')
    if set(truth) != {name for name, _ in camera}:
        raise ValueError('REFERENCE_FRAME_SET_MISMATCH')
    claimed_contiguous = validate_native_sequence(camera, truth, native_ledger)
    predicted = [(name, candidates(wave, obs, residual_max)) for name, obs in camera]
    if any(truth[name][0] < wave[0][0] or truth[name][1] > wave[-1][1] for name, _ in camera):
        raise ValueError('REFERENCE_OUTSIDE_WAVEFORM')
    covered, empty, unique, underbounds, gap_count = 0, 0, 0, 0, 0
    gap_overestimates = []
    for name, feasible in predicted:
        a, b, u = truth[name]
        empty += not bool(feasible)
        unique += len(feasible) == 1
        # Boundary grid and independent timing error are conservative,
        # but reference uncertainty is NOT subtracted from the truth.
        covered += any(abs(s-a)+u <= timing_envelope_ms+1e-9 and
                       abs(e-b)+u <= timing_envelope_ms+1e-9 for s,e in feasible)
    # A row-pair is not a native-adjacent exposure without a capture ledger.
    # The ledger remains a claim until independently authenticated.
    for (na, fa), (nb, fb) in (zip(predicted, predicted[1:]) if claimed_contiguous else ()):
        if not fa or not fb:
            continue
        true_a, true_b, true_u = truth[na]
        next_a, next_b, next_u = truth[nb]
        # Conservative upper bound for all independently measured reference
        # values, not just the reported center timestamps.
        ref_upper = max(0., next_a + next_u - (true_b - true_u))
        predicted_upper = max(0., max(s for s,e in fb) - min(e for s,e in fa)
                              + 2*timing_envelope_ms)
        gap_count += 1
        underbounds += predicted_upper + 1e-9 < ref_upper
        gap_overestimates.append(predicted_upper - ref_upper)
    return {
        'experiment': 'E002-515',
        'evidence_tier': 'OFFLINE_MEASURED_INPUT_REPLAY_NOT_HARDWARE_ATTESTATION',
        'frame_count': len(camera),
        'waveform_bins': len(wave),
        'precalibrated_radiometric_residual_max': residual_max,
        'precalibrated_timing_envelope_ms': timing_envelope_ms,
        'empty_candidate_frames': empty,
        'unique_candidate_frames': unique,
        'reference_exposures_with_matching_candidate': covered,
        'reference_exposures_not_covered': len(camera)-covered,
        'evaluated_adjacent_gaps': gap_count,
        'unverified_csv_row_pairs': max(0, len(camera)-1) if not claimed_contiguous else 0,
        'native_sequence_ledger_supplied': claimed_contiguous,
        'native_frame_continuity_independently_attested': False,
        'native_adjacent_gaps_proven_by_code': 0,
        'unsafe_gap_underbounds_vs_reference_envelope': underbounds,
        'worst_gap_margin_ms': min(gap_overestimates) if gap_overestimates else None,
        'instrument_validation_result': ('FAIL_REFERENCE_COVERAGE' if covered != len(camera) or underbounds
                                         else 'INSUFFICIENT_NATIVE_SEQUENCE_PROVENANCE' if not claimed_contiguous
                                         else 'INSUFFICIENT_GAP_COVERAGE' if gap_count == 0
                                         else 'REPLAY_CONSISTENT_SEQUENCE_UNATTESTED'),
        'independent_instrument_identity_verified_by_code': False,
        'continuous_time_eyelid_speed_certified': False,
        'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--photodiode', required=True)
    p.add_argument('--camera', required=True)
    p.add_argument('--reference', required=True)
    p.add_argument('--sequence', help='Claimed native frame index CSV; NOT independent hardware attestation')
    p.add_argument('--residual-max', type=float, required=True,
                   help='Pre-calibrated radiometric residual bound, NOT fitted on evaluation data')
    p.add_argument('--timing-envelope-ms', type=float, required=True,
                   help='Pre-calibrated optical-grid and phase uncertainty, NOT inferred from camera metadata')
    args = p.parse_args()
    out = replay(waveform(args.photodiode), observations(args.camera), reference(args.reference),
                 args.residual_max, args.timing_envelope_ms,
                 native_sequence(args.sequence) if args.sequence else None)
    print(json.dumps(out, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
