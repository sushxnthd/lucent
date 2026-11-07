"""E002-427: study-only high-rate aperture-trace validation adapter.

Inputs must be deidentified, independently calibrated physical aperture traces.
Never converts video pixels or 3D marker distances into aperture, never authorizes
real-camera or medical claims. Only Python standard library is required.
"""
import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

NUISANCES = ('brightness', 'blur', 'gaze', 'glasses', 'occlusion', 'missingness', 'clock', 'geometry')


def _finite(x):
    v = float(x)
    if not math.isfinite(v):
        raise ValueError('nonfinite numeric input')
    return v


def load_trace(path):
    by_subject = defaultdict(list)
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        needed = {'participant_id', 'time_s', 'aperture_mm', 'valid'} | {'nuisance_' + n for n in NUISANCES}
        if not needed.issubset(reader.fieldnames or []):
            raise ValueError('missing required CSV columns')
        for row in reader:
            subject = row['participant_id'].strip()
            if not subject or '/' in subject or '\\' in subject:
                raise ValueError('invalid pseudonym')
            valid = row['valid']
            if valid not in ('0', '1'):
                raise ValueError('valid must be 0 or 1')
            nuisances = {}
            for n in NUISANCES:
                value = row['nuisance_' + n]
                if value not in ('0', '1'):
                    raise ValueError('nuisance flags must be 0 or 1')
                nuisances[n] = bool(int(value))
            t = _finite(row['time_s'])
            a = _finite(row['aperture_mm']) if valid == '1' else None
            if t < 0 or (a is not None and a < 0):
                raise ValueError('invalid time or aperture')
            by_subject[subject].append((t, a, nuisances))
    if not by_subject:
        raise ValueError('empty study')
    for subject, rows in by_subject.items():
        if len(rows) < 3 or any(y[0] <= x[0] for x, y in zip(rows, rows[1:])):
            raise ValueError('insufficient or unsorted samples: ' + subject)
    return dict(by_subject)


def _integral_linear(rows, lo, hi, max_dt):
    """Exact integral of the piecewise-linear interpolation, or None if uncovered."""
    if lo < rows[0][0] - 1e-12 or hi > rows[-1][0] + 1e-12 or hi <= lo:
        return None
    total = 0.0
    covered = 0.0
    for (t0, y0, n0), (t1, y1, n1) in zip(rows, rows[1:]):
        left, right = max(lo, t0), min(hi, t1)
        if right <= left:
            continue
        if y0 is None or y1 is None or t1-t0 > max_dt or any(n0.values()) or any(n1.values()):
            return None
        yl = y0 + (y1-y0)*(left-t0)/(t1-t0)
        yr = y0 + (y1-y0)*(right-t0)/(t1-t0)
        total += (yl+yr)*0.5*(right-left)
        covered += right-left
    if abs(covered-(hi-lo)) > 1e-9:
        return None
    return total/(hi-lo)


def _config(config):
    required = ('training_participants', 'holdout_participants', 'period_s', 'exposure_s',
                'threshold_mm', 'velocity_hypothesis_mm_s', 'reference_speed_hypothesis_mm_s',
                'aperture_error_mm', 'clock_error_s', 'max_reference_step_s',
                'physical_aperture_registration_ref', 'source_access_ref')
    if not all(k in config for k in required):
        raise ValueError('missing required configuration')
    tr, ho = config['training_participants'], config['holdout_participants']
    if not tr or not ho or set(tr)&set(ho) or len(set(tr))!=len(tr) or len(set(ho))!=len(ho):
        raise ValueError('invalid disjoint split')
    if not all(isinstance(config[k], str) and config[k].strip() for k in
               ('physical_aperture_registration_ref', 'source_access_ref')):
        raise ValueError('missing registration/source reference')
    for k in required[2:11]:
        if k in ('physical_aperture_registration_ref', 'source_access_ref'):
            continue
        config[k] = _finite(config[k])
    if not (0 < config['exposure_s'] <= config['period_s'] and
            config['period_s'] > 0 and config['max_reference_step_s'] > 0 and
            config['velocity_hypothesis_mm_s'] > 0 and config['reference_speed_hypothesis_mm_s'] > 0 and
            config['threshold_mm'] >= 0 and config['aperture_error_mm'] >= 0 and config['clock_error_s'] >= 0):
        raise ValueError('invalid physical parameters')
    return config


