"""E002-493 adversarial software checks; synthetic fixtures are NOT human evidence."""
import tempfile
import unittest
from pathlib import Path

import e002_493_real_nuisance as m
from e002_492_anatomical_review import build_manifest


def checker(patch=None):
    f = bytearray(60 if (x + y) % 2 else 190
                  for y in range(64) for x in range(64))
    if patch:
        x0, y0, x1, y1 = patch
        for y in range(y0, y1):
            for x in range(x0, x1):
                f[y * 64 + x] = 25
    return bytes(f)


def synthetic_clips():
    base = checker()
    a = checker((20, 20, 28, 28))
    b = checker((30, 20, 38, 28))
    clips = []
    for c in build_manifest()["review_clips"]:
        frames = [base] * 13
        if c["candidate"]:
            frames = [a] * 13
            frames[6] = b
        clips.append((c["candidate"], frames))
    return clips


def synthetic_indexed():
    indexed = {}
    for item, (_, frames) in zip(build_manifest()["review_clips"], synthetic_clips()):
        for i, frame in zip(item["native_frames"], frames):
            indexed[i] = frame
    return indexed


class TestRealHumanNuisanceProtocol(unittest.TestCase):
    def test_frozen_selection_has_260_unique_frames(self):
        mft = build_manifest()
        indices = [j for c in mft["review_clips"] for j in c["native_frames"]]
        self.assertEqual(len(indices), 260)
        self.assertEqual(len(set(indices)), 260)
        self.assertEqual(sum(c["candidate"] for c in mft["review_clips"]), 1)

    def test_baseline_reproduces_synthetic_candidate(self):
        r = m.screen(synthetic_clips(), "baseline")
        self.assertEqual(r["analyzed_pairs"], 240)
        self.assertTrue(r["candidate_clip_positive"])
        self.assertEqual(r["control_clip_candidates"], 0)

    def test_brightness_plus8_preserves_constructed_event(self):
        r = m.screen(synthetic_clips(), "brightness_plus8")
        self.assertTrue(r["candidate_clip_positive"])
        self.assertEqual(r["control_clip_candidates"], 0)

    def test_temporal_stride_has_no_cross_clip_pairs(self):
        r = m.screen(synthetic_clips(), "stride2")
        self.assertEqual(r["analyzed_pairs"], 120)

    def test_geometry_jitter_changes_pixels(self):
        frame = bytes(x for y in range(64) for x in range(64))
        a = m.transform(frame, "alternating_jitter_1px", 0)
        b = m.transform(frame, "alternating_jitter_1px", 1)
        self.assertEqual(a[32], 33)
        self.assertEqual(b[32], 31)

    def test_constant_shift_and_blur_preserve_constant_frame(self):
        f = bytes([90] * m.SIZE)
        self.assertEqual(set(m.transform(f, "blur_3x3", 0)), {90})
        self.assertEqual(set(m.transform(f, "brightness_plus8", 0)), {98})
        self.assertEqual(set(m.transform(f, "alternating_jitter_1px", 1)), {90})

    def test_bad_condition_and_geometry_rejected(self):
        with self.assertRaisesRegex(ValueError, "UNKNOWN_CONDITION"):
            m.screen(synthetic_clips(), "unfrozen")
        with self.assertRaisesRegex(ValueError, "INVALID_FRAME_SIZE"):
            m.transform(b"bad", "baseline", 0)

    def test_missing_frame_refuses_analysis(self):
        frames = synthetic_indexed()
        frames.pop(next(iter(frames)))
        with self.assertRaisesRegex(ValueError, "MISSING_FROZEN_NATIVE_FRAME"):
            m.analyze(frames)

    def test_synthetic_result_never_authorizes_product(self):
        r = m.analyze(synthetic_indexed())
        self.assertTrue(r["baseline_reproduced"])
        self.assertEqual(set(r["conditions"]), set(m.CONDITIONS))
        self.assertEqual(r["anatomical_closure_labels"], 0)
        self.assertFalse(r["human_reference_validated"])
        self.assertFalse(r["physical_hidden_closure_certified"])
        self.assertEqual(r["product"], "ABSTAIN_UNCALIBRATED")
        self.assertEqual(r["release"], "BLOCKED")
        self.assertNotIn("per_frame_pixels", r)

    def test_unverified_archive_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "S01.zip"
            p.write_bytes(b"unverified")
            with self.assertRaisesRegex(ValueError, "CHECKSUM_MISMATCH"):
                m.inspect(p)

    def test_baseline_nonreproduction_explicit(self):
        indexed = synthetic_indexed()
        for k in indexed:
            indexed[k] = checker()
        r = m.analyze(indexed)
        self.assertFalse(r["baseline_reproduced"])
        self.assertEqual(r["conditions"]["blur_3x3"]["verdict"],
                         "BASELINE_NOT_REPRODUCED")


if __name__ == "__main__":
    unittest.main()
