"""E002-267 synthetic-only tests; never count these as human validation."""
import unittest, tempfile, pathlib, csv, json, math, random
from evaluate import evaluate,load

def fixture(root,confound=False):
    root=pathlib.Path(root);rows=[];rng=random.Random(267)
    for p,split in (("train_a","train"),("train_b","train"),("test_a","test"),("test_b","test")):
        for i in range(300):
            t=i/60
            ref=3+.24*math.sin(2*math.pi*.6*t)+.15*math.sin(2*math.pi*.22*t)
            rgb=.25+(ref-3)/8+.0001*rng.gauss(0,1)
            rows.append(dict(participant_id=p,session_id="s0",split=split,device="Basler",
              lighting="lab",glasses="none",t_rgb_s=t,t_ref_s=t,rgb_ratio=rgb,
              reference_mm=ref,brightness=rgb if confound else .5+.06*math.sin(2*math.pi*1.7*t+.4),
              geometry=.1+.02*math.sin(2*math.pi*1.8*t+.7),
              iris_ratio=.3+.01*math.sin(2*math.pi*2.1*t+1.3),valid_ref="1"))
    path=root/"paired.csv"
    with path.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    manifest=dict(reference_kind="native_time_same_eye_diameter",
        synchronization="independently_verified_exposure_clock",rgb_modality="visible_color",
        reference_interpolated=False,source_dataset_sha256="synthetic-fixture-not-human",
        participant_split_frozen=True,preoutcome_protocol="E002-261",camera_fps=60,
        data_type="synthetic")
    (root/"manifest.json").write_text(json.dumps(manifest))
    return path,manifest,rows

class Tests(unittest.TestCase):
    def test_clean(self):
        with tempfile.TemporaryDirectory() as d:
            path,m,_=fixture(d);r=evaluate(load(path),m)
            self.assertEqual((r["test_windows"],r["admitted"],r["passed"]),(2,2,2))
            self.assertFalse(r["product_gate_pass"]);self.assertFalse(r["positive_control_gate_pass"])
            self.assertEqual(r["windows"][0]["lag_s"],0)
    def test_brightness_confound(self):
        with tempfile.TemporaryDirectory() as d:
            path,m,_=fixture(d,True);r=evaluate(load(path),m)
            self.assertEqual(r["passed"],0)
    def test_leakage(self):
        with tempfile.TemporaryDirectory() as d:
            path,m,rows=fixture(d);rows[0]["split"]="test"
            with path.open("w",newline="") as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
            with self.assertRaisesRegex(ValueError,"PARTICIPANT_LEAKAGE"):load(path)
    def test_uncertified_clock(self):
        with tempfile.TemporaryDirectory() as d:
            path,m,_=fixture(d);m["synchronization"]="outcome_fitted"
            with self.assertRaisesRegex(ValueError,"PROVENANCE_synchronization"):evaluate(load(path),m)
    def test_reference_interpolation(self):
        with tempfile.TemporaryDirectory() as d:
            path,m,_=fixture(d);m["reference_interpolated"]=True
            with self.assertRaisesRegex(ValueError,"PROVENANCE_reference_interpolated"):evaluate(load(path),m)
    def test_missing_10_percent(self):
        with tempfile.TemporaryDirectory() as d:
            path,m,rows=fixture(d)
            for r in rows:
                if r["split"]=="test" and round(r["t_rgb_s"]*60)%10==0:r["valid_ref"]="0"
            with path.open("w",newline="") as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
            r=evaluate(load(path),m);self.assertEqual(r["admitted"],2)
    def test_timestamp_mismatch(self):
        with tempfile.TemporaryDirectory() as d:
            path,m,rows=fixture(d);rows[0]["t_ref_s"]=.1
            with path.open("w",newline="") as f:
                w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
            with self.assertRaisesRegex(ValueError,"TIMESTAMP_DISCREPANCY"):evaluate(load(path),m)
if __name__=="__main__":unittest.main()
