#!/usr/bin/env python3
"""Synthetic decoder/instrument tests only: no LPW footage and no human annotations."""
import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import e002_575_lpw_packet as m


def template(r, ids):
    return {'experiment': 'E002-574', 'rater': r, 'clips': {
        clip: [{'frame': j, 'upper_y': None, 'lower_y': None, 'iris_diameter': None,
                'uncertainty_px': None, 'flags': ['UNREVIEWED']} for j in range(19)]
        for clip in ids}}


class PacketTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.t = tempfile.TemporaryDirectory()
        cls.root = Path(cls.t.name)
        cls.video = cls.root / 'private_source.mkv'
        subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-f', 'lavfi',
                        '-i', 'testsrc2=size=96x64:rate=95', '-frames:v', '57',
                        '-c:v', 'ffv1', str(cls.video)], check=True)
        cls.digest = m.sha256(cls.video)

    @classmethod
    def tearDownClass(cls):
        cls.t.cleanup()

    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.rootout = Path(self.t.name)
        ids = ['clip_0000', 'clip_0001']
        self.owner = {'experiment': 'E002-574', 'evidence_tier': 'SELECTION_PLAN_ONLY',
                      'window_count': 2, 'owner_mapping': [
                          {'blind_clip': clip, 'participant_id': 'p1', 'video_id': 'v1',
                           'video_sha256': self.digest, 'start_native_frame': start,
                           'native_frames': list(range(start, start + 19))}
                          for clip, start in zip(ids, (0, 38))]}
        self.sources = {'videos': [{'participant_id': 'p1', 'video_id': 'v1',
                                   'video_sha256': self.digest, 'native_frame_count': 57,
                                   'absolute_path': str(self.video)}]}
        self.a, self.b = template('A', ids), template('B', ids)
        self.out = self.rootout / 'packets'

    def build(self):
        return m.build_packet(self.owner, self.sources, self.a, self.b, self.out)

    def test_native_geometry_and_private_packets(self):
        result = self.build()
        self.assertEqual(result['frames_per_reviewer'], 38)
        self.assertEqual(result['independent_human_rater_pairs'], 0)
        for clip in ('clip_0000', 'clip_0001'):
            for j in range(19):
                pa = self.out / 'RATER_A' / 'clips' / clip / f'frame_{j:02d}.png'
                pb = self.out / 'RATER_B' / 'clips' / clip / f'frame_{j:02d}.png'
                self.assertEqual(m.png_dimensions(pa), (96, 64))
                self.assertEqual(m.sha256(pa), m.sha256(pb))
        audit = json.loads((self.out / 'OWNER_ONLY_SOURCE_AUDIT.json').read_text())
        self.assertEqual(len(audit['frames']), 38)
        self.assertEqual(audit['videos'][0]['decoded_frames'], 57)
        self.assertFalse(audit['timing_authenticated'])
        for r in ('A', 'B'):
            root = self.out / f'RATER_{r}'
            self.assertNotIn('private_source', json.dumps([p.name for p in root.rglob('*')]))
            self.assertNotIn(self.digest, (root / 'PACKET_MANIFEST.json').read_text())
            self.assertEqual(json.loads((root / 'BLANK_ANATOMICAL_RATINGS.json').read_text())['rater'], r)

    def test_source_hash_mismatch_abstains_and_cleans(self):
        self.sources['videos'][0]['video_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'SOURCE_NOT_BOUND_TO_PLAN'):
            self.build()
        self.assertFalse(self.out.exists())

    def test_modified_bytes_detected(self):
        fake = self.rootout / 'fake.mkv'
        fake.write_bytes(self.video.read_bytes() + b'corruption')
        self.sources['videos'][0]['absolute_path'] = str(fake)
        with self.assertRaisesRegex(ValueError, 'SOURCE_SHA256_MISMATCH'):
            self.build()
        self.assertFalse(self.out.exists())

    def test_wrong_frame_count_rejected(self):
        self.sources['videos'][0]['native_frame_count'] = 58
        with self.assertRaisesRegex(ValueError, 'NATIVE_FRAME_COUNT_MISMATCH'):
            self.build()
        self.assertFalse(self.out.exists())

    def test_prefilled_annotation_rejected(self):
        self.a['clips']['clip_0000'][0]['upper_y'] = 10
        with self.assertRaisesRegex(ValueError, 'NONBLIND_OR_PREFILLED'):
            self.build()

    def test_missing_clip_rejected(self):
        del self.b['clips']['clip_0001']
        with self.assertRaisesRegex(ValueError, 'RATER_CLIP_MISMATCH'):
            self.build()

    def test_duplicate_or_overlap_rejected(self):
        self.owner['owner_mapping'][1]['start_native_frame'] = 10
        self.owner['owner_mapping'][1]['native_frames'] = list(range(10, 29))
        with self.assertRaisesRegex(ValueError, 'OVERLAPPING_OR_OUT_OF_RANGE'):
            self.build()

    def test_existing_destination_rejected(self):
        self.out.mkdir()
        with self.assertRaisesRegex(ValueError, 'DESTINATION_MUST_BE_NEW'):
            self.build()

    def test_symlink_source_rejected(self):
        link = self.rootout / 'alias.mkv'
        link.symlink_to(self.video)
        self.sources['videos'][0]['absolute_path'] = str(link)
        with self.assertRaisesRegex(ValueError, 'UNSAFE_SOURCE_PATH'):
            self.build()

    def test_timestamp_checks(self):
        good = [{'best_effort_timestamp_time': str(i/95), 'width': 96, 'height': 64} for i in range(4)]
        self.assertEqual(m.validate_timestamps(good), (96, 64))
        bad = copy.deepcopy(good)
        bad[2]['best_effort_timestamp_time'] = bad[1]['best_effort_timestamp_time']
        with self.assertRaisesRegex(ValueError, 'NONMONOTONIC'):
            m.validate_timestamps(bad)
        bad = copy.deepcopy(good)
        bad[3]['width'] = 98
        with self.assertRaisesRegex(ValueError, 'VARIABLE_NATIVE_DIMENSIONS'):
            m.validate_timestamps(bad)

    def test_non_png_rejected(self):
        p = self.rootout / 'not.png'
        p.write_bytes(b'fake')
        with self.assertRaisesRegex(ValueError, 'INVALID_EXTRACTED_PNG'):
            m.png_dimensions(p)

    def test_missing_source_rejected(self):
        self.sources['videos'] = []
        with self.assertRaisesRegex(ValueError, 'MISSING_OR_EXTRA_SOURCE'):
            self.build()

    def test_unreviewed_only(self):
        self.b['clips']['clip_0000'][2]['flags'] = ['CLOSED']
        with self.assertRaisesRegex(ValueError, 'NONBLIND_OR_PREFILLED'):
            self.build()


if __name__ == '__main__':
    unittest.main()
