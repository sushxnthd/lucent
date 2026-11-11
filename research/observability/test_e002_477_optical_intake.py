"""Synthetic instrument fault injection for E002-477. No physical acquisitions."""
import csv
import hashlib
import json
import math
import tempfile
import unittest
from pathlib import Path
from e002_477_optical_intake import SCHEMA, evaluate


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def make_bundle(folder):
    folder = Path(folder)
    period = 1000 / 240
    step = 0.05
    n = math.ceil(2 * period / step - 1e-10) + 1
    cam = folder / "camera.csv"
    clock = folder / "clock.csv"
    raw = folder / "frames.bin"
    raw.write_bytes(b"SYNTHETIC INSTRUMENT FIXTURE - NOT RAW PHYSICAL FRAMES")
    with cam.open("w", newline="") as a, clock.open("w", newline="") as b:
        cw = csv.DictWriter(a, fieldnames=["row_stratum", "phase_index", "repeat_index", "response", "dark_reference", "gain", "saturated", "dropped"])
        tw = csv.DictWriter(b, fieldnames=["row_stratum", "phase_index", "repeat_index", "pulse_start_ms", "pulse_end_ms"])
        cw.writeheader(); tw.writeheader()
        for row in ("top", "bottom"):
            shutter_start = 0.2 if row == "top" else 0.35
            for phase in range(n):
                t = phase * step
                overlap = max(0, min(t + .1, shutter_start + 1.0) - max(t, shutter_start))
                for rep in range(20):
                    cw.writerow(dict(row_stratum=row, phase_index=phase, repeat_index=rep, response=round(.001 + overlap, 8), dark_reference=.001, gain=1, saturated=0, dropped=0))
                    tw.writerow(dict(row_stratum=row, phase_index=phase, repeat_index=rep, pulse_start_ms=round(t, 8), pulse_end_ms=round(t+.1, 8)))
    manifest = dict(schema=SCHEMA, frame_period_ms=period, phase_step_ms=step, scan_periods=2, repeats_per_phase=20,
                    row_strata=["top", "bottom"], pulse_width_ms=.1, pulse_width_tolerance_ms=.005,
                    clock_error_bound_ms=.02, expected_gain=1.0, camera_gain_locked=True,
                    clock_source_type="independent_photodiode_logic_analyzer", camera_device_id="synthetic-camera", clock_device_id="synthetic-clock",
                    camera_csv_sha256=digest(cam), clock_csv_sha256=digest(clock), raw_video_sha256=digest(raw))
    man = folder / "manifest.json"
    man.write_text(json.dumps(manifest))
    return [man, cam, clock, raw]


class OpticalIntakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.paths = make_bundle(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def mutate_manifest(self, key, value):
        p = self.paths[0]
        obj = json.loads(p.read_text()); obj[key] = value; p.write_text(json.dumps(obj))

    def mutate_csv(self, which, mutation, *, rehash=True):
        p = self.paths[which]
        with p.open(newline="") as f:
            rows = list(csv.DictReader(f)); fields = list(rows[0])
        mutation(rows)
        with p.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader(); writer.writerows(rows)
        if rehash:
            self.mutate_manifest("camera_csv_sha256" if which == 1 else "clock_csv_sha256", digest(p))

    def assert_reject(self, code):
        r = evaluate(*self.paths)
        self.assertEqual(r["qa_status"], "REJECT", r)
        self.assertEqual(r["reason"], code, r)
        self.assertFalse(r["physical_release_authorized"])
        self.assertEqual(r["product_claim"], "ABSTAIN_UNCALIBRATED")

    def test_valid_synthetic_intake_never_certifies_shutter(self):
        r = evaluate(*self.paths)
        self.assertEqual(r["qa_status"], "PASS_INTAKE_ONLY")
        self.assertEqual(r["phase_count"], 168)
        self.assertEqual(r["observations"], 6720)
        self.assertGreater(r["row_summaries"]["top"]["max_contrast"], 0)
        self.assertAlmostEqual(r["row_summaries"]["bottom"]["descriptive_contrast_phase_centroid_ms"] - r["row_summaries"]["top"]["descriptive_contrast_phase_centroid_ms"], 0.15, places=7)
        self.assertFalse(r["hardware_independence_authenticated"])
        self.assertFalse(r["physical_shutter_support_authenticated"])
        self.assertEqual(r["product_claim"], "ABSTAIN_UNCALIBRATED")

    def test_missing_phase(self):
        self.mutate_csv(1, lambda r: r.__setitem__(slice(None), [x for x in r if not (x["row_stratum"] == "top" and x["phase_index"] == "5")]))
        self.assert_reject("GRID_INCOMPLETE")

    def test_fewer_repeats(self):
        self.mutate_csv(1, lambda r: r.pop())
        self.assert_reject("GRID_INCOMPLETE")

    def test_same_clock_and_camera(self):
        self.mutate_manifest("clock_device_id", "synthetic-camera")
        self.assert_reject("CLOCK_NOT_INDEPENDENT")

    def test_unrecognized_clock_source(self):
        self.mutate_manifest("clock_source_type", "camera_metadata")
        self.assert_reject("CLOCK_NOT_INDEPENDENT")

    def test_bad_pulse_width(self):
        self.mutate_csv(2, lambda r: r[0].__setitem__("pulse_end_ms", ".3"))
        self.assert_reject("PULSE_WIDTH")

    def test_clock_error_missing(self):
        self.mutate_manifest("clock_error_bound_ms", None)
        self.assert_reject("NONFINITE_OR_INVALID")

    def test_clock_error_too_large(self):
        self.mutate_manifest("clock_error_bound_ms", 0.1)
        self.assert_reject("CLOCK_UNRESOLVED")

    def test_frame_dropped(self):
        self.mutate_csv(1, lambda r: r[0].__setitem__("dropped", "1"))
        self.assert_reject("SENSOR_NUISANCE")

    def test_clipping(self):
        self.mutate_csv(1, lambda r: r[0].__setitem__("saturated", "1"))
        self.assert_reject("SENSOR_NUISANCE")

    def test_gain_drift(self):
        self.mutate_csv(1, lambda r: r[0].__setitem__("gain", "1.2"))
        self.assert_reject("GAIN_DRIFT")

    def test_missing_row(self):
        self.mutate_csv(1, lambda r: r.__setitem__(slice(None), [x for x in r if x["row_stratum"] != "bottom"]))
        self.assert_reject("GRID_INCOMPLETE")

    def test_wrong_phase_units(self):
        self.mutate_csv(2, lambda r: (r[100].__setitem__("pulse_start_ms", "0.00025"), r[100].__setitem__("pulse_end_ms", "0.10025")))
        self.assert_reject("CLOCK_PHASE")

    def test_raw_video_tampered(self):
        self.paths[3].write_bytes(b"TAMPERED")
        self.assert_reject("SHA_MISMATCH")

    def test_camera_csv_tampered(self):
        self.mutate_csv(1, lambda r: r[0].__setitem__("response", "999"), rehash=False)
        self.assert_reject("SHA_MISMATCH")

    def test_duplicate_clock_key(self):
        self.mutate_csv(2, lambda r: r[0].update({"phase_index": r[1]["phase_index"], "repeat_index": r[1]["repeat_index"]}))
        self.assert_reject("DUPLICATE_KEY")

    def test_nonfinite_signal(self):
        self.mutate_csv(1, lambda r: r[0].__setitem__("response", "nan"))
        self.assert_reject("NONFINITE_OR_INVALID")

    def test_phase_out_of_bound(self):
        self.mutate_csv(2, lambda r: (r[0].__setitem__("pulse_start_ms", "0.03"), r[0].__setitem__("pulse_end_ms", "0.13")))
        self.assert_reject("CLOCK_PHASE")

    def test_phase_step_too_coarse(self):
        self.mutate_manifest("phase_step_ms", .1)
        self.assert_reject("PHASE_GRID_TOO_COARSE")

    def test_gain_unlocked(self):
        self.mutate_manifest("camera_gain_locked", False)
        self.assert_reject("GAIN_DRIFT")


if __name__ == "__main__":
    unittest.main()
