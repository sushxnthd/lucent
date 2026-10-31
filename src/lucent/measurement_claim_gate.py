"""E002-569: fail-closed boundary between camera metadata and human physiology.

This module intentionally does not accept external attestations as authoritative.
No E002-371 human shutter, clock, anatomical, or velocity calibration has been
independently verified. A future implementation must add a separate, reviewed
trust root before it can produce physiological claims.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Mapping

PHYSIOLOGICAL_CLAIMS = frozenset({
    "NO_HIDDEN_CLOSURE", "BLINK_DURATION", "PERCLOS", "SLEEPINESS", "FATIGUE",
})
QUALITY_CLAIM = "ACQUISITION_QUALITY"
MAX_FRAME_COUNT = 10**12


@dataclass(frozen=True)
class GateResult:
    claim: str
    decision: str
    release: str
    evidence_tier: str
    reasons: tuple[str, ...]
    observed_frames: int | None = None
    expected_frames: int | None = None
    frame_completeness: float | None = None


def _invalid(claim: str, reason: str) -> GateResult:
    return GateResult(
        claim=claim, decision="INVALID_INPUT", release="BLOCKED",
        evidence_tier="UNVERIFIED", reasons=(reason,),
    )


def _frame_count(value: object) -> bool:
    return type(value) is int and 0 <= value <= MAX_FRAME_COUNT


def _finite_positive_fps(value: object) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float, str, Decimal)):
        return False
    if isinstance(value, str) and (not value.strip() or len(value) > 32):
        return False
    try:
        x = Decimal(str(value))
    except (InvalidOperation, ValueError):
        return False
    return x.is_finite() and 0 < x <= 1_000_000


def evaluate_claim(request: object) -> GateResult:
    """Evaluate *untrusted* request data without upgrading self-reported evidence.

    Inputs can describe image completeness but cannot certify physiological
    absence, blink duration, fatigue or sleepiness. The return value is a
    deliberately closed claim vocabulary, not a clinical or diagnostic score.
    """
    if not isinstance(request, Mapping):
        return _invalid("UNKNOWN", "REQUEST_NOT_MAPPING")
    claim = request.get("claim")
    if not isinstance(claim, str) or claim not in PHYSIOLOGICAL_CLAIMS | {QUALITY_CLAIM}:
        return _invalid("UNKNOWN", "UNKNOWN_CLAIM")
    observed = request.get("observed_frames")
    expected = request.get("expected_frames")
    if not _frame_count(observed) or not _frame_count(expected) or expected == 0:
        return _invalid(claim, "INVALID_FRAME_COUNTS")
    if observed > expected:
        return _invalid(claim, "OBSERVED_EXCEEDS_EXPECTED")
    if "nominal_fps" in request and not _finite_positive_fps(request["nominal_fps"]):
        return _invalid(claim, "INVALID_NOMINAL_FPS")
    if "evidence" in request and not isinstance(request["evidence"], Mapping):
        return _invalid(claim, "MALFORMED_UNTRUSTED_EVIDENCE")
    nuisances = request.get("nuisances", ())
    if not isinstance(nuisances, (list, tuple)) or any(
        not isinstance(n, str) or not n or len(n) > 128 for n in nuisances
    ):
        return _invalid(claim, "INVALID_NUISANCE_RECORD")
    if claim in PHYSIOLOGICAL_CLAIMS:
        return GateResult(
            claim=claim, decision="ABSTAIN_UNCALIBRATED", release="BLOCKED",
            evidence_tier="NOT_PHYSIOLOGICALLY_VALIDATED",
            reasons=("NO_INDEPENDENT_HUMAN_AND_PHYSICAL_CALIBRATION",),
            observed_frames=observed, expected_frames=expected,
        )
    return GateResult(
        claim=claim, decision="ACQUISITION_QUALITY_ONLY", release="BLOCKED",
        evidence_tier="NOT_PHYSIOLOGICALLY_VALIDATED",
        reasons=("FRAME_COUNTS_ARE_NOT_BLINK_EVIDENCE",),
        observed_frames=observed, expected_frames=expected,
        frame_completeness=observed / expected,
    )
