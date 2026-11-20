import unittest, zipfile, tempfile
from pathlib import Path
from e002_443_sparse_frame_clock import evaluate_events, analyze_zip

class TestSparse(unittest.TestCase):
    def test_500hz_burst_passes(self):
        self.assertTrue(evaluate_events([i*.002 for i in range(1000)],1000)["candidate_event_clock"])
    def test_missing_event_rejects(self):
        self.assertFalse(evaluate_events([i*.002 for i in range(1000)],1001)["candidate_event_clock"])
    def test_reversed_event_rejects(self):
        t=[i*.002 for i in range(1000)]
        t[500],t[501]=t[501],t[500]
        self.assertFalse(evaluate_events(t,1000)["candidate_event_clock"])
    def test_one_fps_rejects(self):
        self.assertFalse(evaluate_events(list(range(1000)),1000)["candidate_event_clock"])
    def test_gap_burst_can_pass(self):
        t=[i*.002 for i in range(500)]+[10+i*.002 for i in range(500)]
        a=evaluate_events(t,1000)
        self.assertTrue(a["candidate_event_clock"])
        self.assertEqual(a["gaps_over_100ms"],1)
    def test_sparse_event_zip_does_not_certify(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"s.zip"
            csv="Time,RelTime\n"+"".join(f'{i*.001},{i*.002 if i%2==0 else ""}\n' for i in range(2000))
            with zipfile.ZipFile(p,"w") as z:z.writestr("x_sync.csv",csv)
            a=analyze_zip(p,verify=False)
            self.assertFalse(a["physical_release_authorized"])
            self.assertEqual(a["product_claim"],"ABSTAIN_UNCALIBRATED")
    def test_nan_rejects(self):
        self.assertFalse(evaluate_events([0,.002,float("nan")],3)["candidate_event_clock"])

if __name__=="__main__":unittest.main()
