"""E002-479 regression against the actual E002-477 intake."""
import tempfile
import unittest
from pathlib import Path

from e002_477_optical_intake import evaluate
from e002_479_phase_island import (
    AMPLITUDE, BLOCKED, ISLAND, PHASE_COUNT, REPEATS, ROWS, STEP, T, U, WIDTH,
    detect, heldout_readings, overlap, pulse_contrast, robust_island_unseen,
    run_experiment, write_fixture,
)


class PhaseIslandTests(unittest.TestCase):
    def test_nominal_grid_is_identical(self):
        for i in range(PHASE_COUNT):
            t = i * STEP
            self.assertAlmostEqual(pulse_contrast(t, 0), pulse_contrast(t, AMPLITUDE), places=9)

    def test_full_phase_uncertainty_support_misses_corrected_island(self):
        self.assertTrue(robust_island_unseen())

    def test_original_frozen_island_did_not_survive_second_period(self):
        # Preserve a pre-implementation falsification, not an invisible protocol edit.
        original = (2.020, 2.030)
        self.assertGreater(overlap(6.2 - U, 6.2 + WIDTH + U, T + original[0], T + original[1]), 0)

    def test_periodic_not_one_shot(self):
        for t in (0.1, 0.9, 2.017, 3.1):
            self.assertAlmostEqual(pulse_contrast(t, AMPLITUDE), pulse_contrast(t + T, AMPLITUDE), places=9)

    def test_heldout_probe_discriminates_both_periods(self):
        self.assertEqual(len(heldout_readings(AMPLITUDE)), 2 * REPEATS * len(ROWS))
        self.assertTrue(detect(heldout_readings(AMPLITUDE)))
        self.assertFalse(detect(heldout_readings(0)))

    def test_weak_island_remains_uncertain_not_absent(self):
        self.assertFalse(detect(heldout_readings(0.004)))
        self.assertGreater(max(heldout_readings(0.004)), 0)

    def test_high_probe_separation_survives_frozen_jitter_and_noise(self):
        self.assertGreater(min(heldout_readings(AMPLITUDE)), 0.04)
        self.assertLess(max(heldout_readings(0)), 0.04)

    def test_real_intake_passes_both_indistinguishable_models(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = write_fixture(Path(tmp) / "a", 0.0)
            b = write_fixture(Path(tmp) / "b", AMPLITUDE)
            self.assertTrue(all(x.read_bytes() == y.read_bytes() for x, y in zip(a, b)))
            ra, rb = evaluate(*a), evaluate(*b)
            self.assertEqual(ra, rb)
            self.assertEqual(ra["qa_status"], "PASS_INTAKE_ONLY")
            self.assertEqual(ra["observations"], 6720)
            self.assertFalse(ra["physical_release_authorized"])
            self.assertEqual(ra["product_claim"], BLOCKED)

    def test_wrong_grid_phase_does_not_create_unseen_guarantee(self):
        self.assertGreater(STEP - WIDTH - 2 * U, 0)
        # A pulse deliberately placed inside the island sees the sensitivity.
        self.assertAlmostEqual(pulse_contrast(2.017, AMPLITUDE), AMPLITUDE, places=8)

    def test_aggregate_never_authorizes_physical_claim(self):
        r = run_experiment()
        self.assertTrue(r["two_period_robust_island_unseen"])
        self.assertTrue(r["all_source_files_identical"])
        self.assertTrue(r["intake_output_identical"])
        self.assertTrue(r["heldout_high_island_detected"])
        self.assertFalse(r["heldout_low_island_detected"])
        self.assertEqual(r["physical_acquisitions"], 0)
        self.assertEqual(r["product_claim"], BLOCKED)


if __name__ == "__main__":
    unittest.main()
