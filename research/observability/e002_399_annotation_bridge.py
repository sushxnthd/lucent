#!/usr/bin/env python3
"""Fail-closed bridge from E002-398 blinded two-rater CSVs to E002-399 reference labels.

This tool NEVER infers event/control linkage, and requires independently calibrated
exposure, timebase, velocity, optical mapping and geometry. Its output is label-free.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
from pathlib import Path

from e002_399_reference_adequacy import Calibration, Frame, certify

FLAGS=('occlusion','glare','glasses','blur','gaze_issue','unresolved')
TRUTHY={'1','true','yes','y'}


def read_index(path):
    with open(path,newline='') as f:
        rows=list(csv.DictReader(f))
    out={}
    for row in rows:
        key=(row['clip_id'],str(int(row['frame_in_clip'])))
        if key in out:
            raise ValueError(f'Duplicate clip/frame in {path}')
        out[key]=row
    return out


def measurement_interval(a,b,scale_lo,scale_hi,error):
    if not (math.isfinite(scale_lo) and math.isfinite(scale_hi) and 0<scale_lo<=scale_hi
            and math.isfinite(error) and error>=0):
        raise ValueError('Invalid independently calibrated scale/error')
    def central_distance(row):
        x1=float(row['center_upper_x']);y1=float(row['center_upper_y'])
        x2=float(row['center_lower_x']);y2=float(row['center_lower_y'])
        if not all(math.isfinite(v) for v in (x1,y1,x2,y2)):
            raise ValueError('Nonfinite landmark')
        if not all(0<=x<190 for x in (x1,x2)) or not all(0<=y<130 for y in (y1,y2)):
            raise ValueError('Landmark outside crop')
        return math.hypot(x1-x2,y1-y2)
    d1,d2=central_distance(a),central_distance(b)
    return max(0.,(min(d1,d2)-2*error)/scale_hi),(max(d1,d2)+2*error)/scale_lo


def analyze(manifest, sheet1, sheet2, timing, cfg):
    if manifest.get('experiment')!='E002-398':
        raise ValueError('Requires E002-398 blinded manifest')
    ids={(clip['clip_id'],str(f['frame_in_clip'])) for clip in manifest['clips'] for f in clip['frames']}
    if not (set(sheet1)==set(sheet2)==set(timing)==ids):
        raise ValueError('Rater/time keys do not match blinded manifest exactly')
    gates=cfg.get('gates',{})
    # E002-400: static landmark/optical calibration is NOT exposure-mean calibration.
    # This quantitative bound is in normalized physical-aperture units and must
    # include shutter/optical inversion and landmark-extraction bias. Its source
    # remains externally auditable, not cryptographically verified by this script.
    raw_optical_error=cfg.get('optical_mean_error_bound')
    optical_error=None if raw_optical_error is None else float(raw_optical_error)
    provenance=cfg.get('optical_mean_error_provenance','')
    if optical_error is not None:
        if not math.isfinite(optical_error) or optical_error<0:
            raise ValueError('Invalid optical exposure-mean error bound')
        if not isinstance(provenance,str) or len(provenance.strip())<8:
            raise ValueError('Quantitative optical error needs an auditable provenance label')
    # E002-401: two landmarks on different rolling-shutter rows are not
    # simultaneous. A bound on aperture velocity alone cannot control their
    # common-mode motion. Require independent row offsets and per-landmark
    # normalized position-speed envelopes even for asserted global shutter.
    row_cfg=cfg.get('row_timing_calibration')
    row_error=None
    if row_cfg is not None:
        fields=('upper_offset_abs_s_upper','lower_offset_abs_s_upper',
                'upper_landmark_speed_upper_per_s','lower_landmark_speed_upper_per_s')
        vals=[float(row_cfg[key]) for key in fields]
        if not all(math.isfinite(v) and v>=0 for v in vals):
            raise ValueError('Invalid rolling-shutter temporal geometry/speed bounds')
        row_provenance=row_cfg.get('provenance','')
        if not isinstance(row_provenance,str) or len(row_provenance.strip())<8:
            raise ValueError('Row timing/speed calibration needs auditable provenance')
        if row_cfg.get('equal_row_exposure_verified') is not True:
            raise ValueError('Equal row exposure profile not verified')
        row_error=vals[0]*vals[2]+vals[1]*vals[3]
    shutter_gate=(bool(gates.get('uniform_shutter_verified',False)) or
                  bool(gates.get('calibrated_row_shutter',False)))
    # The Calibration field retains its historical name, but its meaning here
    # is qualified shutter timing: either true global shutter or calibrated
    # rolling shutter with equal exposure profiles.
    shutter_gate=shutter_gate and row_error is not None
    cal=Calibration(speed_upper=float(cfg['speed_upper']),threshold=float(cfg['threshold']),
                    independent_velocity=bool(gates.get('independent_velocity',False)),
                    aperture_geometry=bool(gates.get('aperture_geometry',False)),
                    optical_response=(bool(gates.get('optical_response',False)) and
                                      optical_error is not None),
                    exposure_timing=bool(gates.get('exposure_timing',False)),
                    clock_synchronization=bool(gates.get('clock_synchronization',False)),
                    nuisance_resolved=bool(gates.get('nuisance_resolved',False)),
                    uniform_shutter_verified=shutter_gate)
    names=[]
    for sheet in (sheet1,sheet2):
        who={v.get('rater_id','').strip() for v in sheet.values()}
        if len(who)!=1 or not next(iter(who)):
            raise ValueError('Each sheet needs a single nonempty rater_id')
        names.append(next(iter(who)))
    if names[0]==names[1]:
        raise ValueError('Two independent rater IDs required')
    totals={'CONFIRMED_CROSSING':0,'CONFIRMED_NO_CROSSING':0,
            'UNRESOLVED':0,'ABSTAIN_UNCALIBRATED':0}
    excluded_frames=0
    for clip in manifest['clips']:
        frames=[]
        for item in clip['frames']:
            key=(clip['clip_id'],str(item['frame_in_clip']))
            a,b=sheet1[key],sheet2[key]
            if any(a.get(flag,'').strip().lower() in TRUTHY or
                   b.get(flag,'').strip().lower() in TRUTHY for flag in FLAGS):
                excluded_frames+=1
                continue
            try:
                lo,hi=measurement_interval(a,b,float(cfg['iris_scale_lower_px']),
                                           float(cfg['iris_scale_upper_px']),
                                           float(cfg['landmark_error_px']))
            except (ValueError,KeyError):
                excluded_frames+=1
                continue
            # A static landmark measurement is not automatically the physical
            # exposure mean. Missing quantitative calibration forces abstention.
            if optical_error is not None and row_error is not None:
                lo-=optical_error+row_error
                hi+=optical_error+row_error
            t=timing[key]
            frames.append(Frame(float(t['nominal_time_s']),lo,hi,
                                float(t['exposure_s']),float(t['clock_error_s'])))
        frames.sort(key=lambda x:x.t)
        result=certify(frames,cal)
        totals[result.decision]+=1
    return {'experiment':'E002-399','evidence_tier':'requires independently calibrated rater sheets',
            'total_clips':len(manifest['clips']),'excluded_frames':excluded_frames,
            'decisions':totals,'calibration_gates_passed':cal.qualified(),
            'optical_mean_error_bound_applied':optical_error,
            'row_skew_error_bound_applied':row_error,
            'warning':'No physical-aperture claim unless the quantitative optical mean-error '
                      'bound and all calibration gates are independently verified. '
                      'A provenance string is NOT external verification. '
                      'Rolling shutter needs independent per-landmark row timing and speed bounds. '
                      'No event/control linkage or EEG labels used.'}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--rater-a',type=Path,required=True)
    p.add_argument('--rater-b',type=Path,required=True)
    p.add_argument('--private-timing',type=Path,required=True)
    p.add_argument('--calibration',type=Path,required=True)
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    report=analyze(json.loads(args.manifest.read_text()),read_index(args.rater_a),
                   read_index(args.rater_b),read_index(args.private_timing),
                   json.loads(args.calibration.read_text()))
    out=json.dumps(report,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(out)
    print(out)

if __name__=='__main__':main()
