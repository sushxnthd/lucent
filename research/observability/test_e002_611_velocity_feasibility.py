import unittest
from fractions import Fraction as F
from e002_611_velocity_feasibility import (threshold_mean,gate_possible,illustrative_gate_passes,boxcar_margin,rows)

class VelocityFeasibilityTest(unittest.TestCase):
    def test_units(self):
        self.assertEqual(threshold_mean(400,F('7.4'),30),F(1,5)+F(400,444))
    def test_strict_equality(self):
        v=F(2)*F('9.8')*30*(1-F('0.2'))
        self.assertEqual(threshold_mean(v,F('9.8'),30),1)
        self.assertFalse(gate_possible(v,F('9.8'),30))
    def test_30hz_small_aperture_400(self):
        self.assertFalse(gate_possible(400,F('7.4'),30))
        self.assertTrue(gate_possible(400,F('7.4'),60))
    def test_literature_scenarios(self):
        self.assertFalse(illustrative_gate_passes(243,F('9.8'),30,F('0.5')))
        self.assertTrue(illustrative_gate_passes(93,F('9.8'),30,F('0.5')))
    def test_monotonicity(self):
        for a in (F('7.4'),F('9.8')):
            for f in (30,60):
                self.assertGreater(threshold_mean(243,a,f),threshold_mean(93,a,f))
                self.assertGreater(threshold_mean(243,a,f),threshold_mean(243,a,2*f))
        self.assertGreater(threshold_mean(243,F('7.4'),30),threshold_mean(243,F('9.8'),30))
        self.assertFalse(illustrative_gate_passes(243,F('9.8'),30,F('0.5')))
        self.assertTrue(illustrative_gate_passes(243,F('9.8'),30,F('0.9')))
    def test_exposure_invariance_idealized_only(self):
        for f in (30,60,120):
            period=F(1000,f)
            self.assertEqual(boxcar_margin(243,F('9.8'),f,F(2),F('0.5')),
                             boxcar_margin(243,F('9.8'),f,F(4,5)*period,F('0.5')))
    def test_invalid_domains(self):
        for bad in ((100,0,30),(100,10,0),(-1,10,30)):
            with self.assertRaises(ValueError):threshold_mean(*bad)
        with self.assertRaises(ValueError):boxcar_margin(100,10,30,40,F('0.5'))
        with self.assertRaises(ValueError):illustrative_gate_passes(100,10,30,F('1.1'))
    def test_grid(self):
        rr=list(rows());self.assertEqual(len(rr),72)
        self.assertTrue(all(r['product']=='ABSTAIN_UNCALIBRATED' and r['release']=='BLOCKED' for r in rr))

if __name__=='__main__':unittest.main()
