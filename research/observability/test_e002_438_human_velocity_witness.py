import unittest

from e002_438_human_velocity_witness import (
    WitnessError, published_cap_audit, calibrated_pair_witness,
    equal_endpoint_scenario, demonstration, NUISANCES, PRODUCT)


def fixture(**kw):
    base = dict(trace_id='private_test', y0_mm=2.0, y1_mm=3.2,
                t0_s=0, t1_s=.005, aperture_error_mm=.01,
                clock_error_s=.0001, candidate_cap_mm_s=120,
                physical_scale_attested=True, sensor_timing_attested=True,
                nuisance_flags={k: False for k in NUISANCES},
                external_calibration_reference='fixture-not-real')
    base.update(kw)
    return base


class TestWitness(unittest.TestCase):
    def test_published_mean_rejects_low_cap(self):
        self.assertEqual(published_cap_audit(120)['decision'], 'INCOMPATIBLE_WITH_PUBLISHED_PEAK_MEAN')

    def test_mean_does_not_certify_higher_cap(self):
        x = published_cap_audit(300)
        self.assertEqual(x['decision'], 'NOT_FALSIFIED_BY_THIS_AGGREGATE')
        self.assertFalse(x['physical_certificate_authorized'])

    def test_metric_mismatch_abstains(self):
        self.assertEqual(published_cap_audit(100, 'average_opening_speed_mm_s')['decision'], 'UNRESOLVED_METRIC_MISMATCH')

    def test_reporting_rounding(self):
        self.assertEqual(published_cap_audit(242.49)['decision'], 'INCOMPATIBLE_WITH_PUBLISHED_PEAK_MEAN')
        self.assertEqual(published_cap_audit(242.5)['decision'], 'NOT_FALSIFIED_BY_THIS_AGGREGATE')

    def test_necessary_speed_witness(self):
        x = calibrated_pair_witness(fixture())
        self.assertAlmostEqual(x['necessary_speed_lower_mm_s'], (1.2-.02)/(.005+.0002))
        self.assertEqual(x['decision'], 'CONDITIONAL_CAP_FALSIFIED')

    def test_pair_cannot_validate_cap(self):
        x = calibrated_pair_witness(fixture(candidate_cap_mm_s=500))
        self.assertEqual(x['decision'], 'CAP_NOT_FALSIFIED_BY_PAIR')
        self.assertFalse(x['physical_certificate_authorized'])

    def test_independent_linear_oracle(self):
        # Physical x(t)=2+250t, t in [0,0.005]. True speed 250.
        # Opposite endpoint errors shrink observed difference to 1.23.
        x = calibrated_pair_witness(fixture(y0_mm=2.01, y1_mm=3.24,
                                             clock_error_s=0, candidate_cap_mm_s=240))
        self.assertAlmostEqual(x['necessary_speed_lower_mm_s'], 242.0)
        self.assertEqual(x['decision'], 'CONDITIONAL_CAP_FALSIFIED')

    def test_nuisance_abstention(self):
        for k in NUISANCES:
            flags = {v: False for v in NUISANCES}
            flags[k] = True
            x = calibrated_pair_witness(fixture(nuisance_flags=flags))
            self.assertEqual(x['decision'], PRODUCT)
            self.assertIsNone(x['necessary_speed_lower_mm_s'])

    def test_unattested_abstains(self):
        self.assertEqual(calibrated_pair_witness(fixture(sensor_timing_attested=False))['decision'], PRODUCT)

    def test_invalid_inputs(self):
        for change in [dict(y0_mm=float('nan')), dict(y1_mm=True),
                       dict(t1_s=.0001), dict(candidate_cap_mm_s=0),
                       dict(aperture_error_mm=-1), dict(clock_error_s=-1),
                       dict(nuisance_flags={'blur': False}),
                       dict(external_calibration_reference='')]:
            with self.subTest(change=change), self.assertRaises(WitnessError):
                calibrated_pair_witness(fixture(**change))

    def test_30fps_margin(self):
        x = equal_endpoint_scenario(6, 2, 30, 243)
        self.assertAlmostEqual(x['conditional_lower_mm'], 1.95)
        self.assertEqual(x['scenario_decision'], 'UNRESOLVED')
        self.assertFalse(x['physical_certificate_authorized'])

    def test_60fps_margin_and_nuisance_monotonicity(self):
        x = equal_endpoint_scenario(6, 2, 60, 243)
        self.assertAlmostEqual(x['conditional_lower_mm'], 3.975)
        self.assertEqual(x['scenario_decision'], 'CONDITIONAL_EXCLUSION_IF_PREMISES_TRUE')
        for e, d in ((.1, 0), (0, .001), (.1, .001)):
            self.assertLessEqual(equal_endpoint_scenario(6, 2, 60, 243, e, d)['conditional_lower_mm'], x['conditional_lower_mm'])

    def test_never_certifies(self):
        d = demonstration()
        self.assertEqual(d['product'], PRODUCT)
        for x in d['equal_endpoint_scenarios']+d['published_human_aggregate_audit']:
            self.assertFalse(x['physical_certificate_authorized'])


if __name__ == '__main__':
    unittest.main()
