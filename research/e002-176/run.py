#!/usr/bin/env python3
"""E002-176: original-human tracker-only ideal sampling experiment. NOT RGB validation."""
import csv,hashlib,io,json,math,re,sys,time,urllib.request,zipfile
from pathlib import Path
import numpy as np
from scipy.signal import butter,sosfiltfilt,periodogram
URL="https://zenodo.org/records/20300972/files/dataset.zip?download=1"
MD5="5e04a7b5e50f7508775e1daea527246b"
base=Path("research/e002-176");out=base/"results";out.mkdir(parents=True,exist_ok=True)
src=Path("dataset.zip")
def digest(path,kind):
 h=hashlib.new(kind)
 with path.open("rb") as f:
  for b in iter(lambda:f.read(8*1024*1024),b""):h.update(b)
 return h.hexdigest()
if not src.exists():
 for attempt in range(3):
  try:
   req=urllib.request.Request(URL,headers={"User-Agent":"Lucent-E002-176-science"})
   with urllib.request.urlopen(req,timeout=120) as r,src.open("wb") as f:
    while True:
     b=r.read(8*1024*1024)
     if not b:break
     f.write(b)
   break
  except Exception as e:
   print("download failure",attempt+1,repr(e),flush=True)
   src.unlink(missing_ok=True);time.sleep(5*(attempt+1))
 else:raise RuntimeError("DOWNLOAD_FAILED_3X")
md5=digest(src,"md5");sha=digest(src,"sha256")
if md5!=MD5:raise RuntimeError("ARCHIVE_MD5_MISMATCH:"+md5)
def col(headers,aliases):
 d={re.sub("[^a-z0-9]","",s.lower()):s for s in headers}
 return next((d[a] for a in aliases if a in d),None)
def read(f):
 rd=csv.DictReader(io.TextIOWrapper(f,encoding="utf-8-sig",newline=""),delimiter="\t")
 if not rd.fieldnames:raise ValueError("NO_HEADER")
 t=col(rd.fieldnames,["systemtimestamp","devicetimestamp","timestamp"])
 l=col(rd.fieldnames,["leftpupildiameter","pupildiameterleft","leftpupildiametermm"])
 r=col(rd.fieldnames,["rightpupildiameter","pupildiameterright","rightpupildiametermm"])
 lv=col(rd.fieldnames,["leftpupilvalidity","leftpupildiametervalidity","pupilvalidityleft"])
 rv=col(rd.fieldnames,["rightpupilvalidity","rightpupildiametervalidity","pupilvalidityright"])
 if not all([t,l,r,lv,rv]):raise ValueError("AMBIGUOUS_SCHEMA:"+str(rd.fieldnames[:70]))
 rows=[]
 for row in rd:
  try:rows.append((float(row[t]),float(row[l]),float(row[r]),row[lv].strip().lower(),row[rv].strip().lower()))
  except (ValueError,TypeError,KeyError):continue
 if len(rows)<120:raise ValueError("TOO_FEW_ROWS")
 ts=np.array([x[0] for x in rows]);delta=np.diff(ts)
 if not np.all(delta>0):raise ValueError("NONMONOTONIC_TIMESTAMPS")
 m=np.median(delta)
 if 6000<m<11000:unit=1e6
 elif .006<m<.011:unit=1
 elif 6<m<11:unit=1e3
 elif 6e6<m<11e6:unit=1e9
 else:raise ValueError("UNKNOWN_TIME_UNIT:"+str(m))
 ts=(ts-ts[0])/unit
 if not 1/140<np.median(np.diff(ts))<1/100:raise ValueError("NOT_120_HZ")
 tokens={x[3] for x in rows}|{x[4] for x in rows}
 if not tokens.issubset({"0","1","0.0","1.0","true","false"}):raise ValueError("AMBIGUOUS_VALIDITY:"+str(tokens))
 valid=lambda v:v in ("1","1.0","true")
 y=np.array([(x[1]+x[2])/2 if valid(x[3]) and valid(x[4]) and 1<=x[1]<=10 and 1<=x[2]<=10 else np.nan for x in rows])
 return ts,y,{"columns":[t,l,r,lv,rv],"n":len(rows),"valid_fraction":float(np.isfinite(y).mean()),"median_dt":float(np.median(np.diff(ts)))}
