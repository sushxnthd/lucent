import copy
import hashlib
import unittest
from e002_562_replay import predict, adjudicate, split

SOURCE = hashlib.sha256(b'synthetic-only').hexdigest()


def fixture(v=80, closure=True):
    participants = []
    for n in range(8):
        samples = []
        for i in range(401):
            t = i/400
            # Sharp V=80/s Lipschitz closure at 12.5ms, full opening by 25ms.
            a = min(1., 80*abs(t-.0125)) if closure else 1.
            samples.append({'t_s':t, 'a':a, 'nuisance':[]})
        participants.append({'id':f'S{n:02d}', 'samples':samples})
    cert = {'velocity_hard_bound':v, 'aperture_error':0., 'clock_error_s':0.,
            'threshold':.2, 'anatomy_verified':True, 'sensor_timing_verified':True,
            'instantaneous_transfer_verified':True, 'velocity_independent':True,
            'exposure_point_model_verified':True, 'nuisance_envelope_verified':True}
    return {'schema':'lucent-e002-562-v1', 'source_sha256':SOURCE,
            'certificate':cert, 'participants':participants}


def witness(data):
    _, held = split([p['id'] for p in data['participants']])
    return {'source_sha256':SOURCE,
            'positives':[{'participant_id':pid,'t_s':.0125,'timing_error_s':0}
                         for pid in held]}


class ReplayTests(unittest.TestCase):
    def test_correct_bound_no_false_exclusions(self):
        d = fixture()
        p = predict(d)
        a = adjudicate(p, witness(d))
        self.assertEqual(a['positive_witness_candidates'], 0)
        self.assertEqual(a['heldout_participants'], 4)
        self.assertEqual(a['certified_exclusions'], 0)
        self.assertGreater(a['abstentions'], 0)

    def test_understated_velocity_falsified(self):
        d = fixture(v=10)
        p = predict(d)
        a = adjudicate(p, witness(d))
        self.assertGreater(a['positive_witness_candidates'], 0)
        self.assertEqual(a['human_physical_validation'], False)

    def test_absent_bound_abstains(self):
        d = fixture()
        del d['certificate']['velocity_hard_bound']
        p = predict(d)
        self.assertEqual({r['decision'] for r in p['rows']}, {'ABSTAIN'})

    def test_unverified_shutter_abstains(self):
        d = fixture()
        d['certificate']['exposure_point_model_verified'] = False
        self.assertEqual({r['decision'] for r in predict(d)['rows']}, {'ABSTAIN'})

    def test_nuisance_endpoint_abstains(self):
        d = fixture(v=10, closure=False)
        for participant in d['participants']:
            for sample in participant['samples']:
                sample['nuisance'] = ['blur']
        self.assertEqual({r['decision'] for r in predict(d)['rows']}, {'ABSTAIN'})

    def test_no_reference_label_leak(self):
        d = fixture()
        d['participants'][0]['samples'][0]['ref_closed'] = True
        with self.assertRaises(ValueError):
            predict(d)

    def test_nonmonotone_and_duplicates(self):
        d = fixture()
        d['participants'][0]['samples'][2]['t_s'] = 0
        with self.assertRaises(ValueError):
            predict(d)
        d = fixture()
        d['participants'][1]['id'] = d['participants'][0]['id']
        with self.assertRaises(ValueError):
            predict(d)

    def test_tampered_prediction_rejected(self):
        d = fixture()
        p = predict(d)
        p['rows'][0]['decision'] = 'EXCLUDE_CONDITIONAL'
        with self.assertRaises(ValueError):
            adjudicate(p, witness(d))

    def test_source_mismatch_and_duplicate_witness_rejected(self):
        d = fixture()
        p = predict(d)
        w = witness(d)
        w['source_sha256'] = 'a'*64
        with self.assertRaises(ValueError):
            adjudicate(p, w)
        w = witness(d)
        w['positives'].append(copy.deepcopy(w['positives'][0]))
        with self.assertRaises(ValueError):
            adjudicate(p, w)

    def test_negative_only_not_absence_proof(self):
        d = fixture(closure=False)
        p = predict(d)
        a = adjudicate(p, {'source_sha256':SOURCE, 'positives':[]})
        self.assertEqual(a['reference_negative_evidence'], 'CENSORED')
        self.assertEqual(a['certified_exclusions'], 0)
        self.assertEqual(a['release'], 'BLOCKED')

    def test_nonfinite_rejected(self):
        d = fixture()
        d['participants'][0]['samples'][0]['a'] = float('nan')
        with self.assertRaises(ValueError):
            predict(d)

if __name__ == '__main__':
    unittest.main()
