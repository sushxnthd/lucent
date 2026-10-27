"""E002-480: adversarial regression, positive controls, and fail-closed claims."""
import unittest
from e002_480_phase_dither import (
    T, W, U, CENTER, ISLAND_WIDTH, AMPLITUDE, ABSTAIN,
    adversarial_grid, avoid_island, response, grid, coverage, periodic_overlap,
    even_starts, core_width, threshold_ceiling, experiment,
)

class PhaseDitherTests(unittest.TestCase):
    def test_all_dither_grids_miss_with_adversarial_timing(self):
        for n in (1,2,4,8):
            result=adversarial_grid(n)
            self.assertTrue(result["adversarial_timing_schedule_exists"],result)
            self.assertEqual(result["unavoidable_island_intersections"],0)
            self.assertEqual(result["max_optical_response_difference"],0)

    def test_two_periods_and_wrap(self):
        for nominal in (CENTER,CENTER+T,CENTER+2*T):
            delta=avoid_island(nominal)
            self.assertIsNotNone(delta)
            self.assertAlmostEqual(response(nominal+delta,True),response(nominal+delta,False),places=11)

    def test_island_is_real_in_constructed_world(self):
        t=CENTER-W/2
        self.assertGreater(response(t,True)-response(t,False),0)

    def test_robust_core_boundary(self):
        self.assertEqual(core_width(W,U),0)
        self.assertEqual(core_width(W,W/2),0)
        self.assertEqual(core_width(W,0),W)

    def test_eightfold_nominal_dither_not_guaranteed(self):
        r=coverage(grid(8),W,U)
        self.assertFalse(r["guaranteed_full_phase_coverage"])
        self.assertEqual(r["covered_fraction"],0)

    def test_1042_even_phases_cover_with_improved_clock(self):
        self.assertTrue(coverage(even_starts(1042),W,.001)["guaranteed_full_phase_coverage"])

    def test_1041_even_phases_leave_gap(self):
        r=coverage(even_starts(1041),W,.001)
        self.assertFalse(r["guaranteed_full_phase_coverage"])
        self.assertGreater(r["maximum_uncovered_gap_ms"],0)

    def test_nonuniform_phase_gap(self):
        self.assertFalse(coverage([0,.001,.002],W,.001)["guaranteed_full_phase_coverage"])

    def test_circular_wrap_positive(self):
        self.assertTrue(coverage([0,T/2],T/2+.02,.001)["guaranteed_full_phase_coverage"])

    def test_detection_ceiling_kills_narrow_island(self):
        r=threshold_ceiling()
        self.assertAlmostEqual(r["max_noise_free_contrast"],1/60,places=12)
        self.assertFalse(r["threshold_can_be_crossed"])
        self.assertGreater(r["minimum_width_for_worst_case_detection_ms"],ISLAND_WIDTH)

    def test_wider_island_positive_control(self):
        self.assertTrue(threshold_ceiling(.2,.003,W)["threshold_can_be_crossed"])

    def test_periodic_model(self):
        for t in (.8,CENTER,3.5):
            self.assertAlmostEqual(response(t,True),response(t+T,True),places=11)

    def test_invalid_inputs_fail_closed(self):
        for v in (float("nan"),float("inf"),-.001):
            with self.assertRaises(ValueError):
                core_width(W,v)
        with self.assertRaises(ValueError):
            coverage([],W,.001)
        with self.assertRaises(ValueError):
            threshold_ceiling(.2,.001,0)
        with self.assertRaises(ValueError):
            adversarial_grid(0)

    def test_exploratory_shared_clock_offset_is_different(self):
        # Post-freeze control. The primary counterexample permits independent
        # pulse errors; it must not be generalized to a single common offset.
        for delta in (-U, 0, U):
            hits=sum(periodic_overlap(t+delta,t+delta+W)>1e-13 for t in grid(8))
            self.assertGreater(hits,0)

    def test_aggregate_never_authorizes_product(self):
        r=experiment()
        self.assertEqual(r["product_claim"],ABSTAIN)
        self.assertFalse(r["physical_release_authorized"])
        self.assertEqual(r["physical_shutter_acquisitions"],0)
        self.assertEqual(r["new_anatomical_human_sequences"],0)
        self.assertTrue(r["minimum_even_phase_count_covers"])
        self.assertFalse(r["one_fewer_even_phases_covers"])

if __name__=="__main__":
    unittest.main()
