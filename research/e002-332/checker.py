"""Independent reproducibility checker of the public EyeDentify alignment core.
Synthetic data only. Run: python checker.py (numpy/pandas).
"""
import json
import numpy as np
import pandas as pd
from datetime import datetime
FS=90; N=270; M=90
base=1792540800000
timestamps=base+np.rint(np.arange(N)*1000/FS).astype(np.int64)
labels=[datetime.fromtimestamp(int(t)/1000).strftime("%Y-%m-%d %H:%M:%S") for t in timestamps]
def code_map(x):
    df=pd.DataFrame({"time":labels,"diameter":x})
    seconds=df.time.unique()
    assert len(seconds)==3
    a=[df.loc[df.time==s,"diameter"].reset_index(drop=True) for s in seconds]
    return pd.concat(a,axis=1).mean(axis=1).to_numpy()[:M]
def analytic(x):
    return np.asarray(x).reshape(3,90).mean(axis=0)
t=np.arange(N)/FS
r0=np.full(N,3.5)
r1=3.5+.2*np.cos(2*np.pi*t/3)
assert np.max(np.abs(code_map(r0)-code_map(r1)))<1e-13
truth=3.5+.2*np.cos(2*np.pi*np.arange(M)/30/3)
rmse=float(np.sqrt(np.mean((code_map(r1)-truth)**2)))
assert abs(rmse-.2/np.sqrt(2))<1e-12
one_hz=3.5+.2*np.cos(2*np.pi*t)
f=np.fft.rfftfreq(M,1/30)
spec=np.fft.rfft(code_map(one_hz)-code_map(one_hz).mean())
apparent=float(f[1+np.argmax(abs(spec[1:]))])
assert abs(apparent-1/3)<1e-12
rng=np.random.default_rng(332)
for _ in range(300):
    x=rng.normal(size=N)
    assert np.allclose(code_map(x),analytic(x),rtol=0,atol=1e-13)
    v=rng.normal(size=90)
    assert np.max(abs(code_map(np.r_[v,-v,np.zeros(90)])))<1e-14
for q in [1/3,2/3,4/3,5/3,7/3]:
    assert abs(sum(np.exp(2j*np.pi*q*s) for s in range(3))/3)<1e-12
print(json.dumps({"status":"PASS","synthetic_only":True,"nullity":180,"random_trials":300,"smooth_collision_mm":0,"reference_rmse_mm":rmse,"1hz_apparent_hz":apparent,"human_evaluation":"NOT RUN"},indent=2))
