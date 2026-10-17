#!/usr/bin/env python3
"""Independent algebraic expectation for the 16-window synthetic control."""
import json, pathlib
p=pathlib.Path(__file__).parent/'RESULTS.json'
r=json.loads(p.read_text())
assert r['source_type']=='synthetic'
assert r['test_participants']==8 and r['test_windows']==16
assert r['blind_admitted']==16 and r['scorable_admitted']==16
# Training: pupil mm = 3 + .24 sin(.6*2pi*t), RGB = .25 + .03 sin(.6*2pi*t).
# Hence trained amplitude is .24 mm for every test window. In the 8 low
# reference-amplitude windows, amplitude ratio is .24/.02 = 12, violating <=1.25.
expected={(f'p{i:02}',s):((i%2==0)==(s=='a')) for i in range(2,10) for s in ('a','b')}
assert sum(expected.values())==8
for w in r['windows']:
    assert w['admitted'] and w['scorable']
    assert w['accurate']==expected[(w['participant'],w['session'])]
assert r['passed']==8 and r['conditional_accuracy']==.5
assert not r['product_certificate'] and not r['statistical_candidate']
print('E002-269 independent algebraic checker: PASS')
