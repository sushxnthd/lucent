#!/usr/bin/env python3
"""Adversarial tests for E002-467 human image-level preflight."""
import importlib.util
import math
import unittest
from pathlib import Path

p = Path(__file__).with_name("e002_467_human_video_preflight.py")
spec = importlib.util.spec_from_file_location("e002_467", p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def row(subject="S01", seq="a", idx=0, t=0, aperture="1.0", error="0.1", **kw):
    d = dict(participant_id=subject, sequence_id=seq, frame_index=str(idx),
             timestamp_ms=str(t), aperture_mm=str(aperture),
             aperture_error_mm=str(error), quality_ok="1", annotation_ok="1",
             geometry_ok="1", sync_ok="1", shutter_ok="1", nuisance_ok="1")
    d.update(kw)
    return d

def total(r, field):
    return sum(r["counts"][s][field] for s in ("calibration", "holdout"))

class Preflight(unittest.TestCase):
    def test_split_no_leakage(self):
        self.assertEqual(len(m.CALIBRATION), 23)
        self.assertEqual(len(m.HOLDOUT), 8)
        self.assertFalse(m.CALIBRATION & m.HOLDOUT)
        self.assertEqual(m.CALIBRATION | m.HOLDOUT, set(m.SUBJECTS))

    def test_robust_below_is_candidate_not_physical(self):
        r=m.analyze([row()],2)
        self.assertEqual(total(r,"image_subthreshold_candidates"),1)
        self.assertFalse(r["physical_release_authorized"])
        self.assertEqual(r["physical_hidden_closure_exclusion"],"ABSTAIN_UNCALIBRATED")
        self.assertEqual(r["anatomical_negative_labels"],0)

    def test_equal_threshold_unresolved(self):
        r=m.analyze([row(aperture="1.9",error="0.1")],2)
        self.assertEqual(total(r,"image_subthreshold_candidates"),0)
        self.assertEqual(total(r,"unresolved_frames"),1)

    def test_no_above_threshold_negative_labels(self):
        r=m.analyze([row(aperture="5")],2)
        self.assertEqual(r["anatomical_negative_labels"],0)
        self.assertEqual(total(r,"unresolved_frames"),1)

    def test_gap_invalidates_whole_sequence(self):
        r=m.analyze([row(),row(idx=2,t=13.333333)],2)
        self.assertEqual(total(r,"invalid_sequences"),1)
        self.assertEqual(total(r,"unresolved_frames"),2)

    def test_reverse_timestamp_invalid(self):
        r=m.analyze([row(),row(idx=1,t=-1)],2)
        self.assertEqual(total(r,"invalid_sequences"),1)

    def test_duplicate_frame_invalid(self):
        r=m.analyze([row(),row(idx=0,t=6.666667)],2)
        self.assertEqual(total(r,"invalid_sequences"),1)

    def test_timestamp_jitter_invalid(self):
        r=m.analyze([row(),row(idx=1,t=11.0)],2)
        self.assertEqual(total(r,"invalid_sequences"),1)

    def test_nan_aperture_unresolved(self):
        r=m.analyze([row(aperture="nan")],2)
        self.assertEqual(total(r,"unresolved_frames"),1)

    def test_negative_uncertainty_unresolved(self):
        r=m.analyze([row(error="-0.1")],2)
        self.assertEqual(total(r,"unresolved_frames"),1)

    def test_bad_flag_unresolved(self):
        r=m.analyze([row(shutter_ok="unknown")],2)
        self.assertEqual(total(r,"unresolved_frames"),1)

    def test_glasses_or_blur_nuisance_unresolved(self):
        r=m.analyze([row(nuisance_ok="0")],2)
        self.assertEqual(total(r,"unresolved_frames"),1)

    def test_annotation_disagreement_unresolved(self):
        r=m.analyze([row(annotation_ok="0")],2)
        self.assertEqual(total(r,"unresolved_frames"),1)

    def test_unknown_subject_rejected(self):
        with self.assertRaises(ValueError):
            m.analyze([row(subject="S32")],2)

    def test_missing_field_rejected(self):
        d=row(); del d["geometry_ok"]
        with self.assertRaises(ValueError):
            m.analyze([d],2)

    def test_invalid_threshold_rejected(self):
        for v in (float("nan"),float("inf"),0,-1):
            with self.assertRaises(ValueError):
                m.analyze([row()],v)

    def test_invalid_tolerance_rejected(self):
        with self.assertRaises(ValueError):
            m.analyze([row()],2,tolerance_ms=10)

    def test_subject_disjoint_multiple_sessions(self):
        cal=sorted(m.CALIBRATION)[0]; hold=sorted(m.HOLDOUT)[0]
        r=m.analyze([row(subject=cal,seq="sess1"),
                     row(subject=cal,seq="sess2"),
                     row(subject=hold,seq="sess1")],2)
        self.assertEqual(r["counts"]["calibration"]["sequences"],2)
        self.assertEqual(r["counts"]["holdout"]["sequences"],1)
        self.assertEqual(total(r,"image_subthreshold_candidates"),3)

if __name__ == "__main__":
    unittest.main()
