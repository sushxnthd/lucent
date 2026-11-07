#!/usr/bin/env python3
"""E002-487 adversarial synthetic archive tests. No real human data."""
import hashlib
import importlib.util
from pathlib import Path
import stat
import subprocess
import tempfile
import unittest
import zipfile

MODULE = Path(__file__).with_name('e002_487_human_video_intake.py')
spec = importlib.util.spec_from_file_location('intake', MODULE)
intake = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intake)


class IntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.dir = Path(cls.tmp.name)
        for fps in (150, 500):
            subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-f', 'lavfi',
                            '-i', f'color=c=black:s=64x64:r={fps}:d=0.2',
                            '-c:v', 'mjpeg', '-y', str(cls.dir / f'{fps}.avi')],
                           check=True, timeout=30)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def archive(self, members):
        path = self.dir / 'fixture.zip'
        with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            for name, data in members:
                z.writestr(name, data)
        return path, hashlib.md5(path.read_bytes()).hexdigest()

    def test_valid_150fps_container(self):
        p, md5 = self.archive([('Sess01/MI241_phantom.avi', (self.dir / '150.avi').read_bytes())])
        r = intake.inspect(p, md5)
        self.assertEqual(r['pilot_acquisition_status'], 'PASS_ARCHIVE_VIDEO_METADATA_ONLY')
        self.assertTrue(r['header_matches_paper_150fps_2pct'])
        self.assertTrue(r['packet_timing']['pts_temporally_usable'])
        self.assertFalse(r['independent_hardware_clock_authenticated'])
        self.assertEqual(r['product_release'], 'BLOCKED')

    def test_500fps_rate_conflict_not_hidden(self):
        p, md5 = self.archive([('Sess01/MI241_phantom.avi', (self.dir / '500.avi').read_bytes())])
        r = intake.inspect(p, md5)
        self.assertTrue(r['source_rate_conflict'])
        self.assertAlmostEqual(r['nominal_rate_hz'], 500)
        self.assertEqual(r['physical_claims'], 'ABSTAIN_UNCALIBRATED')

    def test_checksum_mismatch(self):
        p, _ = self.archive([('Sess01/MI241_phantom.avi', b'dummy')])
        with self.assertRaisesRegex(ValueError, 'CHECKSUM_MISMATCH'):
            intake.inspect(p)

    def test_path_traversal_rejected(self):
        p, md5 = self.archive([('../MI241_phantom.avi', b'fake')])
        with self.assertRaisesRegex(ValueError, 'UNSAFE_ZIP_MEMBER'):
            intake.inspect(p, md5)

    def test_zip_symlink_rejected(self):
        info = zipfile.ZipInfo('Sess01/MI241_phantom.avi')
        info.create_system = 3
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        p, md5 = self.archive([(info, b'outside')])
        with self.assertRaisesRegex(ValueError, 'UNSAFE_ZIP_MEMBER'):
            intake.inspect(p, md5)

    def test_missing_video_rejected(self):
        p, md5 = self.archive([('Sess01/MI241_sync.csv', b'a,b\n')])
        with self.assertRaisesRegex(ValueError, 'NO_PHANTOM_VIDEO'):
            intake.inspect(p, md5)

    def test_corrupt_video_rejected(self):
        p, md5 = self.archive([('Sess01/MI241_phantom.avi', b'not a video')])
        with self.assertRaises(subprocess.CalledProcessError):
            intake.inspect(p, md5)

    def test_nonmonotonic_pts_abstains(self):
        p = intake.pts_audit('0.000000\n0.006667\n0.006667\n0.013333\n')
        self.assertFalse(p['pts_temporally_usable'])
        self.assertEqual(p['nonpositive_steps'], 1)

    def test_empty_pts_abstains(self):
        p = intake.pts_audit('N/A\nN/A\n')
        self.assertFalse(p['pts_temporally_usable'])

    def test_video_size_limit(self):
        p, md5 = self.archive([('Sess01/MI241_phantom.avi', (self.dir / '150.avi').read_bytes())])
        old = intake.MAX_VIDEO_BYTES
        try:
            intake.MAX_VIDEO_BYTES = 100
            with self.assertRaisesRegex(ValueError, 'VIDEO_SIZE_LIMIT'):
                intake.inspect(p, md5)
        finally:
            intake.MAX_VIDEO_BYTES = old


if __name__ == '__main__':
    unittest.main(verbosity=2)
