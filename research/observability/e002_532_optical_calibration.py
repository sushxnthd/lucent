"""E002-532: discrete-grid LED duty-cycle shutter calibration, research only.

This is an instrument study handoff, not a physical measurement or human result.
All times are in milliseconds. Never certify exposure/clock from a grid fit.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction as Q
from itertools import product
from pathlib import Path

OFFSET_Q = (1,1,3,0,1,2,2,2,1,3,2,2,0,0,2,0,0,2,2,1,0,0,2,3,2,3,3,0,3,2,1,1,1,0,3,0,2,2,3,2)
WIDTH_Q = (6,2,4,2,5,3,6,3,4,3,6,6,2,2,3,6,6,3,3,5,6,4,6,2,6,6,2,2,4,6,2,4,5,2,2,5,5,4,2,6)
REQUIRED_ATTESTATIONS = (
    'independent_photodiode_clock', 'linear_photometry_verified',
    'native_frame_identity_verified', 'rolling_row_geometry_verified',
    'camera_clock_trace_verified',
)


def rational(value):
    if isinstance(value, bool) or value is None:
        raise ValueError('invalid rational value')
    try:
        return Q(str(value))
    except (ValueError, ZeroDivisionError, TypeError) as exc:
        raise ValueError('invalid rational value') from exc


def overlap_on(start, end, pulses):
    return sum((max(Q(0), min(end, b) - max(start, a)) for a, b in pulses), Q(0))


def predicted(t, row, delta, exposure, row_delay, pulses):
    if exposure <= 0:
        raise ValueError('exposure must be positive')
    start = t + delta + row * row_delay
    return overlap_on(start, start + exposure, pulses) / exposure


def synthetic_input():
    pulses = [(Q(5*k) + Q(OFFSET_Q[k],4), Q(5*k) + Q(OFFSET_Q[k]+WIDTH_Q[k],4)) for k in range(40)]
    frames = []
    for i in range(20):
        for row in (0,2,4):
            frames.append(dict(native_frame_id=f'f{i:02d}', t_ms=str(10*i), row=row,
                brightness=str(predicted(Q(10*i), Q(row), Q(1), Q(2), Q(1,2), pulses)),
                partition='train' if i < 10 else 'holdout'))
    return dict(version='E002-532-v1', evidence_tier='synthetic_not_physical',
        pulses=[dict(start_ms=str(a), end_ms=str(b)) for a,b in pulses],
        frames=frames, grid=dict(delta_ms=['-1','0','1','2'], exposure_ms=['1','2','3'], row_delay_ms=['0','1/2','1']),
        brightness_tolerance='1/50', attestations={k:False for k in REQUIRED_ATTESTATIONS})


def evaluate(data):
    if not isinstance(data, dict) or data.get('version') != 'E002-532-v1':
        raise ValueError('unsupported schema version')
    if data.get('evidence_tier') not in ('synthetic_not_physical','physical_input_unverified'):
        raise ValueError('evidence tier must be explicit')
    raw_pulses = data.get('pulses')
    if not isinstance(raw_pulses, list) or not raw_pulses:
        raise ValueError('pulses required')
    pulses = []
    for p in raw_pulses:
        a,b = rational(p['start_ms']),rational(p['end_ms'])
        if a >= b or (pulses and a < pulses[-1][1]):
            raise ValueError('pulses must be ordered, non-overlapping and positive')
        pulses.append((a,b))
    grid = data.get('grid')
    if not isinstance(grid,dict):
        raise ValueError('candidate grid required')
    names = ('delta_ms','exposure_ms','row_delay_ms')
    axes = []
    for name in names:
        values = grid.get(name)
        if not isinstance(values,list) or not values or len(values)>100 or len(set(map(str,values)))!=len(values):
            raise ValueError('invalid grid axis: '+name)
        axes.append([rational(x) for x in values])
    if any(x<=0 for x in axes[1]) or any(x<0 for x in axes[2]):
        raise ValueError('invalid exposure or row delay')
    if len(axes[0])*len(axes[1])*len(axes[2])>10000:
        raise ValueError('candidate grid too large')
    tol = rational(data.get('brightness_tolerance'))
    if not Q(0) <= tol < Q(1,2):
        raise ValueError('invalid tolerance')
    records = data.get('frames')
    if not isinstance(records,list) or not records:
        raise ValueError('frame observations required')
    seen=set(); train=[]; holdout=[]; missing=0
    for f in records:
        fid=f.get('native_frame_id'); row=rational(f.get('row')); t=rational(f.get('t_ms'))
        if not isinstance(fid,str) or not fid or row<0 or row.denominator!=1:
            raise ValueError('invalid frame identity/row')
        key=(fid,row)
        if key in seen:
            raise ValueError('duplicate native frame row')
        seen.add(key)
        part=f.get('partition')
        if part not in ('train','holdout'):
            raise ValueError('unfrozen train/holdout partition')
        if f.get('valid',True) is False:
            if 'brightness' in f:
                raise ValueError('invalid frame must not supply brightness')
            missing+=1
            continue
        y=rational(f.get('brightness'))
        if not Q(0)<=y<=Q(1):
            raise ValueError('brightness must be normalized 0..1')
        (train if part=='train' else holdout).append((t,row,y))
    if not train or not holdout:
        raise ValueError('nonempty train and holdout observations required')
    feasible=[]
    for d,e,r in product(*axes):
        if all(abs(predicted(t,row,d,e,r,pulses)-y)<=tol for t,row,y in train):
            feasible.append((d,e,r))
    result=dict(version='E002-532-v1',evidence_tier=data['evidence_tier'],
        candidate_count=len(axes[0])*len(axes[1])*len(axes[2]),
        feasible_train_count=len(feasible),train_rows=len(train),holdout_rows=len(holdout),
        missing_rows=missing,release='BLOCKED',product='ABSTAIN_UNCALIBRATED',
        limitation='Discrete-grid fit only; not a continuous-time or independently authenticated camera calibration')
    if not feasible:
        result['decision']='MODEL_FALSIFIED'
        return result
    if len(feasible)!=1:
        result['decision']='AMBIGUOUS_GRID'
        return result
    d,e,r=feasible[0]
    result['fit_grid_only']=dict(delta_ms=str(d),exposure_ms=str(e),row_delay_ms=str(r))
    max_err=max(abs(predicted(t,row,d,e,r,pulses)-y) for t,row,y in holdout)
    result['heldout_max_abs_error']=str(max_err)
    if max_err>tol:
        result['decision']='FALSIFIED_HELDOUT'
        return result
    attest=data.get('attestations')
    if not isinstance(attest,dict) or any(attest.get(k) is not True for k in REQUIRED_ATTESTATIONS):
        result['decision']='UNVERIFIED_PHYSICAL_INPUT'
    elif data['evidence_tier']=='synthetic_not_physical':
        result['decision']='SYNTHETIC_GRID_FIT_ONLY'
    else:
        result['decision']='GRID_FIT_ONLY_NOT_PHYSICAL_CERTIFICATE'
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,help='Private input JSON, never commit human or instrument data')
    parser.add_argument('--synthetic',action='store_true',help='Run frozen synthetic instrument falsifier')
    args=parser.parse_args()
    if bool(args.input)==bool(args.synthetic):
        parser.error('choose exactly one of --input or --synthetic')
    data=synthetic_input() if args.synthetic else json.loads(args.input.read_text(encoding='utf-8'))
    print(json.dumps(evaluate(data),indent=2,sort_keys=True))

if __name__=='__main__':
    main()
