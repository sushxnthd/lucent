"""Adversarial exact tests for a conditional negative product consequence."""
import unittest
from fractions import Fraction as F
from e002_568_cohort_dropout import (KWON_COHORT_NECESSARY_SPEED_FLOOR as V,
                                     critical_gap, gap_interval, evaluate, report)


class CohortDropout(unittest.TestCase):
    def ev(self, missed, **overrides):
        options = dict(period_min=F(1, 30), period_max=F(1, 30),
                       exposure_min=F(1, 100), exposure_max=F(1, 100), missed=missed)
        options.update(overrides)
        return evaluate(**options)

    def test_exact_floor_not_upper(self):
        self.assertEqual(V, F(24300, 983))
        self.assertEqual(critical_gap(), F(1966, 30375))

    def test_primary_cases(self):
        results = [self.ev(k) for k in range(4)]
        self.assertEqual([r['structural_result'] for r in results], [
            'NO_STRUCTURAL_NOGO_FROM_THIS_COHORT_WITNESS',
            'NO_STRUCTURAL_NOGO_FROM_THIS_COHORT_WITNESS',
            'POSITIVE_DURATION_FEASIBLE_FOR_ALL_ADMISSIBLE_GAPS',
            'POSITIVE_DURATION_FEASIBLE_FOR_ALL_ADMISSIBLE_GAPS'])
        self.assertEqual([F(**{'numerator':r['blind_gap_min_s']['numerator'],
                               'denominator':r['blind_gap_min_s']['denominator']}) for r in results],
                         [F(7, 300), F(17, 300), F(9, 100), F(37, 300)])

    def test_touch_equality_not_certified(self):
        hc = critical_gap()
        r = evaluate(period_min=hc+F(1, 100), period_max=hc+F(1, 100),
                     exposure_min=F(1, 100), exposure_max=F(1, 100), missed=0)
        self.assertEqual(r['structural_result'],
                         'THRESHOLD_TOUCH_FEASIBLE_FOR_ALL_ADMISSIBLE_GAPS')
        self.assertEqual(r['product_decision'], 'ABSTAIN_UNCALIBRATED')

    def test_timing_uncertainty_straddles(self):
        r = self.ev(2, clock_error=F(15, 1000))
        self.assertEqual(r['structural_result'], 'TIMING_INTERVAL_OVERLAPS_CRITICAL_GAP')
        self.assertEqual(r['product_decision'], 'ABSTAIN_UNCALIBRATED')

    def test_robust_positive_with_small_uncertainty(self):
        r = self.ev(2, clock_error=F(1, 1000))
        self.assertEqual(r['structural_result'],
                         'POSITIVE_DURATION_FEASIBLE_FOR_ALL_ADMISSIBLE_GAPS')

    def test_more_missing_never_shortens_gap(self):
        previous = F(0)
        for k in range(12):
            low, _ = gap_interval(period_min=F(1, 30), period_max=F(1, 30),
                                  exposure_min=F(1, 100), exposure_max=F(1, 100),
                                  missed=k)
            self.assertGreaterEqual(low, previous)
            previous = low

    def test_clock_uncertainty_cannot_strengthen_guaranteed_nogo(self):
        for e in (F(0), F(1, 1000), F(5, 1000), F(20, 1000)):
            low, high = gap_interval(period_min=F(1, 30), period_max=F(1, 30),
                                     exposure_min=F(1, 100), exposure_max=F(1, 100),
                                     missed=2, clock_error=e)
            self.assertLessEqual(low, F(9, 100))
            self.assertGreaterEqual(high, F(9, 100))

    def test_threshold_monotonicity(self):
        self.assertGreater(critical_gap(F(1, 10)), critical_gap(F(1, 5)))
        self.assertGreater(critical_gap(F(1, 5)), critical_gap(F(1, 2)))

    def test_invalid_theta(self):
        for theta in (0, 1, -1, 2, True, 'nan', 'inf'):
            with self.assertRaises(ValueError): critical_gap(theta)

    def test_invalid_shutter(self):
        invalid = [dict(period_min=0), dict(exposure_min=0),
                   dict(exposure_max=F(1, 20)), dict(period_max=F(1, 40)),
                   dict(clock_error=-1), dict(missed=-1), dict(missed=1.5),
                   dict(missed=True), dict(period_min='nan')]
        for change in invalid:
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.ev(**{"missed": 0, **change})

    def test_all_cases_always_abstain(self):
        for theta in (F(1, 10), F(1, 5), F(1, 2), F(9, 10)):
            for k in range(10):
                r = self.ev(k, theta=theta)
                self.assertFalse(r['speed_floor_is_safe_upper_bound'])
                self.assertFalse(r['human_closure_observed'])
                self.assertEqual(r['product_decision'], 'ABSTAIN_UNCALIBRATED')
                self.assertEqual(r['release'], 'BLOCKED')

    def test_report_evidence_tier(self):
        r = report()
        self.assertEqual(r['physical_shutter_captures'], 0)
        self.assertEqual(r['independent_human_anatomical_rater_pairs'], 0)
        self.assertEqual(r['certified_continuous_time_human_speed_upper_bounds'], 0)
        self.assertEqual(r['heldout_physical_closure_predictions'], 0)
        self.assertEqual(len(r['cases']), 4)


if __name__ == '__main__':
    unittest.main()
