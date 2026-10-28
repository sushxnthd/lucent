#!/usr/bin/env python3
"""E002-506: independent optical-pulse frame-period bounds. Research-only.

The code cannot authenticate optical timing, pulse-to-exposure attribution,
shutter calibration, or human eyelid speed. Never enables product claims.
"""
import argparse
import json
import unittest
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path


def q(value):
    if value is None or isinstance(value, bool):
        raise ValueError("INVALID_NUMBER")
    try:
        return Fraction(str(value))
    except (ValueError, TypeError, ZeroDivisionError):
        raise ValueError("INVALID_NUMBER") from None


def dec(f):
    return Decimal(f.numerator) / Decimal(f.denominator)


def calibrate(pulses, shutter_min, shutter_max, speed="60",
              mean="0.999", mean_error="0.001", threshold="0.2"):
    if not isinstance(pulses, list) or len(pulses) < 2:
        raise ValueError("INSUFFICIENT_PULSES")
    w0, w1 = q(shutter_min), q(shutter_max)
    if not 0 <= w0 <= w1 or w1 == 0:
        raise ValueError("INVALID_SHUTTER_INTERVAL")
    rows = []
    for p in pulses:
        if not isinstance(p, dict) or type(p.get("frame")) is not int or p["frame"] < 0:
            raise ValueError("INVALID_FRAME")
        l, u = q(p.get("time_lower_s")), q(p.get("time_upper_s"))
        if l > u:
            raise ValueError("INVALID_TIME_BRACKET")
        rows.append((p["frame"], l, u))
    rows.sort()
    if len(set(n for n, _, _ in rows)) != len(rows):
        raise ValueError("DUPLICATE_FRAME")
    lo, hi = Fraction(0), None
    for i, (ni, li, ui) in enumerate(rows):
        for nj, lj, uj in rows[i+1:]:
            d = nj-ni
            lo = max(lo, (lj-w1-ui)/d)
            bound_hi = (uj-li+w1)/d
            hi = bound_hi if hi is None else min(hi, bound_hi)
    if hi is None or hi <= 0 or lo > hi:
        raise ValueError("INCONSISTENT_OPTICAL_CLOCK")
    with localcontext() as ctx:
        ctx.prec = 70
        t = dec(hi)
        v, b, r, th = [dec(q(x)) for x in (speed, mean, mean_error, threshold)]
        if not (v > 0 and 0 <= b <= 1 and 0 <= r <= b and 0 < th < 1
                and dec(w0) <= t):
            raise ValueError("INVALID_PHYSICS_INPUT")
        eta = Decimal(1)-b+r
        wx = dec(w1)
        deficit = min(Decimal(1), (2*v*wx*eta).sqrt()) if eta <= v*wx/2 else min(Decimal(1), eta+v*wx/2)
        risk = deficit+v*(t-dec(w0))/2
        margin = Decimal(1)-th-risk
        return {
            "experiment": "E002-506",
            "evidence_tier": "SYNTHETIC_OR_SELF_ATTESTED_INSTRUMENT_MODEL",
            "period_lower_seconds": str(dec(lo)),
            "period_upper_seconds": str(t),
            "blind_gap_upper_seconds": str(t-dec(w0)),
            "risk_upper": str(+risk),
            "margin": str(+margin),
            "conditional_scalar_result": "CONDITIONAL_EXCLUSION" if margin > Decimal("1e-20") else "NOT_EXCLUDED_OR_BOUNDARY",
            "assumption": "Independently timed optical events assigned to known exposures; affine global shutter; native frames not dropped",
            "instrument_authenticated_by_this_program": False,
            "human_speed_bound_certified": False,
            "physical_hidden_closure_certified": False,
            "product": "ABSTAIN_UNCALIBRATED",
            "release": "BLOCKED"
        }


def fixture(span, wmin="0.010", wmax="0.010"):
    t = Decimal(span)/Decimal(30)
    return calibrate([
        {"frame": 0, "time_lower_s": "-0.0001", "time_upper_s": "0.0001"},
        {"frame": span, "time_lower_s": str(t-Decimal("0.0001")),
         "time_upper_s": str(t+Decimal("0.0001"))}
    ], wmin, wmax)


