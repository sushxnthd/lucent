import unittest
from e002_609_cross_camera_witness import evaluate, fixture


class WitnessTests(unittest.TestCase):
    def test_conflict(self):
        self.assertEqual(evaluate(fixture())['status'], 'WITNESS_CONTRADICTS_CONDITIONAL_EXCLUSION')

    def test_abstaining_prediction_witness(self):
        d = fixture(); d['prediction'] = 'ABSTAIN_HIDDEN_CLOSURE_POSSIBLE'
        self.assertEqual(evaluate(d)['status'], 'HIDDEN_CLOSURE_WITNESS_CONDITIONAL')

    def test_overlap(self):
        d = fixture(); d['reference']['start_earliest_ms'] = '9'; d['reference']['end_latest_ms'] = '11'
        self.assertEqual(evaluate(d)['status'], 'ABSTAIN_REFERENCE_NOT_STRICTLY_INSIDE_GAP')

    def test_touching_both_boundaries(self):
        for a, b in [('0', '2'), ('8', '10')]:
            d = fixture(); d['reference']['start_earliest_ms'] = a; d['reference']['end_latest_ms'] = b
            self.assertEqual(evaluate(d)['status'], 'ABSTAIN_REFERENCE_NOT_STRICTLY_INSIDE_GAP')

    def test_non_witness(self):
        d = fixture(); d['reference']['linear_aperture_upper'] = '0.21'
        self.assertEqual(evaluate(d)['status'], 'NO_REFERENCE_WITNESS')

    def test_missing_attestation_and_hash(self):
        d = fixture(); d['attestations']['reference_linear_anatomy_calibrated'] = False
        self.assertEqual(evaluate(d)['status'], 'ABSTAIN_UNVERIFIED_PREMISE')
        d = fixture(); d['evidence_sha256']['reference_annotation'] = ''
        self.assertEqual(evaluate(d)['status'], 'ABSTAIN_MISSING_EVIDENCE_DIGEST')
        d = fixture(); d['evidence_sha256']['prediction_seal'] = 'c'*64
        self.assertEqual(evaluate(d)['status'], 'ABSTAIN_UNVERIFIED_PREMISE')

    def test_nuisance(self):
        for k in fixture()['nuisances']:
            d = fixture(); d['nuisances'][k] = True
            self.assertEqual(evaluate(d)['status'], 'ABSTAIN_NUISANCE')

    def test_uncertainty_monotonic(self):
        for a,b in [('-1','5'),('3','11'),('0','5'),('3','10')]:
            d = fixture(); d['reference']['start_earliest_ms'] = a; d['reference']['end_latest_ms'] = b
            self.assertNotIn('WITNESS_', evaluate(d)['status'])
        d = fixture(); d['reference']['linear_aperture_upper'] = '0.201'
        self.assertEqual(evaluate(d)['status'], 'NO_REFERENCE_WITNESS')

    def test_invalid_values(self):
        for v in ['NaN', 'Infinity', '1e-2', '1/2', 'garbage']:
            d = fixture(); d['reference']['threshold'] = v
            self.assertEqual(evaluate(d)['status'], 'ABSTAIN_INVALID_NUMERIC_INPUT')
        d = fixture(); d['ordinary_gap']['right_start_earliest_ms'] = '-1'
        self.assertEqual(evaluate(d)['status'], 'ABSTAIN_INVALID_INTERVAL_OR_APERTURE')
        d = fixture(); d['reference']['linear_aperture_upper'] = '1.01'
        self.assertEqual(evaluate(d)['status'], 'ABSTAIN_INVALID_INTERVAL_OR_APERTURE')

    def test_exact_equality(self):
        d = fixture(); d['reference']['linear_aperture_upper'] = '0.20'
        self.assertEqual(evaluate(d)['status'], 'WITNESS_CONTRADICTS_CONDITIONAL_EXCLUSION')

    def test_release_always_blocked(self):
        for mod in ['none','nonwitness','overlap','nuisance']:
            d=fixture()
            if mod=='nonwitness': d['reference']['linear_aperture_upper']='0.9'
            if mod=='overlap': d['reference']['end_latest_ms']='11'
            if mod=='nuisance': d['nuisances']['clock_error']=True
            o=evaluate(d)
            self.assertEqual((o['product'],o['release']), ('ABSTAIN_UNCALIBRATED','BLOCKED'))


if __name__ == '__main__':
    unittest.main()
