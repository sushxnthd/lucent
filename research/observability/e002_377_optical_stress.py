"""E002-377 stylized RGB optical stress; requires numpy and scipy. Not human data."""
import json
from pathlib import Path
import numpy as np
from scipy.ndimage import gaussian_filter
out=Path(__file__).parent
h,w=64,96
y,x=np.mgrid[0:h,0:w]
base=np.zeros((h,w,3))
for k in range(3):
    base[:,:,k]=.28+.02*k+.06*(x/w)+.025*(y/h)
stripe=((abs(y-32)<=1)&(abs(x-48)<=11)).astype(float)
closed=base+stripe[:,:,None]*np.array([.30,.20,.10])[None,None,:]
mask=np.ones((h,w,1));mask[stripe>0]=0
conditions=[
 ('clean',0,None,1,0,0),
 ('blur_1px',1,None,1,0,0),
 ('blur_2px',2,None,1,0,0),
 ('blur_4px',4,None,1,0,0),
 ('blur_8px',8,None,1,0,0),
 ('missing_eye',0,mask,1,0,0),
 ('global_gain',0,None,.7,.1,0),
 ('local_drift',0,None,1,0,.02)]
rows=[]
for name,sigma,occlusion,gain,offset,drift in conditions:
    a,b=base.copy(),closed.copy()
    if sigma:
        a=gaussian_filter(a,(sigma,sigma,0))
        b=gaussian_filter(b,(sigma,sigma,0))
    a=a*gain+offset;b=b*gain+offset
    if occlusion is not None:
        a*=occlusion;b*=occlusion
    c=float(np.max(np.abs(b-a)))
    eps=.01+drift
    for fps in [20,30]:
        F=1000/fps;D=42;wexp=10
        M=min(wexp,max(0,(D-F+wexp)/2))
        Xi=c*M/(2*eps*wexp)
        Xi8=c*M/(2*(eps+1/510)*wexp)
        rows.append({"condition":name,"fps":fps,"contrast":round(c,7),
          "eps":round(eps,5),"overlap_ms":round(M,6),
          "Xi":round(Xi,5),"Xi_8bit":round(Xi8,5),
          "certificate":bool(Xi>1),"8bit_certificate":bool(Xi8>1)})
res={"synthetic_only":True,"human_data":False,
     "negative_control":{"type":"brightness_only","raw_delta":.04,
       "calibrated_epsilon":.01,"decision":"ABSTAIN: out of model"},
     "conditions":rows}
(out/'e002_377_optical_results.json').write_text(json.dumps(res,indent=2))
assert next(z for z in rows if z["condition"]=="clean" and z["fps"]==20)["8bit_certificate"]
assert not next(z for z in rows if z["condition"]=="blur_2px" and z["fps"]==20)["8bit_certificate"]
assert not next(z for z in rows if z["condition"]=="missing_eye" and z["fps"]==30)["certificate"]
print("E002-377 synthetic optical stress PASS",len(rows),"conditions")
