#!/usr/bin/env python3
"""E002-394 independent oracle: reparse raw CSV without importing primary module."""
import argparse
import csv
import hashlib
import io
import json
import math
import zipfile

EXPECTED_MD5="fef02cb7ebf62e4f3efb6303284fd6cb"

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--archive",required=True)
    p.add_argument("--result",required=True)
    a=p.parse_args()
    h=hashlib.md5()
    with open(a.archive,"rb") as f:
        while True:
            chunk=f.read(1<<20)
            if not chunk:break
            h.update(chunk)
    assert h.hexdigest()==EXPECTED_MD5,"unverified source"
    r=json.load(open(a.result))
    assert r["source_verified"] and r["product_decision"]=="ABSTAIN_UNCALIBRATED"
    with zipfile.ZipFile(a.archive) as z:
        files=[n for n in z.namelist() if n.endswith("_sync.csv")]
        assert len(files)==1
        with z.open(files[0]) as f:
            reader=csv.DictReader(io.TextIOWrapper(f,encoding="utf-8-sig"))
            ts=[];markers=[];nrows=0
            for row in reader:
                nrows+=1
                if row["PhanFrame"].strip() and row["Time"].strip():
                    ts.append((int(float(row["PhanFrame"])),float(row["Time"])))
                if row["Blinks"].strip() and float(row["Blinks"])>0:
                    markers.append(float(row["Time"]))
    assert len(ts)==r["distinct_phantom_frames"]
    assert nrows==r["sync_rows"]
    assert len(markers)==r["marker_count"]
    for threshold in (15,20,30,50):
        valid=[(f1-f0,t1-t0) for (f0,t0),(f1,t1) in zip(ts,ts[1:]) if 0<t1-t0<=threshold/1000]
        observed=sum(x for x,y in valid)/sum(y for x,y in valid)
        report=r["EEG_gap_sensitivity"][f"{threshold}ms"]
        assert math.isclose(observed,report["active_fps"],abs_tol=1e-8)
    gaps=[(t0,t1) for (_,t0),(_,t1) in zip(ts,ts[1:]) if t1-t0>.020]
    eligible=[t for t in markers if ts[0][1]<=t<=ts[-1][1] and
              not any(lo<t<hi for lo,hi in gaps)]
    assert len(eligible)==r["eligible_markers"]
    for hz,ms in ((30,1),(30,5),(60,5),(120,10)):
        T=1/hz
        counts=[]
        for k in range(100):
            phase=(k+.5)*T/100
            counts.append(sum(1 for t in eligible if (t-phase)%T < ms/1000))
        value=sum(counts)/(100*len(eligible))
        reported=r["hypothetical_shutter_marker_coverage"][f"{hz}Hz_{ms}ms"]
        assert abs(value-reported["mean_phase_capture_fraction"])<1e-10
    print(json.dumps({"independent_oracle":"PASS","source_md5":h.hexdigest(),
        "frames":len(ts),"rows":nrows,"eligible_markers":len(eligible),
        "product":"ABSTAIN_UNCALIBRATED"}))

if __name__=="__main__":
    main()
