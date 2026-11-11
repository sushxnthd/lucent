#!/usr/bin/env python3
"""E002-591 exact duration-aware full-duty integration boundary.

Idealized normalized-aperture theorem only. Not a human or physical-camera certificate.
"""
from fractions import Fraction as F
import json


def threshold(c, tau, dwell):
    c, tau, dwell = map(F, (c, tau, dwell))
    if not (F(0) <= tau < c < F(1) and F(0) <= dwell < F(1)):
        raise ValueError('INVALID_PARAMETER_DOMAIN')
    s = 1 - dwell
    cap = tau + (1-tau)*s
    if c >= cap:
        return None
    if c-tau <= (1-tau)*s/2:
        return 4*(c-tau)/(s*s)
    return (1-tau)**2/(cap-c)


def maximal_mean(c, tau, dwell, speed):
    c, tau, dwell, speed = map(F, (c, tau, dwell, speed))
    if not (F(0) <= tau < c < 1 and F(0) <= dwell < 1 and speed > 0):
        raise ValueError('INVALID_PARAMETER_DOMAIN')
    s = 1-dwell
    if speed*s < 2*(c-tau):
        return None
    if speed*s <= 2*(1-tau):
        return tau + speed*s*s/4
    return tau + (1-tau)*s - (1-tau)**2/speed


def witness(c, tau, dwell):
    c, tau, dwell = map(F, (c, tau, dwell))
    speed = threshold(c,tau,dwell)
    if speed is None:
        raise ValueError('IMPOSSIBLE_AT_FINITE_SPEED')
    s = 1-dwell
    b = (c-tau)/(1-tau)
    ell = speed*s/(1-tau)
    if ell <= 2:
        knots = [(F(0),b),(b/ell,F(0)),(b/ell+F(1,2),ell/2),(F(1),b)]
    else:
        knots = [(F(0),b),(b/ell,F(0)),((b+1)/ell,F(1)),
                 (1-(1-b)/ell,F(1)),(F(1),b)]
    zero = b/ell
    out=[]
    for j,(u,ap) in enumerate(knots):
        if j > 0 and u == knots[j-1][0]:
            continue
        t = s*u + (dwell if u > zero else 0)
        if j and u > zero and knots[j-1][0] == zero and dwell:
            out.append((s*zero+dwell,tau))
        out.append((t,tau+(1-tau)*ap))
    assert out[0] == (F(0),c) and out[-1] == (F(1),c)
    return speed,out


def verify_witness(c,tau,dwell):
    speed,knots = witness(c,tau,dwell)
    assert knots[0] == (F(0),c) and knots[-1] == (F(1),c)
    assert all(F(0)<=a<=1 for _,a in knots)
    assert all(t2>t1 for (t1,_),(t2,_) in zip(knots,knots[1:])), knots
    slopes = [abs((a2-a1)/(t2-t1)) for (t1,a1),(t2,a2) in zip(knots,knots[1:])]
    assert all(s<=speed for s in slopes)
    mean = sum((a1+a2)*(t2-t1)/2 for (t1,a1),(t2,a2) in zip(knots,knots[1:]))
    assert mean == c, (mean,c)
    intervals = [(t1,t2) for (t1,a1),(t2,a2) in zip(knots,knots[1:]) if a1<=tau and a2<=tau]
    assert any(t2-t1>=dwell for t1,t2 in intervals) if dwell else any(a==tau for _,a in knots)
    assert maximal_mean(c,tau,dwell,speed)==c
    below=speed*F(99,100)
    assert (maximal_mean(c,tau,dwell,below) is None or
            maximal_mean(c,tau,dwell,below)<c)
    return {'c':str(c),'tau':str(tau),'dwell_fraction':str(dwell),
            'critical_speed_VT':str(speed),'mean':str(mean),'knots':len(knots)}


def certified_dwell(samples, tau, velocity_per_ms, domain_ms,
                    independent_velocity_verified=False, clock_verified=False,
                    geometry_verified=False, nuisance_flags=()):
    """One-sided subthreshold dwell witness, not proof of absence when empty."""
    if not (independent_velocity_verified and clock_verified and geometry_verified) or nuisance_flags:
        return {'status':'ABSTAIN_UNCALIBRATED','certified_dwell_ms':None}
    try:
        tau, v, end = F(tau),F(velocity_per_ms),F(domain_ms)
        if not (0<=tau<1 and v>0 and end>0 and samples):
            raise ValueError
        intervals=[]
        for item in samples:
            t,u,e=map(F,(item['time_ms'],item['upper_aperture'],item['time_error_ms']))
            if not (0<=t<=end and 0<=u<=1 and e>=0 and t-e>=0 and t+e<=end):
                raise ValueError
            radius=(tau-u)/v-e
            if radius>=0:
                intervals.append((max(F(0),t-radius),min(end,t+radius)))
        intervals.sort()
        components=[]
        for lo,hi in intervals:
            if not components or lo>components[-1][1]:
                components.append([lo,hi])
            else:
                components[-1][1]=max(components[-1][1],hi)
        longest=max((hi-lo for lo,hi in components),default=F(0))
        return {'status':'ONE_SIDED_WITNESS_ONLY','certified_dwell_ms':str(longest),
                'certified_components':len(components),'excludes_hidden_closure':False}
    except (ValueError,KeyError,TypeError,ZeroDivisionError):
        return {'status':'ABSTAIN_INVALID_INPUT','certified_dwell_ms':None}


