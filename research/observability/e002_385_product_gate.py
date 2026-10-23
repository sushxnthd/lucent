"""Fail-closed prototype policy, NOT validated ocular sensing."""
REQUIRED=('exposure_timestamps','sensor_exposure','clock_uncertainty',
'speed_bound','aperture_transfer','optical_error_bound','geometry',
'brightness','missingness','blur','gaze','glasses','sampling')
def qualify(calibration,lower_gap_bound,threshold=.2):
    missing=[k for k in REQUIRED if not calibration.get(k,False)]
    if missing:return ('ABSTAIN','missing:'+','.join(missing))
    if not calibration.get('device_in_domain',False):return ('ABSTAIN','device-unknown')
    if not calibration.get('hard_error_bound_proven',False):return ('ABSTAIN','statistical-not-deterministic')
    if lower_gap_bound<=threshold:return ('ABSTAIN','observability-failed')
    return ('CERTIFIED_NO_HIDDEN_THRESHOLD_CROSSING','conditional-guarantee')
if __name__=='__main__':
    c={k:True for k in REQUIRED};c.update(device_in_domain=True,hard_error_bound_proven=True)
    assert qualify(c,.3)[0].startswith('CERTIFIED')
    assert qualify(c,.2)[0]=='ABSTAIN'
    for k in REQUIRED+('device_in_domain','hard_error_bound_proven'):
        assert qualify({**c,k:False},.3)[0]=='ABSTAIN'
    print('PASS: 17 fail-closed prototype tests')
