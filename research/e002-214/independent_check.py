#!/usr/bin/env python3
"""Independent verifier: fresh source read, independently recomputed oracle frontier."""
import csv, hashlib, io, json, math, pathlib, urllib.request
ROOT=pathlib.Path(__file__).resolve().parent
PIN="aa9bddf498a3b6e4104c2c000d2cc0c06a816aae"
EXPECTED={"left":"509e14d61455dc6ee119a0fc2ba9e7448eedc9fc","right":"9f55dd52fc6c11c9903ec9c7b0c735192cd4a790"}
def load(eye):
    url=f"https://raw.githubusercontent.com/CondadosAI/pupil-diameter-webcam/{PIN}/output/per_participant_{eye}_eye.csv"
    raw=urllib.request.urlopen(url,timeout=45).read()
    prefix=b"blob "+str(len(raw)).encode()+b"\x00"
    assert hashlib.sha1(prefix+raw).hexdigest()==EXPECTED[eye],"SOURCE_DRIFT"
    parsed=list(csv.DictReader(io.StringIO(raw.decode())))
    assert len(parsed)==51
    return {int(row["participant"]):row for row in parsed}
def verify(frozen,L,R):
    ids=set(L).intersection(R)
    assert len(ids)==51 and set(L)==set(R)
    best={p:max(float(L[p]["pearson_r"]),float(R[p]["pearson_r"])) for p in ids}
    worst={p:min(float(L[p]["pearson_r"]),float(R[p]["pearson_r"])) for p in ids}
    assert frozen["participants"]==51
    assert frozen["source_rows_left"]==sum(int(float(L[p]["n"])) for p in ids)
    assert frozen["source_rows_right"]==sum(int(float(R[p]["n"])) for p in ids)
    assert frozen["diagnostic_r07_oracle"]==len([p for p in ids if best[p]>=.7])
    assert frozen["diagnostic_r07_both"]==len([p for p in ids if worst[p]>=.7])
    assert frozen["negative_r_left"]==sum(float(L[p]["pearson_r"])<0 for p in ids)
    assert frozen["negative_r_right"]==sum(float(R[p]["pearson_r"])<0 for p in ids)
    target=math.ceil(.75*len(ids))
    assert frozen["required_participants_75pct"]==target
    assert abs(frozen["threshold_75pct_oracle_r"]-sorted(best.values(),reverse=True)[target-1])<1e-13
    for row in frozen["frontier"]:
        t=row["min_r"]
        assert row["any_eye"]==sum(v>=t for v in best.values())
        assert row["both_eyes"]==sum(v>=t for v in worst.values())
    def passes(p,eye):
        d=(L if eye=="left" else R)[p]
        return float(d["pearson_r"])>=.7 and .75<=float(d["pred_std_mm"])/float(d["gt_std_mm"])<=1.25
    assert frozen["diagnostic_r07_and_amp075_125_oracle"]==sum(passes(p,"left") or passes(p,"right") for p in ids)
    return True
if __name__=="__main__":
    L,R=load("left"),load("right")
    d=json.loads((ROOT/"RESULTS.json").read_text())
    verify(d,L,R)
    mutant=json.loads(json.dumps(d))
    mutant["diagnostic_r07_oracle"]+=1
    try:verify(mutant,L,R)
    except AssertionError:pass
    else:raise AssertionError("MUTATION_NOT_DETECTED")
    print("PASS_E002_214_INDEPENDENT_CHECK_AND_MUTATION")
