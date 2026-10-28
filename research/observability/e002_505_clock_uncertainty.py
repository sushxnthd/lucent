#!/usr/bin/env python3
"""E002-505: frozen synthetic timing-uncertainty falsifier.

Independent instrument-design sensitivity calculation using the existing
E002-373 scalar exposure theorem. NOT a camera calibration, physiological
measurement, certified speed bound, or product claim. No human data.
"""
import json
import sys
import unittest
from decimal import Decimal, InvalidOperation, localcontext

EPS = Decimal("1e-20")
L = Decimal("0.8")


def dec(x):
    if isinstance(x, bool) or x is None:
        raise ValueError("invalid numeric input")
    try:
        d = Decimal(str(x))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("invalid numeric input") from None
    if not d.is_finite():
        raise ValueError("nonfinite input")
    return d


def bound(*, period, exposure, speed, mean, mean_error, threshold, blind_gap_error):
    """Research-only conditional bound. No physical provenance is authenticated."""
    with localcontext() as ctx:
        ctx.prec = 70
        t, w, v, b, r, th, j = map(dec, (
            period, exposure, speed, mean, mean_error, threshold, blind_gap_error))
        if not (t > 0 and 0 < w <= t and v > 0 and 0 <= b <= 1
                and 0 <= r <= 1 and 0 < th < 1 and j >= 0):
            raise ValueError("out-of-domain instrument parameters")
        eta = Decimal(1) - b + r
        if eta > 1:
            raise ValueError("uncertainty exceeds physical aperture range")
        if eta <= v * w / 2:
            d = min(Decimal(1), (2 * v * w * eta).sqrt())
        else:
            d = min(Decimal(1), eta + v * w / 2)
        h = t - w + j
        risk = d + v * h / 2
        limit = Decimal(1) - th
        margin = limit - risk
        critical_j = 2 * (limit - d) / v - (t - w)
        # Numerical guard prevents false exclusion from a rounded equality.
        conditional = ("CONDITIONAL_EXCLUSION" if margin > EPS
                       else "NOT_EXCLUDED_OR_BOUNDARY")
        return {
            "experiment": "E002-505",
            "evidence_tier": "SYNTHETIC_INSTRUMENT_SENSITIVITY",
            "conditional_scalar_result": conditional,
            "deficit_bound": str(+d),
            "risk_upper": str(+risk),
            "threshold_deficit": str(+limit),
            "margin": str(+margin),
            "critical_total_blind_gap_error_seconds": str(+critical_j),
            "product": "ABSTAIN_UNCALIBRATED",
            "release": "BLOCKED",
            "physical_hidden_closure_certified": False,
            "human_speed_bound_certified": False,
            "camera_timebase_authenticated": False,
        }


def fixture(j="0", fps=30, **kw):
    args = dict(period=Decimal(1) / Decimal(fps), exposure="0.010",
                speed="60", mean="0.999", mean_error="0.001",
                threshold="0.20", blind_gap_error=j)
    args.update(kw)
    return bound(**args)


class FrozenInstrumentTests(unittest.TestCase):
    def test_zero_gap_error_conditional(self):
        a = fixture()
        self.assertEqual(a["conditional_scalar_result"], "CONDITIONAL_EXCLUSION")
        self.assertAlmostEqual(float(a["risk_upper"]), 0.74898979485566, places=11)

    def test_one_millisecond_still_conditional(self):
        self.assertEqual(fixture("0.001")["conditional_scalar_result"],
                         "CONDITIONAL_EXCLUSION")

    def test_two_milliseconds_reverses(self):
        a = fixture("0.002")
        self.assertEqual(a["conditional_scalar_result"], "NOT_EXCLUDED_OR_BOUNDARY")
        self.assertAlmostEqual(float(a["risk_upper"]), 0.80898979485566, places=11)

    def test_critical_gap_error(self):
        a = fixture()
        self.assertAlmostEqual(
            float(a["critical_total_blind_gap_error_seconds"]),
            0.00170034017147788, places=11)

    def test_equality_abstains(self):
        c = fixture()["critical_total_blind_gap_error_seconds"]
        self.assertEqual(fixture(c)["conditional_scalar_result"],
                         "NOT_EXCLUDED_OR_BOUNDARY")

    def test_faster_camera_conditional_given_same_assumptions(self):
        self.assertEqual(fixture("0.002", fps=60)["conditional_scalar_result"],
                         "CONDITIONAL_EXCLUSION")

    def test_gap_error_monotone(self):
        risks = [dec(fixture(str(Decimal(i) / 1000))["risk_upper"])
                 for i in range(5)]
        self.assertEqual(risks, sorted(risks))

    def test_mean_error_monotone(self):
        risks = [dec(fixture(mean_error=str(Decimal(i) / 1000))["risk_upper"])
                 for i in range(5)]
        self.assertEqual(risks, sorted(risks))

    def test_speed_monotone(self):
        risks = [dec(fixture(speed=str(i))["risk_upper"])
                 for i in (20, 40, 60, 80, 100)]
        self.assertEqual(risks, sorted(risks))

    def test_no_physical_certification_from_any_numeric_outcome(self):
        for a in (fixture(), fixture("0.002"), fixture(fps=60)):
            self.assertEqual(a["product"], "ABSTAIN_UNCALIBRATED")
            self.assertEqual(a["release"], "BLOCKED")
            self.assertFalse(a["physical_hidden_closure_certified"])
            self.assertFalse(a["human_speed_bound_certified"])
            self.assertFalse(a["camera_timebase_authenticated"])

    def test_invalid_and_nonfinite_abstain_by_rejection(self):
        for k, value in (("speed", None), ("speed", "NaN"),
                         ("speed", True), ("speed", "Infinity"),
                         ("period", 0), ("exposure", "0.1"),
                         ("blind_gap_error", "-0.001"),
                         ("mean_error", "-0.1"), ("threshold", 1)):
            with self.subTest(k=k, value=value), self.assertRaises(ValueError):
                fixture(**{k: value})

    def test_zero_mean_error_exact_open_means(self):
        a = fixture(mean="1", mean_error="0")
        self.assertEqual(a["deficit_bound"], "0")
        self.assertEqual(a["conditional_scalar_result"], "CONDITIONAL_EXCLUSION")


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
    else:
        print(json.dumps({
            "frozen_30fps_j0": fixture(),
            "frozen_30fps_j2ms": fixture("0.002"),
            "frozen_60fps_j2ms": fixture("0.002", fps=60),
        }, indent=2, sort_keys=True))
