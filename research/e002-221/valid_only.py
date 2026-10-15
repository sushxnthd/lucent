#!/usr/bin/env python3
"""E002-221b: correct nearest-reference matching by selecting valid samples first."""
import json, bisect, math, statistics, collections
from pathlib import Path
P=Path("research/e002-221")
base=json.loads((P/"RESULTS.json").read_text())
def q(x,f):
 if not x:return None
 x=sorted(x);k=int((len(x)-1)*f);return round(x[k],5)
def nearest(a,t):
 i=bisect.bisect_left(a,t)
 return min((abs(a[j]-t) for j in (i-1,i) if 0<=j<len(a)),default=float("inf"))
out={"run":"E002-221b","correction":"nearest VALID sample rather than nearest any sample","participants":{}}
for p,b in base["participants"].items():
 rows=[json.loads(s) for s in Path("/tmp/"+p+"_tracker").read_text().splitlines()]
 t0=b["browser_start_epoch_s"]
 result={"validity_cross_tab":{},"eyes":{}}
 for eye in ("left","right"):
  cross=collections.Counter()
  samples=[]
  for x in rows:
   d=x.get(eye+"_pupil_diameter")
   valid_number=isinstance(d,(int,float)) and math.isfinite(d) and d>0
   cross[(str(x.get(eye+"_pupil_validity")),str(valid_number))]+=1
   if valid_number and x.get(eye+"_pupil_validity")==1:samples.append(float(x["true_time"]))
  samples.sort()
  result["validity_cross_tab"][eye]={str(k):v for k,v in cross.items()}
  dt=[1000*(samples[i]-samples[i-1]) for i in range(1,len(samples))]
  w=[t for t in samples if t0 is not None and t0+5<=t<t0+10]
  result["eyes"][eye]={"valid_samples_total":len(samples),"valid_samples_window":len(w),
   "median_valid_interval_ms":q(dt,.5),"p95_valid_interval_ms":q(dt,.95),
   "max_valid_interval_ms":q(dt,1.0),"offsets":{}}
  if t0 is None:continue
  import subprocess
  pts=[float(x["pts_time"]) for x in json.loads(subprocess.check_output(["ffprobe","-v","error","-select_streams","v:0","-show_entries","packet=pts_time","-of","json","/tmp/"+p+"_video"]))["packets"] if "pts_time" in x]
  video=[t for t in pts if 5<=t<10]
  for shift in (-1,-.5,0,.5,1):
   dist=[nearest(samples,t0+t+shift)*1000 for t in video]
   passed=sum(d<=75 for d in dist)
   result["eyes"][eye]["offsets"][str(shift)]={"valid_reference_within_75ms":passed,
     "coverage":round(passed/len(video),6),"median_distance_ms":q(dist,.5),
     "p95_distance_ms":q(dist,.95)}
 out["participants"][p]=result
(P/"VALID_ONLY.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps(out,indent=2))
