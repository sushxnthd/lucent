"""E002-623: conditional velocity bridge under independently certified acceleration.
Run: python research/observability/e002_623_acceleration_bridge.py
No human physiology is certified by this script.
"""
from fractions import Fraction as F

def velocity_ceiling(samples, dt, acceleration_ceiling, position_error=0):
    """Upper bound on |x'| across each interval if |x''|<=A everywhere.
    Samples are measured apertures, error <= position_error per sample.
    Triangle integration gives |x'(t)-secant| <= A*dt/2, sharp at endpoints.
    """
    if len(samples)<2 or dt<=0 or acceleration_ceiling<0 or position_error<0:
        raise ValueError("invalid calibration")
    return max((abs(samples[i+1]-samples[i])+2*position_error)/dt
               + acceleration_ceiling*dt/2 for i in range(len(samples)-1))

def certificate(left_lower, right_lower, closure_threshold, gap_upper, v_upper):
    """Strict exclusion; equality must abstain."""
    if min(left_lower,right_lower)<0 or gap_upper<0 or v_upper<0:
        raise ValueError("invalid bounds")
    return "EXCLUDE_CONDITIONAL" if left_lower+right_lower-2*closure_threshold > v_upper*gap_upper else "ABSTAIN"

def self_test():
    h=F(1,240)
    # E002-622's triangular subframe event violates any low A assumption:
    # endpoints 3 mm, midpoint 1 mm -> |x''| is unbounded at the cusp.
    assert velocity_ceiling([F(3),F(3)],h,F(0))==0
    assert velocity_ceiling([F(3),F(3)],h,F(1000))==F(25,12)
    assert velocity_ceiling([F(3),F(3)],h,F(1000),F(1,10))==F(601,12)
    assert certificate(F(3),F(3),F(1),F(1,100),F(100))=="EXCLUDE_CONDITIONAL"
    assert certificate(F(3),F(3),F(1),F(1,100),F(400))=="ABSTAIN"
    # Sharp endpoint extremizer: x(t)=s*t + (A/2)*t*(t-h).
    # Secant slope s; endpoint derivative differs by A*h/2.
    A=F(1000); s=F(2); derivative=s+A*h/2
    assert derivative==F(49,12)
    assert velocity_ceiling([F(0),s*h],h,A)==derivative
    try:
        velocity_ceiling([1],h,0)
        raise AssertionError("invalid input accepted")
    except ValueError:
        pass
    print("E002-623: six conditional arithmetic assertions passed; no empirical validation")

if __name__=="__main__":
    self_test()
