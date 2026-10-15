import zipfile,hashlib,json
from pathlib import Path
from source import R
with zipfile.ZipFile(R()) as z:
 a=z.infolist()
 names=[x.filename for x in a]
 out={"run":"E002-220b","manifest_sha256":hashlib.sha256("\n".join(f"{x.filename}|{x.CRC}|{x.file_size}" for x in a).encode()).hexdigest(),"entries":len(a),"browser_log_search":{}}
 for prefix in ("1492456607850","1493129853898"):
  out["browser_log_search"][prefix]=[x.filename for x in a if prefix in x.filename and not x.filename.endswith((".webm",".mp4"))][:25]
 out["text_files"]=[x.filename for x in a if x.filename.endswith((".txt",".json",".csv"))][:110]
Path("research/e002-220/ROOT_LOGS.json").write_text(json.dumps(out,indent=2))
print(json.dumps({"matches":out["browser_log_search"],"text_count":len(out["text_files"])})[:4000])
