#!/usr/bin/env python3
"""Exact-rational shutter instrument surrogate; synthetic, not human evidence."""
from fractions import Fraction as F
import json

def verdict(a,b,c,v,T):
    assert min(a,b)>c and v>0 and T>0 and abs(a-b)<=v*T
    return 'POSSIBLE' if (a-c+b-c)<=v*T else 'EXCLUDED'

def witness(a,b,c,v,T):
    if verdict(a,b,c,v,T)=='EXCLUDED': return None
    t1=(a-c)/v; t2=T-(b-c)/v
    assert 0<=t1<=t2<=T
    return [(F(0),a),(t1,c),(t2,c),(T,b)]

def interpolate(path,t):
    for (ta,xa),(tb,xb) in zip(path,path[1:]):
        if ta<=t<=tb:
            return xa if ta==tb else xa+(xb-xa)*(t-ta)/(tb-ta)
    raise ValueError('outside interval')

def run():
    a=b=F(2); c=F(0); v=F(100)
    cases=[]
    for T in [F(39,1000),F(40,1000),F(41,1000),F(60,1000)]:
        result=verdict(a,b,c,v,T); path=witness(a,b,c,v,T)
        if path:
            assert min(x for _,x in path)==c
            assert all(abs(x2-x1)<=v*(t2-t1) for (t1,x1),(t2,x2) in zip(path,path[1:]))
            assert interpolate(path,F(0))==a and interpolate(path,T)==b
        cases.append({'gap_ms':float(1000*T),'prediction':result,'constructed_closure':bool(path)})
    assert [r['prediction'] for r in cases]==['EXCLUDED','POSSIBLE','POSSIBLE','POSSIBLE']
    nominal=F(39,1000); jitter=F(1,1000)
    assert verdict(a,b,c,v,nominal)=='EXCLUDED'
    assert witness(a,b,c,v,nominal+2*jitter) is not None
    return {'evidence_tier':'exact-rational synthetic instrument surrogate',
            'cases':cases,'clock_counterexample':{'nominal_ms':39,'true_ms':41,
            'nominal_prediction':'EXCLUDED','true_hidden_closure':'POSSIBLE'},
            'limitations':'Assumes pointwise aperture and certified global speed. No physical camera, human speed, or exposure-integration validation.'}

if __name__=='__main__': print(json.dumps(run(),indent=2))
