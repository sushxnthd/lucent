#!/usr/bin/env python3
"""E002-411 source-level instrument and fail-closed tests."""
import unittest
from e002_411_phase_identifiability import (
    experiment, first_abs_moment_ms, pulse_response,
    uncovered_support_ms, shutter_release_gate,
)


class PhaseIdentifiabilityTests(unittest.TestCase):
    def test_preregistered_witnesses(self):
        result = experiment()
        self.assertEqual(result["indistinguishable_pairs"], 1000)
        self.assertAlmostEqual(result["moment_ratio"], 4.6/.6)
        self.assertEqual(result["product"], "ABSTAIN_UNCALIBRATED")

    def test_exploratory_nonzero_observations_still_ambiguous(self):
        mix = experiment()["exploratory_positive_signal_mixture"]
        self.assertTrue(all(y > 0 for y in mix["sparse_pulse_responses"]))
        self.assertAlmostEqual(mix["center_moment_ms"], 1.55)
        self.assertAlmostEqual(mix["edge_moment_ms"], 3.55)
        self.assertAlmostEqual(mix["moment_separation_ms"], 2.0)
        self.assertFalse(mix["preregistered"])

    def test_uncovered_support(self):
        self.assertGreater(uncovered_support_ms(range(10), .2, 10., .05), 7.)
        self.assertLess(uncovered_support_ms([i/10 for i in range(99)], .2, 10.), 1e-9)

    def test_phase_jitter_witness(self):
        for shutter in ((5.5, 5.7), (9.5, 9.7)):
            self.assertEqual(pulse_response(shutter, range(10), .2, .05), [0.]*10)

    def test_exact_moment(self):
        self.assertAlmostEqual(first_abs_moment_ms((5.5, 5.7)), .6)
        self.assertAlmostEqual(first_abs_moment_ms((9.5, 9.7)), 4.6)

    def test_missing_instrument_evidence(self):
        phases = [i/10 for i in range(99)]
        base = dict(phases=phases, pulse_ms=.2, exposure_ms=10., jitter_ms=0.,
                    photodiode_verified=True, hardware_clock_verified=True,
                    row_response_verified=True, physical_moment_bound_verified=True)
        for field in ("photodiode_verified", "hardware_clock_verified",
                      "row_response_verified", "physical_moment_bound_verified"):
            args = dict(base, **{field: False})
            self.assertEqual(shutter_release_gate(**args)["instrument_status"], "REJECT")
            self.assertEqual(shutter_release_gate(**args)["product"], "ABSTAIN_UNCALIBRATED")
        self.assertEqual(shutter_release_gate(**base)["instrument_status"],
                         "NECESSARY_CHECKS_ONLY")
        self.assertEqual(shutter_release_gate(**base)["product"], "ABSTAIN_UNCALIBRATED")

    def test_sparse_calibration_rejected_even_if_other_flags_true(self):
        r = shutter_release_gate(phases=list(range(10)), pulse_ms=.2,
             exposure_ms=10., jitter_ms=.05, photodiode_verified=True,
             hardware_clock_verified=True, row_response_verified=True,
             physical_moment_bound_verified=True)
        self.assertIn("unilluminated_shutter_support", r["reasons"])

    def test_invalid_phase_data_fail_closed(self):
        for phases in ([], [float("nan")], [float("inf")]):
            r = shutter_release_gate(phases=phases, pulse_ms=.2,
                 exposure_ms=10., jitter_ms=0., photodiode_verified=True,
                 hardware_clock_verified=True, row_response_verified=True,
                 physical_moment_bound_verified=True)
            self.assertEqual(r["instrument_status"], "REJECT")
            self.assertEqual(r["product"], "ABSTAIN_UNCALIBRATED")


if __name__ == "__main__":
    unittest.main()
