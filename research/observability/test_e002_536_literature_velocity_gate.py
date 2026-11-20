from fractions import Fraction as Q
import unittest
from e002_536_literature_velocity_gate import REQUIRED, evaluate, frozen_case, run_frozen


class LiteratureVelocityGateTest(unittest.TestCase):
    def test_exact_frozen_reversal(self):
        result = run_frozen()
        self.assertEqual(result['30fps']['dimensionless_gap_ratio'], '7857/15680')
        self.assertEqual(result['15fps']['dimensionless_gap_ratio'], '15957/15680')
        self.assertEqual(result['30fps']['geometric_condition_if_hard_bound'], 'NO_HIDDEN_CROSSING')
        self.assertEqual(result['15fps']['geometric_condition_if_hard_bound'], 'HIDDEN_CROSSING_NOT_EXCLUDED')
        for x in result.values():
            self.assertEqual(x['decision'], 'ILLUSTRATIVE_NOT_CERTIFIED')
            self.assertFalse(x['can_certify_product_hidden_closure_exclusion'])

    def test_cohort_mean_not_certified_even_if_attested(self):
        x = frozen_case(30)
        x['attestations'] = {k: True for k in REQUIRED}
        self.assertEqual(evaluate(x)['decision'], 'ILLUSTRATIVE_NOT_CERTIFIED')

    def test_upper_lid_not_aperture(self):
        x = frozen_case(30)
        x['speed_observable'] = 'upper_lid_only'
        x['attestations'] = {k: True for k in REQUIRED}
        self.assertIn('SPEED_OBSERVABLE_NOT_HARD_APERTURE_DERIVATIVE', evaluate(x)['blockers'])

    def test_sampled_peak_not_hard(self):
        x = frozen_case(30)
        x['speed_observable'] = 'sampled_peak'
        x['attestations'] = {k: True for k in REQUIRED}
        self.assertEqual(evaluate(x)['decision'], 'ILLUSTRATIVE_NOT_CERTIFIED')

    def test_attested_hypothetical_still_not_physical(self):
        x = frozen_case(30)
        x['speed_observable'] = 'aperture_derivative'
        x['attestations'] = {k: True for k in REQUIRED}
        x['dwell_evidence'] = 'eventwise_hard_minimum'
        r = evaluate(x)
        self.assertEqual(r['decision'], 'CONDITIONAL_BOUND_ONLY')
        self.assertFalse(r['physical_validated'])
        self.assertFalse(r['can_certify_product_hidden_closure_exclusion'])

    def test_each_missing_attestation_blocks(self):
        for missing in REQUIRED:
            with self.subTest(missing=missing):
                x = frozen_case(30)
                x['speed_observable'] = 'aperture_derivative'
                x['attestations'] = {k: k != missing for k in REQUIRED}
                self.assertEqual(evaluate(x)['decision'], 'ILLUSTRATIVE_NOT_CERTIFIED')

    def test_group_dwell_not_minimum(self):
        x = frozen_case(30)
        self.assertIn('GROUP_MEAN_DWELL_NOT_EVENTWISE_MINIMUM', evaluate(x)['blockers'])
        self.assertFalse(evaluate(x)['group_mean_dwell_is_minimum'])

    def test_invalid_parameters(self):
        invalid = [('aperture_mm', '0'), ('aperture_mm', '-2'),
                   ('speed_mm_s', '0'), ('period_s', '1/2000'),
                   ('exposure_s', '0'), ('closure_threshold', '1'),
                   ('closure_threshold', '-1/5'), ('endpoint_aperture', '2'),
                   ('speed_mm_s', 'nan')]
        for key, value in invalid:
            with self.subTest(key=key, value=value):
                x = frozen_case(30)
                x[key] = value
                with self.assertRaises(ValueError): evaluate(x)

    def test_missing_and_nonboolean_attestation(self):
        x = frozen_case(30)
        del x['attestations'][REQUIRED[0]]
        with self.assertRaises(ValueError): evaluate(x)
        x['attestations'][REQUIRED[0]] = 1
        with self.assertRaises(ValueError): evaluate(x)

    def test_bad_observable_and_dwell(self):
        x = frozen_case(30)
        x['speed_observable'] = 'eyelid_speed_maybe'
        with self.assertRaises(ValueError): evaluate(x)
        x['speed_observable'] = 'cohort_mean'
        x['dwell_evidence'] = 'minimum_from_mean'
        with self.assertRaises(ValueError): evaluate(x)

    def test_no_external_human_information_in_output(self):
        x = frozen_case(30)
        x['participant_name'] = 'PRIVATE'
        r = evaluate(x)
        self.assertNotIn('PRIVATE', str(r))
        self.assertEqual(r['product'], 'ABSTAIN_UNCALIBRATED')
        self.assertEqual(r['release'], 'BLOCKED')


if __name__ == '__main__':
    unittest.main()
