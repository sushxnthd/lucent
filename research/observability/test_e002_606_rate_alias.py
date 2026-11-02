import unittest
from fractions import Fraction
from e002_606_rate_alias import exact_miss, independent_lattice_miss, three_phase_index_miss, experiment

class TestRateAlias(unittest.TestCase):
    def test_frozen_predictions(self):
        self.assertEqual(exact_miss(100,30,3),Fraction(1,10))
        self.assertEqual(exact_miss(110,30,3),Fraction(2,11))
        self.assertEqual(exact_miss(110,30,2),Fraction(5,11))
        self.assertEqual(exact_miss(110,30,4),0)
    def test_all_frozen_independent(self):
        for h in (100,110):
            for m in (1,2,3,4):
                self.assertEqual(exact_miss(h,30,m),independent_lattice_miss(h,30,m))
    def test_three_phase_is_not_thirty(self):
        self.assertEqual(three_phase_index_miss(3),0)
        self.assertEqual(exact_miss(110,30,3),Fraction(2,11))
    def test_invalid_inputs(self):
        for bad in (0,-1,True,1.0,None,'30',100001):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError): exact_miss(bad,30,1)
                with self.assertRaises(ValueError): independent_lattice_miss(110,bad,1)
    def test_no_release_upgrade(self):
        d=experiment()
        self.assertEqual(d['release'],'BLOCKED')
        self.assertEqual(d['human_closure_events_measured'],0)
        self.assertEqual(len(d['rows']),8)

if __name__=='__main__': unittest.main()
