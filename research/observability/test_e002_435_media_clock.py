"""Independent E002-435 media-retiming falsification and negative controls."""
import copy
import unittest

import e002_435_media_clock as m


def fixture():
    base = {'pts':[i*.04 for i in range(13)],
            'packet_hashes':[f'SHA256:packet-{i}' for i in range(13)],
            'pixel_hashes':[f'pixel-{i}' for i in range(13)],
            'physical_certificate_authorized':False,
            'product':'ABSTAIN_UNCALIBRATED'}
    variants = {}
    for name,pts in [('identity',base['pts']),('scaled',[2*t for t in base['pts']]),
                     ('offset',[t+.8 for t in base['pts']])]:
        variants[name] = {**copy.deepcopy(base), 'pts':list(pts), 'packet_pts':list(pts),
                          'reported_fps':25.0}
    return base, variants


class ClockIdentityTests(unittest.TestCase):
    def test_real_stream_copy_intervention(self):
        result = m.experiment()
        self.assertTrue(result['frozen_predictions_passed'])
        self.assertEqual(result['human_sequences'],0)
        self.assertFalse(result['authenticated_hardware_exposure_timing'])
        self.assertEqual(result['product'],'ABSTAIN_UNCALIBRATED')
        self.assertGreater(result['variants']['scaled']['max_abs_pts_difference_from_base_s'],.4)
        self.assertAlmostEqual(result['variants']['offset']['max_abs_pts_difference_from_base_s'],.8)
        for name in ('identity','scaled','offset'):
            self.assertTrue(result['variants'][name]['packet_payload_sha256_sequence_identical'])
            self.assertTrue(result['variants'][name]['decoded_frame_sha256_sequence_identical'])

    def test_pure_oracle_expected_transformations(self):
        b,v = fixture()
        o = m.evaluate_variants(b,v)
        self.assertEqual(set(o),{'identity','scaled','offset'})
        self.assertAlmostEqual(o['scaled']['max_gap_s'],.08)

    def test_reencoded_packet_change_is_not_identity(self):
        b,v = fixture()
        v['scaled']['packet_hashes'][5]='SHA256:tampered'
        with self.assertRaisesRegex(m.ExperimentFailure,'packet content changed'):
            m.evaluate_variants(b,v)

    def test_pixel_change_is_not_identity(self):
        b,v = fixture()
        v['offset']['pixel_hashes'][5]='tampered'
        with self.assertRaisesRegex(m.ExperimentFailure,'pixels changed'):
            m.evaluate_variants(b,v)

    def test_timestamp_mutation_breaks_frozen_prediction(self):
        b,v = fixture()
        v['scaled']['pts'][7] += .03
        v['scaled']['packet_pts'][7] += .03
        with self.assertRaisesRegex(m.ExperimentFailure,'timing prediction failed'):
            m.evaluate_variants(b,v)

    def test_packet_frame_timestamp_disagreement_rejected(self):
        b,v = fixture()
        v['offset']['packet_pts'][4] += .1
        with self.assertRaisesRegex(m.ExperimentFailure,'packet/frame PTS disagreement'):
            m.evaluate_variants(b,v)

    def test_frame_count_and_nondistinct_pixels_rejected(self):
        b,v = fixture()
        v['scaled']['pts'].pop()
        with self.assertRaisesRegex(m.ExperimentFailure,'frame count changed'):
            m.evaluate_variants(b,v)
        b,v = fixture()
        b['pixel_hashes'][2]=b['pixel_hashes'][1]
        with self.assertRaisesRegex(m.ExperimentFailure,'not distinguishable'):
            m.evaluate_variants(b,v)

    def test_unsafe_certificate_rejected(self):
        b,v = fixture()
        v['identity']['physical_certificate_authorized']=True
        with self.assertRaisesRegex(m.ExperimentFailure,'unsafe physical product'):
            m.evaluate_variants(b,v)
        b,v = fixture()
        v['identity']['product']='NO_HIDDEN_CLOSURE'
        with self.assertRaisesRegex(m.ExperimentFailure,'unsafe physical product'):
            m.evaluate_variants(b,v)


if __name__=='__main__':
    unittest.main()
