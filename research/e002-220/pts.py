import subprocess,json
from pathlib import Path
o={}
for p in ("P_33","P_54"):
 a=subprocess.check_output(["ffprobe","-v","error","-select_streams","v:0","-show_entries","packet=pts_time","-of","json","/tmp/"+p+"_video"])
 pts=[float(x["pts_time"]) for x in json.loads(a)["packets"] if "pts_time" in x]
 w=[t for t in pts if 5<=t<10]
 o[p]={"packets":len(pts),"window_packets":len(w),"unique":len(set(w))}
Path("research/e002-220/VIDEO_PTS.json").write_text(json.dumps(o))
print(o)
