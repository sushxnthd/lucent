import csv,hashlib,io,json,sys,zipfile
from pathlib import Path
from collections import defaultdict
from PIL import Image
import numpy as np
B=Path(sys.argv[1]).read_bytes()
with zipfile.ZipFile(io.BytesIO(B)) as z:
 names=z.namelist()
 raw=z.read(next(x for x in names if x.endswith('/annotation/annotations.csv')))
 assert hashlib.sha256(raw).hexdigest()=='32ebe8e393eda64b1c9fbdbc7048578388a188a317ddb4e57d0e1f7190d266e6'
 rows=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
 seq=defaultdict(list)
 for r in rows:
  if float(r['eye_area'])>0 and float(r['pupil_area'])>0:seq[r['filename'].split('_frame_')[0]].append(r)
 keys=sorted(seq)
 jpg=defaultdict(list);png=defaultdict(list)
 for n in names:
  if n.lower().endswith(('.jpg','.jpeg')):jpg[Path(n).stem].append(n)
  if n.lower().endswith('.png'):png[Path(n).stem].append(n)
 out={'archive_sha256':hashlib.sha256(B).hexdigest(),'archive_bytes':len(B),'n_sequences':len(keys),'jpg':sum(map(len,jpg.values())),'png':sum(map(len,png.values())),'example_jpg':next(iter(jpg.values()),[]),'example_png':next(iter(png.values()),[]),'selected':[]}
 for idx in [0,5,10,15,20,25]:
  k=keys[idx];a=sorted(seq[k],key=lambda x:x['filename'])
  a=[a[round(i*(len(a)-1)/23)] for i in range(24)] if len(a)>24 else a
  matched=[r for r in a if len(jpg[Path(r['filename']).stem])==1 and len(png[Path(r['filename']).stem])==1]
  out['selected'].append({'sequence':k,'selected':len(a),'matched':len(matched),'example':matched[0]['filename'] if matched else None})
 print(json.dumps(out,indent=2))
