"""Independent post-run consistency audit; no human inference."""
import csv,json,math,pathlib,statistics
root=pathlib.Path("research/e002-155")
result=json.loads((root/"RESULTS.json").read_text())
rows=list(csv.DictReader((root/"PAIRS.csv").open()))
T=-2*math.log(.95)
assert result["status"]=="ORIGINAL_HUMAN_MASKS_SCORED"
assert abs(result["threshold"]-T)<1e-14
for row in rows:
    de=float(row["dE"]);dd=float(row["dD"]);dp=float(row["dPn"]);dq=float(row["dq"])
    assert abs(dq-(dp-dd)/2)<1e-10
    assert int(row["frame2"])-int(row["frame1"])==int(row["lag"])
    assert math.isfinite(de+dd+dp+dq)
for lag in (1,5,15,30):
    r=[x for x in rows if int(x["lag"])==lag]
    recorded=result["summary"][str(lag)]
    assert len(r)==recorded["n_pairs"]
    if r:
        observed=sum(abs(float(x["dD"]))>T for x in r)/len(r)
        assert abs(observed-recorded["fraction_scale_normalized"])<1e-12
print("Independent E002-155 consistency checker PASS:",len(rows),"mask-derived pairs")
