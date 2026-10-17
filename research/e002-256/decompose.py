#!/usr/bin/env python3
"""E002-256: exact covariance decomposition of pinned third-party human summaries."""
import csv,io,hashlib,json,math,pathlib,urllib.request
COMMIT="aa9bddf498a3b6e4104c2c000d2cc0c06a816aae"
PINS={"left":("per_participant_left_eye.csv","509e14d61455dc6ee119a0fc2ba9e7448eedc9fc"),"right":("per_participant_right_eye.csv","9f55dd52fc6c11c9903ec9c7b0c735192cd4a790"),"summary":("summary.json","4d51cd922ce11aa040cfc491bce09bab249d5ede")}
BASE="https://raw.githubusercontent.com/CondadosAI/pupil-diameter-webcam/"+COMMIT+"/output/"
def fetch(k):
    name,pin=PINS[k]
    with urllib.request.urlopen(urllib.request.Request(BASE+name,headers={"User-Agent":"Lucent-E002-256"}),timeout=35) as r: raw=r.read()
    sha=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    if sha!=pin: raise ValueError("SOURCE_IDENTITY_FAIL "+k)
    return raw,{"sha256":hashlib.sha256(raw).hexdigest(),"git_blob_sha1":sha,"url":BASE+name,"bytes":len(raw)}
def decompose(raw):
    rows=list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    assert len(rows)==51 and len({int(q["participant"]) for q in rows})==51
    n=sum(int(q["n"]) for q in rows)
    my=sum(int(q["n"])*float(q["gt_mean_mm"]) for q in rows)/n
    mx=sum(int(q["n"])*(float(q["gt_mean_mm"])+float(q["bias_mm"])) for q in rows)/n
    wx=wy=wxy=bx=by=bxy=0.
    for q in rows:
        m=int(q["n"]);sy=float(q["gt_std_mm"]);sx=float(q["pred_std_mm"]);r=float(q["pearson_r"])
        ym=float(q["gt_mean_mm"]);xm=ym+float(q["bias_mm"])
        wx+=(m-1)*sx*sx;wy+=(m-1)*sy*sy;wxy+=(m-1)*r*sx*sy
        bx+=m*(xm-mx)**2;by+=m*(ym-my)**2;bxy+=m*(xm-mx)*(ym-my)
    return {"n":n,"participants":len(rows),"pooled_r_reconstructed":(wxy+bxy)/math.sqrt((wx+bx)*(wy+by)),"participant_centered_r":wxy/math.sqrt(wx*wy),"between_participant_r":bxy/math.sqrt(bx*by),"between_fraction_of_pooled_covariance":bxy/(wxy+bxy),"between_fraction_of_prediction_variance":bx/(wx+bx),"between_fraction_of_reference_variance":by/(wy+by),"pooled_reference_sd":math.sqrt((wy+by)/(n-1)),"components":{"within_xy":wxy,"between_xy":bxy,"within_xx":wx,"between_xx":bx,"within_yy":wy,"between_yy":by}}
def main():
    raw={};manifest={}
    for k in PINS: raw[k],manifest[k]=fetch(k)
    summary=json.loads(raw["summary"])
    result={"run":"E002-256","source_commit":COMMIT,"classification":"posthoc third-party human participant aggregates, not untouched RGB video","five_second_waveform_tested":False}
    for k in ("left","right"):
        result[k]=decompose(raw[k]);r=result[k];s=summary[k+"_eye"]
        assert r["n"]==int(s["n"])
        assert abs(r["pooled_r_reconstructed"]-s["pearson_r"])<1e-10
        assert abs(r["pooled_reference_sd"]-s["gt_std_mm"])<1e-10
    dest=pathlib.Path("research/e002-256");dest.mkdir(parents=True,exist_ok=True)
    (dest/"CI_RESULTS.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    (dest/"CI_SOURCE_HASHES.json").write_text(json.dumps({"upstream":"CondadosAI/pupil-diameter-webcam","files":manifest},indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:{p:result[k][p] for p in ("pooled_r_reconstructed","participant_centered_r","between_fraction_of_pooled_covariance")} for k in ("left","right")},sort_keys=True))
if __name__=="__main__":main()
