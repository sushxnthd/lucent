#!/usr/bin/env python3
"""Fail-closed physical acquisition manifest gate; stdlib only. Numerical screening is NOT authentication."""
import json, math, sys
from pathlib import Path

def check(m):
    errors=[]
    def number(k,positive=False):
        v=m.get(k)
        if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or (positive and v<=0):
            errors.append(k+': missing/nonfinite/nonpositive'); return None
        return float(v)
    fps=number('reference_fps',True)
    dt=number('reference_max_interframe_s',True)
    exp=number('reference_exposure_s',True)
    clock=number('clock_uncertainty_s')
    drift=number('max_clock_drift_s')
    row=number('row_timing_uncertainty_s')
    gap=number('target_max_blind_gap_s',True)
    if fps and dt and dt<1/fps-1e-9: errors.append('max reference interframe gap contradicts nominal frame period')
    if fps and exp and exp>1/fps: errors.append('reference exposure exceeds nominal frame period')
    for k,v in [('clock_uncertainty_s',clock),('max_clock_drift_s',drift),('row_timing_uncertainty_s',row)]:
        if v is not None and v<0: errors.append(k+' negative')
    if all(v is not None for v in (dt,exp,clock,drift,row,gap)):
        if max(0,dt-exp)+2*(clock+drift+row)>=gap:
            errors.append('reference temporal uncertainty cannot resolve target blind gap')
    for k in ('reference_video_sha256','target_video_sha256','photodiode_trace_sha256','calibration_record_sha256'):
        v=m.get(k)
        if not isinstance(v,str) or len(v)!=64 or any(c not in '0123456789abcdef' for c in v):
            errors.append(k+' missing/invalid')
    for k in ('independent_calibrator_id','device_model','shutter_mode','clock_sync_method','rater_protocol_id'):
        if not isinstance(m.get(k),str) or not m[k].strip(): errors.append(k+' missing')
    if m.get('velocity_bound_source') in (None,'finite_difference_max','self_declared'):
        errors.append('independent velocity ceiling absent')
    return {'status':'BLOCKED' if errors else 'AWAIT_INDEPENDENT_AUTHENTICATION',
            'errors':errors,'meaning':'Numerical screening only; NEVER authorizes human closure exclusion.'}

def selftest():
    m=dict(reference_fps=240,reference_max_interframe_s=1/240,reference_exposure_s=.001,
        clock_uncertainty_s=.0001,max_clock_drift_s=.0001,row_timing_uncertainty_s=.0001,
        target_max_blind_gap_s=.04,independent_calibrator_id='lab',device_model='camera',
        shutter_mode='global',clock_sync_method='photodiode',rater_protocol_id='frozen',
        velocity_bound_source='independent_physical_bound')
    for k in ('reference_video_sha256','target_video_sha256','photodiode_trace_sha256','calibration_record_sha256'):m[k]='a'*64
    assert check(m)['status']=='AWAIT_INDEPENDENT_AUTHENTICATION'
    for k,v in [('reference_fps',0),('reference_max_interframe_s',.001),('clock_uncertainty_s',.1),
                ('velocity_bound_source','finite_difference_max'),('photodiode_trace_sha256','fake')]:
        n=dict(m);n[k]=v;assert check(n)['status']=='BLOCKED',(k,check(n))
    print('6 numerical gate selftests passed; authentication deliberately not implemented')

if __name__=='__main__':
    if len(sys.argv)==2 and sys.argv[1]=='--selftest':selftest()
    elif len(sys.argv)==2:print(json.dumps(check(json.loads(Path(sys.argv[1]).read_text())),indent=2))
    else:sys.exit('usage: script --selftest | manifest.json')
