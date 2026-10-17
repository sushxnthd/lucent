#!/usr/bin/env python3
"""Deterministic replay and manifest; all generated data are synthetic."""
import csv, hashlib, json, pathlib, sys, tempfile
ROOT=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'research'/'e002-268'))
sys.path.insert(0,str(ROOT/'research'/'e002-269'))
from audit import make_rows, FIELDS
from score import score
from evaluate import load
manifest=dict(reference_kind='native_time_same_eye_diameter',
 synchronization='independently_verified_exposure_clock',rgb_modality='visible_color',
 reference_interpolated=False,source_dataset_sha256='synthetic-not-human',
 participant_split_frozen=True,preoutcome_protocol='E002-261',camera_fps=60,
 data_type='synthetic',independent_clock_error_bound_s=0)
with tempfile.TemporaryDirectory() as d:
    p=pathlib.Path(d)/'fixture.csv'
    with p.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(make_rows())
    r=score(load(p),manifest)
    source_sha=hashlib.sha256(p.read_bytes()).hexdigest()
    r['synthetic_csv_sha256']=source_sha
    r['source_rows']=len(make_rows())
    r['source_generation']='research/e002-268/audit.py:make_rows() via CSV roundtrip'
    here=pathlib.Path(__file__).parent
    (here/'RESULTS.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    (here/'DATASET_MANIFEST.json').write_text(json.dumps(dict(run='E002-269',kind='SYNTHETIC_ONLY',
      fixture_sha256=source_sha,source_rows=r['source_rows'],
      generator='research/e002-268/audit.py:make_rows',
      native_human_rgb_reference_pairs=0,
      official_eve_hdf5_bytes_inspected=False,
      eve_access='REQUEST_ONLY_NOT_OBTAINED',
      inherited_evaluator_blob_sha='c97fcdc77ca27235e5dc8186529cdbd3e87f6bd4',
      inherited_guard_blob_sha='2521c4a1d0f9eec457dcd03dcab49bafc386f144'),indent=2,sort_keys=True)+'\n')
    print('E002-269 replay:',r['test_windows'],'windows',r['passed'],'passed; fixture SHA-256',source_sha)
