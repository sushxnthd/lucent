import hashlib
import tempfile
import unittest
import zipfile
import subprocess
from pathlib import Path
import e002_563_public_phantom_probe as m


class OriginalHumanSourceProbeTests(unittest.TestCase):
    def test_rate_verdict(self):
        self.assertEqual(m.verdict(150, 150), 'PAPER_RATE_COMPATIBLE_METADATA_ONLY')
        self.assertEqual(m.verdict(500, 500), 'REHOST_RATE_COMPATIBLE_PAPER_CONFLICT')
        self.assertEqual(m.verdict(150, 500), 'UNRESOLVED_RATE')
        self.assertEqual(m.verdict(None, 150), 'UNRESOLVED_RATE')

    def test_real_codec_synthetic_fixture_and_checksum(self):
        with tempfile.TemporaryDirectory() as t:
            video = Path(t) / 'fixture.avi'
            archive = Path(t) / 'fixture.zip'
            subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                            '-f', 'lavfi', '-i', 'color=white:s=64x64:r=150:d=0.4',
                            '-c:v', 'ffv1', str(video)], check=True)
            with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
                z.write(video, 'Sess01/ME011_phantom.avi')
            digest = hashlib.md5(archive.read_bytes()).hexdigest()
            result = m.analyze(archive, digest)
            self.assertEqual(result['rate_verdict'], 'PAPER_RATE_COMPATIBLE_METADATA_ONLY')
            self.assertEqual(result['prefix_exact_adjacent_duplicates'], result['prefix_decoded_frames']-1)
            self.assertFalse(result['sensor_clock_verified'])
            self.assertEqual(result['release'], 'BLOCKED')
            with self.assertRaisesRegex(ValueError, 'MD5 mismatch'):
                m.analyze(archive, '0'*32)

    def test_zip_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            archive = Path(t) / 'fixture.zip'
            with zipfile.ZipFile(archive, 'w') as z:
                z.writestr('../escape_phantom.avi', b'not a video')
            with self.assertRaisesRegex(ValueError, 'unsafe ZIP'):
                m.safe_video(archive, Path(t) / 'output.avi')


if __name__ == '__main__':
    unittest.main()
