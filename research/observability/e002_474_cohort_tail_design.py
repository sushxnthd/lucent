#!/usr/bin/env python3
"""E002-474: post-hoc human-tail design stress; never a physical certification.

Cross-checks the existing E002-472 conservative sufficient design criterion
against exact-rational arithmetic. Uses only checksum-linked, deidentified
published aggregate. No raw human rows, anatomical trajectories or camera
measurements are accessed.
"""
import argparse
import json
import math
from fractions import Fraction
from pathlib import Path

from e002_472_design_feasibility import design_case
from e002_473_literature_stress import SOURCES

HERE = Path(__file__).resolve().parent
EXPECTED_SHA = "6248c00b3c2849115f913eb184821d05efe069dd081587a84472c054494bbc43"
DESIGNS = ((30, 4), (240, 1), (300, 1), (480, 1), (600, 1))
ABSTAIN = "ABSTAIN_UNCALIBRATED"


def cohort_tail(path=HERE / "E002_459_HUMAN_AGGREGATE.json"):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if (data.get("source_sha256") != EXPECTED_SHA
        or data.get("participants") != {"calibration": 12, "holdout": 5}
        or data.get("blinks") != {"calibration": 1657, "holdout": 649}
        or data.get("physical_release_authorized") is not False
        or data.get("product_claim") != ABSTAIN):
        raise ValueError("untrusted or modified human aggregate")
    speeds = data.get("pooled_training_caps", {})
    c, o = speeds.get("closing_mm_s"), speeds.get("opening_mm_s")
    if any(isinstance(v, bool) or not isinstance(v, (float, int))
           or not math.isfinite(v) or v <= 0 for v in (c, o)):
        raise ValueError("invalid directional human sample maxima")
    return c, o


def rational_design(fps, shutter_ms, velocity_mm_s):
    """Independent arithmetic, with exact rational representation of inputs."""
    f = Fraction(str(fps))
    w = Fraction(str(shutter_ms))
    v = Fraction(str(velocity_mm_s))
    period = Fraction(1000) / f
    uncertainty = Fraction(1, 10)
    clock = Fraction(1, 10)
    reference_exposure = Fraction(1, 5)
    reference_clock = Fraction(1, 10)
    denominator = w / 4 + (period + 2 * clock) / 2
    critical_speed = Fraction(1000) * (1 - uncertainty) / denominator
    strict_min_margin = uncertainty + v * denominator / 1000
    reference_feasible = w + reference_exposure + 2 * (clock + reference_clock) < period
    decision = ("ABSTAIN_DESIGN" if not reference_feasible else
                "EXCLUSION_FEASIBLE_CONDITIONALLY" if v < critical_speed else
                "EXCLUSION_NOT_SUPPORTED")
    return critical_speed, strict_min_margin, v / critical_speed, decision


def evaluate(path=HERE / "E002_459_HUMAN_AGGREGATE.json"):
    c, o = cohort_tail(path)
    published = SOURCES["2013_voluntary_optical_mean_peak"]
    if published["velocity_mm_s"] != 243 or "mean" not in published["kind"]:
        raise ValueError("published mean statistic changed")
    rows = []
    for fps, exposure in DESIGNS:
        for label, v in (("2013_mean_of_voluntary_peaks", 243),
                         ("2026_calibration_sample_closing_max", c)):
            crit, margin, ratio, decision = rational_design(fps, exposure, v)
            model = design_case(
                fps=fps, exposure_ms=exposure,
                aperture_margin_mm=1.0, aperture_uncertainty_mm=0.1,
                clock_error_ms=0.1, reference_exposure_ms=0.2,
                reference_clock_error_ms=0.1,
                hypothetical_velocity_mm_s=v)
            if (model["decision"] != decision
                or abs(model["critical_hypothetical_velocity_mm_s"] - float(crit)) > 1e-9
                or model["physical_release_authorized"]
                or model["product_claim"] != ABSTAIN):
                raise AssertionError("independent design/evaluator disagreement")
            rows.append({
                "fps_nominal": fps,
                "shutter_ms_hypothetical": exposure,
                "speed_source": label,
                "hypothetical_symmetric_speed_mm_s": v,
                "critical_speed_mm_s": float(crit),
                "strict_min_margin_mm": float(margin),
                "dimensionless_speed_ratio": float(ratio),
                "conservative_design_decision": decision,
                "is_hard_physiological_cap": False,
                "physical_release_authorized": False,
                "product_claim": ABSTAIN,
            })
    def row(fps, label):
        return next(r for r in rows if r["fps_nominal"] == fps and r["speed_source"] == label)
    mean = "2013_mean_of_voluntary_peaks"
    tail = "2026_calibration_sample_closing_max"
    if not (all(row(f, mean)["conservative_design_decision"] == "EXCLUSION_FEASIBLE_CONDITIONALLY"
                for f in (240, 300, 480))
            and all(row(f, tail)["conservative_design_decision"] == "EXCLUSION_NOT_SUPPORTED"
                    for f in (240, 300))
            and row(480, tail)["conservative_design_decision"] == "EXCLUSION_FEASIBLE_CONDITIONALLY"):
        raise AssertionError("frozen cross-cohort prediction falsified")
    # Ideal known-linear-shutter-aperture model is a distinct, narrower assumption.
    ideal_directional_critical_ms = 1000 / c + 1000 / o
    return {
        "experiment": "E002-474",
        "evidence_tier": "POST_HOC_EXISTING_HUMAN_AGGREGATE_PLUS_DESIGN_FALSIFICATION",
        "human_source_sha256": EXPECTED_SHA,
        "calibration_participants": 12,
        "holdout_participants_not_reopened": 5,
        "rows": rows,
        "conservative_240fps_pilot_tail_supported": False,
        "ideal_linear_aperture_directional_240fps_conditional_exclusion":
            (1000 / 240 < ideal_directional_critical_ms),
        "ideal_linear_aperture_directional_critical_ms": ideal_directional_critical_ms,
        "ideal_linear_model_is_not_authenticated_rgb": True,
        "sample_max_is_not_hard_cap": True,
        "physical_validation": "NOT_ESTABLISHED",
        "physical_release_authorized": False,
        "product_claim": ABSTAIN,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(json.dumps(evaluate(), indent=2, sort_keys=True, allow_nan=False) + "\n")
    print("E002-474: post-hoc cohort-tail design decision; physical release blocked")
