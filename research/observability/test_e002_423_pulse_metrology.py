#!/usr/bin/env python3
"""Independent adversarial checks for frozen E002-423; no human/hardware claims."""
import math
import random
import unittest

try:
    from . import e002_423_pulse_metrology as m
except ImportError:
    import e002_423_pulse_metrology as m


class E002423Tests(unittest.TestCase):
    def test_independent_overlap_oracle(self):
        rng = random.Random(1423)
        for _ in range(1000):
            s = rng.uniform(-10, 10)
            e = rng.uniform(0.1, 5)
            c = rng.uniform(-10, 10)
            # Generator uses the integral of an indicator; fitter uses min/max.
            self.assertAlmostEqual(
                m.independent_pulse_integral(s, e, c),
                m.boxcar_response(s, e, c), places=11)

    def test_frozen_prediction_and_adversaries(self):
        r = m.experiment()
        self.assertEqual(r["phase_count"], 101)
        self.assertEqual(r["train_count_per_row"], 51)
        self.assertEqual(r["heldout_count_per_row"], 50)
        self.assertTrue(all(r["frozen_tests"].values()), r)
        self.assertAlmostEqual(r["baseline"][0]["center_ms"], 0.0, places=1)
        self.assertAlmostEqual(r["baseline"][1]["center_ms"], 3.2, places=1)
        self.assertTrue(any(x["heldout_rmse"] > 0.015 for x in r["jitter_0p8ms"]))
        self.assertTrue(any(x["heldout_rmse"] > 0.015 for x in r["gamma_sqrt"]))
        self.assertTrue(any(x["heldout_rmse"] > 0.015 for x in r["phase_shuffle"]))

    def test_invalid_and_unlabeled_traces_fail_closed(self):
        invalid = [
            (None, [0.0] * 10),
            ([float(i) for i in range(9)], [0.0] * 8),
            ([float(i) for i in range(10)], [0.0] * 9 + [float("nan")]),
            ([0.0] * 10, [0.0] * 10),
            ([float(i) for i in range(10)], [0.0] * 9 + [1.5]),
            ([float(i) for i in range(7)], [0.0] * 7),
        ]
        for phases, values in invalid:
            with self.subTest(phases=phases):
                with self.assertRaises(ValueError):
                    m.fit_row(phases, values)

    def test_operator_assertions_cannot_authenticate_physical_camera(self):
        for flags in (
            {},
            {"photodiode_verified": True, "phase_clock_verified": True,
             "row_clock_verified": True, "linear_raw_verified": True,
             "unsaturated": True},
            {"photodiode_verified": True, "phase_clock_verified": True,
             "row_clock_verified": True, "linear_raw_verified": True,
             "unsaturated": False},
        ):
            decision = m.physical_policy(**flags)
            self.assertEqual(decision["product"], "ABSTAIN_UNCALIBRATED")
            self.assertFalse(decision["physical_calibration_authorized"])
            self.assertFalse(decision["product_claim_authorized"])
            self.assertFalse(decision["physical_provenance_authenticated_by_tool"])


if __name__ == "__main__":
    unittest.main()
