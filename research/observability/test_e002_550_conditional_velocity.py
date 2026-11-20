#!/usr/bin/env python3
"""E002-550 adversarial conditional measurement tests; no human records."""
import math
import unittest
from e002_550_conditional_velocity import evaluate, REQUIRED_NUISANCES


def fixture(values=(0.4, 0.5), dt=0.0025, A=0.0, e=0.0, u=0.0):
    return {
        "assumptions": {
            "acceleration_upper": A, "aperture_error_upper": e,
            "clock_error_upper": u, "complete_coverage": True,
            "nuisance_pass": {k: True for k in REQUIRED_NUISANCES},
        },
        "observations": [
            {"t": i*dt, "a": a, "quality": "OK"}
            for i, a in enumerate(values)
        ],
    }


class VelocityEnvelopeTests(unittest.TestCase):
    def test_linear_exact(self):
        out = evaluate(fixture())
        self.assertEqual(out["status"], "CONDITIONAL_BOUND_ONLY_NOT_AUTHENTICATED")
        self.assertAlmostEqual(out["velocity_upper_per_s"], 40)
        self.assertEqual(out["release"], "BLOCKED")
        self.assertFalse(out["human_validation"])

    def test_error_and_acceleration_correction(self):
        out = evaluate(fixture(A=1000, e=0.01))
        self.assertAlmostEqual(out["velocity_upper_per_s"], 49.25)

    def test_clock_widens_bound(self):
        a = evaluate(fixture(A=1000, e=0.01, u=0.0))
        b = evaluate(fixture(A=1000, e=0.01, u=0.0001))
        self.assertGreater(b["velocity_upper_per_s"], a["velocity_upper_per_s"])

    def test_uncertainty_monotonicity(self):
        base = evaluate(fixture(A=100, e=0.001, u=0.00001))["velocity_upper_per_s"]
        for kwargs in ({"A": 200}, {"e": 0.002}, {"u": 0.00002}):
            self.assertGreater(evaluate(fixture(**{**{"A": 100, "e": 0.001, "u": 0.00001}, **kwargs}))["velocity_upper_per_s"], base)

    def test_analytic_sinusoid(self):
        dt = 1/400
        vals = [0.5 + 0.2*math.sin(2*math.pi*5*i*dt) for i in range(81)]
        # Independent analytic acceleration ceiling = 0.2*(2*pi*5)^2 < 200.
        out = evaluate(fixture(vals, dt=dt, A=200))
        self.assertGreaterEqual(out["velocity_upper_per_s"], 0.2*2*math.pi*5)
        self.assertEqual(out["covered_intervals"], 80)

    def test_no_acceleration_is_not_speed_certificate(self):
        obj = fixture(values=(0.5, 0.5))
        obj["assumptions"].pop("acceleration_upper")
        self.assertEqual(evaluate(obj)["status"], "ABSTAIN_NO_HARD_SPEED_CERTIFICATE")

    def test_between_sample_spike_not_inferable(self):
        # Same two samples, arbitrary 0.5 amplitude between them. As spike
        # width tends to zero, slope tends to infinity. No finite-diff cap.
        observed = fixture(values=(0.5, 0.5))
        observed["assumptions"]["acceleration_upper"] = None
        self.assertEqual(evaluate(observed)["status"], "ABSTAIN_NO_HARD_SPEED_CERTIFICATE")
        for width in (0.0001, 0.00001, 0.000001):
            self.assertGreater(1/width, 4000)

    def test_missing_frame(self):
        obj = fixture()
        obj["assumptions"]["complete_coverage"] = False
        self.assertEqual(evaluate(obj)["reason"], "MISSING_SAMPLING_COVERAGE")

    def test_bad_nuisance(self):
        for name in REQUIRED_NUISANCES:
            obj = fixture()
            obj["assumptions"]["nuisance_pass"][name] = False
            self.assertEqual(evaluate(obj)["reason"], "UNRESOLVED_NUISANCE")

    def test_clock_uncertainty_over_interval(self):
        self.assertEqual(evaluate(fixture(u=0.00125))["reason"], "UNRESOLVED_CLOCK_OR_NONMONOTONE_TIME")

    def test_duplicate_or_reversed_time(self):
        for times in ((0, 0), (0.0025, 0)):
            obj = fixture()
            for s, t in zip(obj["observations"], times):
                s["t"] = t
            self.assertEqual(evaluate(obj)["status"], "ABSTAIN_NO_HARD_SPEED_CERTIFICATE")

    def test_bad_aperture(self):
        for bad in (-0.1, 1.1, float("nan"), "0.5", True):
            obj = fixture()
            obj["observations"][1]["a"] = bad
            self.assertEqual(evaluate(obj)["reason"], "INVALID_APERTURE_OR_TIME")

    def test_bad_bounds(self):
        for name in ("acceleration_upper", "aperture_error_upper", "clock_error_upper"):
            for bad in (-1, float("inf"), None, True):
                obj = fixture()
                obj["assumptions"][name] = bad
                self.assertEqual(evaluate(obj)["reason"], "INDEPENDENT_HARD_BOUNDS_UNAVAILABLE")

    def test_bad_sample_quality(self):
        obj = fixture()
        obj["observations"][0]["quality"] = "OCCLUDED"
        self.assertEqual(evaluate(obj)["reason"], "UNRESOLVED_SAMPLE_QUALITY")

    def test_never_certifies_human(self):
        for obj in (fixture(), fixture(A=1000, e=0.01, u=0.0001)):
            out = evaluate(obj)
            self.assertFalse(out["physical_certification"])
            self.assertFalse(out["human_validation"])
            self.assertEqual(out["product"], "ABSTAIN_UNCALIBRATED")
            self.assertEqual(out["release"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
