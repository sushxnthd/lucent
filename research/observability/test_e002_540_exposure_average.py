import unittest
from fractions import Fraction as F
from math import isclose
from e002_540_exposure_average import edge_min_from_average, symmetric_hidden_floor, frozen_witness

class TestExposureAverage(unittest.TestCase):
    def test_exact_exposure_means(self):
        r=frozen_witness()
        self.assertEqual(r['mean_first'],'9/10')
        self.assertEqual(r['mean_second'],'9/10')
    def test_exact_hidden_closure(self):
        r=frozen_witness()
        self.assertEqual(r['hidden_minimum'],'7/40')
        self.assertEqual(r['closed_dwell_seconds'],'1/900')
    def test_false_pointwise_exclusion(self):
        r=frozen_witness()
        self.assertEqual(r['invalid_pointwise_floor'],'3/8')
        self.assertGreater(F(r['invalid_pointwise_floor']),F(1,5))
        self.assertLess(F(r['hidden_minimum']),F(1,5))
    def test_speed_bound(self):
        r=frozen_witness()
        self.assertEqual(max(abs(F(s)) for s in r['slopes']),F(45))
    def test_physical_range(self):
        r=frozen_witness()
        self.assertTrue(all(F(0)<=F(a)<=F(1) for _,a in r['vertex_times_apertures']))
    def test_exposure_edge(self):
        self.assertTrue(isclose(edge_min_from_average(.9,45,.01),.7,abs_tol=1e-12))
    def test_unseen_speed_40_excludes(self):
        r=symmetric_hidden_floor(.9,.2,40,.01,1/30)
        self.assertTrue(r['conditional_exclusion'])
        self.assertGreater(r['hidden_floor'],.25)
    def test_speed_45_does_not_exclude(self):
        r=symmetric_hidden_floor(.9,.2,45,.01,1/30)
        self.assertFalse(r['conditional_exclusion'])
        self.assertTrue(isclose(r['hidden_floor'],.175,abs_tol=1e-12))
    def test_zero_exposure_is_pointwise(self):
        self.assertEqual(edge_min_from_average(.9,45,0),.9)
    def test_zero_speed_constant(self):
        self.assertEqual(edge_min_from_average(.9,0,.01),.9)
    def test_saturation_zero_edge(self):
        self.assertEqual(edge_min_from_average(.1,100,.02),0)
    def test_unsaturated_case(self):
        self.assertTrue(isclose(edge_min_from_average(.6,20,.01),.5,abs_tol=1e-12))
    def test_invalid_average(self):
        with self.assertRaises(ValueError): edge_min_from_average(1.1,45,.01)
    def test_invalid_exposure(self):
        with self.assertRaises(ValueError): edge_min_from_average(.9,45,-.01)
    def test_invalid_speed(self):
        with self.assertRaises(ValueError): edge_min_from_average(.9,-45,.01)
    def test_invalid_threshold(self):
        with self.assertRaises(ValueError): symmetric_hidden_floor(.9,.9,45,.01,1/30)
    def test_overlapping_exposures_rejected(self):
        with self.assertRaises(ValueError): symmetric_hidden_floor(.9,.2,45,.04,1/30)
    def test_model_never_claims_human_certification(self):
        self.assertIn('NOT_HUMAN_CERTIFIED',symmetric_hidden_floor(.9,.2,40,.01,1/30)['evidence'])

    def test_exploratory_cap_aware_reversal_vs_unbounded_extrapolation(self):
        # Post-hoc distinction from E002-421's interior-headroom theorem.
        # E002-421's unbounded formula is INAPPLICABLE to this saturated case.
        b, V, E, T, c = .9, 45, .01, 1/30, .16
        invalid_extrapolated_floor = b - V*T/2
        self.assertLess(invalid_extrapolated_floor, c)
        cap_aware = symmetric_hidden_floor(b,c,V,E,T)
        self.assertTrue(cap_aware["conditional_exclusion"])
        self.assertGreater(cap_aware["hidden_floor"],c)

if __name__=='__main__': unittest.main()
