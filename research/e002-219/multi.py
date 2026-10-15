import csv,io,json,hashlib
from probe import archive_probe
from scanner import scan
from member import member
a=archive_probe();out=[]
for f in (0.01,0.05,0.1):
 r={"fraction":f,"status":"blocked"}
 try:
  o=a["central_directory_offset"]+int(f*a["central_directory_bytes"])
  for e in scan(a["url"],o):
   b=member(a["url"],e)
   rows=list(csv.reader(io.StringIO(b.decode("utf-8-sig"))))
   r.update(status="ok",member=e[0].decode(),sha256=hashlib.sha256(b).hexdigest(),rows=len(rows)-1,unique_timestamps=len(set(x[0] for x in rows[1:])))
   break
 except Exception as ex:r["error"]=str(ex)[:160]
 out.append(r)
print(json.dumps({"native_time_certified":False,"human_waveform_evaluated":False,"windows":out}))
