#!/usr/bin/env python3
"""E002-562 one-sided, sealed, participant-disjoint 400->30Hz replay.

Research-only ideal point-sample counterfactual. This code cannot authenticate human
sensor provenance, shutter response, independent velocity ceilings, or raters.
"""
import argparse
import bisect
import hashlib
import json
import math
from pathlib import Path

SCHEMA = 'lucent-e002-562-v1'
SPLIT_SALT = 'lucent-e002-550-v1|'
FPS = 30
PHASES = 13
HIGH_DT = 1 / 400
QUANTIZATION_S = HIGH_DT / 2
REQUIRED = ('anatomy_verified', 'sensor_timing_verified',
            'instantaneous_transfer_verified', 'velocity_independent',
            'exposure_point_model_verified', 'nuisance_envelope_verified')


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(obj):
    return hashlib.sha256(canonical(obj).encode()).hexdigest()


def number(x, nonnegative=True):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError('nonfinite or nonnumeric quantity')
    if nonnegative and x < 0:
        raise ValueError('negative quantity')
    return float(x)


def split(ids):
    if len(ids) != 8 or len(set(ids)) != 8 or any(not isinstance(i, str) or not i for i in ids):
        raise ValueError('require eight unique opaque participant IDs')
    ordered = sorted(ids, key=lambda i: hashlib.sha256((SPLIT_SALT+i).encode()).hexdigest())
    return set(ordered[:4]), set(ordered[4:])


def validate(data):
    if data.get('schema') != SCHEMA:
        raise ValueError('schema mismatch')
    source = data.get('source_sha256')
    if not isinstance(source, str) or len(source) != 64 or any(c not in '0123456789abcdef' for c in source):
        raise ValueError('source hash missing')
    if any(k in canonical(data) for k in ('reference_positive', 'ref_closed', 'ground_truth', 'closed_label')):
        raise ValueError('prediction input must not include reference labels')
    participants = data.get('participants')
    if not isinstance(participants, list):
        raise ValueError('participants missing')
    _, held = split([p.get('id') for p in participants])
    for p in participants:
        samples = p.get('samples')
        if not isinstance(samples, list) or len(samples) < 15:
            raise ValueError('insufficient samples')
        last = -math.inf
        for s in samples:
            t, a = number(s.get('t_s')), number(s.get('a'))
            if t <= last:
                raise ValueError('nonmonotone sensor times')
            last = t
            if not isinstance(s.get('nuisance'), list) or any(not isinstance(v, str) for v in s['nuisance']):
                raise ValueError('invalid nuisance list')
    cert = data.get('certificate', {})
    if not isinstance(cert, dict):
        raise ValueError('certificate invalid')
    for k in ('velocity_hard_bound', 'aperture_error', 'clock_error_s', 'threshold'):
        if k in cert and cert[k] is not None:
            number(cert[k])
    if 'threshold' not in cert or not 0 < number(cert['threshold']) < 1:
        raise ValueError('closure threshold must be (0,1)')
    return held


