"""Regression tests: the oracle can no longer inflate product certification."""
import pathlib, tempfile, csv, unittest, sys
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from audit import make_rows, FIELDS
from strict_gate import strict_evaluate,verify_human_source

class StrictGateTest(unittest.TestCase):
    def test_reference_blind_accounting(self):
        rows=make_rows()
        with tempfile.TemporaryDirectory() as d:
            path=pathlib.Path(d)/'paired.csv'
            with path.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
            from evaluate import load
            rows=load(path)
            manifest=dict(reference_kind='native_time_same_eye_diameter',
              synchronization='independently_verified_exposure_clock',rgb_modality='visible_color',
              reference_interpolated=False,source_dataset_sha256='synthetic-not-human',
              participant_split_frozen=True,preoutcome_protocol='E002-261',camera_fps=60,
              data_type='synthetic')
            r=strict_evaluate(rows,manifest)
            self.assertEqual((r['total_windows'],r['blind_admitted'],r['certified_windows'],
                r['unscorable_admitted']),(16,16,8,8))
            self.assertEqual(r['certified_fraction'],.5)
            self.assertFalse(r['product_certificate'])
    def test_source_bytes_not_self_attested(self):
        m=dict(data_type='human',source_dataset_sha256='0'*64,clock_evidence_sha256='0'*64)
        with tempfile.TemporaryDirectory() as d:
            raw=pathlib.Path(d)/'raw';clock=pathlib.Path(d)/'clock'
            raw.write_bytes(b'synthetic');clock.write_bytes(b'fake')
            with self.assertRaisesRegex(ValueError,'HASH_MISMATCH'):
                verify_human_source(m,raw,clock)
            with self.assertRaisesRegex(ValueError,'REQUIRED'):
                verify_human_source(m)
if __name__=='__main__':unittest.main()