class FrozenTests(unittest.TestCase):
    def test_long_span_excludes_conditionally(self):
        x = fixture(300)
        self.assertEqual(x["conditional_scalar_result"], "CONDITIONAL_EXCLUSION")
        self.assertAlmostEqual(float(x["risk_upper"]), 0.7500097948556636, places=11)

    def test_short_span_does_not_exclude(self):
        x = fixture(3)
        self.assertEqual(x["conditional_scalar_result"], "NOT_EXCLUDED_OR_BOUNDARY")
        self.assertAlmostEqual(float(x["risk_upper"]), 0.8509897948556636, places=11)

    def test_unmeasured_shutter_does_not_exclude(self):
        self.assertEqual(fixture(300, "0", "0.010")["conditional_scalar_result"], "NOT_EXCLUDED_OR_BOUNDARY")

    def test_contradictory_third_pulse(self):
        p = [{"frame": n, "time_lower_s": str(t), "time_upper_s": str(t)}
             for n, t in ((0, 0), (150, 6), (300, 10))]
        with self.assertRaisesRegex(ValueError, "INCONSISTENT_OPTICAL_CLOCK"):
            calibrate(p, "0.01", "0.01")

    def test_duplicate_frame(self):
        p = [{"frame": 0, "time_lower_s": "0", "time_upper_s": "0"}]*2
        with self.assertRaisesRegex(ValueError, "DUPLICATE_FRAME"):
            calibrate(p, "0.01", "0.01")

    def test_invalid_bracket(self):
        p = [{"frame": 0, "time_lower_s": "1", "time_upper_s": "0"},
             {"frame": 1, "time_lower_s": "2", "time_upper_s": "2"}]
        with self.assertRaisesRegex(ValueError, "INVALID_TIME_BRACKET"):
            calibrate(p, "0.01", "0.01")

    def test_bad_shutter(self):
        for a, b in (("-0.001", "0.01"), ("0.02", "0.01"), ("NaN", "0.01")):
            with self.subTest(a=a, b=b), self.assertRaises(ValueError):
                fixture(300, a, b)

    def test_invalid_number(self):
        for v in ("NaN", "Infinity", True, None):
            with self.subTest(v=v), self.assertRaises(ValueError):
                calibrate([{"frame": 0, "time_lower_s": v, "time_upper_s": "0"},
                           {"frame": 300, "time_lower_s": "10", "time_upper_s": "10"}],
                          "0.01", "0.01")

    def test_wider_brackets_monotone(self):
        risks = []
        for e in (Decimal("0.0001"), Decimal("0.001"), Decimal("0.005")):
            p = [{"frame": 0, "time_lower_s": str(-e), "time_upper_s": str(e)},
                 {"frame": 300, "time_lower_s": str(Decimal(10)-e),
                  "time_upper_s": str(Decimal(10)+e)}]
            risks.append(Decimal(calibrate(p, "0.01", "0.01")["risk_upper"]))
        self.assertEqual(risks, sorted(risks))

    def test_no_physical_or_product_clearance(self):
        for x in (fixture(3), fixture(300), fixture(300, "0", "0.01")):
            self.assertEqual(x["product"], "ABSTAIN_UNCALIBRATED")
            self.assertEqual(x["release"], "BLOCKED")
            for k in ("instrument_authenticated_by_this_program",
                      "human_speed_bound_certified", "physical_hidden_closure_certified"):
                self.assertFalse(x[k])

    def test_missing_pulse(self):
        with self.assertRaisesRegex(ValueError, "INSUFFICIENT_PULSES"):
            calibrate([{"frame": 0, "time_lower_s": "0", "time_upper_s": "0"}],
                      "0.01", "0.01")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--input", type=Path)
    args = parser.parse_args()
    if args.self_test:
        unittest.main(argv=["e002_506_optical_pulse.py"], verbosity=2)
    elif args.input:
        print(json.dumps(calibrate(**json.loads(args.input.read_text(encoding="utf-8"))),
                         indent=2, sort_keys=True))
    else:
        print(json.dumps({"long_300_frames": fixture(300),
                          "short_3_frames": fixture(3),
                          "unknown_shutter_min": fixture(300, "0", "0.010")},
                         indent=2, sort_keys=True))
