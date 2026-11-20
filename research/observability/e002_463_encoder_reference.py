#!/usr/bin/env python3
"""E002-463: independent encoder-positive witness adapter for E002-456.

Research-only. Input provenance is DECLARED, not authenticated. The adapter
never infers OPEN from sampled encoder negatives and never releases a product.
No raw traces or identifiers are emitted.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import re

from e002_456_prospective_gate import evaluate_interval
from e002_462_finite_dwell import witness as finite_witness

REQUIRED_PROVENANCE = (
    "timebase_calibration_id", "position_calibration_id",
    "bandwidth_calibration_id",
)


def _num(value, *, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("numeric value required")
    v = float(value)
    if not math.isfinite(v) or v < 0 or (positive and v == 0):
        raise ValueError("nonnegative finite numeric value required")
    return v


def _blocked(reason, prediction="ABSTAIN"):
    return {
        "experiment": "E002-463",
        "evidence_tier": "UNVERIFIED_REFERENCE_INPUT",
        "prediction": prediction,
        "reference": "REFERENCE_UNRESOLVED",
        "decision": "ABSTAIN",
        "reason": reason,
        "joint_falsification": False,
        "witness_count": 0,
        "physical_release_authorized": False,
        "product_claim": "ABSTAIN_UNCALIBRATED",
        "encoder_attestations_independently_verified": False,
    }


def evaluate_encoder(case, encoder):
    """Return only a deidentified positive-witness result; no OPEN truth label.

    A 'PASS' self-attestation is not independently verified. A physical study
    must escrow the source trace hash and calibration evidence externally.
    """
    if not isinstance(case, dict) or not isinstance(encoder, dict):
        return _blocked("INVALID_SCHEMA")
    if case.get("reference") != []:
        return _blocked("PREEXISTING_REFERENCE_FORBIDDEN")
    baseline = evaluate_interval(case)
    if baseline["decision"] == "ABSTAIN":
        return _blocked("ORDINARY_PREDICTION_UNCALIBRATED")
    try:
        provenance = encoder["provenance"]
        if not isinstance(provenance, dict):
            raise ValueError("invalid provenance")
        if provenance.get("independent_position_instrument") is not True:
            raise ValueError("non-independent reference")
        if any(not isinstance(provenance.get(k), str) or
               not provenance[k].strip() for k in REQUIRED_PROVENANCE):
            raise ValueError("missing calibration evidence identifiers")
        raw_hash = provenance.get("raw_trace_sha256")
        if not isinstance(raw_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", raw_hash):
            raise ValueError("missing source hash")
        delta = _num(provenance["max_time_error_ms"])
        position_error = _num(provenance["max_position_error_mm"])
        support = _num(provenance["sample_support_ms"])
        if provenance.get("scale_units") != "mm" or provenance.get("time_units") != "ms":
            raise ValueError("invalid physical units")
        shutter = case["shutter"]
        t0, t1 = map(_num, case["endpoint_time_ms"])
        ordinary_width = _num(shutter["exposure_ms"])
        ordinary_delta = _num(shutter["clock_error_ms"])
        c = _num(case["closure_threshold_mm"])
        if not t0 < t1 or ordinary_width >= t1 - t0:
            raise ValueError("no nominal dark gap")
        samples = encoder["samples"]
        if not isinstance(samples, list) or not samples:
            return _blocked("NO_ENCODER_SAMPLES", baseline["decision"])
        prior = -math.inf
        witnessed = []
        for s in samples:
            if not isinstance(s, dict) or s.get("quality") != "PASS":
                raise ValueError("invalid sample or quality")
            t = _num(s["time_ms"])
            a = _num(s["aperture_mm"])
            if t <= prior:
                raise ValueError("nonmonotone or repeated encoder time")
            prior = t
            # Both uncertain support edges must lie strictly within the
            # *ordinary camera's unexposed dark interval*.
            left = t - delta - support / 2
            right = t + delta + support / 2
            dark_left = t0 + ordinary_width / 2 + ordinary_delta
            dark_right = t1 - ordinary_width / 2 - ordinary_delta
            # Never promote floating-point equality at an exposure boundary.
            time_tol_ms = 1e-12
            if (left > dark_left + time_tol_ms and
                    right < dark_right - time_tol_ms and
                    a + position_error <= c):
                witnessed.append((t, a))
        if not witnessed:
            return {
                **_blocked("NO_ROBUST_INTERIOR_CROSSING", baseline["decision"]),
                "decision": baseline["decision"],
            }
        adjudication = copy.deepcopy(case)
        adjudication["shutter"]["reference_exposure_ms"] = support
        adjudication["shutter"]["reference_clock_error_ms"] = delta
        adjudication["reference"] = [
            {"time_ms": t, "aperture_mm": a,
             "uncertainty_mm": position_error, "quality": "PASS"}
            for t, a in witnessed
        ]
        result = evaluate_interval(adjudication)
        if result["decision"] == "ABSTAIN" or result["reference"] != "WITNESSED_CROSSING":
            return _blocked("PROSPECTIVE_GATE_REJECTED_REFERENCE", baseline["decision"])
        return {
            "experiment": "E002-463",
            "evidence_tier": "DECLARED_ENCODER_REFERENCE_NOT_INDEPENDENTLY_AUTHENTICATED",
            "prediction": baseline["decision"],
            "reference": "WITNESSED_CROSSING",
            "decision": baseline["decision"],
            "reason": "NONE",
            "joint_falsification": result["joint_falsification"],
            "witness_count": len(witnessed),
            "physical_release_authorized": False,
            "product_claim": "ABSTAIN_UNCALIBRATED",
            "encoder_attestations_independently_verified": False,
        }
    except (KeyError, ValueError, TypeError, OverflowError):
        return _blocked("ENCODER_PROVENANCE_OR_TRACE_INVALID", baseline["decision"])


def synthetic_fixture(closure=True):
    """Fixed *synthetic* E002-462 shutter-invisible world, never human data."""
    nuisance = {k: "PASS" for k in (
        "geometry", "brightness", "missingness", "blur", "gaze",
        "glasses", "sampling", "clock", "rolling_shutter")}
    case = {
        "interval_id": "private-synthetic-only", "participant_id": "synthetic",
        "split": "development", "closure_threshold_mm": 2.0,
        "endpoint_aperture_mm": [2.3, 2.3],
        "endpoint_uncertainty_mm": [0.0, 0.0],
        "endpoint_time_ms": [0.0, 2.5],
        "shutter": {"kernel": "uniform_symmetric", "exposure_ms": 0.3,
                    "clock_error_ms": 0.0, "reference_exposure_ms": 0.0,
                    "reference_clock_error_ms": 0.02},
        "velocity": {"limit_mm_s": 100.0, "provenance": "ILLUSTRATIVE"},
        "instrument": {
            "geometry_calibration_id": "synthetic-only",
            "clock_calibration_id": "synthetic-only",
            "exposure_calibration_id": "synthetic-only",
            "reference_annotation_id": "synthetic-only",
            "independent_reference": True,
        },
        "nuisance": nuisance, "reference": [],
    }
    encoder = {
        "provenance": {
            "independent_position_instrument": True,
            "timebase_calibration_id": "synthetic-only",
            "position_calibration_id": "synthetic-only",
            "bandwidth_calibration_id": "synthetic-only",
            "raw_trace_sha256": hashlib.sha256(b"E002-463 synthetic only").hexdigest(),
            "max_time_error_ms": 0.02,
            "max_position_error_mm": 0.01,
            "sample_support_ms": 0.0,
            "scale_units": "mm", "time_units": "ms",
        },
        "samples": [
            {"time_ms": 1.0, "aperture_mm": 1.95 if closure else 2.3,
             "quality": "PASS"},
        ],
    }
    return case, encoder


def synthetic_run():
    positive = finite_witness(400, 2.3, 1.95, 0.1, 0.9)
    case, encoder = synthetic_fixture(True)
    closed = evaluate_encoder(case, encoder)
    case, encoder = synthetic_fixture(False)
    open_world = evaluate_encoder(case, encoder)
    if not positive["identical_to_constant_open"]:
        raise AssertionError("E002-462 witness changed")
    if not closed["joint_falsification"] or open_world["joint_falsification"]:
        raise AssertionError("frozen encoder challenge failed")
    return {
        "experiment": "E002-463",
        "tier": "SYNTHETIC_INSTRUMENT_ONLY",
        "shutter_camera_positive_negative_identical": True,
        "positive_subthreshold_duration_ms": positive["subthreshold_duration_ms"],
        "closed_world": closed,
        "open_world": open_world,
        "hard_bound_assumption_intentionally_false": True,
        "real_human_measurements": 0,
        "real_physical_encoder_measurements": 0,
        "physical_release_authorized": False,
    }


if __name__ == "__main__":
    print(json.dumps(synthetic_run(), indent=2, sort_keys=True, allow_nan=False))
