import unittest
from copy import deepcopy
from e002_519_reference_censoring import evaluate


def example():
    return {'version':'E002-519-v1','gaps':[{'id':'g1','prediction':'EXCLUDE',
        'left_end_max_ms':10,'right_start_min_ms':30,'references':[{
        'id':'r1','start_min_ms':12,'end_max_ms':20,'anatomy':'CLOSED_WITNESS',
        'two_independent_raters':True,'photometry_valid':True,'clock_valid':True,
        'native_provenance_valid':True,'nuisance_clear':True}]}]}


class TestReferenceCensoring(unittest.TestCase):
    def check(self, data, expected):
        result = evaluate(data)
        self.assertEqual(result['decisions'][0]['decision'], expected)
        self.assertFalse(result['verified_no_hidden_closure'])
        self.assertEqual(result['product'], 'ABSTAIN_UNCALIBRATED')

    def test_strict_positive_witness(self):
        self.check(example(), 'FALSIFIED_BY_REFERENCE_WITNESS')

    def test_boundary_overlap_is_not_witness(self):
        x=example();x['gaps'][0]['references'][0]['start_min_ms']=10
        self.check(x, 'REFERENCE_CENSORED_NOT_FALSIFIED')

    def test_open_reference_never_verifies_negative(self):
        x=example();x['gaps'][0]['references'][0]['anatomy']='OPEN_OBSERVED'
        self.check(x, 'REFERENCE_CENSORED_NOT_FALSIFIED')

    def test_no_reference_is_unknown(self):
        x=example();x['gaps'][0]['references']=[]
        self.check(x, 'UNKNOWN')

    def test_unverified_clock_is_unknown(self):
        x=example();x['gaps'][0]['references'][0]['clock_valid']=False
        self.check(x, 'UNKNOWN')

    def test_missing_independent_rater_flag_fails_closed(self):
        x=example();del x['gaps'][0]['references'][0]['two_independent_raters']
        with self.assertRaisesRegex(ValueError, 'INVALID_REFERENCE_FLAGS'): evaluate(x)

    def test_no_exclusion_is_not_testable(self):
        x=example();x['gaps'][0]['prediction']='ABSTAIN'
        self.check(x, 'NOT_TESTABLE')

    def test_empty_robust_gap_is_not_testable(self):
        x=example();x['gaps'][0]['right_start_min_ms']=10
        self.check(x, 'NOT_TESTABLE')

    def test_witness_dominates_ambiguous_reference(self):
        x=example();other=deepcopy(x['gaps'][0]['references'][0]);other['id']='r2'
        other['anatomy']='UNKNOWN';x['gaps'][0]['references'].append(other)
        self.check(x, 'FALSIFIED_BY_REFERENCE_WITNESS')

    def test_duplicate_gap_rejected(self):
        x=example();x['gaps'].append(deepcopy(x['gaps'][0]))
        with self.assertRaisesRegex(ValueError, 'INVALID_GAP_ID'): evaluate(x)

    def test_nonfinite_time_rejected(self):
        x=example();x['gaps'][0]['left_end_max_ms']=float('nan')
        with self.assertRaisesRegex(ValueError, 'INVALID_TIME'): evaluate(x)


if __name__ == '__main__':
    unittest.main()
