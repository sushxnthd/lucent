#!/usr/bin/env python3
"""E002-707 adversarial regression suite; run python -m unittest discover -p 'test_e002_707*.py'."""
import copy
import json
import unittest
from e002_707_strict_manifest import validate

def fixture():
    return {"schema":"E002-707-v1","records":[{
      "participant_pseudonym":"p1","session_id":"s1","device_model":"cam",
      "camera_firmware":"1","acquisition_clock_id":"clock",
      "high_rate_file_sha256":"a"*64,"low_rate_file_sha256":"b"*64,
      "exposure_start_interval":[0,0],"exposure_end_interval":[1,1],
      "roi_row":5,"frame_drop_count":0,"aperture_scale_interval":[1,1],
      "aperture_error_interval":[0,0],"speed_ceiling_source":"independent",
      "clock_error_interval":[0,0],"shutter_gap_upper":1,
      "closure_threshold":0.5,"nuisance_tags":["none"]}]}

class ManifestTests(unittest.TestCase):
    def check(self,obj,valid):
        self.assertEqual(validate(json.dumps(obj).encode()) == [],valid)
    def test_valid(self):
        self.check(fixture(),True)
    def test_root_reference_leak(self):
        o=fixture();o["reference_labels"]=[1];self.check(o,False)
    def test_nested_leak(self):
        o=fixture();o["records"][0]["metadata"]={"ground_truth":1};self.check(o,False)
    def test_zero_scale(self):
        o=fixture();o["records"][0]["aperture_scale_interval"]=[0,0];self.check(o,False)
    def test_unhashable_identifier(self):
        o=fixture();o["records"][0]["participant_pseudonym"]=["x"];self.check(o,False)
    def test_duplicate_key(self):
        raw=json.dumps(fixture()).replace('"schema":','"schema":"E002-707-v1","schema":',1)
        self.assertTrue(validate(raw.encode()))
    def test_nonfinite(self):
        o=fixture();o["records"][0]["closure_threshold"]=float("nan");self.check(o,False)
    def test_duplicate_participant_session(self):
        o=fixture();o["records"].append(copy.deepcopy(o["records"][0]));self.check(o,False)
    def test_negative_row(self):
        o=fixture();o["records"][0]["roi_row"]=-1;self.check(o,False)
    def test_extra_envelope(self):
        o=fixture();o["metadata"]={"innocuous":True};self.check(o,False)
    def test_invalid_json(self):
        self.assertTrue(validate(b'{"records":'))

if __name__=="__main__":
    unittest.main()