def evaluate(ts,y):
 total=int(np.floor((ts[-1]+1/120)/5));wins=[];rejections={}
 sos=butter(4,5,fs=120,btype="low",output="sos")
 for k in range(total):
  select=(ts>=k*5)&(ts<(k+1)*5);t=ts[select];v=y[select];good=np.isfinite(v);reason=None
  if len(t)<570:reason="few_samples"
  elif good.mean()<.95:reason="invalid_gt_5pct"
  elif np.max(np.diff(t[good]))>3/120+.001:reason="long_gap"
  elif np.nanstd(v)<1e-4:reason="constant"
  if reason:
   rejections[reason]=rejections.get(reason,0)+1;continue
  grid=k*5+np.arange(600)/120
  ref=sosfiltfilt(sos,np.interp(grid,t[good],v[good]))
  if np.std(ref[24:-24])<1e-4:
   rejections["constant_filtered"]=rejections.get("constant_filtered",0)+1;continue
  rr=[]
  for phase in range(4):
   idx=np.arange(phase,600,4);pred=np.interp(np.arange(600),idx,ref[idx])
   rr.append(float(np.corrcoef(ref[24:-24],pred[24:-24])[0,1]))
  ff,pp=periodogram(np.interp(grid,t[good],v[good]),fs=120,detrend="linear",window="hann")
  fraction=float(pp[(ff>0)&(ff<=5)].sum()/max(pp[(ff>0)&(ff<=60)].sum(),1e-16))
  wins.append({"window":k,"r_phases":rr,"worst_r":min(rr),"low5_power_fraction":fraction,"pass":min(rr)>=.90})
 return total,wins,rejections
result={"run":"E002-176","source_url":URL,"source_md5":md5,"source_sha256":sha,"participants":{},"failures":{},"selection":{}}
with zipfile.ZipFile(src) as z:
 names=z.namelist()
 for i in range(1,16):
  pid=f"participant_{i:03d}"
  members=[n for n in names if ("/"+pid+"/") in ("/"+n) and n.lower().endswith("/image_01_1.tsv")]
  if len(members)!=1:result["failures"][pid]="MISSING_OR_MULTIPLE";continue
  result["selection"][pid]=members[0]
  try:
   with z.open(members[0]) as f:ts,y,meta=read(f)
   total,wins,rejected=evaluate(ts,y)
   result["participants"][pid]={"meta":meta,"total_windows":total,"accepted_windows":len(wins),"rejected":rejected,"windows":wins}
  except Exception as e:result["failures"][pid]=repr(e)
parts=list(result["participants"].values());ww=[w for p in parts for w in p["windows"]]
total=sum(p["total_windows"] for p in parts)
coverage=len(ww)/total if total else 0
passing=sum(w["pass"] for w in ww)/len(ww) if ww else 0
rng=np.random.default_rng(1762026);boots=[]
if ww:
 for _ in range(3000):
  chosen=rng.choice(len(parts),len(parts),replace=True)
  sample=[w for j in chosen for w in parts[int(j)]["windows"]]
  if sample:boots.append(sum(w["pass"] for w in sample)/len(sample))
ci=np.quantile(boots,[.025,.975]).tolist() if boots else [None,None]
result["summary"]={"participants_parsed":len(parts),"total_windows":total,"accepted_windows":len(ww),"eligible_coverage":coverage,"pass_fraction":passing,"bootstrap_ci95":ci,"sampling_only_success":len(parts)>=8 and coverage>=.7 and passing>=.9 and ci[0] is not None and ci[0]>=.8,"physiological_rgb_gate":"NOT_TESTED","primary_paired_data_gate":"NOT_TESTED"}
(out/"RESULTS.json").write_text(json.dumps(result,indent=2))
(out/"SOURCE_MANIFEST.json").write_text(json.dumps({"url":URL,"md5":md5,"sha256":sha,"bytes":src.stat().st_size,"selected_members":result["selection"]},indent=2))
print(json.dumps({"summary":result["summary"],"failures":result["failures"],"selection":result["selection"]},indent=2),flush=True)
if len(parts)<8:sys.exit(2)
