"""Conservative exposure-aware shutter gap diagnostic; synthetic mathematical checks only.

Assumes linear exposure averages of a physically calibrated scalar aperture,
a global Lipschitz velocity ceiling V, disjoint known exposure windows, and
a bounded dark interval G measured edge-to-edge. This is NOT a certified
physiological bound or a deployable closure detector.
"""
from decimal import Decimal, InvalidOperation

def d(x):
    if isinstance(x, bool):
        raise ValueError("boolean is not a measurement")
    try:
        v = Decimal(str(x))
    except (InvalidOperation, TypeError):
        raise ValueError("invalid decimal")
    if not v.is_finite() or v < 0:
        raise ValueError("nonfinite or negative")
    return v

def exposure_boundary(mean0_lower_mm, mean1_lower_mm, exposure0_upper_s,
                      exposure1_upper_s, dark_gap_upper_s,
                      velocity_upper_mm_s, closure_threshold_mm):
    """Return a mathematical diagnostic only; never an authorized product claim."""
    try:
        m0,m1,e0,e1,g,v,c = map(d, (mean0_lower_mm,mean1_lower_mm,
                                      exposure0_upper_s,exposure1_upper_s,
                                      dark_gap_upper_s,velocity_upper_mm_s,
                                      closure_threshold_mm))
        a0 = m0-v*e0/2
        a1 = m1-v*e1/2
        margin = (a0-c)+(a1-c)-v*g
    except (ValueError, ArithmeticError, OverflowError):
        return {"verdict":"ABSTAIN","reason":"INVALID_INTERVAL"}
    if a0 <= c or a1 <= c:
        return {"verdict":"NOT_EXCLUDED","reason":"EDGE_NOT_CERTIFIED_OPEN"}
    if margin > 0:
        return {"verdict":"MATHEMATICALLY_EXCLUDED_ONLY",
                "reason":"REQUIRES_INDEPENDENT_PHYSICAL_CERTIFICATION",
                "margin_mm":str(margin)}
    return {"verdict":"NOT_EXCLUDED","reason":"HIDDEN_CLOSURE_FEASIBLE",
            "margin_mm":str(margin)}

def test():
    f=lambda gap: exposure_boundary("2","2",".01",".01",gap,"100","0")
    assert f(".029")["verdict"] == "MATHEMATICALLY_EXCLUDED_ONLY"
    assert f(".030")["verdict"] == "NOT_EXCLUDED"
    assert f(".031")["verdict"] == "NOT_EXCLUDED"
    assert exposure_boundary("2","2",".04",".04",".001","100","0")["verdict"] == "NOT_EXCLUDED"
    assert exposure_boundary("2","2",".01",".01","NaN","100","0")["verdict"] == "ABSTAIN"
    assert exposure_boundary("2","2",".01",".01",True,"100","0")["verdict"] == "ABSTAIN"
    # If the aperture is constant during each exposure, the mean is exact;
    # the edge correction is conservative, not an equality assumption.
    print("PASS: 6 exposure-boundary synthetic assertions")

if __name__ == "__main__":
    test()
