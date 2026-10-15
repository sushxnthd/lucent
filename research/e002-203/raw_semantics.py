#!/usr/bin/env python3
"""E002-203 raw TSV validity-semantic audit. NOT RGB or fatigue validation."""
import csv,hashlib,io,json,math,re,urllib.request,zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parent
ARCHIVE_URL="https://zenodo.org/records/20300972/files/dataset.zip?download=1"
META_URL="https://zenodo.org/records/20300972/files/data_loss_per_trial.csv?download=1"
ARCHIVE_MD5="5e04a7b5e50f7508775e1daea527246b"
META_MD5="369d9446b62fd00888a6d51e152697bd"
def fetch(url,path,expected_md5):
 if not path.exists():
  req=urllib.request.Request(url,headers={"User-Agent":"Lucent-E002-203-provenance"})
  with urllib.request.urlopen(req,timeout=180) as r,path.open("wb") as f:
   for b in iter(lambda:r.read(8*1024*1024),b""):f.write(b)
 h=hashlib.md5();s=hashlib.sha256()
 with path.open("rb") as f:
  for b in iter(lambda:f.read(8*1024*1024),b""):h.update(b);s.update(b)
 if h.hexdigest()!=expected_md5:raise ValueError("MD5_MISMATCH:"+path.name+":"+h.hexdigest())
 return {"url":url,"md5":h.hexdigest(),"sha256":s.hexdigest(),"bytes":path.stat().st_size}
def normalized(s):return re.sub("[^a-z0-9]","",s.lower())
def get(headers,stem):
 d={normalized(h):h for h in headers}
 return d.get(normalized(stem))
def truth(v):
 t=str(v).strip().lower()
 if t in ("true","1","1.0"):return True
 if t in ("false","0","0.0"):return False
 raise ValueError("UNKNOWN_BOOLEAN_TOKEN:"+repr(t))
def count_raw(raw,eye):
 rows=list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig")),delimiter="\t"))
 if not rows:raise ValueError("NO_TSV_ROWS")
 names=list(rows[0]);pupil=get(names,eye+"_pupil_valid")
 gaze=get(names,eye+"_gaze_point_valid")
 diam=get(names,eye+"_pupil_diameter")
 pavail=get(names,eye+"_pupil_available")
 gavail=get(names,eye+"_gaze_point_available")
 if not all((pupil,gaze,diam)):raise ValueError("MISSING_FIELDS:"+str((eye,names[:70])))
 counts={"pupil_valid":0,"gaze_point_valid":0,"pupil_valid_finite_positive_diameter":0}
 if pavail:counts["pupil_available"]=0
 if gavail:counts["gaze_point_available"]=0
 for row in rows:
  p=truth(row[pupil]);g=truth(row[gaze]);counts["pupil_valid"]+=p;counts["gaze_point_valid"]+=g
  try:d=float(row[diam]);ok=math.isfinite(d) and 0<d<10
  except (ValueError,TypeError):ok=False
  counts["pupil_valid_finite_positive_diameter"]+=p and ok
  if pavail:counts["pupil_available"]+=truth(row[pavail])
  if gavail:counts["gaze_point_available"]+=truth(row[gavail])
 return len(rows),counts,{"pupil_valid":pupil,"gaze_point_valid":gaze,"pupil_diameter":diam,"pupil_available":pavail,"gaze_point_available":gavail}
def main():
 outdir=BASE/"results";outdir.mkdir(exist_ok=True)
 meta_path=Path("e203_data_loss_per_trial.csv");zip_path=Path("e203_dataset.zip")
 sources={"metadata":fetch(META_URL,meta_path,META_MD5),"archive":fetch(ARCHIVE_URL,zip_path,ARCHIVE_MD5)}
 mr=list(csv.DictReader(meta_path.open(encoding="utf-8-sig",newline="")))
 index={(r["pid"],r["trial"],r["eye"]):r for r in mr}
 result={"run":"E002-203-original-tsv-semantics","sources":sources,"selected":[],"errors":[],"source_to_pupil_semantics":"UNRESOLVED","rgb_waveform":"NOT_TESTED"}
 with zipfile.ZipFile(zip_path) as z:
  names=z.namelist()
  for i in range(1,16):
   pid=f"participant_{i:03d}"
   matches=[name for name in names if ("/"+pid+"/") in ("/"+name) and name.endswith("/image_01_1.tsv")]
   if len(matches)!=1:result["errors"].append([pid,"FILE_SELECTION",matches]);continue
   path=matches[0];raw=z.read(path)
   for eye in ("left","right"):
    expected=index.get((pid,"image_01_1",eye))
    if not expected:result["errors"].append([pid,eye,"MISSING_METADATA"]);continue
    try:n,counts,cols=count_raw(raw,eye)
    except Exception as e:result["errors"].append([pid,eye,repr(e)]);continue
    n_meta=int(expected["n_trial_samples"]);valid_meta=int(expected["n_valid_trial_samples"])
    result["selected"].append({"pid":pid,"eye":eye,"path":path,"tsv_sha256":hashlib.sha256(raw).hexdigest(),"n_tsv":n,"n_metadata":n_meta,"valid_metadata":valid_meta,"counts":counts,"fields":cols,"n_equal":n==n_meta,"matches":{k:n==n_meta and v==valid_meta for k,v in counts.items()}})
 summary={}
 for key in ("pupil_valid","gaze_point_valid","pupil_valid_finite_positive_diameter","pupil_available","gaze_point_available"):
  eligible=[r for r in result["selected"] if key in r["counts"]]
  summary[key]={"available_rows":len(eligible),"exact_matches":sum(r["matches"][key] for r in eligible),"disagreements":len(eligible)-sum(r["matches"][key] for r in eligible)}
 result["summary"]=summary;result["rows_compared"]=len(result["selected"])
 result["source_to_pupil_semantics"]="PUPIL_VALID_MATCHED" if summary["pupil_valid"]["exact_matches"]==30 and not result["errors"] else "PUPIL_VALID_NOT_ESTABLISHED"
 (outdir/"RAW_VALIDITY_AUDIT.json").write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps({"rows_compared":result["rows_compared"],"errors":result["errors"],"summary":summary,"semantics":result["source_to_pupil_semantics"]},indent=2),flush=True)
 if result["rows_compared"]!=30 or result["errors"]:raise SystemExit("INCOMPLETE_RAW_SEMANTICS")
if __name__=="__main__":main()
