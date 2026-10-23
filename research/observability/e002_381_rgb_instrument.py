"""E002-381 synthetic 2D RGB instrument. No human recordings."""
from fractions import Fraction as Q
import json
import numpy as np
from scipy.ndimage import gaussian_filter
from e002_381_exact import frozen,certify,whole_eye_duration
F,w,m=Q(1,30),Q(1,100),Q(4,1000)
Y,X=np.mgrid[0:80,0:96]
SKIN=np.array([.72,.56,.46]);SCLERA=np.array([.86,.83,.79]);IRIS=np.array([.15,.24,.22])
BANDS=[(20+8*i,28+8*i) for i in range(5)]
def texture(gaze=0):
    op=np.broadcast_to(SKIN,(80,96,3)).copy();cl=op.copy()
    eye=(X>=18)&(X<78)&(Y>=20)&(Y<60)
    iris=np.exp(-((X-48-gaze)**2+(Y-40)**2)/(2*9**2))
    op[eye]=SCLERA+(IRIS-SCLERA)*iris[eye,None]
    crease=np.exp(-((Y-39)/2)**2)
    cl[eye]=np.clip(SKIN-np.array([.11,.12,.10])*crease[eye,None],0,1)
    return op,cl
def overlap_fraction(phase,row):
    start=float(phase+row["tau"]);stop=start+float(row["D"]);best=0.
    for k in range(-3,6):
        t=k*float(F)+float(row["delta"])
        best=max(best,max(0.,min(stop,t+float(w))-max(start,t))/float(w))
    return best
def image_at(phase,alpha,gaze=0,brightness=0,blur=0,glasses=False,missing=()):
    op,cl=texture(gaze);img=op.copy()
    for j,(a,b) in enumerate(BANDS):
        p=overlap_fraction(phase,frozen(alpha)[j])
        img[a:b,18:78]=(1-p)*op[a:b,18:78]+p*cl[a:b,18:78]
        if j in missing:img[a:b,18:78]=np.nan
    if glasses:img[27:34,20:76]=.99
    img=np.clip(img+brightness,0,1)
    if blur:img=gaussian_filter(np.nan_to_num(img,nan=.6),sigma=(blur,blur,0))
    return img
def score(img,open_img,closed_img,j):
    a,b=BANDS[j];region=np.s_[a:b,18:78]
    x=img[region];d=closed_img[region]-open_img[region]
    if not np.all(np.isfinite(x)):return None
    return float(np.sum((x-open_img[region])*d)/np.sum(d*d))
def run():
    op,cl=texture()
    results=[]
    for alpha in (Q(0),Q(18,100),Q(11,60),Q(19,100),Q(20,100),Q(1)):
        rows=frozen(alpha);cert,witness=certify(F,w,m,rows)
        hits=sum(any(overlap_fraction(Q(i,360000),r)>=float(m/w)-1e-12 for r in rows) for i in range(12000))
        assert (hits==12000)==cert
        results.append(dict(alpha=float(alpha),certified=cert,hit_count=hits,
                            whole_eye_ms=float(1000*whole_eye_duration(rows)),
                            missed_phase_ms=float(1000*witness) if witness is not None else None))
    controls={"gaze_only":texture(gaze=14)[0],"blur_only":gaussian_filter(op,sigma=(5,5,0)),
              "brightness_only":np.clip(op+.14,0,1)}
    false_scores={k:max(score(v,op,cl,j) for j in range(5)) for k,v in controls.items()}
    assert false_scores["gaze_only"]>.2 and false_scores["blur_only"]>.2
    out={"synthetic_only":True,"phase_sweep":results,"open_eye_nuisance_scores":false_scores}
    print(json.dumps(out,indent=2))
if __name__=="__main__":run()
