"""Adversarial no-promotion tests for E002-555."""
import copy
import unittest
from e002_555_rater_audit import audit, InvalidPacket, FLAGS, SCHEMA

def packet(rater, label='closed'):
    return {'schema': SCHEMA, 'timing_type': 'browser_presentation_only', 'packet_id': 'sealed-001', 'rater_id': rater,
            'video_sha256': 'a' * 64,
            'annotations': [{'sample_id': 'frame-0001', 'presentation_time_s': 0.125,
                             'upper': [0.25, 0.2], 'lower': [0.26, 0.5],
                             'vertical_separation_fraction': 0.3,
                             'label': label, 'flags': {k: False for k in FLAGS}}]}

class AuditTests(unittest.TestCase):
    def setUp(self):
        self.a = packet('rater-1')
        self.b = packet('rater-2')

    def test_concordant_closed_not_certified(self):
        r = audit(self.a, self.b)
        self.assertEqual(r['counts']['RATER_CONCORDANT_UNCALIBRATED'], 1)
        self.assertEqual(r['certified_exclusions'], 0)
        self.assertFalse(r['human_physical_validation'])
        self.assertEqual(r['release'], 'BLOCKED')

    def test_concordant_open_censored(self):
        self.a['annotations'][0]['label'] = 'open'
        self.b['annotations'][0]['label'] = 'open'
        self.assertEqual(audit(self.a, self.b)['counts']['REFERENCE_NEGATIVE_CENSORED'], 1)

    def test_disagreement_censored(self):
        self.b['annotations'][0]['label'] = 'open'
        self.assertEqual(audit(self.a, self.b)['counts']['CENSORED'], 1)

    def test_uncertain_censored(self):
        self.b['annotations'][0]['label'] = self.a['annotations'][0]['label'] = 'uncertain'
        self.assertEqual(audit(self.a, self.b)['counts']['CENSORED'], 1)

    def test_nuisance_censored(self):
        for k in FLAGS:
            with self.subTest(k=k):
                b = copy.deepcopy(self.b)
                b['annotations'][0]['flags'][k] = True
                self.assertEqual(audit(self.a, b)['counts']['CENSORED'], 1)

    def test_same_rater_rejected(self):
        self.b['rater_id'] = 'rater-1'
        with self.assertRaises(InvalidPacket): audit(self.a, self.b)

    def test_mismatched_video_rejected(self):
        self.b['video_sha256'] = 'b'*64
        with self.assertRaises(InvalidPacket): audit(self.a, self.b)

    def test_mismatched_packet_rejected(self):
        self.b['packet_id'] = 'different'
        with self.assertRaises(InvalidPacket): audit(self.a, self.b)

    def test_duplicate_sample_rejected(self):
        self.b['annotations'].append(copy.deepcopy(self.b['annotations'][0]))
        with self.assertRaises(InvalidPacket): audit(self.a, self.b)

    def test_timestamp_mismatch_rejected(self):
        self.b['annotations'][0]['presentation_time_s'] += .002
        with self.assertRaises(InvalidPacket): audit(self.a, self.b)

    def test_missing_sample_rejected(self):
        self.b['annotations'][0]['sample_id'] = 'different'
        with self.assertRaises(InvalidPacket): audit(self.a, self.b)

    def test_malformed_coordinate_rejected(self):
        for bad in ([1.5, .2], [float('nan'), .2], [True, .2], ['.2', .2]):
            with self.subTest(bad=bad):
                b = copy.deepcopy(self.b)
                b['annotations'][0]['upper'] = bad
                with self.assertRaises(InvalidPacket): audit(self.a, b)

    def test_forged_separation_rejected(self):
        self.b['annotations'][0]['vertical_separation_fraction'] = .05
        with self.assertRaises(InvalidPacket): audit(self.a, self.b)

    def test_invalid_label_rejected(self):
        self.b['annotations'][0]['label'] = 'certified'
        with self.assertRaises(InvalidPacket): audit(self.a, self.b)

    def test_invalid_flags_rejected(self):
        del self.b['annotations'][0]['flags']['missingness']
        with self.assertRaises(InvalidPacket): audit(self.a, self.b)

    def test_hardware_time_claim_rejected(self):
        self.b['timing_type'] = 'hardware_certified'
        with self.assertRaises(InvalidPacket): audit(self.a, self.b)

    def test_empty_rejected(self):
        self.b['annotations'] = []
        with self.assertRaises(InvalidPacket): audit(self.a, self.b)

if __name__ == '__main__':
    unittest.main()
