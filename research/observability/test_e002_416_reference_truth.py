#!/usr/bin/env python3
"""E002-416 independent grid oracle and adversarial reference-label tests."""
from __future__ import annotations
import random
import unittest
from e002_416_reference_truth import (classify, sharp_lower_envelope, NEGATIVE,
                                       POSITIVE, UNRESOLVED, ABSTAIN, NUISANCES)


def specimen(rate=160, err=0., speed=60., theta=.20, aperture=.30):
    return {
        "frame0": {"time_s": 0., "aperture_lower": aperture,
                   "aperture_upper": aperture, "nuisance_flags": []},
        "frame1": {"time_s": 1 / rate, "aperture_lower": aperture,
                   "aperture_upper": aperture, "nuisance_flags": []},
        "closure_threshold": theta,
        "clock_error_per_endpoint_s": err,
        "velocity_bound_per_s": speed,
        "velocity_bound_kind": "independent_deterministic_hard",
        "evidence": {k: True for k in (
            "independent_physical_aperture_review",
            "independent_camera_hardware_timing",
            "instantaneous_not_exposure_mean",
            "independent_geometry_review",
            "independent_hard_velocity_review")},
    }


class ReferenceTruth(unittest.TestCase):
    def test_H1_rate_transition(self):
        for hz, ratio, label in ((160, 1.875, UNRESOLVED),
                                 (240, 1.25, UNRESOLVED),
                                 (1000, .30, NEGATIVE)):
            r = classify(specimen(hz))
            self.assertEqual(r["conditional_reference_label"], label)
            self.assertAlmostEqual(r["dimensionless_sampling_ratio"], ratio)
            self.assertEqual(r["product"], ABSTAIN)
            self.assertFalse(r["product_claim_authorized"])
            self.assertFalse(r["physical_provenance_authenticated_by_tool"])

    def test_H2_actual_hidden_reference_closure(self):
        d = specimen()["frame1"]["time_s"]
        # Independent piecewise-linear construction: endpoints open, midpoint shut.
        def aperture(t):
            return .30 - 60 * min(t, d - t)
        self.assertAlmostEqual(aperture(0), .30)
        self.assertAlmostEqual(aperture(d), .30)
        self.assertAlmostEqual(aperture(d / 2), .1125)
        self.assertLess(aperture(d / 2), .20)
        self.assertEqual(classify(specimen())["conditional_reference_label"], UNRESOLVED)

    def test_H3_clock_uncertainty_reverses_certificate(self):
        self.assertEqual(classify(specimen(1000))["conditional_reference_label"], NEGATIVE)
        self.assertEqual(classify(specimen(1000, err=.0015))["conditional_reference_label"], UNRESOLVED)

    def test_H4_empirical_max_is_not_hard_bound(self):
        p = specimen(1000)
        p["velocity_bound_kind"] = "empirical_sample_maximum"
        self.assertEqual(classify(p)["conditional_reference_label"], UNRESOLVED)
        p["velocity_bound_kind"] = "independent_deterministic_hard"
        p["velocity_bound_per_s"] = None
        self.assertEqual(classify(p)["conditional_reference_label"], UNRESOLVED)

    def test_H5_nuisance_and_provenance_fail_closed(self):
        for flag in NUISANCES:
            p = specimen(1000)
            p["frame1"]["nuisance_flags"] = [flag]
            self.assertEqual(classify(p)["conditional_reference_label"], UNRESOLVED, flag)
        for key in specimen()["evidence"]:
            p = specimen(1000)
            p["evidence"][key] = False
            self.assertEqual(classify(p)["conditional_reference_label"], UNRESOLVED, key)
        for bad in (float("nan"), float("inf"), True, -1.):
            p = specimen(1000)
            p["frame1"]["time_s"] = bad
            with self.assertRaises(ValueError):
                classify(p)
        p = specimen(1000)
        p["frame1"]["time_s"] = 0
        with self.assertRaises(ValueError):
            classify(p)
        p = specimen(1000)
        p["frame1"]["aperture_lower"] = .9
        p["frame1"]["aperture_upper"] = .91
        self.assertEqual(classify(p)["conditional_reference_label"], UNRESOLVED)
        self.assertIn("inconsistent", classify(p)["reason"])

    def test_H6_witnessed_not_product_certified(self):
        p = specimen()
        p["frame0"]["aperture_lower"] = .18
        p["frame0"]["aperture_upper"] = .19
        r = classify(p)
        self.assertEqual(r["conditional_reference_label"], POSITIVE)
        self.assertEqual(r["product"], ABSTAIN)
        self.assertFalse(r["product_claim_authorized"])
        p["evidence"]["independent_physical_aperture_review"] = False
        self.assertEqual(classify(p)["conditional_reference_label"], UNRESOLVED)
        p["evidence"]["independent_physical_aperture_review"] = True
        p["frame0"]["nuisance_flags"] = ["blur"]
        self.assertEqual(classify(p)["conditional_reference_label"], UNRESOLVED)

    def test_independent_grid_oracle_1000_cases(self):
        rng = random.Random(416)
        for _ in range(1000):
            gap = rng.uniform(.0005, .05)
            speed = rng.uniform(.01, 90.)
            a0 = rng.uniform(.1, .9)
            a1 = min(.99, max(.01, a0 + rng.uniform(-speed * gap, speed * gap)))
            l0 = max(0., a0 - rng.uniform(0., .06))
            l1 = max(0., a1 - rng.uniform(0., .06))
            exact = sharp_lower_envelope(l0, l1, speed, gap)
            # Brute grid independent of analytic cone-intersection location.
            grid = min(max(l0 - speed * gap * (i / 2000),
                           l1 - speed * gap * (1 - i / 2000), 0.)
                       for i in range(2001))
            self.assertLessEqual(exact, grid + 1e-12)
            self.assertLessEqual(grid - exact, speed * gap / 2000 + 1e-12)


if __name__ == "__main__":
    unittest.main(verbosity=2)
