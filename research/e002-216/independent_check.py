#!/usr/bin/env python3
"""Independent exact arithmetic, raw row, and mutation checker."""
import csv,json,math,pathlib
from fractions import Fraction as F
P=pathlib.Path(__file__).resolve().parent
def verify(path):
    d=json.loads(path.read_text())
    assert d["fold_map_shape"]==[90,270]
    assert d["exact_rank"]==90 and d["exact_nullity"]==180
    assert d["collision_max_abs_error"]<1e-12
    e=[F(1)-F(j,45) for j in range(90)]
    assert abs(d["ramp_start_error_seconds"]-float(e[0]))<1e-12
    assert abs(d["ramp_end_error_seconds"]-float(e[-1]))<1e-12
    assert abs(d["ramp_rmse_seconds"]-math.sqrt(sum(float(v*v) for v in e)/90))<1e-12
    rows=list(csv.DictReader((P/"RAW_SYNTHETIC.csv").open()))
    assert len(rows)==90
    for j,row in enumerate(rows):
        assert int(row["frame"])==j
        assert abs(float(row["error_s"])-float(e[j]))<1e-12
    f={round(v["f_hz"],8):v for v in d["frequencies"]}
    assert f[round(1/3,8)]["label_rms"]<1e-12
    assert f[round(1/3,8)]["perfect_webcam_r"] is None
    assert abs(f[1.0]["perfect_webcam_r"])<1e-12
    assert abs(f[1.0]["fold_gain"]-1)<1e-12
if __name__=="__main__":
    verify(P/"RESULTS.json")
    d=json.loads((P/"RESULTS.json").read_text());d["exact_nullity"]=179
    q=P/"_mutated.json";q.write_text(json.dumps(d))
    try:
        try:verify(q)
        except AssertionError:pass
        else:raise RuntimeError("Mutation not rejected")
    finally:q.unlink(missing_ok=True)
    print("Independent checker and mutation rejection PASS")