def self_test():
    cases=[(F(1,2),F(0),F(0),F(2)),
           (F(1,2),F(0),F(1,10),F(5,2)),
           (F(1,2),F(0),F(1,4),F(4)),
           (F(1,2),F(0),F(1,2),None),
           (F(1,2),F(1,10),F(3,10),F(81,23)),
           (F(1,5),F(0),F(1,10),F(80,81)),
           (F(1,2),F(1,10),F(3,5),None)]
    out=[]
    for c,tau,d,expected in cases:
        actual=threshold(c,tau,d)
        assert actual==expected,(c,tau,d,actual,expected)
        if actual is None:
            assert c >= tau+(1-tau)*(1-d)
        else:
            out.append(verify_witness(c,tau,d))
    count=0
    for c in (F(1,5),F(2,5),F(1,2),F(3,5),F(4,5)):
        for tau in (F(0),F(1,10)):
            if tau>=c:continue
            for d in (F(0),F(1,20),F(1,10),F(1,4),F(2,5),F(3,5)):
                if threshold(c,tau,d) is not None:
                    verify_witness(c,tau,d);count+=1
    params={'independent_velocity_verified':True,'clock_verified':True,'geometry_verified':True}
    a=certified_dwell([{'time_ms':10,'upper_aperture':F(1,20),'time_error_ms':1}],F(1,10),F(1,100),30,**params)
    assert a['certified_dwell_ms']=='8' and a['certified_components']==1
    b=certified_dwell([{'time_ms':10,'upper_aperture':F(1,20),'time_error_ms':1},
                       {'time_ms':22,'upper_aperture':F(1,20),'time_error_ms':1}],F(1,10),F(1,100),40,**params)
    assert b['certified_dwell_ms']=='8' and b['certified_components']==2
    c=certified_dwell([{'time_ms':10,'upper_aperture':F(1,20),'time_error_ms':1},
                       {'time_ms':18,'upper_aperture':F(1,20),'time_error_ms':1}],F(1,10),F(1,100),40,**params)
    assert c['certified_dwell_ms']=='16' and c['certified_components']==1
    assert certified_dwell([{'time_ms':10,'upper_aperture':F(1,20),'time_error_ms':1}],F(1,10),F(1,100),30)['status']=='ABSTAIN_UNCALIBRATED'
    assert certified_dwell([{'time_ms':10,'upper_aperture':F(1,20),'time_error_ms':1}],F(1,10),F(1,100),30,**params,nuisance_flags=['blur'])['status']=='ABSTAIN_UNCALIBRATED'
    assert certified_dwell([{'time_ms':10,'upper_aperture':F(1,20),'time_error_ms':6}],F(1,10),F(1,100),30,**params)['certified_dwell_ms']=='0'
    assert certified_dwell([{'time_ms':10,'upper_aperture':None,'time_error_ms':1}],F(1,10),F(1,100),30,**params)['status']=='ABSTAIN_INVALID_INPUT'
    assert certified_dwell([{'time_ms':10,'upper_aperture':F(1,20),'time_error_ms':1}],F(1,10),0,30,**params)['status']=='ABSTAIN_INVALID_INPUT'
    for bad in [(F(1,2),F(1,2),F(0)),(F(1,2),F(0),F(1)),(F(1),F(0),F(0))]:
        try:threshold(*bad)
        except ValueError:pass
        else:raise AssertionError('BAD_DOMAIN_ACCEPTED')
    print(json.dumps({'experiment':'E002-591','status':'PASS','rational_grid_witnesses':count,
                      'frozen_finite_cases':len(out),'frozen_impossible_cases':2,
                      'anatomical_certificate_controls':9,
                      'evidence_tier':'IDEALIZED_THEOREM_SYNTHETIC_ONLY',
                      'physical_human_validation':False,
                      'product':'ABSTAIN_UNCALIBRATED','release':'BLOCKED',
                      'frozen_cases':out},sort_keys=True))

if __name__=='__main__':
    self_test()
