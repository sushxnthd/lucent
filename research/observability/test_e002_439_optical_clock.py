"""Independent adversarial verification of E002-439 virtual optical witness."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).parent))
import e002_439_optical_clock as m

class TestOpticalClock(unittest.TestCase):
    def test_crc_known_vector(self):
        self.assertEqual(m.crc8(b'123456789'), 0xF4)

    def test_gray_known_word(self):
        bits = m.payload_bits(33)
        self.assertEqual(int(''.join(map(str,bits[:16])),2),49)

    def test_all_authored_ticks(self):
        self.assertEqual([m.decode_frame(m.render_frame(t)) for t in m.TICKS],list(m.TICKS))

    def test_maximum_uint16_tick(self):
        self.assertEqual(m.decode_frame(m.render_frame(65535)),65535)

    def test_invalid_ticks(self):
        for v in (-1,65536,1.0,True,'33'):
            with self.subTest(v=v),self.assertRaises(m.OpticalClockError):m.render_frame(v)

    def test_all_single_cell_bit_flips_rejected(self):
        base=bytearray(m.render_frame(439))
        for k in range(24):
            modified=bytearray(base)
            row,col=divmod(k,8)
            for y in range(row*8,(row+1)*8):
                for x in range(col*8,(col+1)*8):
                    j=(y*m.WIDTH+x)*3
                    value=224 if modified[j]<128 else 24
                    modified[j:j+3]=bytes((value,)*3)
            with self.subTest(bit=k),self.assertRaises(m.OpticalClockError):
                m.decode_frame(bytes(modified))

    def test_uniform_saturation_fails(self):
        for value in (0,128,255):
            with self.subTest(value=value),self.assertRaises(m.OpticalClockError):
                m.decode_frame(bytes((value,))*(m.WIDTH*m.HEIGHT*3))

    def test_gain_robustness_with_adaptive_references(self):
        for gain in (0.7,1.3):
            frame=m.render_frame(439)
            shifted=bytes(min(255,round(v*gain)) for v in frame)
            self.assertEqual(m.decode_frame(shifted),439)

    def test_duplicate_and_reorder_fails(self):
        a,b,c=[m.render_frame(t) for t in (0,33,67)]
        for seq in ([a,b,b,c],[a,c,b]):
            with self.assertRaises(m.OpticalClockError):m.adjudicate_frames(seq)

    def test_dropped_frame_preserves_clock_gap(self):
        frames=[m.render_frame(t) for t in m.TICKS]
        dropped=frames[:5]+frames[6:]
        out=m.adjudicate_frames(dropped)
        self.assertEqual(out['ticks'],list(m.TICKS[:5]+m.TICKS[6:]))
        self.assertEqual(out['max_gap_virtual_ms'],100)
        self.assertFalse(out['physical_exposure_authenticated'])

    def test_rolling_shutter_crc_collision_negative_control(self):
        # Two different ticks can share CRC8. A row-spliced image then passes
        # checksum; an in-frame code is NOT a physical shutter-time witness.
        first,second=1322,14003
        self.assertNotEqual(first,second)
        a,b=m.render_frame(first),m.render_frame(second)
        hybrid=a[:16*m.WIDTH*3]+b[16*m.WIDTH*3:]
        self.assertEqual(a[16*m.WIDTH*3:],b[16*m.WIDTH*3:])
        self.assertEqual(hybrid,a)
        self.assertNotEqual(hybrid,b)
        self.assertEqual(m.decode_frame(hybrid),first)
        self.assertEqual(m.adjudicate_frames([hybrid])['product'],m.PRODUCT)

    def test_invalid_frame_length(self):
        with self.assertRaises(m.OpticalClockError):m.decode_frame(b'')

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'ffmpeg required')
    def test_real_ffmpeg_encoder_decoder_retime(self):
        with tempfile.TemporaryDirectory(prefix='e002439-test-') as temp:
            out=m.experiment(temp)
        self.assertEqual(out['frame_count'],12)
        self.assertEqual(out['authored_ticks'],list(m.TICKS))
        self.assertEqual(out['optical_ticks_after_retiming'],list(m.TICKS))
        self.assertEqual(out['retimed_pts_ms'],[2*t for t in m.TICKS])
        self.assertTrue(out['identical_decoded_image_sha256'])
        self.assertEqual(out['original_max_gap_virtual_ms'],100)
        self.assertEqual(out['product'],'ABSTAIN_UNCALIBRATED')

if __name__=='__main__':unittest.main()
