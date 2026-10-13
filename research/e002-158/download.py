import hashlib,pathlib,tempfile,requests
URL="https://zenodo.org/api/records/20492528"
SHA="049df72454682c1c77c50c8236bb607919a6e333528bc2b89c567b625e459700"
def get():
 s=requests.Session();r=s.get(URL,timeout=90);r.raise_for_status()
 f=next(x for x in r.json()["files"] if x["key"].endswith("segmentation_dataset.zip"))
 td=tempfile.TemporaryDirectory();p=pathlib.Path(td.name)/"source.zip"
 h=hashlib.sha256();m=hashlib.md5();n=0
 with s.get(f["links"].get("self") or f["links"]["download"],stream=True,timeout=(40,180)) as r:
  r.raise_for_status()
  with p.open("wb") as out:
   for b in r.iter_content(1048576):
    if b:
     n+=len(b)
     if n>200*1024**2:raise ValueError("archive cap")
     h.update(b);m.update(b);out.write(b)
 if h.hexdigest()!=SHA:raise ValueError("SHA mismatch")
 if f.get("checksum","").startswith("md5:") and m.hexdigest()!=f["checksum"][4:]:raise ValueError("MD5 mismatch")
 return td,p,{"source":URL,"sha256":h.hexdigest(),"md5":m.hexdigest(),"bytes":n,"upstream":f.get("checksum")}
