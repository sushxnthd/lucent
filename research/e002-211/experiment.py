"""E002-211: synthetic pupil radius vs blur/contrast identifiability.
Requires numpy scipy. No human data. All values are normalized RGB intensities.
"""
import csv, json, math
from pathlib import Path
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.optimize import brentq
from scipy.stats import norm
OUT=Path(__file__).resolve().parent
N,SS=80,4
Y,X=np.mgrid[:N*SS,:N*SS]
X=(X+.5)/SS-N/2; Y=(Y+.5)/SS-N/2
YY,XX=np.mgrid[:N,:N]
XX=XX+.5-N/2; YY=YY+.5-N/2

def pupil(r,sigma):
    disk=((X*X+Y*Y)<=r*r).astype(float)
    smooth=gaussian_filter(disk,sigma*SS,mode="constant",truncate=5)
    low=smooth.reshape(N,SS,N,SS).mean(axis=(1,3))
    return low/low.sum()

def variance(im):
    m=im.sum()
    cx=(im*XX).sum()/m; cy=(im*YY).sum()/m
    return (im*((XX-cx)**2+(YY-cy)**2)).sum()/(2*m)

def pair(r0,r1,s0):
    a=pupil(r0,s0); target=variance(a)
    def err(s): return variance(pupil(r1,s))-target
    s1=brentq(err,.1,s0,xtol=1e-8)
    b=pupil(r1,s1)
    mass=.6*math.pi*r0*r0
    mu0=.75-mass*a; mu1=.75-mass*b
    assert min(mu0.min(),mu1.min())>=0
    return mu0,mu1,s1,target,variance(b)

def accuracy(d,noise,n=1,rho=0):
    neff=n/(1+(n-1)*rho)
    return float(norm.cdf(math.sqrt(neff)*d/(2*noise)))

rows=[]
for s0 in (2.,4.,6.):
    for dr in (.1,.2,.4,.8):
        mu0,mu1,s1,v0,v1=pair(6.,6.+dr,s0)
        d=float(np.linalg.norm(mu1-mu0))
        rows.append(dict(r0_px=6.,r1_px=6.+dr,dr_px=dr,
          sigma0_px=s0,sigma1_px=s1,moment2_0=v0,moment2_1=v1,
          moment2_abs_error=abs(v0-v1),image_l2=d,noise_sd=.02,
          accuracy_one_frame=accuracy(d,.02),
          accuracy_150_iid=accuracy(d,.02,150,0),
          accuracy_150_rho_0p2=accuracy(d,.02,150,.2),
          accuracy_150_rho_0p8=accuracy(d,.02,150,.8),
          noise_floor_for_75pct_one_frame=d/(2*norm.ppf(.75)),
          contrast_0=.6,contrast_1=.6*(6/(6+dr))**2))
with (OUT/"RAW_SYNTHETIC.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
key=next(r for r in rows if r["sigma0_px"]==4 and abs(r["dr_px"]-.2)<1e-8)
a=pupil(6.,4.); b=pupil(6.2,4.)
control=float(np.linalg.norm((.75-.6*math.pi*6.2**2*b)-(.75-.6*math.pi*6**2*a)))
rng=np.random.default_rng(211); M=50000
snr=key["image_l2"]/(2*.02)
mc=float(np.mean(snr+rng.normal(size=M)>0))
se=math.sqrt(mc*(1-mc)/M)
result=dict(run="E002-211",date="2026-10-15",dataset="SYNTHETIC_ONLY",
  matched_second_moment_max_abs_error=max(r["moment2_abs_error"] for r in rows),
  prespecified_case=key,uncompensated_control_l2=control,
  matched_control_l2=key["image_l2"],monte_carlo_one_frame_accuracy=mc,
  monte_carlo_standard_error=se,exact_one_frame_accuracy=key["accuracy_one_frame"],
  gates=dict(moment_match_tolerance=1e-5,
   independent_mc_within_5_se=abs(mc-key["accuracy_one_frame"])<5*se,
   product_75pct_single_frame_for_case=key["accuracy_one_frame"]>=.75,
   human_rgb_reference=False,prospective_holdout=False),
  smallest_supported_claim="Exact equal-prior Gaussian binary detection ceiling for specified antialiased disk, defocus and contrast nuisance. No human waveform evidence.")
(OUT/"RESULTS.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps(result,indent=2))
