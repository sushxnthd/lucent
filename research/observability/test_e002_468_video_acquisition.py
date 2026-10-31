"""E002-468 synthetic instrumentation tests; never counted as human validation."""
import hashlib
from pathlib import Path
import subprocess
import tempfile
import unittest
import zipfile

from e002_468_video_acquisition import analyze, fraction, pct

class AcquisitionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def make_archive(self, rate=150, corrupt=False, unsafe=False):
        video = self.root / 'ME191_phantom.avi'
        subprocess.run(['ffmpeg','-y','-v','error','-f','lavfi','-i',
                        f'testsrc=size=96x64:rate={rate}', '-t','0.3',
                        '-c:v','mpeg4',str(video)], check=True)
        archive = self.root / 'sample.zip'
        with zipfile.ZipFile(archive, 'w') as z:
            for name in ('ME191_phantom.avi','ME191_phantom.xml','ME191_sync.csv'):
                arcname = '../'+name if unsafe else 'Sess01/'+name
                if name.endswith('.avi'):
                    z.write(video,arcname)
                else:
                    z.writestr(arcname,'test')
        md5 = hashlib.md5(archive.read_bytes()).hexdigest()
        if corrupt:
            md5 = '0'*32
        return archive, md5

    def test_150fps_is_signal_only(self):
        p, digest = self.make_archive()
        result = analyze(p, digest)
        self.assertEqual(result['container_avg_fps'],150.0)
        self.assertFalse(result['nominal_150fps_conflict'])
        self.assertEqual(result['physical_hidden_closure_exclusion'],'ABSTAIN_UNCALIBRATED')
        self.assertFalse(result['product_release_authorized'])
        self.assertGreater(result['decoded_signal_first_512']['frames'],1)

    def test_nominal_rate_conflict(self):
        p, digest = self.make_archive(rate=240)
        result = analyze(p, digest)
        self.assertTrue(result['nominal_150fps_conflict'])
        self.assertFalse(result['product_release_authorized'])

    def test_checksum_fail_closed(self):
        p, digest = self.make_archive(corrupt=True)
        with self.assertRaisesRegex(ValueError,'MD5 mismatch'):
            analyze(p,digest)

    def test_path_traversal_rejected(self):
        p, digest = self.make_archive(unsafe=True)
        with self.assertRaisesRegex(ValueError,'expected one safe'):
            analyze(p,digest)

    def test_fractions(self):
        self.assertIsNone(fraction('150/0'))
        self.assertIsNone(fraction('bad'))
        self.assertEqual(fraction('300/2'),150)

    def test_percentile(self):
        self.assertEqual(pct([0,2,4,6],0.95),6)
        self.assertIsNone(pct([],0.95))

if __name__=='__main__':
    unittest.main()
