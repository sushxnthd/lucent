import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from e002_566_authentic_handoff_audit import audit, FRAME_NAMES


class AuthenticHandoffAuditTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.viewer = self.root / 'viewer.html'
        self.viewer.write_text('test viewer fixture')
        owner = self.root / 'OWNER_PRIVATE_DO_NOT_SHARE' / 'PRIVATE_FRAMES_DO_NOT_UPLOAD'
        owner.mkdir(parents=True)
        for name in FRAME_NAMES:
            (owner / name).write_bytes(('fixture-' + name).encode())
        for r in 'AB':
            bundle = self.root / 'REVIEWER_PACKETS' / f'RATER_{r}_PRIVATE'
            images = bundle / 'PRIVATE_FRAMES_DO_NOT_UPLOAD'
            images.mkdir(parents=True)
            for name in FRAME_NAMES:
                (images / name).write_bytes(('fixture-' + name).encode())
            (bundle / 'e002_497_offline_rater.html').write_text('test viewer fixture')
            (bundle / 'READ_ME_PRIVATE.txt').write_text('independent private review')
            template = {'experiment':'E002-492','rater':r,'clips':{
                f'clip_{i:02d}':[{'frame':j,'upper_y':None,'lower_y':None,
                'iris_diameter':None,'uncertainty_px':None,'flags':['UNREVIEWED']}
                for j in range(13)] for i in range(20)}}
            (bundle / f'RATER_{r}_TEMPLATE.json').write_text(json.dumps(template))

    def bundle(self, r):
        return self.root / 'REVIEWER_PACKETS' / f'RATER_{r}_PRIVATE'

    def test_valid_synthetic_bundle_remains_uncalibrated(self):
        r = audit(self.root, self.viewer)
        self.assertEqual(r['status'], 'AUTHENTIC_RATER_BUNDLES_VERIFIED')
        self.assertEqual(r['independent_human_raters'], 0)
        self.assertEqual(r['release'], 'BLOCKED')

    def test_tampered_source_frame(self):
        (self.bundle('A')/'PRIVATE_FRAMES_DO_NOT_UPLOAD'/'clip_00_frame_00.png').write_bytes(b'tampered')
        with self.assertRaisesRegex(ValueError, 'SOURCE_BOUND'):
            audit(self.root, self.viewer)

    def test_missing_frame(self):
        (self.bundle('B')/'PRIVATE_FRAMES_DO_NOT_UPLOAD'/'clip_19_frame_12.png').unlink()
        with self.assertRaisesRegex(ValueError, 'FRAME_SET'):
            audit(self.root, self.viewer)

    def test_extra_mapping_leak(self):
        (self.bundle('A')/'owner_mapping.json').write_text('leak')
        with self.assertRaisesRegex(ValueError, 'EXTRA'):
            audit(self.root, self.viewer)

    def test_cross_rater_template(self):
        a = self.bundle('A')/'RATER_A_TEMPLATE.json'
        obj = json.loads(a.read_text())
        obj['rater'] = 'B'
        a.write_text(json.dumps(obj))
        with self.assertRaisesRegex(ValueError, 'IDENTITY'):
            audit(self.root, self.viewer)

    def test_prepopulated_label(self):
        a = self.bundle('A')/'RATER_A_TEMPLATE.json'
        obj = json.loads(a.read_text())
        obj['clips']['clip_00'][0]['upper_y'] = 1
        a.write_text(json.dumps(obj))
        with self.assertRaisesRegex(ValueError, 'PREPOPULATED'):
            audit(self.root, self.viewer)

    def test_symlink_frame(self):
        a = self.bundle('A')/'PRIVATE_FRAMES_DO_NOT_UPLOAD'/'clip_00_frame_00.png'
        a.unlink()
        a.symlink_to(self.root/'OWNER_PRIVATE_DO_NOT_SHARE'/'PRIVATE_FRAMES_DO_NOT_UPLOAD'/'clip_00_frame_00.png')
        with self.assertRaisesRegex(ValueError, 'SOURCE_BOUND'):
            audit(self.root, self.viewer)

    def test_viewer_tamper(self):
        (self.bundle('B')/'e002_497_offline_rater.html').write_text('different viewer')
        with self.assertRaisesRegex(ValueError, 'VIEWER_MISMATCH'):
            audit(self.root, self.viewer)

if __name__ == '__main__':
    unittest.main()
