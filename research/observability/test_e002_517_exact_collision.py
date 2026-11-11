"""E002-517 frozen ideal-model falsification controls (not human evidence)."""
import importlib.util
from fractions import Fraction
from pathlib import Path
import unittest

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location(
    'e002_517_exact_collision', HERE / 'e002_517_exact_collision.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class ExactCollisionFalsification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = m.run()
        cls.w = cls.report['two_world_10ms_witness']

    def test_frozen_seeds_and_exact_counts(self):
        self.assertEqual(self.report['seeds'], [211, 223, 227, 229, 233])
        self.assertEqual(
            [x['exact_same_duration_distant_collision_pairs']
             for x in self.report['per_seed']], [5, 3, 6, 9, 4])
        self.assertEqual(self.report['collision_pairs_total'], 27)
        self.assertEqual(self.report['primary_prediction'], 'PASS')

    def test_preserve_negative_duration_controls(self):
        by_seed = {x['seed']: x['by_duration']
                   for x in self.report['per_seed']}
        self.assertEqual(by_seed[223]['10']['collision_pairs'], 0)
        self.assertEqual(by_seed[227]['10']['collision_pairs'], 0)
        self.assertEqual(by_seed[233]['10']['collision_pairs'], 0)

    def test_exact_two_world_exposure_witness(self):
        self.assertEqual(self.w['seed'], 211)
        self.assertEqual(self.w['left_exposure_ms'], [924, 934])
        self.assertEqual(self.w['world_a_right_exposure_ms'], [954, 964])
        self.assertEqual(self.w['world_b_right_exposure_ms'], [1233, 1243])
        self.assertEqual(self.w['world_a_true_blind_gap_ms'], 20)
        self.assertEqual(self.w['world_b_true_blind_gap_ms'], 299)
        self.assertTrue(self.w['world_a_within_budget'])
        self.assertFalse(self.w['world_b_within_budget'])

    def test_independent_direct_sum_replay(self):
        # Direct integer sums, independent of prefix-sum signature implementation.
        code = m.optical_code(211)
        a = tuple(Fraction(sum(ch[954:964]), 10) for ch in code)
        b = tuple(Fraction(sum(ch[1233:1243]), 10) for ch in code)
        self.assertEqual(a, b)
        self.assertEqual(
            [str(x) for x in a],
            ['7/10', '1/2', '2/5', '2/5', '3/5', '3/5', '2/5', '3/5'])

    def test_same_duration_nonoverlap_and_exact_not_approximate(self):
        self.assertEqual(964 - 954, 1243 - 1233)
        self.assertLess(964, 1233)
        code = m.optical_code(211)
        x = [Fraction(sum(ch[954:964]), 10) for ch in code]
        x[0] += Fraction(1, 1000)
        y = [Fraction(sum(ch[1233:1243]), 10) for ch in code]
        self.assertNotEqual(x, y)

    def test_existing_set_valued_inverse_is_conservative(self):
        self.assertEqual(self.w['inverse_feasible_right_intervals'], 2)
        self.assertEqual(self.w['conservative_gap_upper_ms'], 299)
        self.assertTrue(self.w['inverse_never_underbounds_either_world'])

    def test_no_physical_or_human_clearance(self):
        self.assertEqual(self.report['human_labels'], 0)
        self.assertFalse(self.report['physical_camera_verified'])
        self.assertFalse(self.report['certified_speed_limit'])
        self.assertEqual(self.report['product'], 'ABSTAIN_UNCALIBRATED')
        self.assertEqual(self.report['release'], 'BLOCKED')


if __name__ == '__main__':
    unittest.main()
