#!/usr/bin/env python3
"""E002-402: frozen synthetic landmark-column identifiability experiment.

The physical target is a signed vertical palpebral gap at independently
calibrated x_ref. This is NOT a human or real-camera experiment.
"""
import json
import math
import random
from e002_399_annotation_bridge import measurement_interval
from e002_399_reference_adequacy import Frame, calibrated, certify


def experiment(seed=402,n=1000):
    # Zero vertical aperture, 20 px column mismatch: diagonal distance is
    # incorrectly interpreted as a 0.4 normalized aperture.
    old=math.hypot(60-80,40-40)/50
    a={'center_upper_x':'60','center_upper_y':'40',
       'center_lower_x':'80','center_lower_y':'40'}
    new=measurement_interval(a,a,50,50,0,70,0,0)
    assert old>.2 and new==(0.,0.), 'G1'
    times=(0.,.004)
    naive=certify([Frame(t,old,old,.001,0.) for t in times],calibrated(0.,.2))
    corrected=certify([Frame(t,*new,.001,0.) for t in times],calibrated(0.,.2))
    assert naive.decision=='CONFIRMED_NO_CROSSING', 'G1a'
    assert corrected.decision=='CONFIRMED_CROSSING', 'G1b'

    # The measured vertical gap is 13 px but the physical gap at x=70 is 9.
    b={'center_upper_x':'60','center_upper_y':'38',
       'center_lower_x':'60','center_lower_y':'51'}
    sloped=measurement_interval(b,b,50,50,0,70,.2,.2)
    assert sloped[0]<=9/50<=sloped[1], 'G2'

    rng=random.Random(seed)
    accepted=excluded=0
    max_violation=0.
    for i in range(n):
        x0=rng.uniform(60,80)
        u0=rng.uniform(35,45)
        gap=rng.uniform(1,22)
        l0=u0+gap
        su=rng.uniform(-.25,.25)
        sl=rng.uniform(-.25,.25)
        error=rng.uniform(0,.75)
        rows=[]
        for r in range(2):
            xu=rng.uniform(45,95)
            xl=rng.uniform(45,95)
            yu=u0+su*(xu-x0)
            yl=l0+sl*(xl-x0)
            row={'center_upper_x':str(xu+rng.uniform(-error,error)),
                 'center_upper_y':str(yu+rng.uniform(-error,error)),
                 'center_lower_x':str(xl+rng.uniform(-error,error)),
                 'center_lower_y':str(yl+rng.uniform(-error,error))}
            rows.append(row)
        if any(float(row['center_lower_y'])<float(row['center_upper_y']) for row in rows):
            excluded+=1
            try: measurement_interval(*rows,50,50,error,x0,.25,.25)
            except ValueError: pass
            else: raise AssertionError('G3 inverted landmark not excluded')
            continue
        lo,hi=measurement_interval(*rows,50,50,error,x0,.25,.25)
        assert lo-1e-12<=gap/50<=hi+1e-12, ('G3',i,lo,hi,gap/50)
        max_violation=max(max_violation,max(0.,lo-gap/50,gap/50-hi))
        accepted+=1
        lo2,hi2=measurement_interval(*rows,50,50,error+.25,x0,.35,.35)
        assert lo2<=lo+1e-12 and hi2>=hi-1e-12, ('G5',i)
    assert accepted>500 and excluded>0, ('G3',accepted,excluded)
    return {'experiment':'E002-402','seed':seed,'trials':n,
            'naive_false_no_crossing_witness':naive.decision,
            'corrected_witness':corrected.decision,
            'sloped_contour_interval':sloped,
            'held_out_covered':accepted,'inverted_excluded':excluded,
            'max_interval_violation':max_violation,
            'uncertainty_monotonicity':True,'human_validation':False,
            'product':'ABSTAIN_UNCALIBRATED'}


if __name__=='__main__':
    print(json.dumps(experiment(),indent=2,sort_keys=True))
