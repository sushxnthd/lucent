#!/usr/bin/env python3
"""E002-627 physical acquisition manifest eligibility gate. Never authorizes release."""
import json,sys,math
FLAGS=('reference_exposure_verified','ordinary_exposure_verified','aperture_calibration_verified','velocity_envelope_independent','velocity_envelope_continuous_time','boundary_aperture_intervals_verified','two_blinded_raters','closure_threshold_preregistered','gaze_recorded','illumination_recorded','glasses_recorded','blur_recorded','missingness_recorded')
NUMERIC=('reference_frame_rate_hz','sync_uncertainty_ms','row_timing_uncertainty_ms')
IDENTITY=('participant_id','camera_reference','camera_ordinary','split')
def evaluate(t):
    reasons=[]
    for k in FLAGS:
        if t.get(k) is not True: reasons.append('uncertified:'+k)
    for k in NUMERIC:
        v=t.get(k)
        if type(v) not in (int,float) or not math.isfinite(v) or v<0 or (k=='reference_frame_rate_hz' and v==0):
            reasons.append('invalid:'+k)
    for k in IDENTITY:
        if not isinstance(t.get(k),str) or not t[k].strip(): reasons.append('missing:'+k)
    if t.get('split') not in ('calibration','heldout'): reasons.append('invalid_split')
    return {'decision':'ABSTAIN_UNCALIBRATED' if reasons else 'ELIGIBLE_FOR_BLINDED_ANALYSIS','reasons':reasons}
def audit(data):
    trials=data['trials']
    results=[evaluate(t) for t in trials]
    cal={t.get('participant_id') for t in trials if t.get('split')=='calibration'}
    held={t.get('participant_id') for t in trials if t.get('split')=='heldout'}
    overlap=cal & held
    for t,r in zip(trials,results):
        if t.get('participant_id') in overlap:
            r['decision']='ABSTAIN_UNCALIBRATED'
            r['reasons'].append('participant_leakage')
    return {'results':results,'all_eligible':bool(results) and all(r['decision']=='ELIGIBLE_FOR_BLINDED_ANALYSIS' for r in results),'release':'BLOCKED'}
def self_test():
    t=dict(participant_id='p1',camera_reference='R',camera_ordinary='O',split='calibration',reference_frame_rate_hz=240,sync_uncertainty_ms=.5,row_timing_uncertainty_ms=.2)
    t.update({k:True for k in FLAGS})
    assert evaluate(t)['decision']=='ELIGIBLE_FOR_BLINDED_ANALYSIS'
    for k in ('velocity_envelope_independent','velocity_envelope_continuous_time','ordinary_exposure_verified','two_blinded_raters','aperture_calibration_verified'):
        bad=dict(t);bad[k]=False;assert evaluate(bad)['decision']=='ABSTAIN_UNCALIBRATED'
    bad=dict(t);bad['sync_uncertainty_ms']=float('nan');assert evaluate(bad)['decision']=='ABSTAIN_UNCALIBRATED'
    bad=dict(t);bad['split']='heldout';assert not audit({'trials':[t,bad]})['all_eligible']
    assert audit({'trials':[t]})['release']=='BLOCKED'
    print('PASS: 9 assertions; no physical evidence generated')
if __name__=='__main__':
    if len(sys.argv)==2 and sys.argv[1]=='--self-test': self_test()
    else: print(json.dumps(audit(json.load(sys.stdin)),indent=2))
