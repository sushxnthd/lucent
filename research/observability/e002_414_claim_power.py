#!/usr/bin/env python3
"""E002-414: exact participant-clustered claim-power research gate.

Established binomial/rank statistics applied to Lucent's prospective validation.
This tool does NOT authenticate physical calibration or authorize a product claim.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def _probability(x, name, *, inclusive=False):
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise ValueError(f"{name}: expected numeric probability")
    x = float(x)
    if not math.isfinite(x) or not (0 < x <= 1 if inclusive else 0 < x < 1):
        raise ValueError(f"{name}: probability outside allowed range")
    return x


def _count(x, name):
    if isinstance(x, bool) or not isinstance(x, int) or x < 0:
        raise ValueError(f"{name}: expected nonnegative integer")
    return x


def binomial_cdf(k: int, n: int, p: float) -> float:
    """Numerically stable P(Bin(n,p) <= k); log-sum-exp, no SciPy dependency."""
    _count(n, "n")
    _count(k, "k")
    if k > n:
        raise ValueError("k exceeds n")
    if not 0 <= p <= 1 or not math.isfinite(p):
        raise ValueError("invalid p")
    if p == 0:
        return 1.0
    if p == 1:
        return 1.0 if k == n else 0.0
    if k == n:
        return 1.0
    lp, lq = math.log(p), math.log1p(-p)
    logs = [math.lgamma(n + 1) - math.lgamma(j + 1)
            - math.lgamma(n - j + 1) + j * lp + (n - j) * lq
            for j in range(k + 1)]
    maximum = max(logs)
    return min(1.0, math.exp(maximum) * math.fsum(math.exp(v - maximum) for v in logs))


def clopper_pearson_upper(n: int, failures: int, confidence: float = 0.95) -> float:
    """Exact one-sided upper confidence limit for participant-level failure risk."""
    _count(n, "n")
    _count(failures, "failures")
    if n == 0 or failures > n:
        raise ValueError("invalid participant count")
    confidence = _probability(confidence, "confidence")
    if failures == n:
        return 1.0
    alpha = 1.0 - confidence
    if failures == 0:
        return -math.expm1(math.log(alpha) / n)
    lo, hi = 0.0, 1.0
    for _ in range(90):
        mid = (lo + hi) / 2
        if binomial_cdf(failures, n, mid) > alpha:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def minimum_zero_failure_units(target_risk: float, confidence: float = 0.95) -> int:
    target_risk = _probability(target_risk, "target_risk")
    confidence = _probability(confidence, "confidence")
    n = max(1, math.ceil(math.log1p(-confidence) / math.log1p(-target_risk)))
    # Correct floating-point boundary cases by evaluating the exact expression.
    while clopper_pearson_upper(n, 0, confidence) > target_risk:
        n += 1
    while n > 1 and clopper_pearson_upper(n - 1, 0, confidence) <= target_risk:
        n -= 1
    return n


def minimum_rank_calibrators(future_participants: int, risk_budget: float) -> int:
    m = _count(future_participants, "future_participants")
    if m < 1:
        raise ValueError("need at least one future participant")
    risk_budget = _probability(risk_budget, "risk_budget")
    n = max(1, math.ceil(m * (1 - risk_budget) / risk_budget))
    while m / (n + m) > risk_budget:
        n += 1
    while n > 1 and m / (n - 1 + m) <= risk_budget:
        n -= 1
    return n


def plan(confidence=0.95, validation_risk=0.05, future_participants=10,
         calibration_risk=0.025):
    confidence = _probability(confidence, "confidence")
    validation_risk = _probability(validation_risk, "validation_risk")
    calibration_risk = _probability(calibration_risk, "calibration_risk")
    nval = minimum_zero_failure_units(validation_risk, confidence)
    ncal = minimum_rank_calibrators(future_participants, calibration_risk)
    return {
        "experiment": "E002-414",
        "evidence": "prospective power planning, no physical human validation",
        "confidence": confidence,
        "validation_risk_budget": validation_risk,
        "calibration_marginal_rank_budget": calibration_risk,
        "future_participants": future_participants,
        "minimum_zero_failure_heldout_participants": nval,
        "minimum_disjoint_rank_calibration_participants": ncal,
        "illustrative_disjoint_total": nval + ncal,
        "hypothetical_zero_failure_upper_n2": clopper_pearson_upper(2, 0, confidence),
        "hypothetical_zero_failure_upper_n20": clopper_pearson_upper(20, 0, confidence),
        "invalid_frame_pseudoreplication_upper_n632": clopper_pearson_upper(632, 0, confidence),
        "product": "ABSTAIN_UNCALIBRATED",
        "physical_certificate": "NOT_AUTHORIZED",
        "notes": [
            "No false-certificate outcomes have been measured on S01/S19.",
            "Independent participant outcomes and target-domain exchangeability are assumptions.",
            "Rank-calibration probability is marginal, not a deterministic physical velocity ceiling.",
            "Combined budgets are illustrative; domain shift, shutter and reference errors remain unbounded.",
        ],
    }


REQUIRED_TRUE = (
    "preregistered_challenges", "heldout_participants",
    "independent_reference_review", "hardware_clock_and_shutter_calibrated",
    "physical_aperture_calibrated", "physical_velocity_bound_verified",
    "target_device_domain_reviewed",
)


def audit(manifest, confidence=0.95, target_risk=0.05):
    """Research-only audit of preselected independent participant challenges.

    The provenance booleans are UNAUTHENTICATED self-reports. Passing is never
    evidence that actual physical calibration occurred.
    """
    if manifest.get("experiment") != "E002-414":
        raise ValueError("wrong experiment")
    for key in REQUIRED_TRUE:
        if manifest.get(key) is not True:
            raise ValueError(f"missing independent evidence assertion: {key}")
    domain = manifest.get("target_device_id")
    if not isinstance(domain, str) or not domain.strip():
        raise ValueError("missing target device")
    rows = manifest.get("participants")
    if not isinstance(rows, list) or not rows:
        raise ValueError("missing participant-level outcomes")
    seen = set()
    failures = 0
    certificates = 0
    eligible = 0
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("invalid participant record")
        pid = row.get("participant_id")
        if not isinstance(pid, str) or not pid.strip() or pid in seen:
            raise ValueError("duplicate/invalid participant")
        seen.add(pid)
        if row.get("device_id") != domain or row.get("unseen_participant") is not True:
            raise ValueError("unreviewed device domain or reused participant")
        e = _count(row.get("eligible_gaps"), "eligible_gaps")
        r = _count(row.get("reference_resolved_gaps"), "reference_resolved_gaps")
        c = _count(row.get("issued_certificates"), "issued_certificates")
        f = _count(row.get("false_certificates"), "false_certificates")
        if not (0 < c <= r <= e) or f > c:
            raise ValueError("no evaluable certificate or inconsistent reference denominator")
        # Unresolved gaps cannot silently disappear; all eligible gaps must be
        # either independently reference-resolved or explicitly abstained.
        a = _count(row.get("unresolved_abstentions"), "unresolved_abstentions")
        if a != e - r:
            raise ValueError("unresolved reference gaps not accounted for")
        failures += int(f > 0)
        certificates += c
        eligible += e
    upper = clopper_pearson_upper(len(rows), failures, confidence)
    target_risk = _probability(target_risk, "target_risk")
    return {
        "experiment": "E002-414",
        "evidence": "self-asserted provenance; independently authenticate before use",
        "independent_participants": len(rows),
        "participants_with_any_false_certificate": failures,
        "total_certificates_not_independent": certificates,
        "eligible_gaps_not_independent": eligible,
        "one_sided_confidence": confidence,
        "participant_failure_upper": upper,
        "research_threshold_met_conditional_on_assumptions": upper <= target_risk,
        "product": "ABSTAIN_UNCALIBRATED",
        "physical_certificate": "NOT_AUTHORIZED",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, help="synthetic/test research audit input")
    parser.add_argument("--validation-risk", type=float, default=0.05)
    parser.add_argument("--calibration-risk", type=float, default=0.025)
    parser.add_argument("--future-participants", type=int, default=10)
    parser.add_argument("--confidence", type=float, default=0.95)
    args = parser.parse_args()
    if args.manifest:
        result = audit(json.loads(args.manifest.read_text()), args.confidence, args.validation_risk)
    else:
        result = plan(args.confidence, args.validation_risk,
                      args.future_participants, args.calibration_risk)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
