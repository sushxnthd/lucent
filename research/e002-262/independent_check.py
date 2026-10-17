import json,hashlib,math
from pathlib import Path
o=json.loads(Path("research/e002-262/RESULTS.json").read_text())
for p,v in o["participants"].items():
 b=Path("/tmp/"+p+"_tracker").read_bytes()
 assert hashlib.sha256(b).hexdigest()==v["source_sha256"]["tracker"]
 t=[]
 for line in b.splitlines():
  try:x=json.loads(line)
  except ValueError:continue
  if not isinstance(x,dict):continue
  z=x.get("true_time")
  if not isinstance(z,(int,float)) or not v["session_start_epoch_s"]+5<=z<v["session_start_epoch_s"]+10:continue
  for e in ("left","right"):
   d=x.get(e+"_pupil_diameter")
   if x.get(e+"_pupil_validity")==1 and isinstance(d,(int,float)) and math.isfinite(d) and d>0:t.append(z)
 t=sorted(set(t))
 assert len(t)==v["either_valid_unique_times"]
 gaps=[(b-a)*1000 for a,b in zip(t,t[1:])]
 assert abs(max(gaps)-v["max_any_valid_spacing_ms"])<.002
 assert sum(x>=100 for x in gaps)==len(v["bilateral_valid_free_gaps_ge100ms"])
print("INDEPENDENT_SOURCE_REPLAY_PASS")
