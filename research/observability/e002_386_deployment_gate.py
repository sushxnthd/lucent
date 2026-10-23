"""Fail-closed E002-386 research policy. No actual human calibration is shipped."""
from dataclasses import dataclass,replace
from typing import Optional
import math
@dataclass(frozen=True)
class Evidence:
    paired_human_validation: bool=False
    participant_holdout_passed: bool=False
    device_holdout_passed: bool=False
    optical_transfer_calibrated: bool=False
    independent_speed_bound: bool=False
    exposure_timing_calibrated: bool=False
    rolling_row_timing_calibrated: bool=False
    frame_complete: bool=False
    geometry_in_domain: bool=False
    brightness_in_domain: bool=False
    blur_in_domain: bool=False
    gaze_in_domain: bool=False
    glasses_in_domain: bool=False
    sampling_and_clock_verified: bool=False
    matched_device_identity: bool=False
@dataclass(frozen=True)
class Decision:
    status:str
    reason:str
    guarantee:bool=False
FIELDS=tuple(Evidence.__dataclass_fields__)
def qualify(*,evidence:Evidence,margin:Optional[float],quality:Optional[float],
            selected_margin:Optional[float],selected_quality:Optional[float],
            rolling_shutter:bool=False)->Decision:
    for field in FIELDS:
        if field=='rolling_row_timing_calibrated' and not rolling_shutter:continue
        if not getattr(evidence,field):
            return Decision('ABSTAIN','unverified:'+field)
    if any(x is None or not math.isfinite(x)
           for x in (margin,quality,selected_margin,selected_quality)):
        return Decision('ABSTAIN','invalid_measurement_or_calibration')
    if not (0<=quality<=1 and 0<=selected_quality<=1):
        return Decision('ABSTAIN','quality_out_of_range')
    if margin<selected_margin or quality>selected_quality:
        return Decision('ABSTAIN','outside_calibrated_selection')
    return Decision('STATISTICAL_RISK_QUALIFIED',
                    'conditional population risk only; not a hard closure guarantee',
                    guarantee=False)
def self_test():
    args=dict(margin=.5,quality=.1,selected_margin=.22,selected_quality=1)
    assert qualify(evidence=Evidence(),**args).status=='ABSTAIN'
    fully=Evidence(**{k:True for k in FIELDS})
    assert qualify(evidence=fully,**args).status=='STATISTICAL_RISK_QUALIFIED'
    assert qualify(evidence=fully,**args).guarantee is False
    for field in FIELDS:
        degraded=replace(fully,**{field:False})
        rolling=(field=='rolling_row_timing_calibrated')
        assert qualify(evidence=degraded,rolling_shutter=rolling,**args).status=='ABSTAIN',field
    for changes in [dict(margin=float('nan')),dict(quality=float('inf')),
                    dict(quality=-.1),dict(selected_margin=None),dict(margin=.1)]:
        assert qualify(evidence=fully,**{**args,**changes}).status=='ABSTAIN',changes
    print('E002-386 deployment-gate tests PASS:',len(FIELDS)+8)
if __name__=='__main__':self_test()
