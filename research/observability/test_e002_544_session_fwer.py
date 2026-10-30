import json
import math
import tempfile
import unittest
from pathlib import Path
from e002_544_session_fwer import evaluate, simulate, load_private


def fixture(m=39, n=5):
    def session(i, partition, v):
        return {'session_id': 'session-' + str(i), 'partition': partition,
                'nuisance_stratum': 'camera-A-locked',
                'paired_differences': [v] * n,
                'eligible_outside_verified': True, 'quality_verified': True}
    return {'schema': 'E002-544-v1', 'prelabel_commitment': 'a' * 64,
            'alpha': 0.05, 'nuisance_stratum': 'camera-A-locked',
            'calibration_sessions': [session(i, 'calibration_null', i / 1000) for i in range(m)],
            'test_session': session(m, 'heldout_outside', 0.5)}


class FWERTests(unittest.TestCase):
    def test_frozen_rank_candidate(self):
        r = evaluate(fixture())
        self.assertEqual(r['decision'], 'FALSIFICATION_CANDIDATE_FWER')
        self.assertEqual(r['rank_pvalue'], 1/40)

    def test_conservative_ties(self):
        p = fixture()
        p['test_session']['paired_differences'] = [0.038] * 5
        self.assertEqual(evaluate(p)['rank_pvalue'], 2/40)
        p['test_session']['paired_differences'] = [0.037] * 5
        self.assertEqual(evaluate(p)['rank_pvalue'], 3/40)
        self.assertEqual(evaluate(p)['decision'], 'NO_FALSIFICATION_CENSORED')

    def test_no_candidate_when_test_small(self):
        p = fixture()
        p['test_session']['paired_differences'] = [0] * 5
        self.assertEqual(evaluate(p)['rank_pvalue'], 1.0)

    def test_19_is_minimum_nontrivial(self):
        self.assertEqual(evaluate(fixture(18))['decision'], 'ABSTAIN_INVALID_EVIDENCE')
        self.assertEqual(evaluate(fixture(19))['rank_pvalue'], 1/20)

    def test_mismatched_window_count_abstains(self):
        p = fixture()
        p['calibration_sessions'][0]['paired_differences'].pop()
        self.assertEqual(evaluate(p)['reason'], 'window_count_mismatch')

    def test_shifted_stratum_abstains(self):
        p = fixture()
        p['test_session']['nuisance_stratum'] = 'camera-B'
        self.assertEqual(evaluate(p)['reason'], 'nuisance_shift_or_mismatch')

    def test_duplicate_identity_abstains(self):
        p = fixture()
        p['test_session']['session_id'] = p['calibration_sessions'][0]['session_id']
        self.assertEqual(evaluate(p)['reason'], 'nonunique_session_identity')

    def test_wrong_partition_abstains(self):
        p = fixture()
        p['calibration_sessions'][0]['partition'] = 'heldout_outside'
        self.assertEqual(evaluate(p)['reason'], 'partition')

    def test_false_quality_abstains(self):
        for field in ('eligible_outside_verified', 'quality_verified'):
            p = fixture()
            p['test_session'][field] = False
            self.assertEqual(evaluate(p)['reason'], 'timing_or_quality_not_verified')

    def test_invalid_numeric_abstains(self):
        for value in (True, math.nan, math.inf, 1.01, -1.01, '0.5'):
            p = fixture()
            p['test_session']['paired_differences'][0] = value
            self.assertEqual(evaluate(p)['reason'], 'invalid_roi_difference')

    def test_extra_field_abstains(self):
        p = fixture()
        p['test_session']['participant_id'] = 'PRIVATE'
        self.assertEqual(evaluate(p)['reason'], 'session_schema')

    def test_alpha_not_recalibrated(self):
        p = fixture()
        p['alpha'] = 0.1
        self.assertEqual(evaluate(p)['reason'], 'alpha_not_frozen')

    def test_no_private_fields_in_output(self):
        r = json.dumps(evaluate(fixture()))
        for marker in ('session-0', 'camera-A-locked', 'a' * 64, 'paired_differences'):
            self.assertNotIn(marker, r)

    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / 'private.json'
            f.write_text('{"schema":"x","schema":"y"}')
            with self.assertRaises(ValueError):
                load_private(f)

    def test_never_certifies(self):
        r = evaluate(fixture())
        self.assertEqual(r['release'], 'BLOCKED')
        self.assertEqual(r['product'], 'ABSTAIN_UNCALIBRATED')
        self.assertFalse(r['physical_source_authenticated'])
        self.assertFalse(r['shutter_support_certified'])
        self.assertFalse(r['human_anatomical_validation'])

    def test_exact_naive_any_hit(self):
        self.assertGreater(1 - 0.95**200, 0.9999)

    def test_small_sim_reproducible(self):
        a = simulate(seed=12, replications=3, m=19, windows=4)
        self.assertEqual(a, simulate(seed=12, replications=3, m=19, windows=4))
        self.assertEqual(a['physical_captures'], 0)


if __name__ == '__main__':
    unittest.main()
