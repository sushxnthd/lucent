#!/usr/bin/env python3
"""Post-hoc EyeDentify released-checkpoint human-summary calibration ceiling; NOT a holdout."""
import csv,hashlib,io,json,math,pathlib,statistics,urllib.request
COMMIT="aa9bddf498a3b6e4104c2c000d2cc0c06a816aae"
BASE="https://raw.githubusercontent.com/CondadosAI/pupil-diameter-webcam/"+COMMIT+"/output/"
PINS={"left":("per_participant_left_eye.csv","509e14d61455dc6ee119a0fc2ba9e7448eedc9fc"),
"right":("per_participant_right_eye.csv","9f55dd52fc6c11c9903ec9c7b0c735192cd4a790"),
"summary":("summary.json","4d51cd922ce11aa040cfc491bce09bab249d5ede")}
def read(which):
    filename,pin=PINS[which]
    with urllib.request.urlopen(BASE+filename,timeout=40) as r: raw=r.read()
    actual=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    assert actual==pin,(which,actual)
    return raw,{"git_blob_sha1":pin,"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw),"url":BASE+filename}
def parse(raw):
    return [{k:(int(v) if k in ("participant","n") else float(v)) for k,v in x.items()} for x in csv.DictReader(io.StringIO(raw.decode()))]
def bound(r): return math.sqrt(max(0.,1-r*r)) if r>0 else 1.
def calc(rows):
    assert len(rows)==51 and len({r["participant"] for r in rows})==51
    for x in rows: assert x["n"]>1 and x["gt_std_mm"]>0 and x["pred_std_mm"]>0 and -1<=x["pearson_r"]<=1
    return {"n_observations":sum(x["n"] for x in rows),
        "median_participant_r":statistics.median(x["pearson_r"] for x in rows),
        "median_oracle_positive_affine_nrmse":statistics.median(bound(x["pearson_r"]) for x in rows),
        "negative_r_participants":sorted(x["participant"] for x in rows if x["pearson_r"]<0),
        "r_ge_0p8":sum(x["pearson_r"]>=.8 for x in rows)}
def main():
    raw={};manifest={}
    for k in PINS:raw[k],manifest[k]=read(k)
    L=parse(raw["left"]);R=parse(raw["right"]);S=json.loads(raw["summary"])
    assert sum(x["n"] for x in L)==int(S["left_eye"]["n"])
    assert sum(x["n"] for x in R)==int(S["right_eye"]["n"])
    a={x["participant"]:x for x in L};b={x["participant"]:x for x in R}
    assert set(a)==set(b)
    out={"run":"E002-255","classification":"secondary_post_hoc_public_human_participant_aggregate_audit",
        "source_commit":COMMIT,"n_participants":51,"left":calc(L),"right":calc(R),
        "pooled_r":{"left":S["left_eye"]["pearson_r"],"right":S["right_eye"]["pearson_r"]},
        "exploratory_oracle_positive_affine_nrmse_sensitivity":{},
        "frozen_prospective_human_waveform":"NOT_RUN","independent_exposure_clock":"NOT_CERTIFIED"}
    for t in [.4,.5,.6,.7,.8]:
        A={p for p,x in a.items() if bound(x["pearson_r"])<=t+1e-12}
        B={p for p,x in b.items() if bound(x["pearson_r"])<=t+1e-12}
        out["exploratory_oracle_positive_affine_nrmse_sensitivity"][f"{t:.1f}"]={"left":len(A),"right":len(B),"either":len(A|B),"both":len(A&B)}
    target=pathlib.Path("research/e002-255")
    target.mkdir(parents=True,exist_ok=True)
    (target/"CI_RESULTS.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    (target/"CI_SOURCE_HASHES.json").write_text(json.dumps({"source_commit":COMMIT,"inputs":manifest},indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PINNED_SOURCE_VERIFIED","median_r_left":out["left"]["median_participant_r"],"median_r_right":out["right"]["median_participant_r"],"thresholds":out["exploratory_oracle_positive_affine_nrmse_sensitivity"]},sort_keys=True))
if __name__=="__main__":main()
