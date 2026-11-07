#!/usr/bin/env python3
"""E002-560/561 adversarial regression; requires FFmpeg and FFprobe."""
import shutil
import tempfile
import unittest
from pathlib import Path
import e002_561_media_provenance as m

class MediaProvenanceTests(unittest.TestCase):
    def test_aperture_geometry(self):
        self.assertEqual(m.frame(False)[32*64+32], 0)
        self.assertEqual(m.frame(True)[32*64+32], 200)
        self.assertEqual(len(m.frame(False)), 4096)
        self.assertNotEqual(m.frame(True), m.frame(False))

    def test_eight_phase_prediction(self):
        self.assertEqual(sum(f[32*64+32] == 200 for f in m.raw_frames()), 2)
        self.assertEqual([sum(f[32*64+32] == 200 for f in m.raw_frames(p))
                          for p in range(8)], [0,0,0,8,8,0,0,0])

    def test_invalid_phase_fails_closed(self):
        for phase in (-1, 8, 1.5, "0", True):
            with self.assertRaises(ValueError):
                m.raw_frames(phase)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg required")
    def test_full_encoded_media(self):
        r = m.run_experiment()
        self.assertEqual(r["e002_560_frozen_exact_pts_condition"], "FALSIFIED_MKV_QUANTIZATION")
        self.assertEqual(r["e002_561_corrected_container_condition"], "PASS_SYNTHETIC_REAL_CODEC")
        self.assertEqual(r["low_rate_phases_missing_event"], 6)
        self.assertEqual(r["mkv_pts_steps_us"], [4000,5000])
        self.assertEqual(r["nut_pts_steps_us"], [4166,4167])
        self.assertLess(r["nut_max_pts_error_us"], .51)
        self.assertEqual(r["per_file"]["nut"]["authentic_240"]["closed_frames"], 2)
        self.assertEqual(r["per_file"]["nut"]["phase_3"]["closed_frames"], 8)
        self.assertEqual(r["per_file"]["nut"]["phase_0"]["closed_frames"], 0)
        self.assertFalse(r["human_validation"])
        self.assertFalse(r["physical_sensor_acquisition_verified"])
        self.assertEqual(r["release"], "BLOCKED")

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg required")
    def test_invalid_media_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"invalid.nut"
            p.write_bytes(b"not a video")
            with self.assertRaises(RuntimeError):
                m.inspect(p)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg required")
    def test_short_video_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/"short.nut"
            m.encode(m.raw_frames()[:200], p)
            with self.assertRaisesRegex(AssertionError, "wrong frame count"):
                m.inspect(p)

if __name__ == "__main__":
    unittest.main()
