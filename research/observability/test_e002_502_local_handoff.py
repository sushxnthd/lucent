"""Synthetic privacy and blinding controls. No human images or archive required."""
import json
from pathlib import Path
import tempfile
import unittest
from e002_502_local_handoff import FRAME_NAMES, stage_raters


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root = Path(self.t.name)
        self.owner = self.root / 'OWNER_PRIVATE'
        self.owner.mkdir()
        frames = self.owner / 'PRIVATE_FRAMES_DO_NOT_UPLOAD'
        frames.mkdir()
        for n in FRAME_NAMES:
            (frames / n).write_bytes(b'SYNTHETIC-ONLY' * 16)
        self.viewer = self.root / 'offline.html'
        self.viewer.write_text('SYNTHETIC-ONLY-VIEWER')
        for r in ('A', 'B'):
            t = {'experiment': 'E002-492', 'rater': r, 'clips': {
                f'clip_{i:02d}': [{'frame': j, 'upper_y': None, 'lower_y': None,
                                   'iris_diameter': None, 'uncertainty_px': None,
                                   'flags': ['UNREVIEWED']} for j in range(13)]
                for i in range(20)}}
            (self.owner / f'RATER_{r}_TEMPLATE.json').write_text(json.dumps(t))
        (self.owner / 'OWNER_ONLY_MAPPING.json').write_text('SECRET-CANDIDATE-INDEX')
        self.target = self.root / 'STAGED'

    def test_separate_blinded_packages(self):
        report = stage_raters(self.owner, self.target, self.viewer)
        self.assertEqual(report['status'], 'PRIVATE_HANDOFF_STAGED')
        self.assertFalse(report['physical_hidden_closure_certified'])
        for r in ('A', 'B'):
            folder = self.target / f'RATER_{r}_PRIVATE'
            self.assertEqual(len(list((folder / 'PRIVATE_FRAMES_DO_NOT_UPLOAD').iterdir())), 260)
            self.assertEqual(len(list(folder.iterdir())), 4)
            self.assertNotIn('SECRET-CANDIDATE-INDEX', ''.join(
                p.read_text(errors='ignore') for p in folder.rglob('*') if p.is_file()))
            self.assertFalse((folder / 'OWNER_ONLY_MAPPING.json').exists())
            t = json.loads((folder / f'RATER_{r}_TEMPLATE.json').read_text())
            self.assertEqual(t['rater'], r)
        self.assertFalse((self.target / 'RATER_A_PRIVATE' / 'RATER_B_TEMPLATE.json').exists())

    def test_reject_missing_frame(self):
        (self.owner / 'PRIVATE_FRAMES_DO_NOT_UPLOAD' / sorted(FRAME_NAMES)[0]).unlink()
        with self.assertRaisesRegex(ValueError, 'SOURCE_FRAME_SET_INVALID'):
            stage_raters(self.owner, self.target, self.viewer)
        self.assertFalse(self.target.exists())

    def test_reject_extra_unblinding_file(self):
        (self.owner / 'PRIVATE_FRAMES_DO_NOT_UPLOAD' / 'candidate_5356.txt').write_text('LEAK')
        with self.assertRaisesRegex(ValueError, 'SOURCE_FRAME_SET_INVALID'):
            stage_raters(self.owner, self.target, self.viewer)

    def test_reject_prepopulated_rater(self):
        t = self.owner / 'RATER_A_TEMPLATE.json'
        obj = json.loads(t.read_text())
        obj['clips']['clip_00'][0]['flags'] = []
        t.write_text(json.dumps(obj))
        with self.assertRaisesRegex(ValueError, 'SOURCE_TEMPLATE_NOT_BLANK'):
            stage_raters(self.owner, self.target, self.viewer)

    def test_reject_symlink_frame(self):
        f = self.owner / 'PRIVATE_FRAMES_DO_NOT_UPLOAD' / sorted(FRAME_NAMES)[0]
        f.unlink()
        f.symlink_to(self.viewer)
        with self.assertRaisesRegex(ValueError, 'SOURCE_FRAME_SET_INVALID'):
            stage_raters(self.owner, self.target, self.viewer)

    def test_reject_existing_target(self):
        self.target.mkdir()
        with self.assertRaisesRegex(ValueError, 'REVIEWER_TARGET_MUST_NOT_EXIST'):
            stage_raters(self.owner, self.target, self.viewer)

    def test_reject_cross_rater_template(self):
        t = self.owner / 'RATER_B_TEMPLATE.json'
        obj = json.loads(t.read_text())
        obj['rater'] = 'A'
        t.write_text(json.dumps(obj))
        with self.assertRaisesRegex(ValueError, 'SOURCE_TEMPLATE_IDENTITY_INVALID'):
            stage_raters(self.owner, self.target, self.viewer)


if __name__ == '__main__':
    unittest.main()
