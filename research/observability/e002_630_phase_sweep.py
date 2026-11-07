#!/usr/bin/env python3
"""E002-630: shutter-gap phase sweep, exact triangular occluder ground truth.
Synthetic instrument surrogate, NOT human validation. Standard library only.
"""
from fractions import Fraction as F
import json

def aperture(t, center, baseline=F(2), minimum=F(0), speed=F(200)):
    """Symmetric triangular dip, aperture units mm; time in seconds."""
    return baseline - max(F(0), (baseline-minimum)-speed*abs(t-center))

def hidden_closure(gap_start, gap_end, center, threshold=F(0)):
    """Analytical truth, not derived from camera frames."""
    return gap_start < center < gap_end and aperture(center, center) <= threshold

def exclude_constant_speed(left_lower, right_lower, duration, closing_speed, opening_speed, threshold=F(0)):
    """Strict exclusion: equality permits a triangular hidden closure."""
    if min(left_lower, right_lower) < threshold:
        return False
    if min(closing_speed, opening_speed) <= 0:
        return (left_lower > threshold if closing_speed == 0 else True) or (right_lower > threshold if opening_speed == 0 else True)
    required = (left_lower-threshold)/closing_speed + (right_lower-threshold)/opening_speed
    return duration < required

def exposure_mean(start, duration, center, steps=1000):
    # Midpoint quadrature is a synthetic sensor, not physical exposure calibration.
    return sum((aperture(start+(F(2*i+1,2*steps)*duration),center) for i in range(steps)), F(0))/steps

def run():
    speed=F(200); baseline=F(2); gap=F(1,50) # 20 ms
    # Gap at [0,20ms], symmetric closure reachable at 10ms exactly.
    assert hidden_closure(F(0),gap,F(1,100))
    assert not exclude_constant_speed(baseline,baseline,gap,speed,speed)
    assert exclude_constant_speed(baseline,baseline,F(19,1000),speed,speed)
    assert not exclude_constant_speed(baseline,baseline,F(1,50),speed,speed)
    # Across 101 phases, compare strict certificate to analytically known hidden closures.
    # Conservative endpoint aperture bounds are true instantaneous values here (oracle).
    trials=0; excluded=0; closures=0; false_exclusions=0
    for gap in (F(19,1000),F(20,1000),F(21,1000)):
        for k in range(101):
            center=F(k-25,2500)  # -10ms through +30ms
            left=aperture(F(0),center); right=aperture(gap,center)
            truth=hidden_closure(F(0),gap,center)
            verdict=exclude_constant_speed(left,right,gap,speed,speed)
            trials+=1; excluded+=int(verdict); closures+=int(truth)
            false_exclusions+=int(verdict and truth)
    assert false_exclusions==0
    # Synthetic integration is not instantaneous aperture. Expose that difference.
    center=F(0)
    mean=exposure_mean(F(-1,100),F(1,100),center)
    assert mean != aperture(F(0),center)
    return dict(id="E002-630",evidence="synthetic phase-sweep only",
                trials=trials,oracle_hidden_closures=closures,
                strict_exclusions=excluded,false_exclusions=false_exclusions,
                exposure_average_example=str(mean),
                product="ABSTAIN_UNCALIBRATED",release="BLOCKED")

if __name__=="__main__":
    print(json.dumps(run(),sort_keys=True))
