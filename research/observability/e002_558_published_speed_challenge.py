#!/usr/bin/env python3
"""E002-558: literature-derived lower constraint on any proposed hard blink-speed cap.

This is an independent published-human aggregate *challenge*, not a human-data
reanalysis, instrument calibration, or proof of a continuous-time upper bound.
"""
import json
from fractions import Fraction

DOI = "10.1098/rsif.2013.0227"
PEOPLE = 25
CAMERA_FPS = 600
ANALYSIS_STEP_MS = 5
MEAN_REPORTED_PEAK_MM_S = Fraction(243)
MAX_REPORTED_INITIAL_APERTURE_MM = Fraction(128, 10)


def lower_constraint(peak_downward_bias=Fraction(0), aperture_upward_bias=Fraction(0)):
    """Necessary nominal cap, conditional on bounded systematic errors.

    Since at least one person's peak >= mean peak, and all initial apertures
    <= maximum, max normalized measured speed >= (mean-bias)/(max+bias).
    Both biases are *assumed sensitivity inputs*, not paper-certified errors.
    """
    peak = MEAN_REPORTED_PEAK_MM_S - peak_downward_bias
    aperture = MAX_REPORTED_INITIAL_APERTURE_MM + aperture_upward_bias
    if peak_downward_bias < 0 or aperture_upward_bias < 0 or aperture <= 0:
        raise ValueError("bias assumptions must be nonnegative with positive aperture")
    return max(Fraction(0), peak) / aperture


def decision(cap, bound):
    """A cap below a necessary observed lower constraint is contradicted."""
    return "INCOMPATIBLE_WITH_REPORTED_POINT_ESTIMATES" if cap < bound else "NOT_FALSIFIED_NOT_CERTIFIED"


def main():
    # No error budget is published. These are predeclared sensitivity scenarios,
    # not confidence intervals and not physiological population bounds.
    cases = {
        "nominal_reported": (Fraction(0), Fraction(0)),
        "rounding_only_assumption": (Fraction(1, 2), Fraction(5, 100)),
        "illustrative_10mm_s_0p5mm": (Fraction(10), Fraction(1, 2)),
        "illustrative_50mm_s_1mm": (Fraction(50), Fraction(1)),
    }
    out = {}
    for name, (speed_bias, aperture_bias) in cases.items():
        bound = lower_constraint(speed_bias, aperture_bias)
        out[name] = {
            "necessary_cap_s_inverse": float(bound),
            "exact_fraction": str(bound),
            "assumed_peak_downward_bias_mm_s": float(speed_bias),
            "assumed_aperture_upward_bias_mm": float(aperture_bias),
            "caps_s_inverse": {str(cap): decision(Fraction(cap), bound) for cap in (10, 15, 19, 20, 40)},
        }
    # A 30 Hz, 10 ms exposure gives a 23.333 ms nominal unexposed gap;
    # the next illustration is instantaneous-endpoint ONLY and is not a
    # shutter-averaged Lucent product certificate.
    gap = Fraction(1, 30) - Fraction(10, 1000)
    a, threshold = Fraction(2, 5), Fraction(1, 5)
    cap_needed_for_exclusion = 2 * (a - threshold) / gap
    assert lower_constraint() == Fraction(1215, 64)
    assert decision(Fraction(15), lower_constraint()) == "INCOMPATIBLE_WITH_REPORTED_POINT_ESTIMATES"
    assert decision(Fraction(20), lower_constraint()) == "NOT_FALSIFIED_NOT_CERTIFIED"
    assert cap_needed_for_exclusion == Fraction(120, 7)
    print(json.dumps({
        "experiment": "E002-558",
        "source_doi": DOI,
        "human_participants_in_published_study": PEOPLE,
        "camera_fps_reported": CAMERA_FPS,
        "aperture_sampling_ms_reported": ANALYSIS_STEP_MS,
        "evidence": "PUBLISHED_AGGREGATE_POINT_ESTIMATE_ONLY",
        "scenarios": out,
        "instantaneous_endpoints_only_illustration": {
            "camera_fps": 30,
            "exposure_ms": 10,
            "nominal_unexposed_gap_ms": float(gap * 1000),
            "endpoint_normalized_aperture": float(a),
            "closure_threshold": float(threshold),
            "maximum_cap_permitting_exclusion_s_inverse": float(cap_needed_for_exclusion),
            "warning": "NOT APPLICABLE TO EXPOSURE AVERAGES OR REAL CAMERA WITHOUT CALIBRATION",
        },
        "continuous_time_upper_speed_certified": False,
        "independent_human_rater_pairs": 0,
        "authenticated_physical_shutter_captures": 0,
        "heldout_human_predictions": 0,
        "product": "ABSTAIN_UNCALIBRATED",
        "release": "BLOCKED",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
