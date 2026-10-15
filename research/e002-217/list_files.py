#!/usr/bin/env python3
"""Bounded, public-only Kaggle file-list audit; no data download."""
import datetime,hashlib,json,pathlib,urllib.request
url="https://www.kaggle.com/api/v1/datasets/list/vijuls/PupilDiameterDatasets"
out={"run":"E002-217","utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"url":url}
try:
    request=urllib.request.Request(url,headers={"User-Agent":"Lucent-Research-Provenance/1.0"})
    with urllib.request.urlopen(request,timeout=30) as f: b=f.read(5_000_001)
    if len(b)>5_000_000: raise ValueError("listing too large")
    j=json.loads(b)
    files=j.get("datasetFiles",j.get("files",[])) if isinstance(j,dict) else j
    out.update(status="ok",sha256=hashlib.sha256(b).hexdigest(),count=len(files),
               next_page_token=j.get("nextPageToken") if isinstance(j,dict) else None,
               files=[{"name":x.get("name"),"totalBytes":x.get("totalBytes"),"size":x.get("size")} for x in files[:200]])
except Exception as e:
    out.update(status="blocked",error={"type":type(e).__name__,"code":getattr(e,"code",None),"message":str(e)[:250]})
p=pathlib.Path("research/e002-217/FILE_LIST.json")
p.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps({"file_list_status":out["status"],"count":out.get("count"),"error":out.get("error")}))
