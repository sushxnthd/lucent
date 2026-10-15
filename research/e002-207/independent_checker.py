#!/usr/bin/env python3
import csv,hashlib,json
from collections import defaultdict
from pathlib import Path
p=Path('research/e002-207/source_data_loss_per_trial.csv')
raw=p.read_bytes()
assert hashlib.md5(raw).hexdigest()=='369d9446b62fd00888a6d51e152697bd'
o=json.loads(Path('research/e002-207/results/FRONTIER.json').read_text())
assert hashlib.sha256(raw).hexdigest()==o['summary']['source_sha256']
rows=list(csv.DictReader(p.open(encoding='utf-8-sig')))
by=defaultdict(dict)
for r in rows:
 by[(r['pid'],r['trial'])][r['eye']]=(int(r['n_trial_samples']),int(r['n_valid_trial_samples']))
assert len(by)==o['summary']['n_trials']
people={pid for pid,_ in by}
assert people==set(o['participants']) and len(people)==15
possible=set()
for (pid,trial),eyes in by.items():
 assert set(eyes)=={'left','right'}
 if eyes['left'][0]>=600 and max(eyes['left'][1],eyes['right'][1])>=570:possible.add(pid)
assert len(possible)==o['summary']['possible_participants']
assert set(o['candidate_trials'])==possible
print('PASS independent original-source census')
