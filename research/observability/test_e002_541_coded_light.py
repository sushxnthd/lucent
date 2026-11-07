import unittest
from e002_541_coded_light import light, simulate, estimate, run, TRUTH, exposure_average


class CodedLightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.coded = light('coded')
        cls.results = run()

    def test_frozen_noiseless_identifies(self):
        x = self.results['clean']
        self.assertEqual(x['decision'], 'SYNTHETIC_IDENTIFIED')
        self.assertEqual(x['best'], list(TRUTH))

    def test_frozen_noisy_identifies(self):
        x = self.results['noisy']
        self.assertEqual(x['decision'], 'SYNTHETIC_IDENTIFIED')
        self.assertEqual(x['best'], list(TRUTH))

    def test_periodic_alias_exact(self):
        self.assertTrue(self.results['periodic_phase_7_vs_11_exactly_equal'])
        self.assertEqual(self.results['periodic']['decision'], 'ABSTAIN')

    def test_wrong_row_model_abstains(self):
        self.assertEqual(self.results['wrong_rows']['decision'], 'ABSTAIN')

    def test_clock_drift_abstains(self):
        self.assertEqual(self.results['wrong_clock']['decision'], 'ABSTAIN')

    def test_constant_abstains(self):
        self.assertEqual(self.results['constant']['decision'], 'ABSTAIN')

    def test_missing_abstains(self):
        self.assertEqual(self.results['missing']['decision'], 'ABSTAIN')

    def test_saturation_abstains(self):
        self.assertEqual(self.results['saturated']['decision'], 'ABSTAIN')

    def test_nuisance_row_gain_abstains(self):
        self.assertEqual(self.results['row_gain']['decision'], 'ABSTAIN')

    def test_jitter_abstains(self):
        self.assertEqual(self.results['phase_jitter']['decision'], 'ABSTAIN')

    def test_exploratory_gamma_false_reassurance_preserved(self):
        self.assertEqual(self.results['gamma']['decision'], 'SYNTHETIC_IDENTIFIED')
        self.assertGreater(self.results['gamma']['rmse'], 0.001)

    def test_exploratory_temporal_blur_false_reassurance_preserved(self):
        self.assertEqual(self.results['temporal_blur']['decision'], 'SYNTHETIC_IDENTIFIED')
        self.assertGreater(self.results['temporal_blur']['rmse'], 0.01)

    def test_frozen_40_heldout_seeds(self):
        self.assertEqual(self.results['sweep']['correct_identified'], 40)
        self.assertEqual(self.results['sweep']['failed_seeds'], [])

    def test_duplicate_sample_identity(self):
        s = simulate(self.coded)
        self.assertEqual(estimate(self.coded, s + [s[0]])['reason'], 'invalid_sample_identity')

    def test_unknown_frame_identity(self):
        s = simulate(self.coded)
        s[0] = (99, s[0][1], s[0][2])
        self.assertEqual(estimate(self.coded, s)['reason'], 'invalid_sample_identity')

    def test_nonfinite_sensor(self):
        s = simulate(self.coded)
        s[0] = (s[0][0], s[0][1], float('nan'))
        self.assertEqual(estimate(self.coded, s)['reason'], 'invalid_sample_identity')

    def test_exposure_out_of_signal(self):
        with self.assertRaises(ValueError):
            exposure_average(self.coded, 799, 8)

    def test_no_human_or_product_certification(self):
        self.assertEqual(self.results['evidence_tier'], 'SYNTHETIC_ONLY')
        self.assertEqual(self.results['human_anatomical_ratings'], 0)
        self.assertFalse(self.results['physical_validation'])
        self.assertEqual(self.results['product'], 'ABSTAIN_UNCALIBRATED')


if __name__ == '__main__':
    unittest.main()
