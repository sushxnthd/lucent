import unittest
import numpy as np
import shutil
import subprocess
import tempfile
from pathlib import Path
from e002_535_independent_human_replay import scores, scan, quality, ffmpeg_frames, evaluate, HEIGHT, WIDTH

class IndependentReplayTests(unittest.TestCase):
    def setUp(self):
        self.frames=[np.full((HEIGHT,WIDTH),100,dtype=np.uint8) for _ in range(6)]
        self.ids=list(range(6))
        self.times=[0.007*i for i in self.ids]

    def test_local_eye_pulse(self):
        self.frames[2][118:190,100:230]=20
        m=scores(self.frames)
        self.assertLessEqual(m['eye'][0],8)
        self.assertGreaterEqual(m['eye'][1],18)
        self.assertLessEqual(m['background'][1],8)

    def test_global_flash_veto(self):
        self.frames[2][:]=180
        m=scores(self.frames)
        self.assertFalse(m['eye'][0]<=8 and m['eye'][1]>=18 and m['background'][1]<=8)

    def test_linear_ramp_rejected(self):
        for j,f in enumerate(self.frames):f[118:190,100:230]=100+j*10
        self.assertLess(scores(self.frames)['eye'][1],18)

    def test_missing_id(self):
        self.ids[3]=4
        self.assertFalse(quality(self.ids,self.times))

    def test_nonfinite_clock(self):
        self.times[3]=float('nan')
        self.assertFalse(quality(self.ids,self.times))

    def test_clock_jump(self):
        self.times[3]=.100
        self.assertFalse(quality(self.ids,self.times))

    def test_hand_computed_center_pulse(self):
        self.frames[2][118:190,100:230]=50
        m=scores(self.frames)
        self.assertAlmostEqual(m['eye'][0],0.)
        self.assertAlmostEqual(m['eye'][1],50.)
        self.assertAlmostEqual(m['background'][1],0.)

    def test_scan_counts_and_privacy(self):
        frames=[np.full((HEIGHT,WIDTH),100,dtype=np.uint8) for _ in range(16)]
        frames[2][118:190,100:230]=20
        ids=list(range(16)); times=[.007*i for i in ids]
        c=scan(frames,ids,times,limit=16)
        self.assertEqual(c['0']['eligible'],3)
        self.assertEqual(c['2']['eligible'],2)
        self.assertEqual(c['0']['eye_specific'],1)
        self.assertEqual(set(c['0']),{'eligible','rejected_time_or_id','eye_return','eye_specific','background_return'})

    def test_truncated_source_fails(self):
        with self.assertRaises(ValueError):scan(self.frames,self.ids,self.times,limit=7)

    @unittest.skipUnless(shutil.which('ffmpeg'), 'ffmpeg unavailable')
    def test_lossless_cli_decoder_roundtrip(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'synthetic.avi'
            frames=[np.full((HEIGHT,WIDTH),k*30,dtype=np.uint8) for k in range(6)]
            subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
                '-f','rawvideo','-pix_fmt','gray','-s',f'{WIDTH}x{HEIGHT}',
                '-r','150','-i','pipe:0','-c:v','ffv1',str(path)],
                input=b''.join(f.tobytes() for f in frames),check=True)
            observed=list(ffmpeg_frames(path))
            self.assertEqual(len(observed),6)
            for a,b in zip(frames,observed):
                np.testing.assert_array_equal(a,b)

    def test_checksum_mismatch_fails_before_decode(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'wrong.zip'
            path.write_bytes(b'not an authentic human source')
            with self.assertRaises(ValueError):evaluate(path,'S01')

    def test_geometry_fails(self):
        self.frames[0]=np.zeros((100,100),dtype=np.uint8)
        with self.assertRaises(ValueError):scores(self.frames)

if __name__=='__main__':unittest.main()
