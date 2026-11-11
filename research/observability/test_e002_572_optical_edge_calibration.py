"""E002-572 preregistered synthetic oracle and adversarial instrument controls."""
import unittest
from dataclasses import replace

from e002_572_optical_edge_calibration import (
    CalibrationError, Edge, Instrument, calibrate, edge_start_interval,
    heldout_test, synthetic_fixture,
)


class OpticalEdgeCalibrationTest(unittest.TestCase):
    def setUp(self):
        self.inst, self.training, self.clean, self.delayed = synthetic_fixture()

    def test_feasible_true_clock(self):
        p = calibrate(self.training, self.inst)
        self.assertTrue(p)
        # Independent oracle: the true clock lies in every raw interval.
        for e in self.training:
            lo, hi = edge_start_interval(e, self.inst)
            self.assertLessEqual(lo, .012+1.000020*e.camera_time_s)
            self.assertGreaterEqual(hi, .012+1.000020*e.camera_time_s)

    def test_clean_heldout(self):
        p = calibrate(self.training, self.inst)
        self.assertEqual(heldout_test(p,self.clean,self.inst)["decision"], "CONSISTENT")

    def test_delayed_heldout(self):
        p = calibrate(self.training, self.inst)
        out = heldout_test(p,self.delayed,self.inst)
        self.assertEqual(out["decision"], "CONTRADICTION")
        self.assertEqual(out["physiological_claim"], "ABSTAIN_UNCALIBRATED")

    def test_training_corruption_rejected(self):
        bad = list(self.training)
        bad[2] = replace(bad[2], reference_edge_s=bad[2].reference_edge_s+.010)
        with self.assertRaisesRegex(CalibrationError,"CALIBRATION_REJECTED"):
            calibrate(bad,self.inst)

    def test_non_affine_drift_rejected(self):
        bad = list(self.training)
        bad[-1] = replace(bad[-1], reference_edge_s=bad[-1].reference_edge_s-.020)
        with self.assertRaisesRegex(CalibrationError,"CALIBRATION_REJECTED"):
            calibrate(bad,self.inst)

    def test_no_single_edge(self):
        with self.assertRaisesRegex(CalibrationError,"INSUFFICIENT"):
            calibrate(self.training[:1],self.inst)

    def test_distinct_timestamps_required(self):
        with self.assertRaisesRegex(CalibrationError,"DISTINCT"):
            calibrate([self.training[0]]*3,self.inst)

    def test_saturation_rejected(self):
        with self.assertRaisesRegex(CalibrationError,"INVALID_EDGE"):
            edge_start_interval(replace(self.clean,post_edge_fraction=1),self.inst)

    def test_fraction_uncertainty_cannot_span_plateau(self):
        with self.assertRaisesRegex(CalibrationError,"INVALID_EDGE"):
            edge_start_interval(replace(self.clean,fraction_uncertainty=.6),self.inst)

    def test_missing_photodiode_uncertainty_rejected(self):
        with self.assertRaisesRegex(CalibrationError,"INVALID_EDGE"):
            edge_start_interval(replace(self.clean,edge_uncertainty_s=0),self.inst)

    def test_negative_shutter_rejected(self):
        with self.assertRaisesRegex(CalibrationError,"INVALID_INSTRUMENT"):
            calibrate(self.training,replace(self.inst,shutter_min_s=-.001))

    def test_boolean_and_nan_rejected(self):
        with self.assertRaisesRegex(CalibrationError,"INVALID_"):
            edge_start_interval(replace(self.clean,camera_time_s=True),self.inst)
        with self.assertRaisesRegex(CalibrationError,"INVALID_"):
            edge_start_interval(replace(self.clean,reference_edge_s=float("nan")),self.inst)

    def test_uncertainty_widening_cannot_invent_contradiction(self):
        p = calibrate(self.training,self.inst)
        wide = replace(self.clean,edge_uncertainty_s=.002)
        self.assertEqual(heldout_test(p,wide,self.inst)["decision"],"CONSISTENT")

    def test_no_physio_promotion(self):
        p = calibrate(self.training,self.inst)
        for e in (self.clean,self.delayed):
            r = heldout_test(p,e,self.inst)
            self.assertEqual(r["release"],"BLOCKED")
            self.assertEqual(r["physiological_claim"],"ABSTAIN_UNCALIBRATED")


if __name__ == "__main__":
    unittest.main()
