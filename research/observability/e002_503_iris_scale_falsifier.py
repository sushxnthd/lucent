#!/usr/bin/env python3
"""E002-503: synthetic common-mode iris-scale falsification of E002-492 review.

This script uses the ACTUAL frozen E002-492 adjudicator, not a mock.
All geometry is authored synthetic; no human images, annotations or times.
"""
import json
import math

from e002_492_anatomical_review import adjudicate, build_manifest, template

THRESHOLD = 0.10
CASES = (
    ("false_closed_by_shared_scale", 40.0, 44.0, 4.2, 0.05),
    ("false_open_by_shared_scale", 40.0, 36.0, 3.8, 0.05),
)


def aperture_interval(gap, landmark_error, diameter, diameter_error=0.0):
    """Sharp positive ratio interval for independent bounded numerator/scale."""
    vals = (gap, landmark_error, diameter, diameter_error)
    if any(isinstance(x, bool) or not isinstance(x, (float, int)) or
           not math.isfinite(x) for x in vals):
        raise ValueError("NONFINITE_OR_NONNUMERIC")
    if gap < 0 or landmark_error < 0 or diameter <= 0 or not 0 <= diameter_error < diameter:
        raise ValueError("INVALID_APERTURE_BOUNDS")
    return (max(0.0, gap - 2.0 * landmark_error) / (diameter + diameter_error),
            (gap + 2.0 * landmark_error) / (diameter - diameter_error))


def threshold_decision(interval, threshold=THRESHOLD):
    lo, hi = interval
    if hi < threshold:
        return "BELOW_THRESHOLD"
    if lo > threshold:
        return "ABOVE_THRESHOLD"
    return "THRESHOLD_UNRESOLVED"


def fill_synthetic(manifest, rater, gap, diameter, landmark_error):
    ratings = template(manifest, rater)
    for frames in ratings["clips"].values():
        for f in frames:
            f.update(upper_y=100.0, lower_y=100.0 + gap,
                     iris_diameter=diameter, uncertainty_px=landmark_error,
                     flags=[])
    return ratings


def run():
    manifest = build_manifest()
    cases = []
    for name, true_diameter, observed_diameter, gap, landmark_error in CASES:
        a = fill_synthetic(manifest, "A", gap, observed_diameter, landmark_error)
        b = fill_synthetic(manifest, "B", gap, observed_diameter, landmark_error)
        aggregate = adjudicate(manifest, a, b)
        nominal = aperture_interval(gap, landmark_error, observed_diameter)
        expanded = aperture_interval(gap, landmark_error, observed_diameter, 4.0)
        truth = gap / true_diameter
        nominal_decision = threshold_decision(nominal)
        true_decision = "BELOW_THRESHOLD" if truth < THRESHOLD else "ABOVE_THRESHOLD"
        assert aggregate["agreement_intervals"] == 260
        assert aggregate["dual_measurable"] == 260
        assert aggregate["interval_disagreement"] == 0
        assert aggregate["unreviewed"] == 0
        assert aggregate["nuisance_abstention"] == 0
        assert aggregate["geometry_abstention"] == 0
        assert nominal_decision != true_decision
        assert expanded[0] <= truth <= expanded[1]
        assert threshold_decision(expanded) == "THRESHOLD_UNRESOLVED"
        cases.append({
            "synthetic_case": name,
            "synthetic_true_aperture": round(truth, 9),
            "nominal_aperture_interval": [round(v, 9) for v in nominal],
            "scale_uncertainty_aware_interval": [round(v, 9) for v in expanded],
            "nominal_threshold_decision_not_from_adjudicator": nominal_decision,
            "stipulated_truth_threshold_decision": true_decision,
            "scale_aware_threshold_decision": threshold_decision(expanded),
            "actual_adjudicator_agreement_intervals": aggregate["agreement_intervals"],
            "actual_adjudicator_disagreements": aggregate["interval_disagreement"],
            "actual_adjudicator_abstentions": 260 - aggregate["dual_measurable"],
        })
    return {
        "experiment": "E002-503",
        "evidence_tier": "SYNTHETIC_MEASUREMENT_SYSTEM_FALSIFICATION_ONLY",
        "cases": cases,
        "real_human_anatomical_ratings": 0,
        "authenticated_camera_clock": False,
        "physical_hidden_closure_certified": False,
        "product": "ABSTAIN_UNCALIBRATED",
        "release": "BLOCKED",
        "interpretation": "Two agreeing synthetic raters can share iris-scale bias; "
                          "agreement does not certify a threshold label. "
                          "No human error magnitude is estimated."
    }


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True, indent=2))
