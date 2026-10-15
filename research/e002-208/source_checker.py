import json
from pathlib import Path
d=json.loads((Path(__file__).resolve().parent/'results/SOURCE_FRONTIER.json').read_text())
s=d['summary'];rows=d['original_human']
assert s['participants']==15 and len(rows)==s['evaluated']==45 and not s['errors']
assert len(set((r['pid'],r['stratum']) for r in rows))==45
assert s['rgb_waveform']=='NOT_TESTED'
for r in rows:
 assert len(r['source_sha256'])==64
 for eye in ('left','right'):
  x=r['eyes'][eye]
  assert 0<=x['valid_n']<=r['n']
  assert not x['complete_pass'] or x['old_pass']
  if x['complete_pass']:
   assert x['valid_n']>=570 and x['fraction']>=.95
   assert max(x['first_gap_s'],x['last_gap_s'],x['interior_gap_s'])<=.026000001
 assert r['either_pass']==any(r['eyes'][eye]['complete_pass'] for eye in ('left','right'))
for stratum in ('low','median','high'):
 group=[r for r in rows if r['stratum']==stratum]
 assert len(group)==s[stratum]['evaluated']==15
 assert sum(r['either_pass'] for r in group)==s[stratum]['passing']
print('PASS: independent 45-trial reference gate and nonempty provenance')
