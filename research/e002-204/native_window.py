import csv,io,json,math,statistics,zipfile,hashlib
from pathlib import Path
from importlib.util import spec_from_file_location,module_from_spec
P=Path(__file__).resolve().parent
s=spec_from_file_location("raw",P.parent/"e002-203/raw_semantics.py")
raw=module_from_spec(s);s.loader.exec_module(raw)
def trial(buf):
 a=list(csv.DictReader(io.StringIO(buf.decode("utf-8-sig")),delimiter="\t"))
 h=list(a[0]);tc=next((raw.get(h,k) for k in ("system_timestamp","device_timestamp","timestamp") if raw.get(h,k)),None)
 if not tc or len(a)<600:raise ValueError("TIMESTAMP_OR_LENGTH")
 ts=[float(r[tc]) for r in a];ds=[b-a for a,b in zip(ts,ts[1:])]
 if min(ds)<=0:raise ValueError("NONMONOTONIC")
 d=statistics.median(ds)
 u=1e6 if 6000<d<11000 else 1 if .006<d<.011 else 1e3 if 6<d<11 else 1e9 if 6e6<d<11e6 else None
 if u is None:raise ValueError("TIME_UNIT")
 t=[(v-ts[0])/u for v in ts];w=[i for i,v in enumerate(t) if v<5]
 out={"n":len(a),"eyes":{}}
 for eye in ("left","right"):
  pc=raw.get(h,eye+"_pupil_valid");gc=raw.get(h,eye+"_gaze_point_valid");dc=raw.get(h,eye+"_pupil_diameter")
  if not all((pc,gc,dc)):raise ValueError("PUPIL_FIELDS")
  p=[raw.truth(r[pc]) for r in a];g=[raw.truth(r[gc]) for r in a]
  good=[]
  for r,v in zip(a,p):
   try:z=float(r[dc]);good.append(v and math.isfinite(z) and 0<z<=10)
   except ValueError:good.append(False)
  ix=[i for i in w if good[i]]
  gap=max((t[b]-t[a] for a,b in zip(ix,ix[1:])),default=None)
  out["eyes"][eye]={"pupil_valid":sum(p),"gaze_valid":sum(g),"positive_pupil":sum(good),
    "window_n":len(w),"window_valid":len(ix),"max_gap":gap,
    "pass":len(w)>=570 and len(ix)>=570 and len(ix)/len(w)>=.95 and gap is not None and gap<=.026}
 return out
def main():
 z=Path("e203_dataset.zip");m=Path("e203_data_loss_per_trial.csv")
 if not z.exists() or not m.exists():raise ValueError("ORIGINAL_SOURCES_MISSING")
 idx={(r["pid"],r["trial"],r["eye"]):r for r in csv.DictReader(m.open(encoding="utf-8-sig"))}
 out={"rgb_waveform":"NOT_TESTED","people":{},"errors":[]}
 with zipfile.ZipFile(z) as f:
  names=f.namelist()
  for j in range(1,16):
   pid=f"participant_{j:03d}"
   match=[n for n in names if "/"+pid+"/" in "/"+n and n.endswith("/image_01_1.tsv")]
   if len(match)!=1:out["errors"].append([pid,"SELECTION"]);continue
   b=f.read(match[0])
   try:
    r=trial(b);r["sha256"]=hashlib.sha256(b).hexdigest()
    for eye,e in r["eyes"].items():
     x=idx[(pid,"image_01_1",eye)];v=int(x["n_valid_trial_samples"])
     e["metadata_matches"]={k:v==e[k] for k in ("pupil_valid","gaze_valid","positive_pupil")}
    out["people"][pid]=r
   except Exception as ex:out["errors"].append([pid,repr(ex)])
 dest=P/"results";dest.mkdir(exist_ok=True)
 (dest/"NATIVE_WINDOW.json").write_text(json.dumps(out,indent=2)+"\n")
 print(json.dumps({"participants":len(out["people"]),"errors":out["errors"]}))
 if out["errors"] or len(out["people"])!=15:raise SystemExit("INCOMPLETE_HUMAN")
if __name__=="__main__":main()
