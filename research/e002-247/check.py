import csv,io,json
from pathlib import Path
root=Path("research/e002-228")
d=json.loads((root/"E002_247_RAW.json").read_text())
rows=list(csv.DictReader(io.StringIO(d["raw_csv"])))
assert len(rows)==180
assert len({(r["participant"],r["frame"],r["eye"]) for r in rows})==180
groups={}
for p in ("P_01","P_02","P_07"):
 a=[r for r in rows if r["participant"]==p]
 accepted=[r for r in a if r["eligible"]=="1"]
 endpoint=[r for r in accepted if float(r["radius_ratio"]) in (0.20,0.78)]
 g=d["original_result"]["groups"][p]
 assert len(a)==60
 for eye in ("iris_468","iris_473"):
  assert sum(r["eligible"]=="1" for r in a if r["eye"]==eye)==g[eye]["admitted"]
 groups[p]={"observations":len(a),"admitted":len(accepted),"endpoint":len(endpoint),"interior":len(accepted)-len(endpoint),"endpoint_fraction":len(endpoint)/len(accepted) if accepted else None,"criterion":len(accepted)>=5 and 2*len(endpoint)>=len(accepted)}
out={"run":"E002-247","groups":groups,"replication":sum(v["criterion"] for v in groups.values())>=2,"reference_compared":False,"waveform_certified":False,"source_sha256":{p:d["source"]["participants"][p]["video"]["sha256"] for p in groups}}
(root/"E002_247_RESULTS.json").write_text(json.dumps(out,indent=2,sort_keys=True))
print("E002-247",json.dumps(out,sort_keys=True))
