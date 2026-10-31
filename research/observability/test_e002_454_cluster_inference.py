"""Independent combinatorial and adversarial controls for E002-454."""
import copy
import math
import unittest
from e002_454_cluster_inference import analyze, zero_failure_upper


FIXTURE = {
    'source': {'sha256_verified': True},
    'rows': {'train_subjects': 12, 'holdout_subjects': 5, 'participants': 17,
             'train': 1657, 'holdout': 649, 'valid': 2306},
    'tests': {'pooled_train_max': {'denominator': 649, 'count': 0,
                                  'holdout_subjects_with_exceedance': 0, 'abstained': 0}},
    'train': {'max': 567.1039281430776},
    'holdout': {'max': 427.05309798933393},
    'physical_release_authorized': False,
    'product_claim': 'ABSTAIN_UNCALIBRATED',
}


class TestClusterInference(unittest.TestCase):
    def test_exact_exchangeability_enumeration(self):
        # Enumerate all 17 equally likely placements of a unique global maximum.
        successes = sum(1 for global_max_position in range(17)
                        if global_max_position < 12)
        self.assertEqual(successes, 12)
        self.assertAlmostEqual(analyze(FIXTURE)['null_no_exceedance_probability_if_exchangeable_unique_max'],
                               successes / 17)

    def test_exact_binomial_tail_inversion(self):
        upper = analyze(FIXTURE)['one_sided_95pct_upper_participant_session_failure_if_iid_people']
        self.assertAlmostEqual((1 - upper) ** 5, 0.05, places=13)

    def test_blink_iid_understates_uncertainty(self):
        result = analyze(FIXTURE)
        self.assertGreater(result['one_sided_95pct_upper_participant_session_failure_if_iid_people'], .45)
        self.assertLess(result['invalid_blink_iid_95pct_upper_for_comparison_only'], .005)
        self.assertGreater(result['overconfidence_ratio_participant_vs_blink_iid'], 90)
        self.assertTrue(result['preregistered_kill_triggered'])
        self.assertFalse(result['physical_release_authorized'])

    def test_invalid_counts(self):
        for field, value in [('holdout_subjects', 0), ('train_subjects', -1),
                             ('holdout', 0), ('holdout', 649.1), ('participants', 18),
                             ('valid', 2307)]:
            x = copy.deepcopy(FIXTURE)
            x['rows'][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                analyze(x)

    def test_bad_provenance(self):
        x = copy.deepcopy(FIXTURE)
        x['source']['sha256_verified'] = False
        with self.assertRaises(ValueError):
            analyze(x)

    def test_nonzero_exceedance(self):
        x = copy.deepcopy(FIXTURE)
        x['tests']['pooled_train_max']['count'] = 1
        with self.assertRaises(ValueError):
            analyze(x)

    def test_incomplete_holdout(self):
        x = copy.deepcopy(FIXTURE)
        x['tests']['pooled_train_max']['denominator'] = 648
        with self.assertRaises(ValueError):
            analyze(x)

    def test_nonfinite_max(self):
        x = copy.deepcopy(FIXTURE)
        x['train']['max'] = float('nan')
        with self.assertRaises(ValueError):
            analyze(x)

    def test_holdout_max_above_train(self):
        x = copy.deepcopy(FIXTURE)
        x['holdout']['max'] = 568.0
        with self.assertRaises(ValueError):
            analyze(x)

    def test_release_gate(self):
        x = copy.deepcopy(FIXTURE)
        x['physical_release_authorized'] = True
        with self.assertRaises(ValueError):
            analyze(x)

    def test_confidence_input_rejection(self):
        for n in (0, -1, 2.5, True):
            with self.subTest(n=n), self.assertRaises(ValueError):
                zero_failure_upper(n)
        for alpha in (0, 1, float('nan')):
            with self.subTest(alpha=alpha), self.assertRaises(ValueError):
                zero_failure_upper(5, alpha)


if __name__ == '__main__':
    unittest.main()
