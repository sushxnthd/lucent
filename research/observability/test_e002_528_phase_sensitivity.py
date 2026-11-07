import importlib.util
from fractions import Fraction as F
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('phase528',Path(__file__).with_name('e002_528_phase_sensitivity.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class PhaseSensitivityTests(unittest.TestCase):
    def setUp(self):
        self.p,self.e,self.u=F(25,6),F(1),F(1,10)

    def test_frozen_240_4(self):
        r=m.opportunities(self.p,self.e,F(4),self.u)
        self.assertEqual(r['strict_full_uniform_phase'],F(84,125))
        self.assertEqual(r['ideal_positive_overlap_uniform_phase'],F(1))
        self.assertFalse(r['every_phase_strict_full_guaranteed'])

    def test_frozen_240_3(self):
        self.assertEqual(m.opportunities(self.p,self.e,F(3),self.u)['strict_full_uniform_phase'],F(54,125))

    def test_heldout_240_5(self):
        self.assertEqual(m.opportunities(self.p,self.e,F(5),self.u)['strict_full_uniform_phase'],F(114,125))

    def test_heldout_1000_1p2(self):
        self.assertEqual(m.opportunities(F(1),F(1,2),F(6,5))['strict_full_uniform_phase'],F(7,10))

    def test_zero_event(self):
        r=m.opportunities(self.p,self.e,F(0),self.u)
        self.assertEqual(r['strict_full_uniform_phase'],0)
        self.assertEqual(r['ideal_positive_overlap_uniform_phase'],0)

    def test_exact_lower_boundary(self):
        self.assertEqual(m.opportunities(self.p,self.e,self.e+2*self.u,self.u)['strict_full_uniform_phase'],0)

    def test_exact_upper_boundary_not_every_phase(self):
        d=self.p+self.e+2*self.u
        r=m.opportunities(self.p,self.e,d,self.u)
        self.assertEqual(r['strict_full_uniform_phase'],1)
        self.assertFalse(r['every_phase_strict_full_guaranteed'])
        self.assertFalse(m.brute_strict_full(self.p,self.e,d,self.u,self.u))
        self.assertTrue(m.opportunities(self.p,self.e,d+F(1,10000),self.u)['every_phase_strict_full_guaranteed'])

    def test_phase_locked_counterexample(self):
        self.assertFalse(m.brute_strict_full(self.p,self.e,F(4),F(7,2),self.u))
        self.assertTrue(m.brute_strict_full(self.p,self.e,F(4),F(1),self.u))

    def test_grid_240_4(self):
        r=m.phase_grid_count(self.p,self.e,F(4),self.u)
        self.assertLessEqual(abs(r['fraction']-F(84,125)),F(1,10000))

    def test_grid_240_3(self):
        r=m.phase_grid_count(self.p,self.e,F(3),self.u)
        self.assertLessEqual(abs(r['fraction']-F(54,125)),F(1,10000))

    def test_grid_heldout_240_5(self):
        r=m.phase_grid_count(self.p,self.e,F(5),self.u)
        self.assertLessEqual(abs(r['fraction']-F(114,125)),F(1,10000))

    def test_grid_heldout_1000(self):
        r=m.phase_grid_count(F(1),F(1,2),F(6,5))
        self.assertLessEqual(abs(r['fraction']-F(7,10)),F(1,10000))

    def test_three_independent(self):
        self.assertEqual(m.independent_trial_probability(F(84,125),3,phase_independence_attested=True),
                         F(1884204,1953125))
        self.assertIsNone(m.independent_trial_probability(F(84,125),3))

    def test_total_variation(self):
        self.assertEqual(m.bounded_phase_probability(F(84,125),F(1,10)),
                         {'lower':F(143,250),'upper':F(193,250)})
        self.assertEqual(m.bounded_phase_probability(F(1),F(1,10)),
                         {'lower':F(9,10),'upper':F(1)})

    def test_invalid_params(self):
        for params in [(0,1,1,0),(1,1,1,0),(1,2,1,0),(2,1,-1,0),(2,1,1,-1)]:
            with self.subTest(params=params),self.assertRaises(ValueError):
                m.opportunities(*params)

    def test_float_bool_rejected(self):
        for bad in (0.1,True,float('nan'),float('inf')):
            with self.subTest(bad=bad),self.assertRaises(TypeError):
                m.opportunities(2,1,1,bad)

    def test_independence_flag_rejected(self):
        with self.assertRaises(ValueError):
            m.independent_trial_probability(F(1,2),2,phase_independence_attested='yes')
        with self.assertRaises(ValueError):
            m.independent_trial_probability(F(1,2),True,phase_independence_attested=True)

    def test_tv_out_of_range_rejected(self):
        with self.assertRaises(ValueError):
            m.bounded_phase_probability(F(1,2),F(11,10))

    def test_phase_grid_bad_input(self):
        with self.assertRaises(ValueError):
            m.phase_grid_count(self.p,self.e,F(4),self.u,n=0)

    def test_design_never_claims_product(self):
        r=m.opportunities(self.p,self.e,F(4),self.u)
        self.assertEqual(r['product'],'ABSTAIN_UNCALIBRATED')
        self.assertEqual(r['release'],'BLOCKED')

if __name__=='__main__': unittest.main()
