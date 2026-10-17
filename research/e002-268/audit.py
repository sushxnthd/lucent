#!/usr/bin/env python3
"""E002-268: prospective-admission oracle leakage, synthetic counterexample.
Imports the frozen E002-267 evaluator; never labels synthetic data as human.
"""
import csv, hashlib, json, math, pathlib, sys, tempfile
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research' / 'e002-267'))
from evaluate import load, evaluate, admit_provenance

FIELDS = 'participant_id session_id split device lighting glasses t_rgb_s t_ref_s rgb_ratio reference_mm brightness geometry iris_ratio valid_ref'.split()

def make_rows():
    rows=[]
    for p in range(10):
        split = 'train' if p < 2 else 'test'
        sessions = ['a'] if split=='train' else ['a','b']
        for sess in sessions:
            high = split=='train' or ((p % 2 == 0) == (sess == 'a'))
            for i in range(300):
                t=i/60
                wave=math.sin(2*math.pi*.6*t)
                rgb=.25+.03*wave
                ref=3+(0.24 if high else 0.02)*wave
                rows.append(dict(participant_id=f'p{p:02}',session_id=sess,split=split,
                  device='train_cam' if split=='train' else 'heldout_cam',
                  lighting='train_light' if split=='train' else 'heldout_light',
                  glasses='none' if split=='train' else 'glasses',
                  t_rgb_s=t,t_ref_s=t,rgb_ratio=rgb,reference_mm=ref,
                  brightness=.5+.03*math.sin(2*math.pi*1.3*t+.4),
                  geometry=.2+.03*math.sin(2*math.pi*1.7*t+.8),
                  iris_ratio=.3+.01*math.sin(2*math.pi*2.1*t+.3),valid_ref='1'))
    return rows

def main():
    rows=make_rows()
    manifest=dict(reference_kind='native_time_same_eye_diameter',
      synchronization='independently_verified_exposure_clock',rgb_modality='visible_color',
      reference_interpolated=False,source_dataset_sha256='synthetic-not-human',
      participant_split_frozen=True,preoutcome_protocol='E002-261',camera_fps=60,
      data_type='synthetic')
    with tempfile.TemporaryDirectory() as td:
        path=pathlib.Path(td)/'fixture.csv'
        with path.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
        source_sha=hashlib.sha256(path.read_bytes()).hexdigest()
        old=evaluate(load(path),manifest)
        blind_admitted=old['test_windows']
        true_passes=0
        for p in range(2,10):
            for sess in ('a','b'):
                high=((p%2==0)==(sess=='a'))
                if high: true_passes+=1
        assert old['test_windows']==16 and old['admitted']==8 and old['passed']==8
        assert old['coverage']==.5 and old['conditional_accuracy']==1.0
        assert blind_admitted==16 and true_passes==8
        forged=dict(manifest,data_type='human',source_dataset_sha256='0'*64)
        admit_provenance(forged,load(path))  # Accepted by E002-267: negative test only.
        out=dict(run='E002-268',type='synthetic_counterexample_only',
          source_csv_sha256=source_sha,source_csv_rows=len(rows),test_participants=8,
          test_windows=16,oracle_admitted=old['admitted'],oracle_passed=old['passed'],
          oracle_coverage=old['coverage'],oracle_conditional_accuracy=old['conditional_accuracy'],
          blind_admitted=blind_admitted,blind_passed=true_passes,
          blind_coverage=1.0,blind_conditional_accuracy=true_passes/blind_admitted,
          rgb_nuisance_identical_between_paired_sessions=True,
          source_hash_metadata_spoof_accepted=True,
          human_result=None,remote_ci='not_run')
        print(json.dumps(out,indent=2,sort_keys=True))
        if len(sys.argv)>1:pathlib.Path(sys.argv[1]).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':main()
