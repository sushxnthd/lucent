#!/usr/bin/env python3
"""Predeclared 45-trial original-human pupil reference + paired-RGB archive census."""
import csv,hashlib,importlib.util,json,zipfile
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('e206',ROOT/'research/e002-206/human_edge_coverage.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
def md5(p):return hashlib.md5(p.read_bytes()).hexdigest()
def select(rows):
 pairs=defaultdict(dict)
 for r in rows:
  k=(r['pid'],r['trial']);e=r['eye'].lower()
  if e in pairs[k]:raise ValueError('DUPLICATE_EYE')
  pairs[k][e]=r
 grouped=defaultdict(list)
 for (pid,trial),eyes in pairs.items():
  if set(eyes)!={'left','right'}:raise ValueError('UNPAIRED')
  n=int(eyes['left']['n_trial_samples'])
  if n!=int(eyes['right']['n_trial_samples']):raise ValueError('N_MISMATCH')
  if n<600:continue
  l=int(eyes['left']['n_valid_trial_samples']);r=int(eyes['right']['n_valid_trial_samples'])
  if not(0<=l<=n and 0<=r<=n):raise ValueError('BAD_COUNTS')
  grouped[pid].append((max(l,r)/n,trial,eyes))
 selection=[]
 for pid in sorted({p for p,_ in pairs}):
  ranked=sorted(grouped[pid],key=lambda x:(x[0],x[1]))
  if not ranked:raise ValueError('NO_600_SAMPLE_TRIAL:'+pid)
  for stratum,i in [('low',0),('median',(len(ranked)-1)//2),('high',len(ranked)-1)]:
   quality,trial,eyes=ranked[i]
   selection.append((pid,stratum,trial,quality,eyes))
 return pairs,selection

def main():
 archive=ROOT/'e203_dataset.zip';meta=ROOT/'e203_data_loss_per_trial.csv'
 if md5(archive)!='5e04a7b5e50f7508775e1daea527246b':raise ValueError('BAD_ARCHIVE_MD5')
 if md5(meta)!='369d9446b62fd00888a6d51e152697bd':raise ValueError('BAD_METADATA_MD5')
 rows=list(csv.DictReader(meta.open(encoding='utf-8-sig',newline='')))
 pairs,selection=select(rows)
 if len({pid for pid,_ in pairs})!=15 or len(selection)!=45:raise ValueError('INCOMPLETE_SELECTION')
 output=[];errors=[]
 with zipfile.ZipFile(archive) as z:
  names=z.namelist()
  vids=[p for p in names if Path(p).suffix.lower() in ('.mp4','.avi','.mov','.mkv','.webm','.m4v','.mpeg','.mpg')]
  cam=[p for p in names if any(s in p.lower() for s in ('webcam','camera','front_rgb','rgb_video'))]
  media={'archive_entries':len(names),'video_count':len(vids),'video_sample':vids[:20],
         'camera_named_count':len(cam),'camera_named_sample':cam[:20],
         'paired_rgb_timestamps_verified':False}
  lookup=defaultdict(list)
  for path in names:
   if not path.endswith('.tsv'):continue
   parts=Path(path).parts
   for part in parts[:-1]:
    if part.startswith('participant_'):
     lookup[(part,Path(path).stem)].append(path);break
  for pid,stratum,trial,quality,eyes in selection:
   paths=lookup[(pid,trial)]
   if len(paths)!=1:errors.append([pid,trial,'TSV_MATCHES',len(paths)]);continue
   try:
    alias={(pid,'image_01_1',eye):eyes[eye] for eye in ('left','right')}
    original=h.one_trial(z.read(paths[0]),pid,alias)
    output.append({'pid':pid,'stratum':stratum,'trial':trial,'quality':quality,
                   'source_path':paths[0],'source_sha256':original['tsv_sha256'],
                   'time_field':original['time_field'],'n':original['n'],
                   'eyes':{eye:{k:v for k,v in original['eyes'][eye].items() if k!='bits'}
                           for eye in ('left','right')},
                   'either_pass':any(original['eyes'][eye]['complete_pass'] for eye in ('left','right'))})
   except Exception as ex:errors.append([pid,trial,str(ex)])
 summary={'participants':15,'source_paired_trials':len(pairs),'metadata_rows':len(rows),
          'selected_trials':len(selection),'evaluated':len(output),'errors':errors,
          'rgb_waveform':'NOT_TESTED','paired_rgb_timestamps_verified':False,
          'strata_selection':'metadata-only low/lower-median/high whole-trial best-eye validity fraction; nonrepresentative'}
 for stratum in ('low','median','high'):
  group=[r for r in output if r['stratum']==stratum]
  summary[stratum]={'evaluated':len(group),'passing':sum(r['either_pass'] for r in group)}
 result={'summary':summary,'media':media,'original_human':output}
 dst=HERE/'results';dst.mkdir(exist_ok=True)
 (dst/'SOURCE_FRONTIER.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'summary':summary,'media':media},indent=2),flush=True)
 if errors or len(output)!=45:raise SystemExit('INCOMPLETE_HUMAN_SOURCE')
if __name__=='__main__':main()
