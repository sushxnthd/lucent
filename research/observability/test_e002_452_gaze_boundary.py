"""E002-452 frozen adversarial conditional fixtures; no original human measurements."""
import unittest
from e002_452_gaze_boundary import conditional_boundary, physical_release_gate

BASE = dict(a0_mm=3, a1_mm=3, threshold_mm=2, gap_s=.0095,
            gaze_stratum='upward', behavior='voluntary', velocity_cap_mm_s=200)


class TestGazeBoundary(unittest.TestCase):
    def test_frozen_upward_conditional_exclusion(self):
        r = conditional_boundary(**BASE)
        self.assertAlmostEqual(r['conditional_min_aperture_mm'], 2.05)
        self.assertAlmostEqual(r['dimensionless_travel_ratio'], .95)
        self.assertEqual(r['conditional_outcome'], 'HIDDEN_CROSSING_EXCLUDED_UNDER_ASSUMPTIONS')
        self.assertFalse(r['physical_release_authorized'])

    def test_frozen_downward_conditional_feasibility(self):
        r = conditional_boundary(**{**BASE, 'gaze_stratum':'downward','velocity_cap_mm_s':221})
        self.assertAlmostEqual(r['conditional_min_aperture_mm'], 1.95025)
        self.assertAlmostEqual(r['dimensionless_travel_ratio'], 1.04975)
        self.assertEqual(r['conditional_outcome'], 'HIDDEN_CROSSING_FEASIBLE_UNDER_ASSUMPTIONS')

    def test_exact_boundary_ratio_one(self):
        r = conditional_boundary(**{**BASE,'gap_s':.01})
        self.assertEqual(r['dimensionless_travel_ratio'], 1)
        self.assertEqual(r['conditional_outcome'], 'HIDDEN_CROSSING_FEASIBLE_UNDER_ASSUMPTIONS')

    def test_clock_error_can_reverse_exclusion(self):
        r = conditional_boundary(**{**BASE,'clock_uncertainty_s':.0003})
        self.assertEqual(r['conditional_outcome'], 'HIDDEN_CROSSING_FEASIBLE_UNDER_ASSUMPTIONS')

    def test_shutter_average_refused(self):
        with self.assertRaises(ValueError):
            conditional_boundary(**{**BASE,'aperture_source':'shutter_average'})

    def test_unmeasured_gaze_refused(self):
        with self.assertRaises(ValueError):
            conditional_boundary(**{**BASE,'gaze_stratum':'unknown'})

    def test_unmeasured_behavior_refused(self):
        with self.assertRaises(ValueError):
            conditional_boundary(**{**BASE,'behavior':'unknown'})

    def test_claimed_human_evidence_refused(self):
        with self.assertRaises(ValueError):
            conditional_boundary(**{**BASE,'evidence_tier':'human_certified'})

    def test_inconsistent_endpoints_refused(self):
        with self.assertRaises(ValueError):
            conditional_boundary(**{**BASE,'a1_mm':9})

    def test_nonfinite_and_negative_refused(self):
        for key,val in [('a0_mm',float('nan')),('velocity_cap_mm_s',float('inf')),
                        ('gap_s',-1),('clock_uncertainty_s',-1)]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                conditional_boundary(**{**BASE,key:val})

    def test_endpoint_already_closed(self):
        r = conditional_boundary(**{**BASE,'a0_mm':2,'a1_mm':2})
        self.assertEqual(r['conditional_outcome'],'THRESHOLD_ALREADY_OBSERVED_AT_ENDPOINT')

    def test_untrusted_release_attestation_never_works(self):
        for claimed in ({}, {'all_evidence_valid':True,'independent_review':True}, None):
            r = physical_release_gate(claimed)
            self.assertEqual(r['decision'],'ABSTAIN_UNCALIBRATED')
            self.assertFalse(r['physical_release_authorized'])


if __name__ == '__main__':
    unittest.main()
