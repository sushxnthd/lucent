#!/usr/bin/env python3
"""Independent arithmetic checker; uses only replay JSON."""
import json, pathlib
from fractions import Fraction
r=json.loads((pathlib.Path(__file__).parent/'RESULTS_REPLAY.json').read_text())
assert r['source_type']=='SYNTHETIC_ONLY' and not r['product_certificate']
assert len(r['trials'])==3
for t in r['trials']:
 n=t['missing_frames']; assert n in (15,30,60)
 assert t['targeted_pass'] and not t['placebo_pass'] and not t['full_pass']
 assert t['targeted_mask']['valid_frames']==300-n
 assert t['targeted_mask']['nrmse']<1e-12
 exact=Fraction(n,300)*Fraction(8,5)**2
 assert abs(float(exact)-t['complete_reference']['rmse_mm']**2)<1e-12
 lo,hi=t['conditional_mse_interval_mm2_given_reference_range_2p5_to_3p5']
 assert lo-1e-12<=float(exact)<=hi+1e-12
for p in (-3,0,2,7):
 values=[(p-y)**2 for y in range(5)]
 assert min(values)==max(-p,0,p-4)**2
 assert max(values)==max(p*p,(p-4)**2)
print('E002-270 independent arithmetic checker: PASS')
