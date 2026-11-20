#!/usr/bin/env python3
"""E002-437: acceleration-conditioned reference velocity bridge (study-only).

No physiological acceleration bound is supplied or authenticated here. Even a
finite conditional output NEVER authorizes physical product measurements.
"""
import argparse
import json
import math
import random
from pathlib import Path


class VelocityBridgeError(ValueError):
    pass


NUISANCES = ('geometry', 'brightness', 'missingness', 'blur',
             'gaze', 'glasses', 'sampling', 'clock', 'occlusion', 'shutter')


def finite(value, name, positive=False):
    if type(value) not in (float, int) or not math.isfinite(value):
        raise VelocityBridgeError('nonfinite or invalid ' + name)
    if value <= 0 if positive else value < 0:
        raise VelocityBridgeError('negative or zero ' + name)
    return float(value)


def penalty(h, epsilon, acceleration):
    h = finite(h, 'sample spacing', positive=True)
    e = finite(epsilon, 'aperture error')
    a = finite(acceleration, 'acceleration')
    return 2 * e / h + a * h / 2


def optimal_spacing(epsilon, acceleration):
    e = finite(epsilon, 'aperture error', positive=True)
    a = finite(acceleration, 'acceleration', positive=True)
    h = 2 * math.sqrt(e / a)
    return {'optimal_spacing_s': h, 'optimal_reference_rate_hz': 1 / h,
            'minimum_penalty_mm_s': 2 * math.sqrt(e * a)}


def segment_upper(y0, y1, h, epsilon, acceleration, clock_error=0):
    """Conditional upper bound on |dx/dt| over true intersample segment.

    Observed aperture errors each <= epsilon, true times each within delta of
    nominal times, and |d²x/dt²| <= acceleration throughout true segment.
    """
    y0 = finite(y0, 'first aperture')
    y1 = finite(y1, 'second aperture')
    h = finite(h, 'nominal step', positive=True)
    e = finite(epsilon, 'aperture error')
    a = finite(acceleration, 'acceleration')
    d = finite(clock_error, 'clock error')
    if h <= 2 * d:
        raise VelocityBridgeError('clock uncertainty makes sample order ambiguous')
    return (abs(y1 - y0) + 2 * e) / (h - 2 * d) + a * (h + 2 * d) / 2


def adjudicate(record):
    fields = {'trace_id', 'frames', 'acceleration_upper_mm_s2',
              'aperture_error_mm', 'clock_error_s', 'max_step_s',
              'physical_scale_attested', 'sensor_timing_attested',
              'acceleration_bound_attested', 'nuisance_calibration_attested',
              'external_calibration_reference'}
    if type(record) is not dict or set(record) != fields:
        raise VelocityBridgeError('invalid record schema')
    if not isinstance(record['trace_id'], str) or not record['trace_id'].strip():
        raise VelocityBridgeError('invalid trace ID')
    if not isinstance(record['external_calibration_reference'], str) or not record['external_calibration_reference'].strip():
        raise VelocityBridgeError('missing calibration reference')
    flags = ('physical_scale_attested', 'sensor_timing_attested',
             'acceleration_bound_attested', 'nuisance_calibration_attested')
    if any(type(record[k]) is not bool for k in flags):
        raise VelocityBridgeError('invalid attestation flag')
    epsilon = finite(record['aperture_error_mm'], 'aperture error')
    delta = finite(record['clock_error_s'], 'clock error')
    max_step = finite(record['max_step_s'], 'max reference step', positive=True)
    accel = record['acceleration_upper_mm_s2']
    if accel is not None:
        accel = finite(accel, 'acceleration')
    frames = record['frames']
    if not isinstance(frames, list) or len(frames) < 2:
        raise VelocityBridgeError('at least two frames required')
    previous_id, previous_t = None, None
    for f in frames:
        if type(f) is not dict or set(f) != {'frame_id', 'time_s', 'aperture_mm', 'valid', 'nuisances'}:
            raise VelocityBridgeError('invalid frame schema')
        if type(f['frame_id']) is not int or f['frame_id'] < 0:
            raise VelocityBridgeError('invalid frame ID')
        if type(f['valid']) is not bool:
            raise VelocityBridgeError('invalid frame validity')
        if type(f['nuisances']) is not dict or set(f['nuisances']) != set(NUISANCES) or any(type(v) is not bool for v in f['nuisances'].values()):
            raise VelocityBridgeError('invalid explicit nuisance flags')
        t = finite(f['time_s'], 'timestamp')
        if f['aperture_mm'] is not None:
            finite(f['aperture_mm'], 'aperture')
        if f['valid'] and f['aperture_mm'] is None:
            raise VelocityBridgeError('valid frame missing aperture')
        if previous_id is not None and (f['frame_id'] <= previous_id or t <= previous_t):
            raise VelocityBridgeError('nonmonotone frame IDs or times')
        previous_id, previous_t = f['frame_id'], t
    result = {'experiment': 'E002-437', 'trace_id': record['trace_id'],
              'evidence_tier': 'CONDITIONAL_REFERENCE_VELOCITY_ONLY',
              'external_provenance_authenticated_by_code': False,
              'physical_certificate_authorized': False,
              'product': 'ABSTAIN_UNCALIBRATED',
              'reference_velocity_upper_mm_s': None, 'status': 'ABSTAIN',
              'reason': None, 'segments': 0}
    if not all(record[k] for k in flags):
        result['reason'] = 'independent_calibration_not_attested'
    elif accel is None:
        result['reason'] = 'acceleration_bound_unavailable'
    elif any(not f['valid'] or any(f['nuisances'].values()) for f in frames):
        result['reason'] = 'missing_or_nuisance_affected_reference'
    elif any(b['frame_id'] != a['frame_id'] + 1 for a, b in zip(frames, frames[1:])):
        result['reason'] = 'missing_reference_frame_id'
    elif any(b['time_s'] - a['time_s'] > max_step + 1e-12 for a, b in zip(frames, frames[1:])):
        result['reason'] = 'reference_gap_exceeds_protocol'
    elif any(b['time_s'] - a['time_s'] <= 2 * delta for a, b in zip(frames, frames[1:])):
        result['reason'] = 'clock_uncertainty_overlaps_samples'
    else:
        bounds = [segment_upper(a['aperture_mm'], b['aperture_mm'],
                                b['time_s'] - a['time_s'], epsilon, accel, delta)
                  for a, b in zip(frames, frames[1:])]
        result.update(status='CONDITIONAL_REFERENCE_BOUND',
                      reason='valid_only_if_external_physical_premises_hold',
                      reference_velocity_upper_mm_s=max(bounds), segments=len(bounds))
    return result


