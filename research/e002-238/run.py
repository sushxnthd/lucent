#!/usr/bin/env python3
"""E002-238: exact score-argmax stability bound on E002-237's synthetic stress grid.
Not a human waveform experiment. No deployment rule is authorized.
Run: python research/e002-238/run.py
Requires numpy, opencv-python. Uses source-pinned E002-234/edge.py.
"""
import csv, hashlib, importlib.util, json, sys
from pathlib import Path
import cv2
import numpy as np

HERE=Path(__file__).resolve().parent
EDGE=HERE.parent/'e002-234'/'edge.py'
EXPECTED='569e750d17ea7dab30ad8d4582137eaef06db4fa648006d6e3b0703f9dfe2220'
assert hashlib.sha256(EDGE.read_bytes()).hexdigest()==EXPECTED, 'FROZEN_DETECTOR_MISMATCH'
spec=importlib.util.spec_from_file_location('frozen_edge',EDGE)
edge=importlib.util.module_from_spec(spec);spec.loader.exec_module(edge)
H=192

def render(r,outer,blur,seed,gray):
    s=6
    yy,xx=np.ogrid[:H*s,:H*s]
    rr=np.sqrt(((xx+.5)/s-H/2)**2+((yy+.5)/s-H/2)**2)/r
    im=np.where(rr<=1.,100.,170.).astype('float32')
    im[rr<.40]=40.
    im[(rr>outer-.12)&(rr<outer)]=gray
    im=cv2.resize(im,(H,H),interpolation=cv2.INTER_AREA)
    im=cv2.GaussianBlur(im,(0,0),blur)
    return np.clip(im+np.random.default_rng(seed).normal(0,.8,im.shape),0,255).astype('uint8')

def margin(q):
    return float(np.max(q)-np.partition(q,-2)[-2])

def main():
    grid=[('core',18,.68,.7,0)]
    for r in (12,18,24):
      for outer in (.60,.68,.76):
       for blur in (.5,.7):
        for seed in (0,1,2):
         if (r,outer,blur,seed)==(18,.68,.7,0): continue
         grid.append(('stress',r,outer,blur,seed))
    rows=[]
    for j,(subset,r,outer,blur,seed) in enumerate(grid):
        images=[render(r,outer,blur,seed,gray) for gray in (27,35)]
        pts=np.array([[96,96],[96+r,96],[96,96+r],[96-r,96],[96,96-r]],float)
        det=[edge.evaluate(im,pts) for im in images]
        v,w=[edge.profile(im.astype('float32'),96,96,r) for im in images]
        eps=float(np.max(np.abs(v-w)))
        m1,m2=margin(v),margin(w)
        a,b=np.argmax(v),np.argmax(w)
        set_a=edge.R[v>=max(v)-2*eps-1e-10]
        set_b=edge.R[w>=max(w)-2*eps-1e-10]
        assert np.any(np.isclose(set_a,edge.R[b]))
        assert np.any(np.isclose(set_b,edge.R[a]))
        both=bool(det[0]['eligible'] and det[1]['eligible'])
        delta=abs(float(det[0]['radius_ratio'])-float(det[1]['radius_ratio']))
        rows.append(dict(pair=j,subset=subset,both_admitted=int(both),
          false_change=int(both and delta>.15),eps=round(eps,7),
          margin_a=round(m1,7),margin_b=round(m2,7),
          stable_a=int(m1>2*eps),stable_b=int(m2>2*eps),
          observed_delta=round(delta,6),
          ambiguity_diameter_a=round(float(set_a[-1]-set_a[0]),6),
          ambiguity_diameter_b=round(float(set_b[-1]-set_b[0]),6)))
    assert len(rows)==54
    assert sum(x['both_admitted'] for x in rows[1:])==29
    assert sum(x['false_change'] for x in rows[1:])==5
    assert not any(x['stable_a'] or x['stable_b'] for x in rows)
    raw=HERE/'RAW_STABILITY.csv'
    with raw.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)
    result={'run':'E002-238','n_pairs':54,'n_stress':53,
      'both_admitted_stress':29,'false_change_stress':5,
      'certified_stable_a':0,'certified_stable_b':0,
      'human_waveform_tested':False,'product_candidate_pass':False,
      'raw_stability_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),
      'claim':'Exact argmax margin > 2*epsilon bound is non-discriminating here: 0/54 pairs certified when epsilon is observed cross-frame score sup norm.'}
    (HERE/'RESULTS.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__': main()
