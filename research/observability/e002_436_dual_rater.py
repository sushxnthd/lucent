"""E002-436: exact conditional reference-envelope adjudicator (study-only).

Two independently blinded aperture raters must agree on physical intervals.
Metadata declarations are NOT independently authenticated by this code.
Never authorizes a physical measurement product claim.
"""
import argparse
import bisect
import json
import math
from pathlib import Path


class ReferenceError(ValueError):
    pass


def number(x, name, *, minimum=0):
    if type(x) not in (int, float) or not math.isfinite(x) or x < minimum:
        raise ReferenceError(f'invalid {name}')
    return float(x)


def _bool(data, name):
    if type(data.get(name)) is not bool:
        raise ReferenceError(f'missing boolean {name}')
    return data[name]


def exact_lipschitz_lower(times, lowers, velocity, start, end, clock_error):
    """Exact min_t max_i[l_i - V(|t-t_i|+delta)] over [start,end].

    This is the greatest pointwise lower bound implied by the stipulated
    sample lower limits and a common Lipschitz velocity cap. The value is
    not an unconditional anatomical lower bound without verified premises.
    """
    v = number(velocity, 'velocity', minimum=1e-15)
    delta = number(clock_error, 'clock_error')
    start = number(start, 'start')
    end = number(end, 'end')
    if end <= start or not times or len(times) != len(lowers):
        raise ReferenceError('invalid envelope domain')
    ts = [number(t, 'sample time') for t in times]
    ls = [number(l, 'sample lower') - v * delta for l in lowers]
    if any(b <= a for a, b in zip(ts, ts[1:])):
        raise ReferenceError('sample times must increase')
    n = len(ts)
    prefix = [0.0] * n
    suffix = [0.0] * n
    for i in range(n):
        z = ls[i] + v * ts[i]
        prefix[i] = max(prefix[i-1], z) if i else z
    for i in range(n-1, -1, -1):
        z = ls[i] - v * ts[i]
        suffix[i] = max(suffix[i+1], z) if i < n-1 else z

    # Between samples the envelope is the maximum of one descending and
    # one ascending affine line. Its minimum is at their intersection or
    # at a segment endpoint. Including start/end and all sample times
    # gives an exact global minimum, without temporal grid sampling.
    boundaries = [start] + [t for t in ts if start < t < end] + [end]
    minimum = float('inf')
    argmin = None
    for left, right in zip(boundaries, boundaries[1:]):
        mid = (left + right) / 2
        i = bisect.bisect_right(ts, mid) - 1
        j = i + 1
        A = prefix[i] if i >= 0 else None
        B = suffix[j] if j < n else None
        candidates = [left, right]
        if A is not None and B is not None:
            candidates.append(max(left, min(right, (A-B)/(2*v))))
        for t in candidates:
            val = max((A - v*t) if A is not None else -float('inf'),
                      (B + v*t) if B is not None else -float('inf'))
            # At a sample boundary a cone's apex must be included; for
            # segment interiors this is already represented by A or B.
            k = bisect.bisect_left(ts, t)
            if k < n and ts[k] == t:
                val = max(val, ls[k])
            if val < minimum:
                minimum, argmin = val, t
    return {'lower_envelope_mm': max(0.0, minimum), 'argmin_s': argmin}