def _reference_label(rows, start, end, cfg):
    selected = [r for r in rows if start <= r[0] <= end]
    if len(selected) < 2:
        return 'UNRESOLVED'
    # A definite, nuisance-free observed crossing remains a falsification even
    # when other samples in the interval are missing or ambiguous.
    if any(r[1] is not None and not any(r[2].values()) and
           r[1]+cfg['aperture_error_mm'] <= cfg['threshold_mm'] for r in selected):
        return 'WITNESSED_CROSSING'
    if any(r[1] is None or any(r[2].values()) for r in selected):
        return 'UNRESOLVED'
    if selected[0][0] > start + cfg['max_reference_step_s'] or selected[-1][0] < end - cfg['max_reference_step_s']:
        return 'UNRESOLVED'
    if any(b[0]-a[0] > cfg['max_reference_step_s'] for a,b in zip(selected, selected[1:])):
        return 'UNRESOLVED'
    # This negative label is *conditional* on an independently justified reference speed cap.
    max_nearest_distance = max(selected[0][0]-start, end-selected[-1][0],
                               max(b[0]-a[0] for a,b in zip(selected, selected[1:]))/2)
    conservative_min = min(r[1] for r in selected) - cfg['aperture_error_mm'] - cfg['reference_speed_hypothesis_mm_s'] * max_nearest_distance
    return 'NEGATIVE_CONDITIONAL' if conservative_min > cfg['threshold_mm'] else 'UNRESOLVED'


def analyze(trace, raw_config):
    cfg = _config(dict(raw_config))
    if set(trace) != set(cfg['training_participants']) | set(cfg['holdout_participants']):
        raise ValueError('trace/split participants mismatch')
    out = {'evidence_tier':'SYNTHETIC_VIRTUAL_CAMERA_ON_HUMAN_TRACE_IF_PROVIDED',
           'product':'ABSTAIN_UNCALIBRATED', 'physical_certificate_authorized':False,
           'hypotheses_not_hard_bounds':True, 'participants':{},
           'pooled':{'conditional':0,'witnessed_failures':0,'unresolved':0,'negative_conditional':0,'abstain':0}}
    for participant in cfg['holdout_participants']:
        rows = trace[participant]
        slopes = [abs((b[1]-a[1])/(b[0]-a[0])) for a,b in zip(rows, rows[1:])
                  if a[1] is not None and b[1] is not None and not any(a[2].values()) and not any(b[2].values())]
        stats = {'samples':len(rows), 'observed_max_secant_mm_s':max(slopes) if slopes else None,
                 'secant_exceeds_hypothesis':bool(slopes and max(slopes) > cfg['velocity_hypothesis_mm_s']),
                 'conditional':0,'witnessed_failures':0,'unresolved':0,'negative_conditional':0,'abstain':0}
        period, exposure = cfg['period_s'], cfg['exposure_s']
        # Exact virtual exposure centers are defined from first observed time; no real shutter inference.
        center = rows[0][0] + exposure/2
        while center + period + exposure/2 <= rows[-1][0] + 1e-12:
            a = _integral_linear(rows, center-exposure/2, center+exposure/2, cfg['max_reference_step_s'])
            b = _integral_linear(rows, center+period-exposure/2, center+period+exposure/2, cfg['max_reference_step_s'])
            start, end = center-exposure/2, center+period+exposure/2
            if a is None or b is None:
                stats['abstain'] += 1
            else:
                # Conservative interpolation envelope V_ref*dt/2; not a validated physical cap.
                epsilon = cfg['aperture_error_mm'] + cfg['reference_speed_hypothesis_mm_s']*cfg['max_reference_step_s']/2 + cfg['velocity_hypothesis_mm_s']*cfg['clock_error_s']
                balanced = abs(a-b)+2*epsilon <= cfg['velocity_hypothesis_mm_s']*max(0, period-exposure-2*cfg['clock_error_s'])
                lower = (a+b-cfg['velocity_hypothesis_mm_s']*period)/2 - epsilon
                if balanced and lower > cfg['threshold_mm']:
                    stats['conditional'] += 1
                    label = _reference_label(rows, start, end, cfg)
                    if label == 'WITNESSED_CROSSING':
                        stats['witnessed_failures'] += 1
                    elif label == 'UNRESOLVED':
                        stats['unresolved'] += 1
                    else:
                        stats['negative_conditional'] += 1
                else:
                    stats['abstain'] += 1
            center += period
        out['participants'][participant] = stats
        for k in out['pooled']:
            out['pooled'][k] += stats[k]
    n = out['pooled']['conditional']
    out['pooled']['finite_set_false_fraction_interval'] = ([out['pooled']['witnessed_failures']/n,
        (out['pooled']['witnessed_failures']+out['pooled']['unresolved'])/n] if n else None)
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--csv', required=True, help='private normalized aperture CSV; never upload')
    p.add_argument('--config', required=True)
    p.add_argument('--output', help='private output JSON (stdout if omitted)')
    a = p.parse_args()
    report = analyze(load_trace(a.csv), json.loads(Path(a.config).read_text(encoding='utf-8')))
    result = json.dumps(report, sort_keys=True, indent=2) + '\n'
    if a.output:
        Path(a.output).write_text(result, encoding='utf-8')
    else:
        print(result, end='')


if __name__ == '__main__':
    main()
