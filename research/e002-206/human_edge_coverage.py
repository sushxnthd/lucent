#!/usr/bin/env python3
"""E002-206 original-human same-eye reference admission; no RGB measurements."""
import csv, hashlib, io, json, math, statistics, zipfile
from pathlib import Path
P=Path(__file__).resolve().parent
def normalized(s):
    return "".join(c for c in s.lower() if c.isalnum())
def column(names, key):
    d={normalized(n):n for n in names}
    return d.get(normalized(key))
def valid_flag(s):
    if str(s).strip().lower() in ("1","1.0","true"):return True
    if str(s).strip().lower() in ("0","0.0","false"):return False
    raise ValueError("BAD_VALIDITY_TOKEN")
def one_trial(data,pid,metadata):
    rows=list(csv.DictReader(io.StringIO(data.decode("utf-8-sig")),delimiter="\t"))
    names=list(rows[0])
    tc=next((column(names,k) for k in ("system_timestamp","device_timestamp","timestamp") if column(names,k)),None)
    if tc is None:raise ValueError("NO_TIMESTAMP")
    stamps=[float(r[tc]) for r in rows]
    differences=[v-u for u,v in zip(stamps,stamps[1:])]
    if not differences or min(differences)<=0:raise ValueError("BAD_TIME")
    dt=statistics.median(differences)
    scale=1e6 if 6000<dt<11000 else 1 if .006<dt<.011 else 1e3 if 6<dt<11 else 1e9 if 6e6<dt<11e6 else None
    if scale is None:raise ValueError("UNKNOWN_TIME_UNIT")
    t=[(v-stamps[0])/scale for v in stamps]
    window=[i for i,v in enumerate(t) if 0<=v<5]
    if len(window)<570:raise ValueError("WINDOW_TOO_SHORT")
    result={"pid":pid,"tsv_sha256":hashlib.sha256(data).hexdigest(),
            "n":len(rows),"time_field":tc,"scale":scale,
            "times_s":[round(t[i],9) for i in window],"eyes":{}}
    for eye in ("left","right"):
        vc=column(names,eye+"_pupil_valid")
        dc=column(names,eye+"_pupil_diameter")
        if vc is None or dc is None:raise ValueError("PUPIL_FIELD_MISSING")
        flags=[valid_flag(r[vc]) for r in rows]
        expected=metadata[(pid,"image_01_1",eye)]
        if len(rows)!=int(expected["n_trial_samples"]) or sum(flags)!=int(expected["n_valid_trial_samples"]):
            raise ValueError("METADATA_PUPIL_SEMANTICS_MISMATCH")
        good=[]
        for r,v in zip(rows,flags):
            try:
                d=float(r[dc]);good.append(v and math.isfinite(d) and 0<d<=10)
            except (TypeError,ValueError):good.append(False)
        bits="".join("1" if good[i] else "0" for i in window)
        tv=[t[i] for i in window if good[i]]
        interior=max((v-u for u,v in zip(tv,tv[1:])),default=None)
        first=tv[0] if tv else None
        last=5-tv[-1] if tv else None
        fraction=len(tv)/len(window)
        old=len(window)>=570 and len(tv)>=570 and fraction>=.95 and interior is not None and interior<=.026
        repaired=bool(old and max(first,last,interior)<=.026)
        result["eyes"][eye]={"bits":bits,"valid_n":len(tv),"fraction":fraction,
            "first_gap_s":first,"last_gap_s":last,"interior_gap_s":interior,
            "old_pass":old,"complete_pass":repaired}
    return result
def main():
    archive=Path("e203_dataset.zip")
    metadata_file=Path("e203_data_loss_per_trial.csv")
    if not archive.exists() or not metadata_file.exists():raise ValueError("MISSING_ORIGINAL_SOURCES")
    with metadata_file.open(encoding="utf-8-sig",newline="") as f:
        metadata={(r["pid"],r["trial"],r["eye"]):r for r in csv.DictReader(f)}
    result={"run":"E002-206","participants":[],"errors":[],"rgb":"NOT_TESTED",
            "fatigue":"NOT_TESTED","source_archive_md5_expected":"5e04a7b5e50f7508775e1daea527246b",
            "frozen":{"window_s":5,"min_n":570,"valid_fraction":.95,"max_gap_s":.026}}
    with zipfile.ZipFile(archive) as z:
        names=z.namelist()
        for j in range(1,16):
            pid=f"participant_{j:03d}"
            paths=[x for x in names if "/"+pid+"/" in "/"+x and x.endswith("/image_01_1.tsv")]
            if len(paths)!=1:result["errors"].append([pid,"SELECTION"]);continue
            try:result["participants"].append(one_trial(z.read(paths[0]),pid,metadata))
            except Exception as ex:result["errors"].append([pid,str(ex)])
    for eye in ("left","right"):
        old=sum(p["eyes"][eye]["old_pass"] for p in result["participants"])
        new=sum(p["eyes"][eye]["complete_pass"] for p in result["participants"])
        result[eye]={"old_pass":old,"complete_pass":new,"edge_false_accept":old-new,
                     "product_75pct":len(result["participants"])==15 and new>=12}
    out=P/"results";out.mkdir(exist_ok=True)
    (out/"HUMAN_EDGE_COVERAGE.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"participants":len(result["participants"]),"errors":result["errors"],
                      "left":result["left"],"right":result["right"]}),flush=True)
    if result["errors"] or len(result["participants"])!=15:raise SystemExit("INCOMPLETE_HUMAN")
if __name__=="__main__":main()
