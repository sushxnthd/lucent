#!/usr/bin/env python3
"""Synthetic exact-rational shutter exposure study; standard library only."""
from fractions import Fraction as F
from pathlib import Path
import random,json,csv
rng=random.Random(2872026)
cases=[]
for name,fps,duty in [('10fps_20pct',10,F(1,5)),('10hz_loader_from_30fps_1_60s',10,F(1,6)),('30fps_50pct',30,F(1,2)),('60fps_100pct',60,F(1)),('24fps_unseen_24pct',24,F(6,25))]:
    P=F(1,fps);T=P*duty;N=5*fps;eta=F(1,100)
    segments=[];t=F(0)
    while t<5:
        end=min(F(5),t+F(rng.randint(1,35),1000))
        segments.append((t,end,F(rng.randint(0,10),10)));t=end
    def integrate(a,b):
        return sum((v*max(F(0),min(b,r)-max(a,l)) for l,r,v in segments),F(0))
    y=[integrate(i*P,i*P+T)/T for i in range(N)]
    D=integrate(F(0),F(5))
    low=T*sum((max(F(0),v-eta) for v in y),F(0))
    high=T*sum((min(F(1),v+eta) for v in y),F(0))+N*(P-T)
    assert low<=D<=high
    assert high-low<=N*(P-T+2*T*eta)
    if duty==1:assert T*sum(y,F(0))==D
    cases.append({'configuration':name,'fps':fps,'duty':float(duty),'frames':N,'exposure_ms':float(1000*T),'eta':float(eta),'reference_D_s':float(D),'exposed_D_s':float(T*sum(y,F(0))),'D_min_s':float(low),'D_max_s':float(high),'width_s':float(high-low),'unclipped_width_fraction':float(1-duty+2*duty*eta),'gap_collision_s':float(N*(P-T)),'synthetic_holdout':name.startswith('24fps')})
out=Path(__file__).resolve().parent
(out/'results.json').write_text(json.dumps({'human_evidence':False,'camera_calibrated':False,'cases':cases,'P80_collision':{'y':0.2,'P80_A':0.2,'P80_B':0}},indent=2)+'\n')
with (out/'raw_cases.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=cases[0].keys());w.writeheader();w.writerows(cases)
print('PASS',len(cases),'synthetic configurations; full-duty conservation and dose intervals')