def demo(seed=437, traces=500):
    """Synthetic smooth-trace experiment with independent analytic derivative oracle."""
    rng = random.Random(seed)
    h = 1 / 400
    epsilon = .005
    max_margin = -math.inf
    violations = 0
    for _ in range(traces):
        amp = rng.uniform(.02, .25)
        frequency = rng.uniform(2.0, 8.0)
        phase = rng.uniform(0, 2 * math.pi)
        omega = 2 * math.pi * frequency
        A = amp * omega ** 2  # independently specified exact global acceleration cap
        t0 = rng.uniform(0, .5)
        x0 = 2.5 + amp * math.sin(omega * t0 + phase)
        x1 = 2.5 + amp * math.sin(omega * (t0 + h) + phase)
        y0 = x0 + rng.uniform(-epsilon, epsilon)
        y1 = x1 + rng.uniform(-epsilon, epsilon)
        U = segment_upper(y0, y1, h, epsilon, A)
        # Independent analytic maximum of |dx/dt|: endpoints and all cos extrema.
        times = [t0, t0 + h]
        k_lo = math.ceil((omega * t0 + phase) / math.pi)
        k_hi = math.floor((omega * (t0 + h) + phase) / math.pi)
        times.extend((k * math.pi - phase) / omega for k in range(k_lo, k_hi + 1))
        truth = max(abs(amp * omega * math.cos(omega * t + phase)) for t in times)
        max_margin = max(max_margin, truth - U)
        violations += truth > U + 1e-10
    # Independent adversarial quadratic: true acceleration is 3600, but a
    # false zero-acceleration assertion would understate endpoint speed.
    hq, v0, Aq, eq = .0025, 30.0, 3600.0, .005
    y0 = 2.0 + eq
    y1 = 2.0 + v0*hq - Aq*hq*hq/2 - eq
    falsification = {
        'true_initial_speed_mm_s': v0,
        'observed_secant_mm_s': round((y1-y0)/hq, 8),
        'valid_conditional_bound_mm_s': round(segment_upper(y0,y1,hq,eq,Aq), 8),
        'false_zero_acceleration_bound_mm_s': round(segment_upper(y0,y1,hq,eq,0), 8),
        'false_zero_localization_error_bound_mm_s': round(segment_upper(y0,y1,hq,0,Aq), 8),
    }
    return {'experiment': 'E002-437', 'evidence': 'SYNTHETIC_SMOOTH_TRACE_ONLY',
            'seed': seed, 'traces': traces, 'violations_under_true_premises': violations,
            'adversarial_misspecification': falsification,
            'maximum_truth_minus_bound_mm_s': round(max_margin, 10),
            'sampling_penalty_mm_s': {str(hz): round(penalty(1/hz, .005, 3600), 8)
                                       for hz in (200, 400, 1000)},
            'optimal_spacing': optimal_spacing(.005, 3600),
            'human_participants': 0, 'product': 'ABSTAIN_UNCALIBRATED',
            'physical_certificate_authorized': False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--private-record', help='private calibrated-reference JSON; never upload human data')
    p.add_argument('--output', help='private output JSON')
    p.add_argument('--traces', type=int, default=500)
    a = p.parse_args()
    if a.traces < 1 or a.traces > 100000:
        p.error('traces must be 1..100000')
    result = adjudicate(json.loads(Path(a.private_record).read_text())) if a.private_record else demo(traces=a.traces)
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if a.output:
        Path(a.output).write_text(text)
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
