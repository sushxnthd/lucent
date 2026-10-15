import io,urllib.request as u,zipfile,json
from pathlib import Path
U="https://webgazer.cs.brown.edu/data/WebGazerETRA2018Dataset_Release20180420.zip"
class R(io.RawIOBase):
 def __init__(self):
  with u.urlopen(u.Request(U,headers={"Range":"bytes=0-0"})) as r:self.n=int(r.headers["Content-Range"].split("/")[-1])
  self.p=0
 def seekable(self):return True
 def readable(self):return True
 def tell(self):return self.p
 def seek(self,x,w=0):
  self.p=x+(self.p if w==1 else self.n if w==2 else 0);return self.p
 def read(self,n=-1):
  n=min(self.n-self.p,n if n>=0 else self.n-self.p)
  if n<=0:return b""
  a=self.p;self.p+=n
  with u.urlopen(u.Request(U,headers={"Range":f"bytes={a}-{a+n-1}"})) as r:return r.read(n)
o={"run":"E002-220","status":"blocked","subjects":[],"errors":[]}
try:
 with zipfile.ZipFile(R()) as z:
  a=z.infolist();o["entries"]=len(a)
  for p in ("P_33","P_54"):
   q=[x for x in a if f"/{p}/" in "/"+x.filename]
   o["subjects"].append({"id":p,"candidates":[{"name":x.filename,"size":x.file_size,"crc":x.CRC} for x in q if x.filename.endswith((".webm",".txt"))][:35]})
  o["status"]="manifest_complete"
except Exception as e:o["errors"].append(str(e)[:250])
Path("research/e002-220/RESULTS.json").write_text(json.dumps(o,indent=2))
print(o["status"],o["errors"],len(o["subjects"]))
