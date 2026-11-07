import json, subprocess, tempfile, unittest, zipfile
from pathlib import Path
from e002_441_human_acquisition import inspect

class TestAcquisition(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name);self.avi=self.root/"SSVEP191_phantom.avi"
  subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-f","lavfi","-i",
   "testsrc=size=32x24:rate=500","-frames:v","3","-c:v","ffv1",str(self.avi)],
   check=True,capture_output=True)
  self.zip=self.root/"S19.zip"
  with zipfile.ZipFile(self.zip,"w",zipfile.ZIP_DEFLATED) as z:
   z.write(self.avi,"Sess01/SSVEP191_phantom.avi")
   z.writestr("Sess01/SSVEP191_sync.csv","timestamp,blink_label,gaze\n0,0,1\n")
   z.writestr("Sess01/SSVEP191_phantom.xml","<Annotations><Pupil/></Annotations>")
 def test_real_decoder_fixture_and_abstention(self):
  d=inspect(self.zip,"S19",verify=False)
  self.assertEqual(d["human_video_count"],1)
  self.assertEqual(d["video_probe"][0]["r_frame_rate"],"500/1")
  self.assertEqual(d["video_probe"][0]["decoded_probe_frames"],2)
  self.assertEqual(d["sync_column_schema"][0]["blink_named_columns"],["blink_label"])
  self.assertFalse(d["physical_release_authorized"])
  self.assertEqual(d["product_claim"],"ABSTAIN_UNCALIBRATED")
  self.assertNotIn("Pupil",json.dumps(d))
 def test_bad_archive_hash(self):
  with self.assertRaisesRegex(ValueError,"MD5"):inspect(self.zip,"S19")
 def test_missing_video(self):
  z=self.root/"none.zip"
  with zipfile.ZipFile(z,"w") as f:f.writestr("file.txt","no video")
  with self.assertRaisesRegex(ValueError,"Phantom"):inspect(z,"S19",verify=False)
 def test_traversal(self):
  z=self.root/"unsafe.zip"
  with zipfile.ZipFile(z,"w") as f:f.write(self.avi,"../SSVEP191_phantom.avi")
  with self.assertRaisesRegex(ValueError,"Unsafe"):inspect(z,"S19",verify=False)
 def test_unknown_subject(self):
  with self.assertRaisesRegex(ValueError,"Unknown"):inspect(self.zip,"S01",verify=False)

if __name__=="__main__":unittest.main()
