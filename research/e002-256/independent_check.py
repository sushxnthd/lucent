#!/usr/bin/env python3
"""Independent reconstruction from uncentered group moments; no video claims."""
import csv,io,json,math,pathlib
from decompose import fetch
result=json.loads(pathlib.Path("research/e002-256/CI_RESULTS.json").read_text())
for eye in ("left","right"):
    raw,_=fetch(eye); rows=list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    N=0; SX=SY=SXX=SYY=SXY=WXY=WXX=WYY=0.
    for q in rows:
        n=int(q["n"]);ym=float(q["gt_mean_mm"]);xm=ym+float(q["bias_mm"])
        sy=float(q["gt_std_mm"]);sx=float(q["pred_std_mm"]);r=float(q["pearson_r"])
        N+=n;SX+=n*xm;SY+=n*ym
        SXX+=(n-1)*sx*sx+n*xm*xm
        SYY+=(n-1)*sy*sy+n*ym*ym
        SXY+=(n-1)*r*sx*sy+n*xm*ym
        WXY+=(n-1)*r*sx*sy;WXX+=(n-1)*sx*sx;WYY+=(n-1)*sy*sy
    C=SXY-SX*SY/N;VX=SXX-SX*SX/N;VY=SYY-SY*SY/N
    checks={"pooled_r_reconstructed":C/math.sqrt(VX*VY),"participant_centered_r":WXY/math.sqrt(WXX*WYY),"between_fraction_of_pooled_covariance":(C-WXY)/C}
    for k,v in checks.items():
        if abs(v-result[eye][k])>1e-9: raise AssertionError(f"INDEPENDENT_FAIL {eye} {k}")
print("INDEPENDENT_CHECK_PASS both eyes; source fetched and independently reconstructed")
