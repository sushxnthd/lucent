#!/usr/bin/env python3
"""E002-592 exact sensor-transfer envelope; synthetic only, no physical certification."""
from fractions import Fraction as F
import json, random

def mean(c,tau,d,L):
    c,tau,d,L=map(F,(c,tau,d,L))
    if not (0<=tau<c<1 and 0<d<1 and L>0): raise ValueError('DOMAIN')
    s=1-d
    if L*s<2*(c-tau): return None
    if L*s<=2*(1-tau): return tau+L*s*s/4
    return tau+(1-tau)*s-(1-tau)**2/L

def decide(c,tau,d,L,k,b,e,calibrated=True,nuisances=()):
    if not calibrated or nuisances or k is None: return 'ABSTAIN_UNCALIBRATED',None
    try:
        if any(isinstance(x,float) for x in (c,tau,d,L,k,b,e)): raise ValueError('FLOAT')
        k,b,e=map(F,(k,b,e))
        if not (0<k<=1 and 0<=b<=1 and 0<=e<=1): raise ValueError('SENSOR')
        m=mean(c,tau,d,L)
        if m is None: return 'MODEL_CLOSURE_UNREACHABLE_ONLY',None
        margin=k*(F(c)-m)-2*(b+e)
        return ('MODEL_SEPARABLE_ONLY' if margin>0 else 'OVERLAP_ABSTAIN'),margin
    except (ValueError,TypeError,ZeroDivisionError):
        return 'ABSTAIN_INVALID_INPUT',None

def witness():
    pts=[(F(0),F(1,2)),(F(1,50),F(1,10)),(F(31,50),F(1,10)),
         (F(133,200),F(1)),(F(39,40),F(1)),(F(1),F(1,2))]
    assert pts[2][0]-pts[1][0]==F(3,5)
    assert all(0<=a<=1 for _,a in pts)
    assert all(t2>t1 and abs((a2-a1)/(t2-t1))<=20 for (t1,a1),(t2,a2) in zip(pts,pts[1:]))
    val=sum((a1+a2)*(t2-t1)/2 for (t1,a1),(t2,a2) in zip(pts,pts[1:]))
    assert val==F(839,2000)==mean(F(1,2),F(1,10),F(3,5),20)
    return val

def overlap(k,b,e,c,m):
    k,b,e,c,m=map(F,(k,b,e,c,m))
    lo=max(k*c-(b+e),k*m-(b+e))
    hi=min(k*c+(b+e),k*m+(b+e))
    if lo>hi:return None
    y=(lo+hi)/2
    for center in (k*c,k*m):
        offset=y-center
        illum=max(-b,min(b,offset))
        read=offset-illum
        assert abs(illum)<=b and abs(read)<=e and center+illum+read==y
    return str(y)

def test():
    base=(F(1,2),F(1,10),F(3,5))
    cases=[
        ('low_contrast',20,F(1,5),F(1,100),F(1,200),'OVERLAP_ABSTAIN',F(-139,10000)),
        ('high_contrast',20,F(3,5),F(1,100),F(1,200),'MODEL_SEPARABLE_ONLY',F(183,10000)),
        ('illumination_drift',20,F(3,5),F(1,50),F(1,200),'OVERLAP_ABSTAIN',F(-17,10000)),
        ('high_speed',100,F(3,5),F(1,100),F(1,200),'OVERLAP_ABSTAIN',F(-57,50000)),
        ('exact_tangent',20,F(60,161),F(1,100),F(1,200),'OVERLAP_ABSTAIN',F(0))]
    rows=[]
    for name,L,k,b,e,expected,margin in cases:
        actual,v=decide(*base,L,k,b,e)
        assert (actual,v)==(expected,margin),(name,actual,v)
        assert (overlap(k,b,e,base[0],mean(*base,L)) is None)==(expected=='MODEL_SEPARABLE_ONLY')
        rows.append({'case':name,'status':actual,'margin':str(v)})
    flags=['geometry','brightness','missingness','blur','gaze','glasses','clock','shutter','response','saturation']
    for f in flags:
        assert decide(*base,20,F(3,5),F(1,100),F(1,200),nuisances=[f])[0]=='ABSTAIN_UNCALIBRATED'
    assert decide(*base,20,None,F(1,100),F(1,200))[0]=='ABSTAIN_UNCALIBRATED'
    assert decide(*base,20,F(3,5),F(1,100),F(1,200),calibrated=False)[0]=='ABSTAIN_UNCALIBRATED'
    for args in [(-1,F(1,100),F(1,200)),(F(3,5),-1,0),(F(3,5),0,-1)]:
        assert decide(*base,20,*args)[0]=='ABSTAIN_INVALID_INPUT'
    rng=random.Random(592)
    counts={'MODEL_SEPARABLE_ONLY':0,'OVERLAP_ABSTAIN':0,'MODEL_CLOSURE_UNREACHABLE_ONLY':0}
    for i in range(1000):
        L=rng.randint(2,120);k=F(rng.randint(1,100),100)
        b=F(rng.randint(0,30),1000);e=F(rng.randint(0,20),1000)
        verdict,margin=decide(*base,L,k,b,e)
        counts[verdict]+=1
        m=mean(*base,L)
        if m is None:assert verdict=='MODEL_CLOSURE_UNREACHABLE_ONLY';continue
        assert (overlap(k,b,e,base[0],m) is None)==(verdict=='MODEL_SEPARABLE_ONLY')
    print(json.dumps({'experiment':'E002-592','status':'PASS','frozen_cases':rows,
          'exact_witness_mean':str(witness()),'adversarial_trials':1000,
          'seed':592,'counts':counts,'nuisance_abstention_controls':12,
          'invalid_controls':3,'evidence':'SYNTHETIC_ONLY',
          'human_physical_trials':0,'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED'},sort_keys=True))

if __name__=='__main__':test()
