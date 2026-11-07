#!/usr/bin/env python3
"""E002-586 finite-grid synthetic optical phase-scan instrument (NOT physical certification)."""
import argparse
import json
import math

GRID_S = [x / 2 for x in range(0, 9)]
GRID_E = [x / 2 for x in range(4, 13)]
GRID_D = [x / 20 for x in range(0, 5)]
REQUIRED = ('photodiode_edge_timed', 'linear_response_verified',
            'unclipped_pixels', 'row_geometry_verified',
            'rolling_mode_fixed', 'gain_and_dark_calibrated',
            'led_transition_bounded', 'same_imaging_path')


def reject(msg):
    raise ValueError(msg)


def brightness(s, e, p):
    return min(1., max(0., (s + e - p) / e))


def synth(s=2., e=4., d=.1, rows=(0, 20, 40), phases=None, row_offset=None):
    if phases is None:
        phases = [i / 2 for i in range(25)]
    return [{'row': r, 'phase_ms': p,
             'intensity': brightness(s + r * d + (row_offset or {}).get(r, 0), e, p)}
            for r in rows for p in phases]


def analyze(obs, controls, *, phase_unc_ms=0., intensity_unc=0.):
    if not isinstance(controls, dict) or not all(controls.get(k) is True for k in REQUIRED):
        reject('UNCALIBRATED_OPTICAL_OR_GEOMETRY_CONTROL')
    if any(type(x) not in (float, int) or not math.isfinite(x) or x < 0
           for x in (phase_unc_ms, intensity_unc)):
        reject('BAD_UNCERTAINTY')
    if not isinstance(obs, list) or not obs:
        reject('MISSING_PHASE_DATA')
    grouped = {}
    seen = set()
    for x in obs:
        if not isinstance(x, dict):
            reject('BAD_OBSERVATION')
        r, p, y = (x.get(k) for k in ('row', 'phase_ms', 'intensity'))
        if type(r) is not int or r < 0 or r > 10000 or any(
                type(v) not in (int, float) or not math.isfinite(v)
                for v in (p, y)) or not 0 <= y <= 1:
            reject('BAD_OBSERVATION')
        key = (r, p)
        if key in seen:
            reject('DUPLICATE_PHASE')
        seen.add(key)
        grouped.setdefault(r, []).append(x)
    if len(grouped) < 2:
        reject('INSUFFICIENT_ROW_GEOMETRY')
    for group in grouped.values():
        if len(group) < 6 or not any(.2 < x['intensity'] < .8 for x in group) or not (
                any(x['intensity'] <= .05 for x in group) and
                any(x['intensity'] >= .95 for x in group)):
            reject('UNIDENTIFIABLE_PHASE_SWEEP')
    candidates = []
    for s in GRID_S:
        for e in GRID_E:
            for d in GRID_D:
                ok = True
                for x in obs:
                    start = s + x['row'] * d
                    low = brightness(start, e, x['phase_ms'] + phase_unc_ms)
                    high = brightness(start, e, x['phase_ms'] - phase_unc_ms)
                    if low > x['intensity'] + intensity_unc + 1e-10 or high < x['intensity'] - intensity_unc - 1e-10:
                        ok = False
                        break
                if ok:
                    candidates.append((s, e, d))
    if not candidates:
        reject('MODEL_FALSIFIED_OR_GRID_MISSES_TRUTH')
    bounds = {str(r): [round(min(s + r*d for s,e,d in candidates), 8),
                       round(max(s + r*d + e for s,e,d in candidates), 8)]
              for r in sorted(grouped)}
    return {'experiment': 'E002-586', 'evidence_tier': 'FINITE_GRID_SYNTHETIC_INSTRUMENT',
            'feasible_grid_candidates': len(candidates), 'rows': len(grouped),
            'outer_exposure_support_ms_by_row': bounds,
            'physical_certificate': False, 'human_data': False,
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}


def fixtures():
    controls = {k: True for k in REQUIRED}
    data = synth()
    base = analyze(data, controls)
    assert base['feasible_grid_candidates'] == 1, base
    assert base['outer_exposure_support_ms_by_row'] == {'0': [2., 6.], '20': [4., 8.], '40': [6., 10.]}
    global_data = synth(d=0)
    assert analyze(global_data, controls)['feasible_grid_candidates'] == 1
    relaxed = analyze(data, controls, phase_unc_ms=.5, intensity_unc=.1)
    assert relaxed['feasible_grid_candidates'] >= base['feasible_grid_candidates']
    for row, interval in base['outer_exposure_support_ms_by_row'].items():
        wider = relaxed['outer_exposure_support_ms_by_row'][row]
        assert wider[0] <= interval[0] and wider[1] >= interval[1]
    try:
        analyze(synth(phases=[0, .5, 1, 11, 11.5, 12]), controls)
    except ValueError as exc:
        assert str(exc) == 'UNIDENTIFIABLE_PHASE_SWEEP'
    else:
        raise AssertionError('SATURATION_FALSE_CONFIDENCE')
    try:
        analyze([x for x in data if x['row'] != 20 or x['phase_ms'] < 2], controls)
    except ValueError as exc:
        assert str(exc) == 'UNIDENTIFIABLE_PHASE_SWEEP'
    else:
        raise AssertionError('MISSINGNESS_FALSE_CONFIDENCE')
    for key in REQUIRED:
        cc = dict(controls)
        cc[key] = False
        try:
            analyze(data, cc)
        except ValueError as exc:
            assert str(exc) == 'UNCALIBRATED_OPTICAL_OR_GEOMETRY_CONTROL'
        else:
            raise AssertionError('UNVERIFIED_' + key)
    try:
        analyze(synth(row_offset={40: 1.}), controls)
    except ValueError as exc:
        assert str(exc) == 'MODEL_FALSIFIED_OR_GRID_MISSES_TRUTH'
    else:
        raise AssertionError('NONAFFINE_NOT_DETECTED')
    bad = [dict(x) for x in data]
    bad[0]['intensity'] = .4
    try:
        analyze(bad, controls)
    except ValueError as exc:
        assert str(exc) == 'MODEL_FALSIFIED_OR_GRID_MISSES_TRUTH'
    else:
        raise AssertionError('INCONSISTENT_DATA_ACCEPTED')
    assert not base['physical_certificate']
    return {'synthetic_tests_passed': 16, 'exact_grid_candidates': 1,
            'exact_support_ms': base['outer_exposure_support_ms_by_row'],
            'relaxed_grid_candidates': relaxed['feasible_grid_candidates'],
            'relaxed_support_ms': relaxed['outer_exposure_support_ms_by_row'],
            'human_data': False, 'physical_shutter_captures': 0,
            'product': 'ABSTAIN_UNCALIBRATED', 'release': 'BLOCKED'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--self-test', action='store_true')
    p.add_argument('--input')
    args = p.parse_args()
    if args.self_test:
        print(json.dumps(fixtures(), sort_keys=True))
    elif args.input:
        from pathlib import Path
        payload = json.loads(Path(args.input).read_text())
        print(json.dumps(analyze(payload['observations'], payload['controls'],
                                 phase_unc_ms=payload['phase_unc_ms'],
                                 intensity_unc=payload['intensity_unc']), sort_keys=True))
    else:
        p.error('provide --self-test or --input')


if __name__ == '__main__':
    main()
