"""E002-213: nuisance-projected Fisher information, SYNTHETIC ONLY.
Run: python research/e002-213/experiment.py
Dependencies: numpy scipy
"""
import csv, json
from pathlib import Path
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.special import expit

OUT=Path(__file__).resolve().parent
N=64; S=3
Y,X=np.mgrid[:N*S,:N*S]
X=(X+.5)/S-N/2; Y=(Y+.5)/S-N/2
XX,YY=np.mgrid[:N,:N]; XX=XX+.5-N/2; YY=YY+.5-N/2

def render(r=5.,blur=3.,contrast=.55,background=.75,x=0.,y=0.,ellipticity=1.,gradient=0.):
    disk=expit((r-np.sqrt((X-x)**2+((Y-y)/ellipticity)**2))/.18)
    sm=gaussian_filter(disk,blur*S,mode='constant',truncate=5.)
    mask=sm.reshape(N,S,N,S).mean(axis=(1,3))
    return (background+gradient*XX/N-contrast*mask).ravel()

def derivative(p,k,h):
    a=p.copy(); b=p.copy(); a[k]+=h; b[k]-=h
    return (render(**a)-render(**b))/(2*h)

STEPS={'r':.025,'blur':.025,'contrast':.01,'background':.01,'x':.025,'y':.025,'ellipticity':.005,'gradient':.005}
SETS={'known':[],'contrast':['contrast'],'photometric':['contrast','background','gradient'],'focus':['contrast','background','gradient','blur'],'full':['contrast','background','gradient','blur','x','y','ellipticity']}

def evaluate(p,nuis,noise=.02):
    j=derivative(p,'r',STEPS['r'])
    if nuis:
        J=np.column_stack([derivative(p,k,STEPS[k]) for k in nuis])
        Q,R=np.linalg.qr(J,mode='reduced')
        if min(abs(np.diag(R)))<1e-9: raise ValueError('singular nuisance basis')
        residual=j-Q@(Q.T@j)
    else: residual=j
    raw=float(j@j/noise**2)
    eff=float(residual@residual/noise**2)
    return dict(info_raw=raw,info_eff=eff,retention=eff/raw,sigma_r_crlb_px=1/np.sqrt(eff),residual_l2=float(np.linalg.norm(residual)))

def main():
    rows=[]
    for r in (3.,5.,8.):
        for blur in (1.,2.,3.,4.,5.,7.):
            p=dict(r=r,blur=blur,contrast=.55,background=.75,x=.14,y=-.12,ellipticity=.95,gradient=.01)
            for label,nuis in SETS.items():
                rows.append(dict(radius_px=r,blur_px=blur,model=label,**evaluate(p,nuis)))
    assert len(rows)==90 and all(0<=x['retention']<=1+1e-10 for x in rows)
    with (OUT/'RAW_SYNTHETIC.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print(json.dumps({'synthetic_cases':len(rows),'small_blurred':next(x for x in rows if x['radius_px']==3 and x['blur_px']==4 and x['model']=='full'),'large_sharp':next(x for x in rows if x['radius_px']==8 and x['blur_px']==3 and x['model']=='full')},indent=2))
if __name__=='__main__':main()
