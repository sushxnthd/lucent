"""E002-469 synthetic fixtures; never counted as independent human validation."""
import hashlib
from pathlib import Path
import tempfile
import unittest
import zipfile
from e002_469_sync_reconciliation import analyze, frame_clock_candidate

class TimingTests(unittest.TestCase):
    def test_explicit_clock_positive(self):
        rows=[[str(i),str(i*2)] for i in range(1500)]
        result=frame_clock_candidate(['frame_index','timestamp_ms'],rows)
        self.assertEqual(result['status'],'CANDIDATE_FRAME_CLOCK')
        self.assertEqual(result['candidate_fps'],500)
        self.assertFalse(result['hardware_shutter_authenticated'])

    def test_unknown_unit_abstains(self):
        rows=[[str(i),str(i*2)] for i in range(1500)]
        self.assertEqual(frame_clock_candidate(['frame_index','timestamp'],rows)['status'],'NO_EXPLICIT_FRAME_CLOCK')

    def test_nonmonotonic_rejected(self):
        rows=[[str(i),str(i*2)] for i in range(1500)]
        rows[600][1]=rows[599][1]
        self.assertEqual(frame_clock_candidate(['frame_index','timestamp_ms'],rows)['status'],'NONMONOTONIC_CLOCK')

    def test_weak_sample_rejected(self):
        rows=[[str(i),str(i*2)] for i in range(999)]
        self.assertEqual(frame_clock_candidate(['frame_index','timestamp_ms'],rows)['status'],'INSUFFICIENT_EXPLICIT_PAIRS')

    def test_archive_integrity_and_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'s.zip'
            with zipfile.ZipFile(p,'w') as z:
                z.writestr('Sess01/ME191_phantom.xml','<root fps="500"/>')
                z.writestr('Sess01/ME191_sync.csv','frame_index,timestamp_ms\n'+''.join(f'{i},{i*2}\n' for i in range(1500)))
            digest=hashlib.md5(p.read_bytes()).hexdigest()
            result=analyze(p,digest)
            self.assertEqual(result['sync_csv']['clock_test']['candidate_fps'],500)
            self.assertFalse(result['hardware_exposure_timing_authenticated'])
            self.assertFalse(result['product_release_authorized'])
            with self.assertRaisesRegex(ValueError,'MD5 mismatch'): analyze(p,'0'*32)

if __name__=='__main__':unittest.main()
