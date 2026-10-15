#!/usr/bin/env python3
"""E002-214: exact source-blob pinned participant-level frontier. Stdlib only."""
import argparse, csv, hashlib, io, json, math, pathlib, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
SOURCE_COMMIT = "aa9bddf498a3b6e4104c2c000d2cc0c06a816aae"
SOURCE_REPO = "CondadosAI/pupil-diameter-webcam"
EXPECTED = {"left": "509e14d61455dc6ee119a0fc2ba9e7448eedc9fc", "right": "9f55dd52fc6c11c9903ec9c7b0c735192cd4a790"}
THRESHOLDS = [0, .3, .4, .5, .6, .65, .7, .75, .8, .85, .9]

def fetch(eye):
    url = "https://raw.githubusercontent.com/" + SOURCE_REPO + "/" + SOURCE_COMMIT + "/output/per_participant_" + eye + "_eye.csv"
    raw = urllib.request.urlopen(url, timeout=45).read()
    blob = hashlib.sha1(("blob %d\\0" % len(raw)).encode().replace(b"\\0", b"\x00") + raw).hexdigest()
    if blob != EXPECTED[eye]:
        raise RuntimeError("SOURCE_BLOB_MISMATCH " + eye + " " + blob)
    data = list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))
    out = {}
    for row in data:
        p = int(row["participant"])
        if p in out:
            raise ValueError("duplicate participant")
        out[p] = {k: float(v) for k,v in row.items() if k != "participant"}
    return out, {"url":url,"git_blob_sha1":blob,"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw)}

def calculate(left, right):
    ids = sorted(left)
    if ids != sorted(right) or len(ids) != 51:
        raise ValueError("participant alignment / count")
    rows = []
    for p in ids:
        l, r = left[p], right[p]
        lr, rr = l["pearson_r"], r["pearson_r"]
        la = l["pred_std_mm"] / l["gt_std_mm"]
        ra = r["pred_std_mm"] / r["gt_std_mm"]
        rows.append({"participant":p,"best_r":max(lr,rr),"both_r":min(lr,rr),"left_r":lr,"right_r":rr,"left_amp_ratio":la,"right_amp_ratio":ra})
    frontier = [{"min_r":t,"any_eye":sum(x["best_r"]>=t for x in rows),"both_eyes":sum(x["both_r"]>=t for x in rows)} for t in THRESHOLDS]
    both_metrics = sum((x["left_r"]>=.7 and .75<=x["left_amp_ratio"]<=1.25) or (x["right_r"]>=.7 and .75<=x["right_amp_ratio"]<=1.25) for x in rows)
    result = {
      "run":"E002-214","source_repo":SOURCE_REPO,"source_commit":SOURCE_COMMIT,
      "source_blob_sha_left":EXPECTED["left"],"source_blob_sha_right":EXPECTED["right"],
      "participants":len(ids),"source_rows_left":sum(int(left[p]["n"]) for p in ids),"source_rows_right":sum(int(right[p]["n"]) for p in ids),
      "thresholds_are_exploratory":True,"frontier":frontier,
      "threshold_75pct_oracle_r":sorted((x["best_r"] for x in rows),reverse=True)[math.ceil(.75*len(ids))-1],
      "required_participants_75pct":math.ceil(.75*len(ids)),
      "diagnostic_r07_oracle":sum(x["best_r"]>=.7 for x in rows),
      "diagnostic_r07_both":sum(x["both_r"]>=.7 for x in rows),
      "diagnostic_r07_and_amp075_125_oracle":both_metrics,
      "negative_r_left":sum(x["left_r"]<0 for x in rows),
      "negative_r_right":sum(x["right_r"]<0 for x in rows),
      "limitations":["Third-party derived per-participant aggregates; original images and checkpoint not rerun.","Checkpoint training split undocumented; possible in-sample overlap.","Correlations pooled across multiple three-second stimulus trials, not continuous five-second waveforms.","No native RGB/tracker timestamp or clock uncertainty; no lag, NRMSE, glasses, lighting or device holdout.","Thresholds 0.7 and amplitude 0.75-1.25 are exploratory diagnostics, not Lucent frozen human gates."]
    }
    return result, rows

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",default=str(ROOT/"ci_output"))
    args=ap.parse_args()
    out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True)
    l,lh=fetch("left");r,rh=fetch("right")
    result,rows=calculate(l,r)
    expected=json.loads((ROOT/"RESULTS.json").read_text())
    if result != expected:
        raise AssertionError("FROZEN_RESULT_MISMATCH")
    (out/"results.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    (out/"provenance.json").write_text(json.dumps({"left":lh,"right":rh},indent=2,sort_keys=True)+"\n")
    with (out/"derived_participant.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print("PASS_E002_214",result["diagnostic_r07_oracle"],"/51",result["threshold_75pct_oracle_r"])

if __name__=="__main__":main()
