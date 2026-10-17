import hashlib,json,sys,zipfile
from pathlib import Path
sys.path.insert(0,"research/e002-220")
import source,extract
P=("P_01","P_02","P_07")
r=source.R();manifest={}
with zipfile.ZipFile(r) as z:
 a=z.infolist()
 for p in P:
  q=[i for i in a if "/"+p+"/" in "/"+i.filename]
  pick=lambda end:next(i for i in q if i.filename.endswith(end))
  selected={"video":pick("-study-dot_test.webm"),"tracker":pick("/"+p+".txt"),"events":next(i for i in q if i.filename.endswith(".json"))}
  manifest[p]={}
  for kind,i in selected.items():
   b=extract.raw(r,i)
   manifest[p][kind]={"name":i.filename,"bytes":len(b),"crc32":i.CRC,"sha256":hashlib.sha256(b).hexdigest()}
   if kind=="video":Path("/tmp/"+p+"_video").write_bytes(b)
Path("research/e002-228/E002_247_SOURCE.json").write_text(json.dumps({"dataset":source.U,"participants":manifest,"crc_verified":True,"reference_clock_certified":False},indent=2))
print("E002-247 SOURCE",list(manifest))
