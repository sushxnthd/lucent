import unittest
from e002_565_guarded_replay import guarded_replay

SHA = 'a' * 64

def src(record='18970793'):
    mi = record == '18970793'
    stem = 'MI011' if mi else 'ME011'
    return {
        'zenodo_record': record,
        'paradigm': 'motor_imagery' if mi else 'motor_execution',
        'archive_md5': 'fb56109542a13aa7879778833fe4cbaa' if mi else 'bce89dd9fbb67e27a656623aa27927e0',
        'video_member': f'Sess01/{stem}_phantom.avi',
        'session': 'Sess01', 'participant_id': 'S01',
        'video_sha256': SHA, 'frame_namespace': f'native-index:{stem}_phantom.avi',
    }


class GuardedReplayTests(unittest.TestCase):
    def test_cross_paradigm_never_reaches_adjudicator(self):
        calls = []
        def oracle(*args):
            calls.append(1)
            return {'positive_witness_candidates': 5, 'heldout_participants': 4}
        r = guarded_replay({'source_sha256': SHA}, {'source_sha256': SHA},
                           src(), src('18971758'), oracle)
        self.assertEqual(r['status'], 'REJECT_CROSS_PARADIGM')
        self.assertFalse(r['adjudication_attempted'])
        self.assertEqual(calls, [])
        self.assertEqual(r['positive_witness_candidates'], 0)

    def test_claimed_original_video_sha_must_match_sealed_replay(self):
        calls = []
        def oracle(*args):
            calls.append(1)
            return {'positive_witness_candidates': 5, 'heldout_participants': 4}
        r = guarded_replay({'source_sha256': 'b'*64}, {'source_sha256': SHA},
                           src(), src(), oracle)
        self.assertEqual(r['status'], 'REJECT_VIDEO_IDENTITY')
        self.assertEqual(calls, [])

    def test_matching_source_does_not_certify_positive_witness(self):
        calls = []
        def oracle(*args):
            calls.append(1)
            return {'positive_witness_candidates': 5, 'heldout_participants': 1}
        r = guarded_replay(
            {'source_sha256': SHA, 'rows': [{'participant_id': 'S01'}]},
            {'source_sha256': SHA, 'positives': [{'participant_id': 'S01'}]},
            src(), src(), oracle)
        self.assertEqual(r['status'], 'SOURCE_MATCH_ONLY_UNCALIBRATED')
        self.assertTrue(r['adjudication_attempted'])
        self.assertEqual(r['positive_witness_candidates'], 5)
        self.assertFalse(r['physical_validation'])
        self.assertEqual(r['release'], 'BLOCKED')
        self.assertEqual(len(calls), 1)

    def test_multi_participant_aggregate_is_not_one_video(self):
        calls = []
        def oracle(*args):
            calls.append(1)
            return {'positive_witness_candidates': 5, 'heldout_participants': 4}
        r = guarded_replay(
            {'source_sha256': SHA, 'rows': [
                {'participant_id': 'S01'}, {'participant_id': 'S02'}]},
            {'source_sha256': SHA, 'positives': [{'participant_id': 'S02'}]},
            src(), src(), oracle)
        self.assertEqual(r['status'], 'REJECT_SAMPLE_NAMESPACE')
        self.assertFalse(r['adjudication_attempted'])
        self.assertEqual(r['positive_witness_candidates'], 0)
        self.assertEqual(calls, [])


if __name__ == '__main__':
    unittest.main()
