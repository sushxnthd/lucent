#!/usr/bin/env python3
"""E002-568: exact cohort-constrained structural no-go; NOT a human velocity ceiling.

Published group means only imply a necessary speed floor for a universal cohort
ceiling. The output never certifies absence of a human blink.
"""
from __future__ import annotations

from fractions import Fraction
import json

KWON_COHORT_NECESSARY_SPEED_FLOOR = Fraction(24300, 983)  # per second
DEFAULT_THETA = Fraction(1, 5)


def q(value):
    if isinstance(value, bool):
        raise ValueError("booleans are not physical quantities")
    try:
        result = Fraction(str(value)) if not isinstance(value, Fraction) else value
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("invalid rational physical quantity") from exc
    return result


def critical_gap(theta=DEFAULT_THETA, necessary_speed_floor=KWON_COHORT_NECESSARY_SPEED_FLOOR):
    theta, v = q(theta), q(necessary_speed_floor)
    if not (0 < theta < 1 and v > 0):
        raise ValueError("theta must be in (0,1), necessary speed floor positive")
    return 2 * (1 - theta) / v


def gap_interval(*, period_min, period_max, exposure_min, exposure_max, missed, clock_error=0):
    f0, f1 = q(period_min), q(period_max)
    w0, w1 = q(exposure_min), q(exposure_max)
    e = q(clock_error)
    if isinstance(missed, bool) or not isinstance(missed, int) or missed < 0:
        raise ValueError("missed exposure count must be a nonnegative integer")
    if not (0 < f0 <= f1 and 0 < w0 <= w1 <= f0 and e >= 0):
        raise ValueError("invalid global-shutter period, exposure, or clock bounds")
    lower = max(Fraction(0), (missed + 1) * f0 - w1 - 2 * e)
    upper = (missed + 1) * f1 - w0 + 2 * e
    if upper < 0 or lower > upper:
        raise ValueError("inconsistent blind gap bounds")
    return lower, upper


def evaluate(*, period_min, period_max, exposure_min, exposure_max, missed,
             clock_error=0, theta=DEFAULT_THETA):
    h0, h1 = gap_interval(period_min=period_min, period_max=period_max,
                          exposure_min=exposure_min, exposure_max=exposure_max,
                          missed=missed, clock_error=clock_error)
    hc = critical_gap(theta)
    if h0 > hc:
        structural = "POSITIVE_DURATION_FEASIBLE_FOR_ALL_ADMISSIBLE_GAPS"
    elif h0 == hc:
        structural = "THRESHOLD_TOUCH_FEASIBLE_FOR_ALL_ADMISSIBLE_GAPS"
    elif h1 < hc:
        structural = "NO_STRUCTURAL_NOGO_FROM_THIS_COHORT_WITNESS"
    else:
        structural = "TIMING_INTERVAL_OVERLAPS_CRITICAL_GAP"
    return {
        "missed_exposure_opportunities": missed,
        "blind_gap_min_s": rational(h0),
        "blind_gap_max_s": rational(h1),
        "critical_gap_s": rational(hc),
        "structural_result": structural,
        "speed_floor_is_safe_upper_bound": False,
        "human_closure_observed": False,
        "product_decision": "ABSTAIN_UNCALIBRATED",
        "release": "BLOCKED",
    }


def rational(value):
    value = q(value)
    return {"numerator": value.numerator, "denominator": value.denominator}


def report():
    f = Fraction(1, 30)
    w = Fraction(1, 100)
    cases = [evaluate(period_min=f, period_max=f, exposure_min=w,
                      exposure_max=w, missed=k) for k in range(4)]
    return {
        "experiment": "E002-568",
        "evidence_tier": "published_2013_cohort_means_plus_exact_model_only",
        "source_doi": "10.1098/rsif.2013.0227",
        "scope": "universal_normalized_speed_ceiling_applicable_to_all_25_Kwon_participants",
        "necessary_speed_floor_per_second": rational(KWON_COHORT_NECESSARY_SPEED_FLOOR),
        "theta": rational(DEFAULT_THETA),
        "camera_model": "ideal_exact_gap_endpoints_global_shutter_30Hz_10ms",
        "cases": cases,
        "independent_human_anatomical_rater_pairs": 0,
        "physical_shutter_captures": 0,
        "certified_continuous_time_human_speed_upper_bounds": 0,
        "heldout_physical_closure_predictions": 0,
        "product": "ABSTAIN_UNCALIBRATED",
        "release": "BLOCKED",
    }


if __name__ == "__main__":
    print(json.dumps(report(), indent=2, sort_keys=True))
