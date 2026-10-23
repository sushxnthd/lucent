"""E002-383 conditional camera qualification; NOT a blink or fatigue detector."""
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Calibration:
    speed_bound: float | None
    aperture_error: float | None
    gap_upper_s: float | None
    exposure_s: float | None
    intermediate_transfer_valid: bool
    geometry_valid: bool
    photometry_valid: bool
    missingness_valid: bool
    blur_valid: bool
    gaze_valid: bool
    glasses_valid: bool
    clock_valid: bool

def qualify_gap(left, right, threshold, cal):
    flags=(cal.intermediate_transfer_valid,cal.geometry_valid,
           cal.photometry_valid,cal.missingness_valid,cal.blur_valid,
           cal.gaze_valid,cal.glasses_valid,cal.clock_valid)
    if not all(flags): return 'ABSTAIN'
    vals=(left,right,threshold,cal.speed_bound,cal.aperture_error,
          cal.gap_upper_s,cal.exposure_s)
    if any(x is None or not math.isfinite(x) for x in vals):return 'ABSTAIN'
    l,r,t,v,e,h,w=vals
    if not(0<=l<=1 and 0<=r<=1 and 0<=t<=1 and v>0 and
           0<=e<=1 and h>=0 and w>0):return 'ABSTAIN'
    def endpoint(b):
        b=max(0,b-e);q=v*w
        return max(0,1-math.sqrt(max(0,2*q*(1-b)))) if b>=1-q/2 else max(0,b-q/2)
    L=endpoint(l);R=endpoint(r)
    lower=max(0,L-v*h,R-v*h,(L+R-v*h)/2)
    return 'CERTIFIED_NO_HIDDEN_CLOSURE_IN_GAP' if lower>t else 'ABSTAIN'