def adjudicate(trial):
    required = {'trial_id', 'interval_start_s', 'interval_end_s', 'threshold_mm',
                'clock_error_s', 'max_reference_step_s', 'velocity_upper_mm_s',
                'velocity_bound_attested', 'sensor_timing_attested',
                'physical_scale_attested', 'rater_blinding_attested', 'frames'}
    if not isinstance(trial, dict) or set(trial) != required:
        raise ReferenceError('invalid trial schema')
    if not isinstance(trial['trial_id'], str) or not trial['trial_id'].strip():
        raise ReferenceError('invalid trial_id')
    a = number(trial['interval_start_s'], 'start')
    b = number(trial['interval_end_s'], 'end')
    theta = number(trial['threshold_mm'], 'threshold')
    delta = number(trial['clock_error_s'], 'clock error')
    step = number(trial['max_reference_step_s'], 'max reference step', minimum=1e-15)
    if b <= a:
        raise ReferenceError('invalid trial interval')
    flags = {key: _bool(trial, key) for key in ('velocity_bound_attested',
             'sensor_timing_attested', 'physical_scale_attested', 'rater_blinding_attested')}
    v = trial['velocity_upper_mm_s']
    if v is not None:
        v = number(v, 'velocity', minimum=1e-15)
    frames = trial['frames']
    if not isinstance(frames, list) or not frames:
        raise ReferenceError('missing reference frames')
    times, lowers, uppers, ids, positives = [], [], [], [], []
    corrupted = []
    ambiguous_witness = []
    partial_witness = []
    for frame in frames:
        if not isinstance(frame, dict) or set(frame) != {'frame_id','time_s','nuisance_ok','rater_a','rater_b'}:
            raise ReferenceError('invalid frame schema')
        fid = frame['frame_id']
        if type(fid) is not int or fid < 0 or (ids and fid <= ids[-1]):
            raise ReferenceError('nonmonotone frame IDs')
        t = number(frame['time_s'], 'time')
        if times and t <= times[-1]:
            raise ReferenceError('nonmonotone reference times')
        if type(frame['nuisance_ok']) is not bool:
            raise ReferenceError('invalid nuisance flag')
        ids.append(fid)
        times.append(t)
        rater_intervals = []
        for name in ('rater_a','rater_b'):
            pair = frame[name]
            if pair is None:
                rater_intervals = []
                break
            if not isinstance(pair, list) or len(pair) != 2:
                raise ReferenceError('invalid rater interval')
            low = number(pair[0], 'aperture lower')
            high = number(pair[1], 'aperture upper')
            if low > high:
                raise ReferenceError('inverted aperture interval')
            rater_intervals.append((low, high))
        if not frame['nuisance_ok'] or len(rater_intervals) != 2:
            lowers.append(None)
            uppers.append(None)
            corrupted.append(fid)
            continue
        low = max(rater_intervals[0][0], rater_intervals[1][0])
        high = min(rater_intervals[0][1], rater_intervals[1][1])
        if low > high:
            lowers.append(None)
            uppers.append(None)
            corrupted.append(fid)
            continue
        lowers.append(low)
        uppers.append(high)
        if min(rater_intervals[0][1],rater_intervals[1][1]) <= theta and t+delta >= a and t-delta <= b:
            if max(rater_intervals[0][1],rater_intervals[1][1]) > theta:
                partial_witness.append(fid)
            elif a <= t-delta and t+delta <= b:
                positives.append(fid)
            else:
                ambiguous_witness.append(fid)
    out = {'experiment':'E002-436', 'trial_id':trial['trial_id'],
           'evidence_tier':'CONDITIONAL_REFERENCE_INSTRUMENT_ONLY',
           'product':'ABSTAIN_UNCALIBRATED', 'product_claim_authorized':False,
           'external_provenance_authenticated_by_code':False,
           'reference_label':'UNRESOLVED', 'reason':'',
           'lower_envelope_mm':None, 'argmin_s':None,
           'witnessed_frame_ids':positives, 'clock_ambiguous_witness_frame_ids':ambiguous_witness,
           'single_rater_witness_frame_ids':partial_witness, 'invalid_frame_ids':corrupted}
    if not all(flags[k] for k in ('sensor_timing_attested','physical_scale_attested','rater_blinding_attested')):
        out['reason'] = 'physical_provenance_or_blinding_not_attested'
    elif positives:
        out['reference_label'] = 'WITNESSED_CROSSING'
        out['reason'] = 'dual_rater_interval_below_threshold'
    elif corrupted:
        out['reason'] = 'missing_nuisance_or_rater_disagreement'
    elif ambiguous_witness:
        out['reason'] = 'witness_frame_clock_overlap_not_contained'
    elif partial_witness:
        out['reason'] = 'single_rater_crossing_not_corroborated'
    elif not flags['velocity_bound_attested'] or v is None:
        out['reason'] = 'no_independently_attested_velocity_bound'
    elif times[0] > a or times[-1] < b:
        out['reason'] = 'reference_does_not_bracket_interval'
    elif any(y-x > step + 1e-12 for x,y in zip(times, times[1:])):
        out['reason'] = 'reference_gap_exceeds_protocol'
    elif any(y-x <= 2*delta for x,y in zip(times,times[1:])):
        out['reason'] = 'reference_clock_order_unresolved'
    elif any(l1 > u2 + v*(abs(t2-t1)+2*delta) or l2 > u1 + v*(abs(t2-t1)+2*delta)
             for i,(t1,l1,u1) in enumerate(zip(times,lowers,uppers))
             for t2,l2,u2 in zip(times[i+1:],lowers[i+1:],uppers[i+1:])):
        out['reason'] = 'reference_intervals_incompatible_with_velocity'
    else:
        env = exact_lipschitz_lower(times, lowers, v, a, b, delta)
        out.update(env)
        if env['lower_envelope_mm'] > theta:
            out['reference_label'] = 'NEGATIVE_CONDITIONAL'
            out['reason'] = 'exact_lipschitz_envelope_excludes_crossing'
        else:
            out['reason'] = 'reference_sampling_cannot_exclude_crossing'
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--private-trial', required=True, help='locally held dual-rater reference JSON')
    p.add_argument('--output', help='write private result instead of stdout')
    args = p.parse_args()
    result = json.dumps(adjudicate(json.loads(Path(args.private_trial).read_text())), indent=2, sort_keys=True) + '\n'
    if args.output:
        Path(args.output).write_text(result)
    else:
        print(result, end='')


if __name__ == '__main__':
    main()
