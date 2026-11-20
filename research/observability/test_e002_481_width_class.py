"""Independent adversarial tests for E002-481, no physical validation implied."""
import unittest
from fractions import Fraction as F
import e002_481_width_class as m

class TestWidthClass(unittest.TestCase):
    def test_pointwise_core_zero(self):
        self.assertEqual(max(F(0),m.W-2*m.U),0)
    def test_narrow_no_guarantee(self):
        self.assertEqual(m.guaranteed_overlap(island_width=F(5,10000)),0)
        self.assertIsNone(m.min_phase_count(F(5,10000)))
    def test_geometric_but_not_detectable(self):
        l=F(3,1000)
        self.assertEqual(m.guaranteed_overlap(island_width=l),F(1,2000))
        self.assertIsNone(m.min_phase_count(l))
    def test_detectable_despite_empty_core(self):
        l=F(6,1000)
        self.assertEqual(m.guaranteed_overlap(island_width=l),F(1,500))
        self.assertTrue(m.robust_contrast(2816,l)['detectable_strict'])
    def test_phase_boundary(self):
        l=F(6,1000)
        self.assertEqual(m.min_phase_count(l),2816)
        self.assertFalse(m.robust_contrast(2815,l)['detectable_strict'])
        self.assertFalse(m.robust_contrast(668,l)['detectable_strict'])
    def test_exact_width_boundary(self):
        l=F(113,25000)
        self.assertEqual(l,2*(m.U+(m.THETA+m.EPS)*m.W/m.A)-m.W)
        self.assertIsNone(m.min_phase_count(l))
        self.assertIsNotNone(m.min_phase_count(l+F(1,1000000)))
    def test_brute_endpoint_adversary(self):
        for n in (17, 71, 668, 2815, 2816):
            self.assertEqual(m.brute_worst_phase(n,m.W),m.guaranteed_grid_overlap(n,island_width=m.W))
    def test_uncertainty_monotone(self):
        self.assertGreaterEqual(m.guaranteed_overlap(uncertainty=F(3,1000)),m.guaranteed_overlap())
    def test_width_monotone(self):
        self.assertGreaterEqual(m.guaranteed_overlap(island_width=F(7,1000)),m.guaranteed_overlap())
    def test_phase_monotone(self):
        self.assertGreaterEqual(m.guaranteed_grid_overlap(2816),m.guaranteed_grid_overlap(2815))
    def test_noise_amplitude_monotone(self):
        l=m.W
        self.assertTrue(m.robust_contrast(2816,l)['detectable_strict'])
        self.assertFalse(m.robust_contrast(2816,l,noise=F(1,20))['detectable_strict'])
        self.assertFalse(m.robust_contrast(2816,l,amplitude=F(1,10))['detectable_strict'])
    def test_period_wrap(self):
        self.assertEqual(m.brute_worst_phase(2816,m.W),m.guaranteed_grid_overlap(2816,island_width=m.W))
    def test_invalid_inputs(self):
        for bad in (float('nan'),float('inf'),-1,True):
            with self.assertRaises(ValueError):
                m.guaranteed_overlap(uncertainty=bad)
        with self.assertRaises(ValueError):m.min_phase_count(m.W,period=F(1,100))
        with self.assertRaises(ValueError):m.guaranteed_grid_overlap(0)
    def test_no_physical_release(self):
        self.assertEqual(m.experiment()['physical_claim'],m.ABSTAIN)
        self.assertEqual(m.experiment()['physical_shutter_acquisitions'],0)

if __name__=='__main__':unittest.main()
