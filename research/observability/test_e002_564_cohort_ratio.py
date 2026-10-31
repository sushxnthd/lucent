import unittest
from fractions import Fraction
from e002_564_cohort_ratio import ratio_bound, verify_pairwise_witness, report

class TestCohortRatio(unittest.TestCase):
    def test_kwon_exact(self):
        self.assertEqual(ratio_bound('243', '9.83'), Fraction(24300, 983))
    def test_sun_exact(self):
        self.assertEqual(ratio_bound('427', '11.7'), Fraction(4270, 117))
    def test_stronger_than_old_max_aperture_bound(self):
        self.assertGreater(ratio_bound('243', '9.83'), ratio_bound('243', '12.8'))
    def test_sharp_equal_ratios(self):
        bound, witnesses = verify_pairwise_witness([2, 4, 6], [1, 2, 3])
        self.assertEqual(bound, 2)
        self.assertEqual(witnesses, [0, 1, 2])
    def test_unpaired_high_speed_high_aperture(self):
        bound, witnesses = verify_pairwise_witness([10, 1], [1, 10])
        self.assertEqual(bound, 1)
        self.assertEqual(witnesses, [0])
    def test_permutation_of_pairs_changes_individuals_not_cohort_bound(self):
        a, _ = verify_pairwise_witness([10, 1], [1, 10])
        b, _ = verify_pairwise_witness([10, 1], [10, 1])
        self.assertEqual(a, b)
    def test_no_zero_aperture(self):
        with self.assertRaises(ValueError): ratio_bound(100, 0)
        with self.assertRaises(ValueError): verify_pairwise_witness([1, 2], [0, 1])
    def test_no_negative_speed(self):
        with self.assertRaises(ValueError): ratio_bound(-1, 1)
        with self.assertRaises(ValueError): verify_pairwise_witness([-1, 2], [1, 1])
    def test_reject_unpaired_cohort(self):
        with self.assertRaises(ValueError): verify_pairwise_witness([1, 2], [1])
        with self.assertRaises(ValueError): verify_pairwise_witness([], [])
    def test_10pct_scenario(self):
        self.assertEqual(ratio_bound('427', '11.7')*Fraction(9, 11), Fraction(4270, 117)*Fraction(9, 11))
    def test_evidence_tiers_preserved(self):
        r = report()
        self.assertFalse(r['sun1997_primary_numeric_table_verified'])
        self.assertFalse(r['hard_continuous_time_human_upper_bound_certified'])
        self.assertEqual(r['cohorts'][0]['evidence'], 'primary_table')
        self.assertTrue(all(c['evidence']=='secondary_table_transcription' for c in r['cohorts'][1:]))
        self.assertEqual(r['release'], 'BLOCKED')

if __name__ == '__main__': unittest.main()
