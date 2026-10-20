"""Primary synthetic tests: run python experiments.py. No human data."""
import json
import numpy as np
from model import fold_reference,wave,bias_coefficient
x=wave(1/3)
y=fold_reference(x)
assert np.max(abs(y-3))<1e-12
assert np.ptp(x[::3])>.39
A=np.zeros((90,270))
for j in range(90): A[j,[j,j+90,j+180]]=1/3
assert np.max(abs(A@A.T-np.eye(90)/3))==0
assert np.linalg.matrix_rank(A)==90
rng=np.random.default_rng(319)
err=0
for _ in range(1000):
    x=rng.normal(3,.2,270)
    err=max(err,abs(np.mean(fold_reference(x))-np.mean(x)))
assert err<1e-12
x=3+.1*np.arange(270)/90
y=fold_reference(x)
slope=np.polyfit(np.arange(90)/30,y,1)[0]
assert abs(slope/.1-1/3)<1e-12
for j in (0,45,89):
    x=3+.2*abs(np.arange(270)/90-j/30)
    assert abs(abs(fold_reference(x)[j]-x[3*j])-.2*bias_coefficient(j))<1e-12
out=dict(rank=90,nullity=180,slow_null_max_error_mm=float(np.max(abs(fold_reference(wave(1/3))-3))),native_peak_to_peak_mm=float(np.ptp(wave(1/3)[::3])),random_session_mean_max_error=err,linear_slope_ratio=float(slope/.1),B0=bias_coefficient(0),B45=bias_coefficient(45),B89=bias_coefficient(89),human_data="NOT RUN")
open("results.json","w").write(json.dumps(out,indent=2)+"\n")
print(out)
