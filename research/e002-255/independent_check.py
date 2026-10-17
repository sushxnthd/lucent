#!/usr/bin/env python3
"""Independent checker with separately implemented gate logic and source retrieval."""
import csv,hashlib,io,json,math,pathlib,statistics,urllib.request
BASE="https://raw.githubusercontent.com/CondadosAI/pupil-diameter-webcam/aa9bddf498a3b6e4104c2c000d2cc0c06a816aae/output/"
PINS={"left":"509e14d61455dc6ee119a0fc2ba9e7448eedc9fc","right":"9f55dd52fc6c11c9903ec9c7b0c735192cd4a790"}
def fetch(eye):
    with urllib.request.urlopen(BASE+"per_participant_"+eye+"_eye.csv",timeout=40) as r: data=r.read()
    assert hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()==PINS[eye]
    return {int(x["participant"]):{k:float(v) for k,v in x.items() if k!="participant"} for x in csv.DictReader(io.StringIO(data.decode()))}
def nrmse(r):return 1. if r<=0 else math.sqrt(1-r*r)
def main():
    actual=json.loads(pathlib.Path("research/e002-255/CI_RESULTS.json").read_text())
    A=fetch("left");B=fetch("right")
    assert len(A)==len(B)==51 and set(A)==set(B)
    for eye,table in (("left",A),("right",B)):
        assert int(sum(x["n"] for x in table.values()))==actual[eye]["n_observations"]
        assert abs(statistics.median(x["pearson_r"] for x in table.values())-actual[eye]["median_participant_r"])<1e-12
        assert abs(statistics.median(nrmse(x["pearson_r"]) for x in table.values())-actual[eye]["median_oracle_positive_affine_nrmse"])<1e-12
        assert sorted(p for p,x in table.items() if x["pearson_r"]<0)==actual[eye]["negative_r_participants"]
    for t in [.4,.5,.6,.7,.8]:
        a={p for p,x in A.items() if nrmse(x["pearson_r"])<=t+1e-12}
        b={p for p,x in B.items() if nrmse(x["pearson_r"])<=t+1e-12}
        assert actual["exploratory_oracle_positive_affine_nrmse_sensitivity"][f"{t:.1f}"]=={"left":len(a),"right":len(b),"either":len(a|b),"both":len(a&b)}
    expected={"0.4":(0,0,0,0),"0.5":(2,2,4,0),"0.6":(16,11,16,11),"0.7":(30,26,34,22),"0.8":(41,35,42,34)}
    for t,z in expected.items():
        x=actual["exploratory_oracle_positive_affine_nrmse_sensitivity"][t]
        assert (x["left"],x["right"],x["either"],x["both"])==z
    print("INDEPENDENT HUMAN AGGREGATE CHECK PASSED")
if __name__=="__main__":main()
