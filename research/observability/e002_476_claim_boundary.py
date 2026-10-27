#!/usr/bin/env python3
"""E002-476: prevent research-conditional outputs from becoming physical claims.

The underlying evaluator accepts *declared* assumptions; neither this renderer
nor a caller can authenticate a camera shutter, anatomical truth, or a hard
physiological velocity bound. A valid conditional exclusion is NOT a product
statement that no eyelid closure occurred.
"""
from __future__ import annotations

import argparse
import copy
import json
import math
from pathlib import Path

from e002_456_prospective_gate import NUISANCES, evaluate_interval

ABSTAIN = "ABSTAIN_UNCALIBRATED"
VALID_REFERENCES = {
    "WITNESSED_CROSSING", "REFERENCE_INCOMPLETE",
    "REFERENCE_INDETERMINATE", "NO_WITNESSED_CROSSING",
}
VALID_CAPS = {"ILLUSTRATIVE", "EXTERNAL_HARD_BOUND_DECLARED"}


def render_public(result):
    """Untrusted interval result -> research label and a non-releasable claim.

    This intentionally has NO caller-provided flag capable of authorizing a
    physical claim. Even a forged physical_release_authorized=True is rejected.
    """
    output = {
        "physical_claim": ABSTAIN,
        "physical_release_authorized": False,
        "research_label": "NOT_DISPLAYED",
        "reason": "INVALID_OR_UNTRUSTED_RESEARCH_RESULT",
    }
    if not isinstance(result, dict):
        return output
    if (result.get("physical_release_authorized") is not False or
            result.get("external_hard_bound_verified_by_this_program") is not False or
            result.get("product_claim") != ABSTAIN):
        return output

    decision = result.get("decision")
    ref = result.get("reference")
    falsified = result.get("joint_falsification")
    if type(falsified) is not bool:
        return output
    if decision == "ABSTAIN":
        if ref != "NOT_EVALUATED" or falsified or not isinstance(result.get("reason"), str):
            return output
        return {**output, "research_label": "RESEARCH_ABSTAIN",
                "reason": "INPUT_OR_CALIBRATION_NOT_ACCEPTED"}
    if decision not in {"EXCLUDED_CONDITIONALLY", "NOT_EXCLUDED"}:
        return output
    if result.get("reason") != "NONE" or ref not in VALID_REFERENCES:
        return output
    if result.get("velocity_cap_tier") not in VALID_CAPS:
        return output
    bound = result.get("lower_envelope_mm")
    if type(bound) not in (int, float) or not math.isfinite(bound) or bound < 0:
        return output
    if falsified != (decision == "EXCLUDED_CONDITIONALLY" and ref == "WITNESSED_CROSSING"):
        return output

    if falsified:
        label = "JOINT_MODEL_ASSUMPTIONS_FALSIFIED"
    elif decision == "EXCLUDED_CONDITIONALLY":
        label = "CONDITIONAL_MODEL_EXCLUSION_ONLY"
    elif ref == "WITNESSED_CROSSING":
        label = "REFERENCE_WITNESS_RESEARCH_ONLY"
    else:
        label = "CLOSURE_NOT_EXCLUDED"
    return {**output, "research_label": label,
            "reason": "PHYSICAL_METROLOGY_AND_HARD_SPEED_CAP_NOT_VERIFIED"}


def _synthetic_case():
    return {
        "closure_threshold_mm": 2.0,
        "endpoint_aperture_mm": [3.0, 3.0],
        "endpoint_uncertainty_mm": [0.0, 0.0],
        "endpoint_time_ms": [0.0, 10.0],
        "shutter": {"kernel": "uniform_symmetric", "exposure_ms": 0.0,
                    "clock_error_ms": 0.0, "reference_exposure_ms": 0.2,
                    "reference_clock_error_ms": 0.1},
        "velocity": {"limit_mm_s": 100.0, "provenance": "ILLUSTRATIVE"},
        "instrument": {"geometry_calibration_id": "synthetic",
                       "clock_calibration_id": "synthetic",
                       "exposure_calibration_id": "synthetic",
                       "reference_annotation_id": "synthetic",
                       "independent_reference": True},
        "nuisance": {name: "PASS" for name in NUISANCES},
        "reference": [{"time_ms": 5.0, "aperture_mm": 2.8,
                       "uncertainty_mm": 0.0, "quality": "PASS"}],
    }


def run_frozen():
    base = _synthetic_case()
    cases = {"illustrative": base}
    declared = copy.deepcopy(base)
    declared["velocity"]["provenance"] = "EXTERNAL_HARD_BOUND_DECLARED"
    cases["declared_external"] = declared
    missing = copy.deepcopy(base)
    missing["reference"] = []
    cases["no_reference"] = missing
    witnessed = copy.deepcopy(base)
    witnessed["reference"][0]["aperture_mm"] = 1.8
    cases["witnessed_counterexample"] = witnessed
    empirical = copy.deepcopy(base)
    empirical["velocity"]["provenance"] = "EMPIRICAL_SAMPLE_MAX"
    cases["empirical_sample_max"] = empirical
    nuisance = copy.deepcopy(base)
    nuisance["nuisance"]["clock"] = "UNKNOWN"
    cases["uncalibrated_clock"] = nuisance

    observed = {}
    for name, case in cases.items():
        research = evaluate_interval(case)
        public = render_public(research)
        observed[name] = {
            "research_decision": research["decision"],
            "reference": research["reference"],
            "joint_falsification": research["joint_falsification"],
            **public,
        }
        assert public["physical_claim"] == ABSTAIN
        assert public["physical_release_authorized"] is False
    assert observed["illustrative"]["research_decision"] == "EXCLUDED_CONDITIONALLY"
    assert observed["declared_external"]["research_decision"] == "EXCLUDED_CONDITIONALLY"
    assert observed["no_reference"]["research_decision"] == "EXCLUDED_CONDITIONALLY"
    assert observed["no_reference"]["reference"] == "REFERENCE_INCOMPLETE"
    assert observed["witnessed_counterexample"]["research_label"] == "JOINT_MODEL_ASSUMPTIONS_FALSIFIED"
    assert observed["empirical_sample_max"]["research_decision"] == "ABSTAIN"
    assert observed["uncalibrated_clock"]["research_decision"] == "ABSTAIN"
    return {
        "experiment": "E002-476",
        "evidence_tier": "SYNTHETIC_SOFTWARE_INTERFACE_FALSIFICATION_ONLY",
        "cases": observed,
        "physical_acquisitions": 0,
        "new_human_anatomical_measurements": 0,
        "physical_release_authorized": False,
        "product_claim": ABSTAIN,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    args.output.write_text(
        json.dumps(run_frozen(), sort_keys=True, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
