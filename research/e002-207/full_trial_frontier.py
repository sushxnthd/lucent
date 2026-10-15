#!/usr/bin/env python3
# Original-human pupil-reference marginal feasibility audit.
import csv, hashlib, json, math
from pathlib import Path
p=Path('research/e002-207/source_data_loss_per_trial.csv')
assert hashlib.md5(p.read_bytes()).hexdigest()=='369d9446b62fd00888a6d51e152697bd'
rows=list(csv.DictReader(p.open(encoding='utf-8-sig')))
by={}
for r in rows:
 key=(r['pid'],r['trial']); eye=r['eye']
 by.setdefault(key,{})[eye]=(int(r['n_trial_samples']),int(r['n_valid_trial_samples']))
result={}
for (pid,trial),eyes in by.items():
 if set(eyes)!={'left','right'}: raise ValueError('UNPAIRED_TRIAL')
 n=eyes['left'][0]
 if n!=eyes['right'][0]: raise ValueError('N_MISMATCH')
 if n>=600 and max(eyes['left'][1],eyes['right'][1])>=570:
  result.setdefault(pid,[]).append(trial)
participants=sorted({pid for pid,_ in by})
assert len(participants)==15
summary={'n_participants':15,'needed':12,'possible_participants':sum(pid in result for pid in participants),'n_trials':len(by),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'rgb_waveform':'NOT_TESTED','actual_temporal_coverage':'NOT_MEASURED'}
out=Path('research/e002-207/results');out.mkdir(exist_ok=True)
(out/'FRONTIER.json').write_text(json.dumps({'summary':summary,'candidate_trials':result,'participants':participants},indent=2))
print(json.dumps(summary,indent=2))
