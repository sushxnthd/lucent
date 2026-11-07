import unittest
from e002_562_replay import predict, split
from e002_565_guarded_replay import guarded_replay

SHA = 'a' * 64

def source():
    return {'zenodo_record': '18970793', 'paradigm': 'motor_imagery',
            'archive_md5': 'fb56109542a13aa7879778833fe4cbaa',
            'video_member': 'Sess01/MI011_phantom.avi', 'session': 'Sess01',
            'participant_id': 'S01', 'video_sha256': SHA,
            'frame_namespace': 'native-index:MI011_phantom.avi'}


class ActualReplayIntegrationTests(unittest.TestCase):
    def test_eight_person_synthetic_bundle_cannot_claim_one_video_source(self):
        people = []
        for n in range(8):
            samples = []
            for i in range(401):
                t = i / 400
                a = min(1.0, 80 * abs(t - 0.0125))
                samples.append({'t_s': t, 'a': a, 'nuisance': []})
            people.append({'id': f'P{n:02d}', 'samples': samples})
        certificate = {'velocity_hard_bound': 10, 'aperture_error': 0,
                       'clock_error_s': 0, 'threshold': .2,
                       'anatomy_verified': True, 'sensor_timing_verified': True,
                       'instantaneous_transfer_verified': True,
                       'velocity_independent': True,
                       'exposure_point_model_verified': True,
                       'nuisance_envelope_verified': True}
        data = {'schema': 'lucent-e002-562-v1', 'source_sha256': SHA,
                'participants': people, 'certificate': certificate}
        pred = predict(data)
        _, held = split([p['id'] for p in people])
        witness = {'source_sha256': SHA, 'positives': [
            {'participant_id': pid, 't_s': .0125, 'timing_error_s': 0}
            for pid in held]}
        result = guarded_replay(pred, witness, source(), source())
        self.assertFalse(result['adjudication_attempted'])
        self.assertEqual(result['status'], 'REJECT_SAMPLE_NAMESPACE')
        self.assertEqual(result['positive_witness_candidates'], 0)
        self.assertFalse(result['physical_validation'])
        self.assertEqual(result['release'], 'BLOCKED')


if __name__ == '__main__':
    unittest.main()
