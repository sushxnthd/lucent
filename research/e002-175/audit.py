#!/usr/bin/env python3
"""E002-175: source-byte-verified MCFW-Gaze quality metadata audit."""
import csv, hashlib, io, json, pathlib, urllib.request
ROOT=pathlib.Path(__file__).resolve().parent
FILES={
"data_loss_per_trial.csv":"369d9446b62fd00888a6d51e152697bd",
"data_quality_validation.csv":"ec1d4b585300d9de18142ea54bdaeaeb"
}
BASE="https://zenodo.org/records/20300972/files/"
def get_file(name,md5):
    path=ROOT/name
    if not path.exists():
        req=urllib.request.Request(BASE+name+"?download=1",headers={"User-Agent":"Lucent-Research/1.0"})
        with urllib.request.urlopen(req,timeout=90) as response: path.write_bytes(response.read())
    data=path.read_bytes()
    got=hashlib.md5(data).hexdigest()
    if got!=md5: raise RuntimeError("SOURCE_HASH_MISMATCH "+name+" "+got)
    return data
def rows(data): return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))
def check_fraction(records,key):
    bad=[]; finite=0; missing=0; mn=float("inf"); mx=float("-inf")
    for i,r in enumerate(records):
        value=r.get(key,"")
        if value is None or not value.strip(): missing+=1;continue
        x=float(value);finite+=1;mn=min(mn,x);mx=max(mx,x)
        if not (0<=x<=1) and len(bad)<8: bad.append({"row":i+2,"participant":r.get("pid"),"trial":r.get("trial"),"eye":r.get("eye"),"value":x})
    violations=sum(bool(r.get(key,"").strip()) and not (0<=float(r[key])<=1) for r in records)
    return {"total":len(records),"finite":finite,"missing":missing,"violations":violations,"min":mn if finite else None,"max":mx if finite else None,"examples":bad}
def run():
    raw={k:get_file(k,v) for k,v in FILES.items()}
    a=rows(raw["data_loss_per_trial.csv"]);b=rows(raw["data_quality_validation.csv"])
    result={"run":"E002-175","source":"Zenodo 20300972 v3","n_trial_rows":len(a),"n_quality_rows":len(b),"n_trial_participants":len(set(x["pid"] for x in a)),"n_quality_participants":len(set(x["pid"] for x in b)),"hashes":{k:{"md5":hashlib.md5(v).hexdigest(),"sha256":hashlib.sha256(v).hexdigest(),"bytes":len(v)} for k,v in raw.items()}}
    result["fraction_checks"]={}
    for key in ("prop_invalid_samples","prop_missing_data"):
        result["fraction_checks"][key]=check_fraction(a,key)
    for key in ("Prop_data_loss_left_eye","Prop_data_loss_right_eye"):
        result["fraction_checks"][key]=check_fraction(b,key)
    wrong=[]; nonpositive=[]; invalid_counts=[]
    for i,r in enumerate(a):
        n=int(r["n_trial_samples"]); v=int(r["n_valid_trial_samples"])
        if n<=0: nonpositive.append(i+2);continue
        if v<0 or v>n: invalid_counts.append(i+2)
        if abs(float(r["prop_invalid_samples"])-(n-v)/n)>1e-10:wrong.append(i+2)
    result["count_identity"]={"failures":len(wrong),"examples":wrong[:8],"nonpositive_n":len(nonpositive),"invalid_count_bounds":len(invalid_counts)}
    result["frozen_gate_pass"]=all(x["violations"]==0 for x in result["fraction_checks"].values()) and not wrong and not invalid_counts
    result["scientific_scope"]="published metadata numeric validity only; no original waveform or RGB"
    (ROOT/"RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("hashes","fraction_checks")},indent=2))
    print("fraction violations", {k:v["violations"] for k,v in result["fraction_checks"].items()})
if __name__=="__main__":run()
