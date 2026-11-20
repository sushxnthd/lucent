#!/usr/bin/env python3
"""E002-589 exact synthetic full-duty exposure-integration aliasing.

No human data, physical shutter measurement or physiological velocity ceiling.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F

OPEN = ((F(0),F(1,2)),(F(1),F(1,2)))
CLOSED = ((F(0),F(1,2)),(F(1,8),F(1,2)),(F(1,4),F(0)),
          (F(3,8),F(1,2)),(F(5,8),F(1,2)),(F(3,4),F(1)),
          (F(7,8),F(1,2)),(F(1),F(1,2)))
TAU = F(1,5)

def rat(x):
    return f'{x.numerator}/{x.denominator}'

def check(knots):
    assert knots[0][0]==0 and knots[-1][0]==1
    assert knots[0][1]==knots[-1][1]==F(1,2)
    assert all(F(0)<=y<=F(1) for _,y in knots)
    assert all(b[0]>a[0] for a,b in zip(knots,knots[1:]))

def point(knots,u):
    assert F(0)<=u<=F(1)
    for (t0,y0),(t1,y1) in zip(knots,knots[1:]):
        if u<=t1:
            return y0+(y1-y0)*(u-t0)/(t1-t0)
    raise AssertionError('uncovered')

def integrate_segment(y0,y1,dt,power):
    if power==1:
        return dt*(y0+y1)/2
    if power==2:
        return dt*(y0*y0+y0*y1+y1*y1)/3
    raise ValueError('power must be 1 or 2')

def integrate_one(knots,lo,hi,power=1):
    assert F(0)<=lo<hi<=F(1)
    s=F(0)
    for (t0,_),(t1,_) in zip(knots,knots[1:]):
        left,right=max(t0,lo),min(t1,hi)
        if left<right:
            s+=integrate_segment(point(knots,left),point(knots,right),right-left,power)
    return s

def integral_periodic(knots,lo,hi,power=1):
    assert lo>=0 and hi>lo
    out=F(0)
    while lo<hi:
        k=lo.numerator//lo.denominator
        end=min(hi,F(k+1))
        left=lo-F(k)
        right=end-F(k)
        if right==0: right=F(1)
        out+=integrate_one(knots,left,right,power)
        lo=end
    return out

def avg(knots,lo,hi,power=1):
    return integral_periodic(knots,lo,hi,power)/(hi-lo)

def max_slope(knots):
    return max(abs((y1-y0)/(t1-t0)) for (t0,y0),(t1,y1) in zip(knots,knots[1:]))

def closure_intervals(knots,tau):
    intervals=[]
    for (t0,y0),(t1,y1) in zip(knots,knots[1:]):
        if y0<=tau and y1<=tau:
            intervals.append((t0,t1))
        elif y0>tau and y1>tau:
            continue
        elif y0==y1:
            continue
        else:
            crossing=t0+(tau-y0)*(t1-t0)/(y1-y0)
            if y0>tau: intervals.append((crossing,t1))
            else: intervals.append((t0,crossing))
    if not intervals: return []
    merged=[list(intervals[0])]
    for a,b in intervals[1:]:
        if a<=merged[-1][1]: merged[-1][1]=max(merged[-1][1],b)
        else: merged.append([a,b])
    return [tuple(x) for x in merged]

def run():
    check(OPEN);check(CLOSED)
    assert max_slope(OPEN)==0 and max_slope(CLOSED)==4
    assert closure_intervals(OPEN,TAU)==[]
    assert closure_intervals(CLOSED,TAU)==[(F(1,5),F(3,10))]
    assert point(CLOSED,F(1,4))==0 and point(OPEN,F(1,4))==F(1,2)
    frames=[]
    for k in range(24):
        x,y=avg(OPEN,F(k),F(k+1)),avg(CLOSED,F(k),F(k+1))
        assert x==y==F(1,2)
        assert point(OPEN,F(0))==point(CLOSED,F(0))
        frames.append({'frame':k,'open':rat(x),'closure':rat(y)})
    assert avg(OPEN,F(0),F(1,2))==F(1,2)
    assert avg(CLOSED,F(0),F(1,2))==F(3,8)
    assert avg(CLOSED,F(1,2),F(1))==F(5,8)
    assert avg(CLOSED,F(1,4),F(3,4))==F(1,2)
    assert avg(CLOSED,F(1,8),F(9,8))==F(1,2)
    assert avg(OPEN,F(0),F(1),power=2)==F(1,4)
    assert avg(CLOSED,F(0),F(1),power=2)==F(7,24)
    altered=tuple((t,F(9,10) if t==F(3,4) else y) for t,y in CLOSED)
    assert avg(altered,F(0),F(1))==F(39,80)
    assert avg(OPEN,F(0),F(1))*F(3,2)+F(1,8)==F(7,8)
    assert avg(CLOSED,F(0),F(1))*F(3,2)+F(1,8)==F(7,8)
    assert F(1,2)-F(3,5)/2==F(1,5)
    assert F(1,2)-F(1,2)/2>TAU
    return {'experiment':'E002-589','evidence_tier':'EXACT_SYNTHETIC_INSTRUMENT_MODEL_ONLY',
            'frames_tested':len(frames),'full_duty_fraction':'1/1',
            'world_open_full_exposure':'1/2','world_closed_full_exposure':'1/2',
            'closure_interval':['1/5','3/10'],'closure_duration_fraction':'1/10',
            'max_slope_per_period':'4/1',
            'heldout_first_half_open':'1/2','heldout_first_half_closed':'3/8',
            'heldout_second_half_open':'1/2','heldout_second_half_closed':'5/8',
            'heldout_phase_blind_spot_closed':'1/2',
            'preintegration_square_open':'1/4','preintegration_square_closed':'7/24',
            'perturbed_bump_closed':'39/80',
            'velocity_L_times_T_strict_certificate_below':'3/5',
            'human_sequences':0,'physical_captures':0,
            'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED',
            'per_frame':frames}

def main():
    p=argparse.ArgumentParser();p.add_argument('--json',action='store_true');a=p.parse_args()
    x=run()
    if a.json:print(json.dumps(x,sort_keys=True))
    else:print('PASS: 24/24 full-duty frames identical, one world closes; heldout half exposures and nonlinear controls differ; 0 physical captures')

if __name__=='__main__':main()
