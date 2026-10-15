import json
from pathlib import Path
from records import rows
out={}
for p in ("P_33","P_54"):
 e=list(rows("/tmp/"+p+"_events"))
 t=list(rows("/tmp/"+p+"_tracker"))
 out[p]={"event_rows":len(e),"tracker_rows":len(t),"start_events":sum(x.get("event")=="video started" for x in e)}
Path("research/e002-220/COUNT_SUMMARY.json").write_text(json.dumps(out,indent=2))
print(out)
