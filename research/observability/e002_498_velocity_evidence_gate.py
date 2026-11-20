#!/usr/bin/env python3
"""E002-498: conservative research-only population speed-envelope evidence gate.

This is not a velocity estimator, human annotation, or physical certificate.
Only aggregate provenance-attested evidence is accepted; release is always blocked.
"""
import argparse
import json
import math
from pathlib import Path

NUISANCES = ("geometry", "brightness", "missingness", "blur", "gaze",
             "glasses", "sampling", "clock_error", "shutter")
ATTESTATIONS = ("camera_clock_authenticated", "shutter_calibrated",
                "geometry_calibrated", "independent_anatomical_review",
                "continuous_upper_bound_certified",
                "independent_participant_sampling",
                "participant_disjoint_holdout",
                "independent_replay")
PROHIBITED = ("frames", "blinks", "subject_ids", "individual_velocities",
              "rater_sheets", "raw_images", "participant_records")


def valid_probability(x):
    return (type(x) in (int, float) and math.isfinite(x)
            and 0 < x < 1)


def minimum_participants(coverage, confidence):
    if not valid_probability(coverage) or not valid_probability(confidence):
        raise ValueError("INVALID_PROBABILITY")
    # Stable near one, with a final exact-boundary correction.
    n = max(1, math.ceil(math.log1p(-confidence) / math.log(coverage)))
    while 1 - coverage ** n < confidence - 1e-14:
        n += 1
    while n > 1 and 1 - coverage ** (n - 1) >= confidence + 1e-14:
        n -= 1
    return n


def assess(evidence):
    result = {
        "experiment": "E002-498",
        "evidence_tier": "AGGREGATE_ATTESTATION_ONLY",
        "decision": "ABSTAIN_UNCALIBRATED",
        "physical_hidden_closure_certified": False,
        "universal_human_velocity_bound": False,
        "blink_duration_certified": False,
        "perclos_certified": False,
        "fatigue_or_medical_claims": False,
        "release": "BLOCKED",
        "reasons": [],
    }
    if not isinstance(evidence, dict):
        result["reasons"] = ["INVALID_INPUT"]
        return result
    if any(k in evidence for k in PROHIBITED):
        result["reasons"] = ["INDIVIDUAL_DATA_OR_WRONG_SAMPLE_UNIT"]
        return result

    p = evidence.get("target_population_coverage")
    confidence = evidence.get("target_confidence")
    if not valid_probability(p) or not valid_probability(confidence):
        result["reasons"] = ["INVALID_TARGET"]
        return result
    needed = minimum_participants(p, confidence)
    result["minimum_independent_participants"] = needed
    result["target_population_coverage"] = p
    result["target_confidence"] = confidence

    n = evidence.get("distinct_participants")
    if type(n) is not int or n < 0 or n > 10000000:
        result["reasons"].append("INVALID_PARTICIPANT_COUNT")
    elif n < needed:
        result["reasons"].append("INSUFFICIENT_INDEPENDENT_PARTICIPANTS")
    if evidence.get("sampling_unit") != "independent_participants":
        result["reasons"].append("WRONG_SAMPLING_UNIT")

    population = evidence.get("target_population")
    if (not isinstance(population, str) or not population.strip()
            or evidence.get("calibration_population") != population
            or evidence.get("holdout_population") != population):
        result["reasons"].append("POPULATION_MISMATCH")

    for name in ATTESTATIONS:
        if evidence.get(name) is not True:
            result["reasons"].append("MISSING_" + name.upper())

    nuisance = evidence.get("nuisance_controls")
    if not isinstance(nuisance, dict) or set(nuisance) != set(NUISANCES):
        result["reasons"].append("INCOMPLETE_NUISANCE_INVENTORY")
    elif any(nuisance[k] is not True for k in NUISANCES):
        result["reasons"].append("UNVERIFIED_NUISANCE_CONTROL")

    vmax = evidence.get("certified_max_normalized_speed_per_second")
    if (type(vmax) not in (float, int) or not math.isfinite(vmax)
            or vmax <= 0):
        result["reasons"].append("NO_CERTIFIED_CONTINUOUS_SPEED_UPPER_BOUND")

    if not result["reasons"]:
        result["decision"] = "STATISTICAL_ENVELOPE_RESEARCH_ONLY"
        result["evidence_tier"] = "SELF_ATTESTED_AGGREGATE_REQUIRES_EXTERNAL_AUDIT"
        result["max_certified_normalized_speed_per_second"] = vmax
        result["distribution_free_confidence_lower_bound"] = round(
            -math.expm1(n * math.log(p)), 12)
        result["scope"] = "target population under stated calibration and nuisance conditions"
        result["reasons"] = ["NOT_A_DETERMINISTIC_BOUND_OR_PRODUCT_CERTIFICATE"]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True,
                        help="Private or synthetic aggregate-only evidence JSON")
    parser.add_argument("--output", type=Path,
                        help="Optional aggregate-only result JSON")
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        outcome = assess(data)
    except (OSError, ValueError, UnicodeError, json.JSONDecodeError):
        outcome = assess(None)
    output = json.dumps(outcome, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()
