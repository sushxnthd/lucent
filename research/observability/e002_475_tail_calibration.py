#!/usr/bin/env python3
"""E002-475: classical participant-level maximum calibration limits.

No anatomical, timing or physical-camera validation is inferred. Published
per-blink proxies are NOT instantaneous anatomical hard speed limits.
"""
import argparse
import itertools
import json
import random
from decimal import Decimal, getcontext
from fractions import Fraction

getcontext().prec = 45
CALIBRATION_PARTICIPANTS = 12
HELDOUT_PARTICIPANTS = 5
CALIBRATION_BLINKS = 1657  # Never a sample size for participant-level inference.
PRODUCT = "ABSTAIN_UNCALIBRATED"


def exact_joint_rank(n: int, m: int) -> Fraction:
    if type(n) is not int or type(m) is not int or n < 1 or m < 1:
        raise ValueError("positive integer participant counts required")
    return Fraction(n, n + m)


def tolerance_confidence(n: int, content: Decimal) -> Decimal:
    if type(n) is not int or n < 1 or not isinstance(content, Decimal) or not (0 < content < 1):
        raise ValueError("invalid iid continuous participant tolerance inputs")
    return Decimal(1) - content ** n


def minimum_tolerance_n(content: Decimal, confidence: Decimal) -> int:
    if not isinstance(confidence, Decimal) or not (0 < confidence < 1):
        raise ValueError("invalid confidence")
    n = 1
    while tolerance_confidence(n, content) < confidence:
        n += 1
    return n


def minimum_joint_n(m: int, target: Fraction) -> int:
    if not isinstance(target, Fraction) or not (0 < target < 1):
        raise ValueError("invalid joint target")
    n = 1
    while exact_joint_rank(n, m) < target:
        n += 1
    return n


def exhaustive_rank_check(n: int, m: int) -> Fraction:
    if n + m > 8:
        raise ValueError("exhaustive check limited to <=8 ranks")
    success = total = 0
    for permutation in itertools.permutations(range(1, n + m + 1)):
        total += 1
        success += max(permutation[:n]) > max(permutation[n:])
    return Fraction(success, total)


def synthetic_joint_coverage(n: int, m: int, trials: int = 25000, seed: int = 475,
                             shift: bool = False) -> float:
    if trials < 20000 or type(seed) is not int:
        raise ValueError("frozen trial count or seed violated")
    rng = random.Random(seed)
    covered = 0
    for _ in range(trials):
        training_max = max(rng.random() for _ in range(n))
        future_max = max((2.0 if shift else 0.0) + rng.random() for _ in range(m))
        covered += future_max <= training_max
    return covered / trials


def evaluate(calibration_participants: int = CALIBRATION_PARTICIPANTS):
    if type(calibration_participants) is not int or calibration_participants != CALIBRATION_PARTICIPANTS:
        raise ValueError("cannot substitute blink count or change frozen calibration unit")
    n = calibration_participants
    p = Decimal("0.95")
    confidence = Decimal("0.95")
    rank_one = exact_joint_rank(n, 1)
    rank_eight = exact_joint_rank(n, 8)
    finite = exhaustive_rank_check(3, 2)
    if finite != exact_joint_rank(3, 2):
        raise AssertionError("independent exhaustive rank test disagrees")
    tolerance_n = minimum_tolerance_n(p, confidence)
    joint_n = minimum_joint_n(8, Fraction(95, 100))
    if tolerance_n != 59 or joint_n != 152:
        raise AssertionError("frozen integer thresholds falsified")
    if not (tolerance_confidence(58, p) < confidence <= tolerance_confidence(59, p)):
        raise AssertionError("tolerance threshold boundary failed")
    if not (exact_joint_rank(151, 8) < Fraction(95, 100) <= exact_joint_rank(152, 8)):
        raise AssertionError("joint threshold boundary failed")
    mc = synthetic_joint_coverage(n, 8)
    shifted = synthetic_joint_coverage(n, 8, shift=True)
    if abs(mc - float(rank_eight)) > 0.02 or shifted != 0.0:
        raise AssertionError("prespecified synthetic controls falsified")
    return {
        "experiment": "E002-475",
        "evidence_tier": "CLASSICAL_ORDER_STATISTICS_PLUS_SYNTHETIC_CHECK_NOT_PHYSICAL_VALIDATION",
        "unit": "independent_participant_maximum_of_published_peak_speed_proxy",
        "calibration_participants": n,
        "sealed_heldout_participants_not_reopened": HELDOUT_PARTICIPANTS,
        "calibration_blinks_not_independent": CALIBRATION_BLINKS,
        "one_future_marginal_rank_coverage": float(rank_one),
        "eight_future_joint_rank_coverage": float(rank_eight),
        "three_train_two_future_exhaustive_rank": float(finite),
        "ninetyfive_content_confidence_n12": float(tolerance_confidence(n, p)),
        "minimum_independent_participants_95_content_95_confidence": tolerance_n,
        "minimum_independent_participants_95_joint_eight_future": joint_n,
        "iid_uniform_25000_trials_joint_coverage": mc,
        "shifted_future_25000_trials_joint_coverage": shifted,
        "assumptions": ["iid continuous participant-level proxy maxima", "no gaze/lighting/device/behavior distribution shift"],
        "sample_max_is_not_hard_cap": True,
        "recorded_peak_proxy_is_not_instantaneous_anatomical_speed": True,
        "physical_validation": "NOT_ESTABLISHED",
        "physical_release_authorized": False,
        "product_claim": PRODUCT,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    with open(args.output, "w", encoding="utf-8") as stream:
        json.dump(evaluate(), stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
    print("E002-475: participant-level rank ceiling; physical release blocked")
