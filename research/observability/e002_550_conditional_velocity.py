#!/usr/bin/env python3
"""E002-550 conditional continuous-time speed envelope from sampled aperture.

NOT a human physiological measurement. A, e, u must be independent *hard*
bounds; supplied JSON cannot authenticate them. Always block product use.
"""
import argparse
import json
import math


def finite_number(x):
    return type(x) in (int, float) and math.isfinite(x)


REQUIRED_NUISANCES = (
    "geometry", "illumination", "blur", "gaze", "glasses",
    "missingness", "marker_identity", "anatomical_transfer",
)


def evaluate(obj):
    blocked = {"experiment": "E002-550", "product": "ABSTAIN_UNCALIBRATED",
               "release": "BLOCKED", "human_validation": False,
               "physical_certification": False}
    def abstain(reason):
        return {**blocked, "status": "ABSTAIN_NO_HARD_SPEED_CERTIFICATE",
                "reason": reason}

    if type(obj) is not dict:
        return abstain("INVALID_RECORD")
    assumptions = obj.get("assumptions")
    samples = obj.get("observations")
    if type(assumptions) is not dict or type(samples) is not list:
        return abstain("MISSING_ASSUMPTIONS_OR_OBSERVATIONS")
    nuisance = assumptions.get("nuisance_pass")
    if type(nuisance) is not dict or any(nuisance.get(k) is not True for k in REQUIRED_NUISANCES):
        return abstain("UNRESOLVED_NUISANCE")
    if assumptions.get("complete_coverage") is not True:
        return abstain("MISSING_SAMPLING_COVERAGE")
    keys = ("acceleration_upper", "aperture_error_upper", "clock_error_upper")
    if any(not finite_number(assumptions.get(k)) or assumptions[k] < 0 for k in keys):
        return abstain("INDEPENDENT_HARD_BOUNDS_UNAVAILABLE")
    A, e, u = (float(assumptions[k]) for k in keys)
    if len(samples) < 2:
        return abstain("INSUFFICIENT_SAMPLES")
    times, values = [], []
    for s in samples:
        if type(s) is not dict or s.get("quality") != "OK":
            return abstain("UNRESOLVED_SAMPLE_QUALITY")
        t, a = s.get("t"), s.get("a")
        if not finite_number(t) or not finite_number(a) or not 0 <= a <= 1:
            return abstain("INVALID_APERTURE_OR_TIME")
        times.append(float(t))
        values.append(float(a))
    upper = 0.0
    max_nominal_secant = 0.0
    for i in range(len(times) - 1):
        dt = times[i+1] - times[i]
        if dt <= 2*u or dt <= 0:
            return abstain("UNRESOLVED_CLOCK_OR_NONMONOTONE_TIME")
        # The actual interval is in [dt-2u, dt+2u].
        secant = abs(values[i+1] - values[i]) / dt
        interval_upper = (abs(values[i+1]-values[i]) + 2*e)/(dt-2*u) + A*(dt+2*u)/2
        if not math.isfinite(interval_upper):
            return abstain("NUMERIC_OVERFLOW")
        max_nominal_secant = max(max_nominal_secant, secant)
        upper = max(upper, interval_upper)
    return {**blocked, "status": "CONDITIONAL_BOUND_ONLY_NOT_AUTHENTICATED",
            "velocity_upper_per_s": upper,
            "observed_max_secant_per_s": max_nominal_secant,
            "covered_intervals": len(times)-1,
            "assumptions_are_external_not_verified": True,
            "claim": "Not a certified human velocity bound"}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input_json")
    args = p.parse_args()
    with open(args.input_json, encoding="utf-8") as f:
        obj = json.load(f)
    print(json.dumps(evaluate(obj), sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
