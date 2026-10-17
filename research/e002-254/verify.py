#!/usr/bin/env python3
"""Verify E002-254 against original GitHub Actions artifact ZIP, not internal hashes."""
import hashlib,json,sys,zipfile
pins={
'e002-221/RESULTS.json':'688049957370a381b6db7f31bf9b91c464bd17b0a8806ac7b72b907ebf1fcc5a',
'e002-221/VALID_ONLY.json':'7e3793b8a7721e8ac4357b2fcc1544170968faf3b24cd9a71a79aefa953ccd8c',
'e002-220/MEMBER_HASHES.json':'5c821e090378d15ad2d8d3278dee1cc9e95b80262917ec58bb127882d692ccc2'}
with zipfile.ZipFile(sys.argv[1]) as z:
 assert set(z.namelist())==set(pins)
 raw={k:z.read(k) for k in pins}
for k in pins:assert hashlib.sha256(raw[k]).hexdigest()==pins[k],k
a=json.loads(raw['e002-221/RESULTS.json'])
b=json.loads(raw['e002-221/VALID_ONLY.json'])
c=json.loads(raw['e002-220/MEMBER_HASHES.json'])
assert set(a['participants'])==set(b['participants'])==set(c)=={'P_33','P_54'}
for p in ('P_33','P_54'):
 x=a['participants'][p];y=b['participants'][p];n=x['video_window_packets']
 assert n==({'P_33':150,'P_54':149}[p])
 assert x['video_window_unique']==({'P_33':145,'P_54':83}[p])
 assert x['exposure_sync_certified'] is False and x['waveform_tested'] is False
 for eye in ('left','right'):
  d=y['eyes'][eye]
  assert 24<d['median_valid_interval_ms']<26
  assert set(map(float,d['offsets']))=={-1,-.5,0,.5,1}
  for q in d['offsets'].values():
   assert q['valid_reference_within_75ms']==n
   assert q['coverage']==1
   assert q['p95_distance_ms']<12
print('E002-254 independent source and clock-ambiguity audit: PASS')
