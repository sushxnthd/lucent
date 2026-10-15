#!/usr/bin/env python3
"""Offline fail-closed tests for E002-203 original TSV parser."""
import importlib.util, pathlib
source = pathlib.Path(__file__).resolve().parents[1] / 'e002-203' / 'raw_semantics.py'
if not source.exists(): raise SystemExit('MISSING_PRIMARY_RAW_AUDIT_CODE')
spec = importlib.util.spec_from_file_location('raw_semantics',source)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
raw=('left_pupil_valid\tleft_gaze_point_valid\tleft_pupil_diameter\tleft_pupil_available\n'
     '1\t0\t3.1\t1\n0\t1\t3.2\t0\n1\t1\t-1.0\t1\n1\t1\tNaN\t1\n1\t1\t4.2\t1\n').encode()
n,c,fields=m.count_raw(raw,'left')
assert n==5 and c['pupil_valid']==4 and c['gaze_point_valid']==4
assert c['pupil_valid_finite_positive_diameter']==2 and c['pupil_available']==4
assert c['pupil_valid']!=c['pupil_valid_finite_positive_diameter']
try: m.truth('not-a-boolean')
except ValueError: pass
else: raise AssertionError('INVALID_BOOLEAN_ACCEPTED')
try: m.count_raw(b'left_pupil_valid\n1\n','left')
except ValueError: pass
else: raise AssertionError('MISSING_REFERENCE_FIELDS_ACCEPTED')
print('PASS synthetic divergence, diameter and missing-field controls')