def predict(data):
    held = validate(data)
    cert = data['certificate']
    calibrated = all(cert.get(k) is True for k in REQUIRED) and all(
        cert.get(k) is not None for k in ('velocity_hard_bound', 'aperture_error', 'clock_error_s'))
    v = number(cert['velocity_hard_bound']) if calibrated else None
    e = number(cert['aperture_error']) if calibrated else None
    u = number(cert['clock_error_s']) + QUANTIZATION_S if calibrated else None
    theta = number(cert['threshold'])
    rows = []
    for p in data['participants']:
        if p['id'] not in held:
            continue
        ss = p['samples']
        times = [s['t_s'] for s in ss]
        for phase in range(PHASES):
            selected = []
            k = 0
            while True:
                target = times[0] + phase*HIGH_DT + k/FPS
                if target > times[-1] + 1e-12:
                    break
                i = bisect.bisect_left(times, target)
                choices = [j for j in (i-1, i) if 0 <= j < len(ss)]
                if choices:
                    j = min(choices, key=lambda z: abs(times[z]-target))
                    if abs(times[j]-target) <= QUANTIZATION_S + 1e-9 and (not selected or j > selected[-1]):
                        selected.append(j)
                k += 1
            for j0, j1 in zip(selected, selected[1:]):
                s0, s1 = ss[j0], ss[j1]
                d = s1['t_s'] - s0['t_s']
                decision = 'ABSTAIN'
                lower = None
                reason = 'NO_INDEPENDENT_CERTIFICATE'
                if calibrated:
                    reason = 'NUISANCE_OR_MISSINGNESS'
                    if not s0['nuisance'] and not s1['nuisance'] and d <= 1/FPS + 2*QUANTIZATION_S + 1e-8:
                        reason = 'UNRESOLVED'
                        if abs(s1['a']-s0['a']) > v*(d+2*u)+2*e+1e-12:
                            reason = 'INCONSISTENT_WITH_HARD_BOUND'
                        else:
                            lower = max(0., (s0['a']+s1['a']-2*e-v*(d+2*u))/2)
                            if s0['a']-e > theta and s1['a']-e > theta and lower > theta+1e-12:
                                decision, reason = 'EXCLUDE_CONDITIONAL', 'IDEAL_POINT_ONLY'
                rows.append({'participant_id':p['id'], 'phase':phase, 't0':s0['t_s'],
                             't1':s1['t_s'], 'decision':decision, 'reason':reason,
                             'lower':lower})
    payload = {'schema':SCHEMA, 'source_sha256':data['source_sha256'],
               'heldout_split_hash':digest(sorted(held)), 'fps':FPS,
               'phases':PHASES, 'counterfactual':'IDEAL_POINT_SAMPLES_ONLY',
               'rows':rows, 'certificates_external_unverified':True,
               'product':'ABSTAIN_UNCALIBRATED', 'release':'BLOCKED'}
    payload['prediction_sha256'] = digest(payload)
    return payload


def adjudicate(pred, witness):
    sealed = dict(pred)
    supplied = sealed.pop('prediction_sha256', None)
    if supplied != digest(sealed):
        raise ValueError('prediction seal mismatch')
    if pred.get('schema') != SCHEMA or pred.get('counterfactual') != 'IDEAL_POINT_SAMPLES_ONLY':
        raise ValueError('prediction schema mismatch')
    if witness.get('source_sha256') != pred['source_sha256']:
        raise ValueError('witness source mismatch')
    positives = witness.get('positives')
    if not isinstance(positives, list):
        raise ValueError('missing positive witnesses')
    seen = set()
    positive = []
    for x in positives:
        pid = x.get('participant_id')
        t = number(x.get('t_s'))
        uncertainty = number(x.get('timing_error_s'))
        key = (pid, t)
        if key in seen:
            raise ValueError('duplicate positive witness')
        seen.add(key)
        positive.append((pid, t, uncertainty))
    counts = {'EXCLUDE_CONDITIONAL':0, 'ABSTAIN':0}
    reasons = {}
    candidates = 0
    affected = set()
    for r in pred['rows']:
        counts[r['decision']] += 1
        reasons[r['reason']] = reasons.get(r['reason'], 0) + 1
        if r['decision'] == 'EXCLUDE_CONDITIONAL':
            for pid, t, uncertainty in positive:
                if pid == r['participant_id'] and r['t0']+uncertainty < t < r['t1']-uncertainty:
                    candidates += 1
                    affected.add(pid)
    return {'schema':SCHEMA, 'prediction_sha256':supplied,
            'heldout_participants':len(set(r['participant_id'] for r in pred['rows'])),
            'phase_count':PHASES, 'conditional_exclusions':counts['EXCLUDE_CONDITIONAL'],
            'abstentions':counts['ABSTAIN'], 'reasons':reasons,
            'positive_witness_candidates':candidates,
            'participants_with_candidates':len(affected),
            'reference_negative_evidence':'CENSORED',
            'external_provenance_verified':False,
            'human_physical_validation':False,
            'certified_exclusions':0,
            'product':'ABSTAIN_UNCALIBRATED', 'release':'BLOCKED'}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='command', required=True)
    p = sub.add_parser('predict')
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    a = sub.add_parser('adjudicate')
    a.add_argument('--prediction', required=True)
    a.add_argument('--witness', required=True)
    a.add_argument('--output', required=True)
    args = ap.parse_args()
    if args.command == 'predict':
        result = predict(json.loads(Path(args.input).read_text()))
    else:
        result = adjudicate(json.loads(Path(args.prediction).read_text()),
                            json.loads(Path(args.witness).read_text()))
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows',)}, indent=2))


if __name__ == '__main__':
    main()
