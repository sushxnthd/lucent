#!/usr/bin/env python3
"""E002-464: dynamic-transfer-aware positive reference gate (research only).

A delayed or signed encoder response is not an anatomical point sample.
This wrapper enforces a DECLARED finite influence interval and a DECLARED
nonnegative unit-mass response before using the E002-463 positive-only gate.
It never authenticates physical calibration or releases product claims.
"""
from __future__ import annotations

import copy
import json

from e002_463_encoder_reference import evaluate_encoder, synthetic_fixture, _blocked, _num


def _reject(reason):
    result = _blocked(reason)
    result["experiment"] = "E002-464"
    result["dynamic_response_independently_verified"] = False
    return result


def evaluate_dynamic_encoder(case, encoder):
    if not isinstance(case, dict) or not isinstance(encoder, dict):
        return _reject("INVALID_SCHEMA")
    try:
        provenance = encoder["provenance"]
        if not isinstance(provenance, dict):
            return _reject("DYNAMIC_PROVENANCE_INVALID")
        if provenance.get("response_nonnegative_unit_mass_declared") is not True:
            return _reject("RESPONSE_KERNEL_NOT_POSITIVE_NORMALIZED")
        for key in ("dynamic_support_calibration_id", "response_kernel_calibration_id"):
            if not isinstance(provenance.get(key), str) or not provenance[key].strip():
                return _reject("DYNAMIC_CALIBRATION_MISSING")
        # These are upper bounds on physical input influence relative to the
        # timestamped, centered acquisition support, NOT estimated mean lags.
        past = _num(provenance["max_past_memory_ms"])
        future = _num(provenance["max_future_lead_ms"])
        width = _num(provenance["sample_support_ms"])
        _num(provenance["max_time_error_ms"])
        _num(provenance["max_position_error_mm"])
        effective_width = width + past + future
        if not (effective_width < float("inf")):
            return _reject("UNBOUNDED_DYNAMIC_SUPPORT")
        samples = encoder["samples"]
        if not isinstance(samples, list):
            return _reject("INVALID_ENCODER_SAMPLES")
        shifted = copy.deepcopy(encoder)
        shifted["provenance"]["sample_support_ms"] = effective_width
        shift = (future - past) / 2.0
        for sample in shifted["samples"]:
            if not isinstance(sample, dict):
                return _reject("INVALID_ENCODER_SAMPLES")
            t = _num(sample["time_ms"])
            shifted_t = t + shift
            if not (0 <= shifted_t < float("inf")):
                return _reject("DYNAMIC_SUPPORT_TIME_INVALID")
            sample["time_ms"] = shifted_t
        # The legacy gate's sample is interpreted only as a positive
        # *existence* witness somewhere in the expanded support, not as a
        # measured anatomical aperture at the shifted center.
        result = evaluate_encoder(case, shifted)
        result["experiment"] = "E002-464"
        result["dynamic_response_independently_verified"] = False
        result["positive_witness_semantics"] = "EXISTENTIAL_IN_INFLUENCE_SUPPORT"
        result["physical_release_authorized"] = False
        result["product_claim"] = "ABSTAIN_UNCALIBRATED"
        return result
    except (KeyError, TypeError, ValueError, OverflowError):
        return _reject("DYNAMIC_PROVENANCE_OR_TRACE_INVALID")


def dynamic_fixture(*, closed=True, past=0.1, future=0.0, signed=False):
    case, encoder = synthetic_fixture(closed)
    encoder["provenance"].update({
        "response_nonnegative_unit_mass_declared": not signed,
        "dynamic_support_calibration_id": "synthetic-transfer-only",
        "response_kernel_calibration_id": "synthetic-kernel-only",
        "max_past_memory_ms": past,
        "max_future_lead_ms": future,
    })
    return case, encoder


def synthetic_run():
    case, encoder = dynamic_fixture(past=1.4)
    # The legacy adapter falsely treats a 1.4-ms delayed report as a
    # timestamped aperture crossing in the dark gap.
    legacy = evaluate_encoder(case, encoder)
    corrected = evaluate_dynamic_encoder(case, encoder)
    case, encoder = dynamic_fixture(past=0.1)
    calibrated = evaluate_dynamic_encoder(case, encoder)
    case, encoder = dynamic_fixture(signed=True)
    signed = evaluate_dynamic_encoder(case, encoder)
    if not legacy["joint_falsification"] or corrected["joint_falsification"]:
        raise AssertionError("delayed-reference counterexample not reproduced")
    if not calibrated["joint_falsification"] or signed["joint_falsification"]:
        raise AssertionError("positive control or signed-kernel guard failed")
    return {
        "experiment": "E002-464",
        "tier": "SYNTHETIC_DYNAMIC_INSTRUMENT_ONLY",
        "legacy_delayed_false_dark_gap_witness": legacy["reference"],
        "corrected_delayed_reference": corrected["reference"],
        "calibrated_positive_reference": calibrated["reference"],
        "signed_kernel_reference": signed["reference"],
        "true_dark_gap_open_in_delayed_world": True,
        "real_human_measurements": 0,
        "real_physical_encoder_measurements": 0,
        "physical_release_authorized": False,
        "product_claim": "ABSTAIN_UNCALIBRATED",
    }


if __name__ == "__main__":
    print(json.dumps(synthetic_run(), indent=2, sort_keys=True, allow_nan=False))
