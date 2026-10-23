#!/usr/bin/env python3
"""Fail-closed prototype for E002-390; not approved for clinical/consumer deployment."""
from dataclasses import dataclass
from math import isfinite
from typing import Optional
import numpy as np

THRESHOLD = .2

@dataclass(frozen=True)
class Calibration:
    independent_speed_upper: Optional[float] = None
    aperture_mean_error_upper: Optional[float] = None
    frame_period: Optional[float] = None
    exposure_seconds: Optional[float] = None
    exposure_timing_verified: bool = False
    aperture_transfer_verified: bool = False
    human_holdout_verified: bool = False
    nuisance_envelope_verified: bool = False
    within_device_envelope: bool = False
    reference_labels_adequate: bool = False

def qualify(means, cal: Calibration):
    required = (cal.exposure_timing_verified, cal.aperture_transfer_verified,
                cal.human_holdout_verified, cal.nuisance_envelope_verified,
                cal.within_device_envelope, cal.reference_labels_adequate)
    if not all(required):
        return {'decision':'ABSTAIN','reason':'unverified physical/human calibration'}
    V, eps, F, w = (cal.independent_speed_upper, cal.aperture_mean_error_upper,
                    cal.frame_period, cal.exposure_seconds)
    if any(x is None or not isfinite(x) for x in (V,eps,F,w)):
        return {'decision':'ABSTAIN','reason':'missing quantitative envelope'}
    if not (V >= 0 and eps >= 0 and F > 0 and 0 < w <= F):
        return {'decision':'ABSTAIN','reason':'invalid calibration values'}
    try:
        y = np.asarray(means, dtype=float)
    except (TypeError,ValueError):
        return {'decision':'ABSTAIN','reason':'invalid observations'}
    if y.ndim != 1 or len(y) < 2 or not np.all(np.isfinite(y)):
        return {'decision':'ABSTAIN','reason':'missing observations'}
    if np.any(y < -eps) or np.any(y > 1+eps):
        return {'decision':'ABSTAIN','reason':'observations outside calibrated range'}
    # Independent V; never derive it from differences between y values.
    t = np.linspace(0, (len(y)-1)*F+w, 2001)
    low = np.full(t.shape, -np.inf)
    for i, mu in enumerate(y):
        a = i*F
        b = a+w
        d = ((b-t)*np.abs(b-t)-(a-t)*np.abs(a-t))/(2*w)
        low = np.maximum(low, mu-eps-V*d)
    # Grid-continuum allowance: distance to nearest sample <= h/2.
    bound = float(np.min(low)-V*(t[1]-t[0])/2)
    if bound > THRESHOLD:
        return {'decision':'CONDITIONAL_NO_CROSSING','bound':bound,
                'reason':'requires independently validated assumptions'}
    return {'decision':'ABSTAIN','bound':bound,'reason':'threshold crossing not excluded'}

def self_test():
    base=Calibration()
    assert qualify([1,1,1],base)['decision']=='ABSTAIN'
    flags=dict(independent_speed_upper=132,aperture_mean_error_upper=0,
               frame_period=1/30,exposure_seconds=.01,
               exposure_timing_verified=True,aperture_transfer_verified=True,
               human_holdout_verified=True,nuisance_envelope_verified=True,
               within_device_envelope=True,reference_labels_adequate=True)
    valid=Calibration(**flags)
    assert qualify([1]*7,valid)['decision']=='ABSTAIN'
    for flag in ('exposure_timing_verified','aperture_transfer_verified',
                 'human_holdout_verified','nuisance_envelope_verified',
                 'within_device_envelope','reference_labels_adequate'):
        bad=Calibration(**{**flags,flag:False})
        assert qualify([1]*7,bad)['decision']=='ABSTAIN'
    assert qualify([1,float('nan')],valid)['decision']=='ABSTAIN'
    print('PASS 9 fail-closed qualification checks')

if __name__=='__main__':
    self_test()
