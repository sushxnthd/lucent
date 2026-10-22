"""Camera qualification, not a live blink detector. Independent reference duration required."""
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Certificate:
    decision: str
    coverage_lower: Optional[float]
    coverage_upper: Optional[float]
    guaranteed: bool
    reason: str

def phase_fraction(D:float,F:float,w:float,m:float)->float:
    if not(F>0 and 0<w<=F and m>0):raise ValueError('invalid shutter')
    if D<0:raise ValueError('negative duration')
    if m>w or D<m:return 0.0
    return min(1.0,max(0.0,(D+w-2*m)/F))

def qualify_camera(*,F:float,w:float,m:float,D_lower:Optional[float],
                   D_upper:Optional[float],phase_uniform:bool,
                   timing_calibrated:bool)->Certificate:
    if not timing_calibrated:
        return Certificate('ABSTAIN',None,None,False,'timestamps uncalibrated')
    if D_lower is None or D_upper is None:
        return Certificate('ABSTAIN',None,None,False,'no independent reference duration')
    if not(0<=D_lower<=D_upper):raise ValueError('invalid duration bounds')
    lo=phase_fraction(D_lower,F,w,m);hi=phase_fraction(D_upper,F,w,m)
    guarantee=(D_lower>=m and m<=w and D_lower+w-2*m>=F)
    if guarantee:
        return Certificate('GEOMETRICALLY_GUARANTEED',1.0,1.0,True,
                           'overlap only, not optical visibility')
    if not phase_uniform:
        return Certificate('ABSTAIN',None,None,False,
                           'phase locking can hide every event')
    return Certificate('PHASE_COVERAGE_ONLY',lo,hi,False,
                       'uniform phase assumed; not RGB sensitivity')
