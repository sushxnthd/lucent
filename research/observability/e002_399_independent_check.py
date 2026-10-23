#!/usr/bin/env python3
"""Independent numerical oracle and synthetic annotation-bridge adversarial checks."""
import json
import math
import random
from e002_399_reference_adequacy import (Frame,calibrated,certify,
                                         exact_lower_envelope_min,simulate)
from e002_399_annotation_bridge import analyze,measurement_interval


def dense_envelope(times,lower,v,n=30001):
    """Separate O(n*m) grid oracle, no prefix/suffix optimization."""
    a,b=times[0],times[-1]
    return min(max(li-v*abs(a+(b-a)*j/(n-1)-ti)
                   for ti,li in zip(times,lower)) for j in range(n))


def check_envelope():
    rng=random.Random(3991)
    max_disagreement=0.
    for rep in range(150):
        n=rng.randint(2,11)
        times=sorted(rng.sample(range(1,2000),n))
        times=[t/10000 for t in times]
        lower=[rng.uniform(-.5,1.5) for _ in times]
        v=rng.uniform(.01,100)
        exact=exact_lower_envelope_min(times,lower,v)
        dense=dense_envelope(times,lower,v,n=2001)
        error_bound=v*(times[-1]-times[0])/(2*2000)+1e-10
        assert -1e-10 <= dense-exact <= error_bound, (rep,dense,exact,error_bound)
        max_disagreement=max(max_disagreement,abs(dense-exact))
    return max_disagreement


def check_adversarial():
    c=calibrated()
    two=[Frame(0,.95,.95,.01,0),Frame(1/30,.95,.95,.01,0)]
    assert certify(two,c).decision=='UNRESOLVED'
    a={'center_upper_x':'50','center_upper_y':'30','center_lower_x':'50','center_lower_y':'40'}
    b={'center_upper_x':'50','center_upper_y':'30','center_lower_x':'50','center_lower_y':'70'}
    lo,hi=measurement_interval(a,b,100,100,1)
    assert abs(lo-.08)<1e-12 and abs(hi-.42)<1e-12
    clip='a'*20
    manifest={'experiment':'E002-398','clips':[{'clip_id':clip,'frames':[
        {'frame_in_clip':i} for i in range(7)]}]}
    def row(i,who):
        return {'clip_id':clip,'frame_in_clip':str(i),'rater_id':who,
                'center_upper_x':'50','center_upper_y':'30',
                'center_lower_x':'50','center_lower_y':'70'}
    s1={(clip,str(i)):row(i,'rater-A') for i in range(7)}
    s2={(clip,str(i)):row(i,'rater-B') for i in range(7)}
    timing={(clip,str(i)):{'nominal_time_s':str(i/240),'exposure_s':'.001',
                           'clock_error_s':'.0001'} for i in range(7)}
    cfg={'speed_upper':60,'threshold':.2,'iris_scale_lower_px':100,
         'iris_scale_upper_px':100,'landmark_error_px':1,'gates':{}}
    assert analyze(manifest,s1,s2,timing,cfg)['decisions']['ABSTAIN_UNCALIBRATED']==1
    cfg['gates']={k:True for k in ('independent_velocity','aperture_geometry',
        'optical_response','exposure_timing','clock_synchronization',
        'nuisance_resolved','uniform_shutter_verified')}
    assert analyze(manifest,s1,s2,timing,cfg)['decisions']['CONFIRMED_NO_CROSSING']==1
    for i in (1,3,5):s1[(clip,str(i))]['glare']='true'
    assert analyze(manifest,s1,s2,timing,cfg)['decisions']['UNRESOLVED']==1
    for i in range(7):s2[(clip,str(i))]['rater_id']='rater-A'
    try:analyze(manifest,s1,s2,timing,cfg)
    except ValueError:pass
    else:raise AssertionError('Rater identity collision accepted')


def main():
    gap=dense_envelope([0,.01],[.6,.6],60,n=50001)
    assert abs(gap-.3)<1e-10
    disagreement=check_envelope()
    check_adversarial()
    result=simulate()
    assert result['total_wrong_certificates']==0
    print(json.dumps({'independent_checks_passed':True,
                      'random_envelopes':150,'max_grid_difference':disagreement,
                      'adversarial_bridge_checks_passed':True,
                      'synthetic_trials':sum(v['CONFIRMED_CROSSING']+
                        v['CONFIRMED_NO_CROSSING']+v['UNRESOLVED']+
                        v['ABSTAIN_UNCALIBRATED'] for v in result['cohorts'].values()),
                      'human_aperture_validated':False},indent=2))


if __name__=='__main__':main()
