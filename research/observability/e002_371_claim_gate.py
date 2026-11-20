"""Fail-closed conditional shutter-gap diagnostic. Synthetic-only self-tests."""
from decimal import Decimal, InvalidOperation
import json, sys

def number(x):
    if isinstance(x, bool):
        raise ValueError("bool")
    try:
        d = Decimal(str(x))
    except (InvalidOperation, TypeError):
        raise ValueError("invalid")
    if not d.is_finite() or d < 0:
        raise ValueError("invalid")
    return d

def evaluate(r):
    if not isinstance(r, dict):
        return {"verdict":"ABSTAIN","reason":"INVALID_RECORD_TYPE"}
    for field, expected, reason in (
        ("aperture_observation","instantaneous","EXPOSURE_OR_OBSERVATION_UNVERIFIED"),
        ("velocity_bound_provenance","independent_certified_upper","VELOCITY_UNCERTIFIED"),
        ("timing_provenance","hardware_bounded","TIMING_UNVERIFIED"),
        ("geometry_provenance","independently_calibrated","GEOMETRY_UNVERIFIED"),
        ("nuisance_clear",True,"NUISANCE_UNRESOLVED")):
        if r.get(field) != expected:
            return {"verdict":"ABSTAIN","reason":reason}
    try:
        a=number(r["endpoint0_lower_mm"])
        b=number(r["endpoint1_lower_mm"])
        c=number(r["closure_threshold_mm"])
        v=number(r["velocity_upper_mm_s"])
        t=number(r["gap_upper_s"])
    except (KeyError, ValueError, TypeError, OverflowError):
        return {"verdict":"ABSTAIN","reason":"INVALID_OR_MISSING_INTERVAL"}
    if a <= c or b <= c:
        return {"verdict":"NOT_EXCLUDED","reason":"ENDPOINT_CAN_BE_CLOSED"}
    try:
        q=v*t/(a+b-2*c)
    except (ArithmeticError, OverflowError):
        return {"verdict":"ABSTAIN","reason":"ARITHMETIC_UNRESOLVED"}
    # Provenance strings are caller-controlled. No authenticated certificate verifier exists.
    # A mathematical exclusion is NOT an authorized product exclusion.
    if q < 1:
        return {"verdict":"ABSTAIN","reason":"CERTIFICATE_NOT_AUTHENTICATED",
                "q_upper":str(q),"mathematical_condition":"q_upper_lt_1"}
    return {"verdict":"NOT_EXCLUDED","reason":"HIDDEN_CLOSURE_FEASIBLE",
            "q_upper":str(q)}

def self_test():
    r=dict(aperture_observation="instantaneous",
        velocity_bound_provenance="independent_certified_upper",
        timing_provenance="hardware_bounded",
        geometry_provenance="independently_calibrated",nuisance_clear=True,
        endpoint0_lower_mm="2",endpoint1_lower_mm="2",
        closure_threshold_mm="0",velocity_upper_mm_s="100",gap_upper_s="0.039")
    cases=[
        ({}, "ABSTAIN"),
        ({"gap_upper_s":"0.040"}, "NOT_EXCLUDED"),
        ({"gap_upper_s":"0.041"}, "NOT_EXCLUDED"),
        ({"aperture_observation":"exposure_integrated"}, "ABSTAIN"),
        ({"velocity_bound_provenance":"empirical_percentile"}, "ABSTAIN"),
        ({"timing_provenance":"nominal_fps"}, "ABSTAIN"),
        ({"geometry_provenance":"uncalibrated"}, "ABSTAIN"),
        ({"nuisance_clear":False}, "ABSTAIN"),
        ({"gap_upper_s":"NaN"}, "ABSTAIN"),
        ({"gap_upper_s":"Infinity"}, "ABSTAIN"),
        ({"endpoint0_lower_mm":"0"}, "NOT_EXCLUDED"),
        ({"velocity_upper_mm_s":True}, "ABSTAIN")]
    for changes, verdict in cases:
        assert evaluate({**r,**changes})["verdict"] == verdict
    assert evaluate(r)["reason"] == "CERTIFICATE_NOT_AUTHENTICATED"
    for payload in (None, [], [r], "bad", 1, True):
        assert evaluate(payload) == {"verdict":"ABSTAIN","reason":"INVALID_RECORD_TYPE"}
    print("PASS: 12 claim-gate scenarios and 6 hostile top-level payloads")

if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        self_test()
    else:
        try:
            print(json.dumps(evaluate(json.load(sys.stdin)),sort_keys=True))
        except (ValueError, TypeError):
            print(json.dumps({"verdict":"ABSTAIN","reason":"INVALID_JSON"}))
