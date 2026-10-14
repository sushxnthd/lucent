#!/usr/bin/env python3
"""E002-177 synthetic photometric identifiability audit; no human data."""
import json
from pathlib import Path
import numpy as np
from scipy.special import ndtr, ndtri
R_VALUES=(6.,9.,12.)
DELTA=(-.45,.45)
BLURS=(.8,1.5,2.5)
GAMMAS=(1.,1.2,1.6,2.2)
X=np.arange(0.,32.0001,.125)
def gauge_map(u,dr,s):
    return ndtr(ndtri(u)-dr/s)
def gamma_shift(gamma,s):
    return s*ndtri(2.**(-1./gamma))
cases=[]
for R in R_VALUES:
    for dr in DELTA:
        for s in BLURS:
            u=ndtr((X-R)/s)
            v=ndtr((X-(R+dr))/s)
            mask=(u>1e-12)&(u<1-1e-12)
            pred=gauge_map(u[mask],dr,s)
            max_error=float(np.max(np.abs(pred-v[mask])))
            diffs=np.diff(pred)
            cases.append({'radius_px':R,'delta_radius_px':dr,'blur_px':s,'points_checked':int(mask.sum()),'max_abs_residual':max_error,'monotonic':bool(np.all(diffs>=-1e-15)),'pass':bool(max_error<=1e-12 and np.all(diffs>=-1e-15))})
gamma=[]
for g in GAMMAS:
    for s in BLURS:
        shift=float(gamma_shift(g,s))
        gamma.append({'gamma':g,'blur_px':s,'edge_shift_px':shift,'as_fraction_of_5pct_change_at_R9':shift/(.05*9.)})
result={'run':'E002-177','classification':'synthetic exact-model mechanism; no human RGB','construction':'h(u)=Phi(Phi^{-1}(u)-deltaR/s)','cases':cases,'gamma_cases':gamma,'summary':{'gauge_cases':len(cases),'gauge_pass':sum(c['pass'] for c in cases),'max_abs_residual':max(c['max_abs_residual'] for c in cases),'gamma_2p2_s1p5_px':next(g['edge_shift_px'] for g in gamma if g['gamma']==2.2 and g['blur_px']==1.5),'physiological_rgb_gate':'NOT_TESTED'}}
Path(__file__).with_name('RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result['summary'],indent=2))
assert all(c['pass'] for c in cases)
