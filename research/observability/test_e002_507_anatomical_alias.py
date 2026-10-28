import unittest
import copy
from e002_508_manifest_attack import mutations
from e002_492_anatomical_review import build_manifest, template
from e002_507_anatomical_alias import evaluate, classify, frozen_start


def frame(state, j):
    # d=100; normalized open=0.2, closed=0.0, ambiguous=0.1
    gap = {'OPEN': 20, 'CLOSED': 0, 'AMBIGUOUS': 10}[state]
    return {'frame': j, 'upper_y': 100, 'lower_y': 100+gap,
            'iris_diameter': 100, 'uncertainty_px': 0, 'flags': []}


class Tests(unittest.TestCase):
    def setUp(self):
        self.m = build_manifest()
        self.a = template(self.m, 'A')
        self.b = template(self.m, 'B')
        self.d = {c['clip']: 1 for c in self.m['review_clips']}

    def fill(self, state='OPEN'):
        for c in self.a['clips']:
            self.a['clips'][c] = [frame(state, j) for j in range(13)]
            self.b['clips'][c] = [frame(state, j) for j in range(13)]

    def test_unreviewed_abstains(self):
        r = evaluate(self.m, self.a, self.b, self.d)
        self.assertEqual((r['windows'], r['endpoint_not_both_open']), (20, 20))

    def test_observed_hidden_native_frame(self):
        self.fill()
        c = self.m['review_clips'][0]['clip']
        k = frozen_start(c)+2
        self.a['clips'][c][k] = frame('CLOSED', k)
        self.b['clips'][c][k] = frame('CLOSED', k)
        r = evaluate(self.m, self.a, self.b, self.d)
        self.assertEqual(r['observed_interior_closed_witness'], 1)
        self.assertEqual(r['no_observed_interior_closure'], 19)
        self.assertFalse(r['physical_hidden_closure_certified'])

    def test_all_open_not_physical_exclusion(self):
        self.fill()
        r = evaluate(self.m, self.a, self.b, self.d)
        self.assertEqual(r['no_observed_interior_closure'], 20)
        self.assertFalse(r['continuous_time_speed_certified'])
        self.assertEqual(r['product'], 'ABSTAIN_UNCALIBRATED')

    def test_common_scale_uncertainty_abstains(self):
        self.fill()
        c = self.m['review_clips'][0]['clip']
        j = frozen_start(c)
        for r in (self.a, self.b):
            r['clips'][c][j] = frame('AMBIGUOUS', j)
        self.assertEqual(evaluate(self.m, self.a, self.b, self.d)['endpoint_not_both_open'], 1)

    def test_rater_disagreement_abstains(self):
        self.fill()
        c = self.m['review_clips'][0]['clip']
        j = frozen_start(c)+1
        self.b['clips'][c][j] = frame('CLOSED', j)
        self.assertEqual(evaluate(self.m, self.a, self.b, self.d)['interior_unresolved'], 1)

    def test_nuisance_abstains(self):
        self.fill()
        c = self.m['review_clips'][0]['clip']
        j = frozen_start(c)+1
        self.a['clips'][c][j]['flags'] = ['GAZE']
        self.assertEqual(evaluate(self.m, self.a, self.b, self.d)['interior_unresolved'], 1)

    def test_scale_delta_changes_classification(self):
        x = frame('OPEN', 0)
        x['lower_y'] = 119
        self.assertEqual(classify(x, x, 1), 'OPEN')
        self.assertEqual(classify(x, x, 99), 'UNKNOWN')

    def test_missing_scale_rejected(self):
        self.d.pop(next(iter(self.d)))
        with self.assertRaisesRegex(ValueError, 'CALIBRATION_REQUIRED'):
            evaluate(self.m, self.a, self.b, self.d)

    def test_bad_delta_rejected(self):
        self.d[next(iter(self.d))] = -1
        with self.assertRaisesRegex(ValueError, 'INVALID_IRIS_SCALE_DELTA'):
            evaluate(self.m, self.a, self.b, self.d)

    def test_duplicate_clips_rejected(self):
        self.m['review_clips'][0]['clip'] = self.m['review_clips'][1]['clip']
        with self.assertRaisesRegex(ValueError, 'CLIP_SET_MISMATCH'):
            evaluate(self.m, self.a, self.b, self.d)

    def test_bad_frame_order_rejected(self):
        self.a['clips'][next(iter(self.a['clips']))][0]['frame'] = 12
        with self.assertRaisesRegex(ValueError, 'FRAME_ORDER_MISMATCH'):
            evaluate(self.m, self.a, self.b, self.d)

    def test_offsets_stable_and_bounded(self):
        self.assertTrue(all(frozen_start(c['clip']) == 3 for c in self.m['review_clips']))
        self.assertEqual(frozen_start('clip_00'), frozen_start('clip_00'))

    def test_no_independence_authentication(self):
        self.fill()
        r = evaluate(self.m, self.a, self.b, self.d)
        self.assertFalse(r['human_rater_independence_authenticated_by_code'])
        self.assertFalse(r['iris_scale_calibration_authenticated_by_code'])
        self.assertEqual(r['release'], 'BLOCKED')



    def test_e002_508_source_provenance_substitution_rejected(self):
        self.fill()
        for name, bad in mutations(self.m).items():
            with self.subTest(name=name):
                with self.assertRaisesRegex(ValueError, 'NONCANONICAL_FROZEN_SOURCE_MANIFEST'):
                    evaluate(bad, self.a, self.b, self.d)

    def test_e002_508_canonical_copy_accepted(self):
        self.fill()
        result = evaluate(copy.deepcopy(self.m), self.a, self.b, self.d)
        self.assertEqual(result['windows'], 20)
        self.assertEqual(result['product'], 'ABSTAIN_UNCALIBRATED')

if __name__ == '__main__':
    unittest.main()
