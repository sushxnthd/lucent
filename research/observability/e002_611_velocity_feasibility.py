#!/usr/bin/env python3
"""E002-611: published-velocity scenarios for an existing sufficient shutter gate.
No physical data, hard speed bounds, or actual exclusion certificates are produced.
"""
import argparse
import csv
import json
from fractions import Fraction as F
from itertools import product

FPS=(30,60,120)
APERTURES_MM=(F('7.4'),F('9.8'),F('12.8'))
VELOCITIES_MM_S=(93,160,243,400)
MEANS=(F('0.5'),F('1'))
TAU=F('0.2')

def threshold_mean(v_mm_s,aperture_mm,fps,tau=TAU):
    v,a,f,t=map(F,(v_mm_s,aperture_mm,fps,tau))
    if not (a>0 and f>0 and v>=0 and 0<=t<1):
        raise ValueError('invalid physical domain')
    return t+v/(2*a*f)

def gate_possible(v_mm_s,aperture_mm,fps,tau=TAU):
    return threshold_mean(v_mm_s,aperture_mm,fps,tau)<1

def illustrative_gate_passes(v_mm_s,aperture_mm,fps,mean,tau=TAU):
    m=F(mean)
    if not 0<=m<=1:
        raise ValueError('mean out of domain')
    return m>threshold_mean(v_mm_s,aperture_mm,fps,tau)

def boxcar_margin(v_mm_s,aperture_mm,fps,exposure_ms,mean,tau=TAU):
    f,e,a,v,m,t=map(F,(fps,exposure_ms,aperture_mm,v_mm_s,mean,tau))
    period=F(1000,1)/f
    if not (f>0 and 0<e<=period and a>0 and v>=0 and 0<=m<=1 and 0<=t<1):
        raise ValueError('invalid boxcar geometry')
    gap=period-e
    V=v/(1000*a)
    return 2*(m-t)-V*(gap+e)

def fmt(x):
    return f'{float(F(x)):.9f}'

def rows():
    for f,a,v,m in product(FPS,APERTURES_MM,VELOCITIES_MM_S,MEANS):
        thr=threshold_mean(v,a,f)
        possible=gate_possible(v,a,f)
        passes=illustrative_gate_passes(v,a,f,m)
        period=F(1000,f)
        margins=[boxcar_margin(v,a,f,e,m) for e in (F(2),F(4,5)*period)]
        assert margins[0]==margins[1], 'exposure invariance regression'
        assert (margins[0]>0)==passes
        yield dict(fps=f,aperture_mm=str(float(a)),velocity_mm_s=v,
                   illustrative_mean=str(float(m)),threshold_mean=fmt(thr),
                   dimensionless_Q=fmt(v/(2*a*f*(1-TAU))),
                   any_mean_can_pass=int(possible),illustrative_mean_passes=int(passes),
                   exposure_2ms_margin=fmt(margins[0]),
                   exposure_80pct_period_margin=fmt(margins[1]),
                   evidence_tier='LITERATURE_ANCHORED_SCENARIO_NOT_CERTIFICATE',
                   product='ABSTAIN_UNCALIBRATED',release='BLOCKED')

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--csv',action='store_true')
    args=p.parse_args()
    rr=list(rows())
    if args.csv:
        out=csv.DictWriter(__import__('sys').stdout,fieldnames=list(rr[0]),lineterminator='\n')
        out.writeheader()
        out.writerows(rr)
    else:
        print(json.dumps(dict(cases=len(rr),
            impossible_for_any_mean_cases=sum(1 for r in rr if not r['any_mean_can_pass']),
            illustrative_mean_pass_cases=sum(r['illustrative_mean_passes'] for r in rr),
            physical_validation='NOT_PERFORMED',
            product='ABSTAIN_UNCALIBRATED',release='BLOCKED'),indent=2))

if __name__=='__main__':
    main()
