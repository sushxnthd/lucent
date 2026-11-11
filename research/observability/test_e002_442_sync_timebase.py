import unittest, tempfile, zipfile
from pathlib import Path
from e002_442_sync_timebase import summarize_column, analyze_zip

class TestTimebase(unittest.TestCase):
    def test_500hz_seconds(self):
        a=summarize_column([str(i*.002) for i in range(1500)],1500)
        self.assertTrue(a["units"]["seconds"]["candidate_frame_clock"])
        self.assertFalse(a["units"]["milliseconds"]["candidate_frame_clock"])
    def test_500hz_milliseconds(self):
        a=summarize_column([str(i*2) for i in range(1500)],1500)
        self.assertTrue(a["units"]["milliseconds"]["candidate_frame_clock"])
    def test_frame_count_mismatch(self):
        a=summarize_column([str(i*.002) for i in range(1500)],1499)
        self.assertFalse(any(x["candidate_frame_clock"] for x in a["units"].values()))
    def test_dropped_tick(self):
        v=[str(i*.002) for i in range(1500)]
        v[800]=""
        a=summarize_column(v,1500)
        self.assertFalse(any(x["candidate_frame_clock"] for x in a["units"].values()))
    def test_reordered_tick(self):
        v=[str(i*.002) for i in range(1500)]
        v[500],v[501]=v[501],v[500]
        a=summarize_column(v,1500)
        self.assertFalse(any(x["candidate_frame_clock"] for x in a["units"].values()))
    def test_1hz_false_camera_rate(self):
        a=summarize_column([str(i) for i in range(1500)],1500)
        self.assertFalse(any(x["candidate_frame_clock"] for x in a["units"].values()))
    def test_incomplete_zip_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"bad.zip"
            with zipfile.ZipFile(p,"w") as z:z.writestr("S19_sync.csv","Time,PhanTime\n1,2\n")
            with self.assertRaisesRegex(ValueError,"columns missing"):analyze_zip(p,verify=False)
    def test_nonfinite_and_missing(self):
        a=summarize_column(["0","nan","inf","","4"])
        self.assertEqual(a["unparseable_count"],3)
        self.assertFalse(any(x["candidate_frame_clock"] for x in a["units"].values()))
    def test_always_abstain(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"fake.zip"
            headers="Time,PhanTime,RelTime,RecordingTimestamp,LocalTimeStamp\n"
            data="".join(f"{i*.002},{i*.002},{i*.002},{i*.002},{i*.002}\n" for i in range(1500))
            with zipfile.ZipFile(p,"w") as z:z.writestr("x_sync.csv",headers+data)
            a=analyze_zip(p,video_frames=1500,verify=False)
            self.assertFalse(a["physical_release_authorized"])
            self.assertEqual(a["product_claim"],"ABSTAIN_UNCALIBRATED")

if __name__=="__main__": unittest.main()
