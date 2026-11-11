import copy
import unittest
from e002_613_cap_falsifier import synthetic, evaluate, NUISANCE, ATTEST, EVIDENCE


class CapFalsifier(unittest.TestCase):
    def check(self, d, status):
        a = evaluate(d)
        self.assertEqual(a['status'], status)
        self.assertEqual(a['product'], 'ABSTAIN_UNCALIBRATED')
        self.assertEqual(a['release'], 'BLOCKED')
        self.assertFalse(a['velocity_ceiling_certified'])
        return a

    def test_frozen_rejection(self):
        self.assertEqual(self.check(synthetic(), 'CONDITIONAL_REJECT_CLAIMED_CEILING')['lower_speed_mm_s'], '160')

    def test_equality_does_not_reject(self):
        d = synthetic(); d['claimed_ceiling_mm_s'] = '160'
        self.check(d, 'NO_CEILING_REJECTION_NOT_A_CERTIFICATE')

    def test_wider_clock_does_not_reject(self):
        d = synthetic(); d['dt_max_s'] = '0.003'
        self.assertEqual(self.check(d, 'NO_CEILING_REJECTION_NOT_A_CERTIFICATE')['lower_speed_mm_s'], '400/3')

    def test_wider_error_does_not_reject(self):
        d = synthetic(); d['error0_mm'] = '0.25'; d['error1_mm'] = '0.25'
        self.assertEqual(self.check(d, 'NO_CEILING_REJECTION_NOT_A_CERTIFICATE')['lower_speed_mm_s'], '0')

    def test_zero_difference(self):
        d = synthetic(); d['z1_mm'] = '8.0'
        self.check(d, 'NO_CEILING_REJECTION_NOT_A_CERTIFICATE')

    def test_bad_time(self):
        for v in ('0', '-1', 'NaN', 'Infinity', '1e-3', '0.0'):
            d = synthetic(); d['dt_max_s'] = v
            self.assertTrue(self.check(d, 'ABSTAIN_INVALID_TIME' if v in ('0', '0.0') else 'ABSTAIN_INVALID_NUMERIC_INPUT'))

    def test_bad_numeric(self):
        for field in ('z0_mm', 'z1_mm', 'error0_mm', 'error1_mm', 'claimed_ceiling_mm_s'):
            for v in ('-0.1', 0.1, None, 'NaN', '1e2'):
                d = synthetic(); d[field] = v
                self.check(d, 'ABSTAIN_INVALID_NUMERIC_INPUT')

    def test_missing_nuisance_fails(self):
        for k in NUISANCE:
            d = synthetic(); d['nuisances'][k] = True
            self.check(d, 'ABSTAIN_NUISANCE')
            d = synthetic(); del d['nuisances'][k]
            self.check(d, 'ABSTAIN_NUISANCE')

    def test_missing_attestation_fails(self):
        for k in ATTEST:
            d = synthetic(); d['attestations'][k] = False
            self.check(d, 'ABSTAIN_UNVERIFIED_PREMISE')

    def test_evidence_digest_required(self):
        for k in EVIDENCE:
            d = synthetic(); d['evidence_sha256'][k] = 'not-a-digest'
            self.check(d, 'ABSTAIN_MISSING_EVIDENCE_DIGEST')

    def test_unit_mismatch(self):
        d = synthetic(); d['units'] = 'pixels_and_seconds'
        self.check(d, 'ABSTAIN_UNIT_MISMATCH')

    def test_invalid_schema(self):
        d = synthetic(); d['pair_id'] = '../secret'
        self.check(d, 'ABSTAIN_INVALID_SCHEMA')

    def test_monotonicity(self):
        base = synthetic()
        a = evaluate(base)
        d = copy.deepcopy(base); d['dt_max_s'] = '0.004'
        b = evaluate(d)
        self.assertLessEqual(float(b['lower_speed_mm_s']), float(a['lower_speed_mm_s']))
        d = copy.deepcopy(base); d['error0_mm'] = '0.10'
        b = evaluate(d)
        self.assertLessEqual(float(b['lower_speed_mm_s']), float(a['lower_speed_mm_s']))


if __name__ == '__main__':
    unittest.main()
