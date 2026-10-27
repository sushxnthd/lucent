"""E002-478 adversarial synthetic controls. No physical or human evidence."""
import csv
import json
import math
import tempfile
import unittest

from test_e002_477_optical_intake import make_bundle, digest
from e002_477_optical_intake import evaluate as intake
from e002_478_periodic_replay import evaluate_periodicity

BUDGETS = dict(verified_period_ms=1000/240, period_error_bound_ms=0.0,
               response_slope_bound_per_ms=1.0, contrast_error_bound=0.0005,
               interperiod_drift_bound=0.001, pulse_phase_error_bound_ms=0.001,
               minimum_detectable_contrast=0.02)

class PeriodicityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.paths = make_bundle(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def run_eval(self, **changes):
        return evaluate_periodicity(*self.paths, **(BUDGETS | changes))

    def mutate_camera(self, change):
        p = self.paths[1]
        with p.open(newline="") as f:
            rows = list(csv.DictReader(f))
        change(rows)
        with p.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        m = json.loads(self.paths[0].read_text())
        m["camera_csv_sha256"] = digest(p)
        self.paths[0].write_text(json.dumps(m))

    def periodic(self):
        T = 1000/240
        def modify(rows):
            for r in rows:
                phase = int(r["phase_index"]) * .05
                start = .2 if r["row_stratum"] == "top" else .35
                t = phase % T
                overlap = max(0.0, min(t + .1, start + 1.0) - max(t, start))
                r["response"] = round(.001 + overlap, 8)
        self.mutate_camera(modify)

    def test_original_fixture_passes_intake_but_violates_periodicity(self):
        self.assertEqual(intake(*self.paths)["qa_status"], "PASS_INTAKE_ONLY")
        result = self.run_eval()
        self.assertEqual(result["periodicity_status"], "REJECT_STATIONARY_PERIODIC_MODEL", result)
        self.assertGreater(result["violations"], 0)
        self.assertFalse(result["physical_release_authorized"])

    def test_stationary_periodic_control_survives(self):
        self.periodic()
        result = self.run_eval()
        self.assertEqual(result["periodicity_status"], "CONSISTENT_WITH_PERIODICITY_ONLY", result)
        self.assertEqual(result["violations"], 0)
        self.assertGreater(result["matched_phase_pairs"], 100)
        self.assertFalse(result["instrument_budgets_authenticated"])

    def test_unmodeled_second_period_brightness_shift_rejects(self):
        self.periodic()
        self.mutate_camera(lambda rows: [r.__setitem__("response", float(r["response"]) + .04)
                                         for r in rows if int(r["phase_index"]) * .05 >= 1000/240])
        self.assertEqual(self.run_eval()["periodicity_status"], "REJECT_STATIONARY_PERIODIC_MODEL")

    def test_no_optical_response_indeterminate(self):
        self.mutate_camera(lambda rows: [r.__setitem__("response", r["dark_reference"]) for r in rows])
        self.assertEqual(self.run_eval()["reason"], "INSUFFICIENT_OPTICAL_RESPONSE")

    def test_one_dark_row_abstains_instead_of_passing(self):
        self.periodic()
        self.mutate_camera(lambda rows: [r.__setitem__("response", r["dark_reference"])
                                         for r in rows if r["row_stratum"] == "bottom"])
        self.assertEqual(self.run_eval()["reason"], "INSUFFICIENT_OPTICAL_RESPONSE_ROW")

    def test_missing_independent_slope_budget_abstains(self):
        self.assertEqual(self.run_eval(response_slope_bound_per_ms=None)["reason"],
                         "INDEPENDENT_BUDGETS_REQUIRED")

    def test_bad_period_abstains(self):
        self.assertEqual(self.run_eval(verified_period_ms=4.0)["reason"],
                         "FRAME_PERIOD_NOT_AUTHENTICATED")

    def test_infinite_slope_abstains(self):
        self.assertEqual(self.run_eval(response_slope_bound_per_ms=math.inf)["reason"],
                         "INDEPENDENT_BUDGETS_REQUIRED")

    def test_increased_drift_budget_avoids_false_rejection(self):
        self.periodic()
        self.mutate_camera(lambda rows: [r.__setitem__("response", float(r["response"]) + .003)
                                         for r in rows if int(r["phase_index"]) * .05 >= 1000/240])
        result = self.run_eval(interperiod_drift_bound=.01)
        self.assertEqual(result["periodicity_status"], "CONSISTENT_WITH_PERIODICITY_ONLY", result)

    def test_corrupt_camera_file_fails_intake(self):
        self.paths[1].write_text("tampered")
        self.assertEqual(self.run_eval()["periodicity_status"], "REJECT_INTAKE")

if __name__ == "__main__":
    unittest.main()
