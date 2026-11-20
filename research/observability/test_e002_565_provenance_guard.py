import unittest
from e002_565_provenance_guard import adjudicate_source, valid_identity

SHA = 'a' * 64


def src(record='18970793'):
    is_mi = record == '18970793'
    stem = 'MI011' if is_mi else 'ME011'
    return {
        'zenodo_record': record,
        'paradigm': 'motor_imagery' if is_mi else 'motor_execution',
        'archive_md5': 'fb56109542a13aa7879778833fe4cbaa' if is_mi else 'bce89dd9fbb67e27a656623aa27927e0',
        'video_member': f'Sess01/{stem}_phantom.avi',
        'session': 'Sess01',
        'participant_id': 'S01',
        'video_sha256': SHA,
        'frame_namespace': f'native-index:{stem}_phantom.avi',
    }


def verdict(a, b):
    return adjudicate_source({'source': a}, {'source': b})


class ProvenanceTests(unittest.TestCase):
    def test_both_public_source_identities_are_valid(self):
        self.assertTrue(valid_identity(src()))
        self.assertTrue(valid_identity(src('18971758')))

    def test_cross_paradigm_same_subject_and_nominal_rate_rejected(self):
        a, b = src(), src('18971758')
        a['nominal_fps'] = b['nominal_fps'] = 1
        self.assertEqual(verdict(a, b)['status'], 'REJECT_CROSS_PARADIGM')

    def test_video_identity_mismatch_rejected(self):
        a, b = src(), src()
        b['video_sha256'] = 'b' * 64
        self.assertEqual(verdict(a, b)['status'], 'REJECT_VIDEO_IDENTITY')

    def test_session_and_namespace_mismatch_rejected(self):
        a, b = src(), src()
        b['session'] = 'Sess02'; b['video_member'] = 'Sess02/MI011_phantom.avi'
        self.assertEqual(verdict(a, b)['status'], 'REJECT_SAMPLE_NAMESPACE')
        b = src(); b['video_member'] = 'Sess01/MI012_phantom.avi'
        b['frame_namespace'] = 'native-index:MI012_phantom.avi'
        self.assertEqual(verdict(a, b)['status'], 'REJECT_SAMPLE_NAMESPACE')

    def test_missing_or_unrecognized_provenance_rejected(self):
        for k, val in [('video_sha256', None), ('zenodo_record', '99999999'),
                       ('archive_md5', '0'*32), ('video_member', '../MI011_phantom.avi'),
                       ('paradigm', 'motor_execution'), ('frame_namespace', 'unknown')]:
            b = src()
            if val is None: b.pop(k)
            else: b[k] = val
            self.assertEqual(verdict(src(), b)['status'], 'REJECT_INCOMPLETE_OR_CONTRADICTORY_SOURCE', k)

    def test_exact_match_is_not_physical_validation(self):
        r = verdict(src(), src())
        self.assertEqual(r['status'], 'SOURCE_MATCH_ONLY_UNCALIBRATED')
        self.assertFalse(r['physical_validation'])
        self.assertEqual(r['release'], 'BLOCKED')
        self.assertEqual(r['reference_negative_evidence'], 'CENSORED')

    def test_self_asserted_physical_certificates_cannot_promote(self):
        a, b = src(), src()
        for item in (a,b):
            item.update({'sensor_clock_verified': True, 'hard_velocity_certified': True,
                         'independent_anatomical_raters': 2, 'shutter_calibrated': True})
        self.assertFalse(verdict(a, b)['physical_validation'])

    def test_source_malformed_types_and_case_rejected(self):
        for key, value in [('video_sha256', 'A'*64), ('archive_md5', 'F'*32),
                           ('session', 1), ('participant_id', 'S01/../../S02'),
                           ('video_member', 'Sess01\\MI011_phantom.avi')]:
            b = src(); b[key] = value
            self.assertFalse(valid_identity(b), key)

    def test_absent_or_nonobject_packets_rejected(self):
        for bad in (None, [], 0, {}, {'source': None}):
            self.assertEqual(adjudicate_source({'source': src()}, bad)['status'],
                             'REJECT_INCOMPLETE_OR_CONTRADICTORY_SOURCE')


if __name__ == '__main__':
    unittest.main()
