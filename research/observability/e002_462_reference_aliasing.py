"""E002-462 synthetic high-speed reference-camera aliasing; no human/physical validation."""
from __future__ import annotations
import argparse
import json
import math
import random

C = 567.103928 / 1000
O = 274.616337 / 1000
THRESHOLD = 2.0
SEED = 462
NUISANCES = ('geometry','brightness','missingness','blur','gaze','glasses',
             'sampling','clock','rolling_shutter','exposure_kernel')

def triangle_interval(b, tau, c=THRESHOLD):
    if not all(math.isfinite(v) for v in (b,tau,c)) or b <= c or c < 0:
        raise ValueError('invalid aperture/phase')
    return tau-(b-c)/C, tau+(b-c)/O

def exposure_mean(b, tau, center, width, c=THRESHOLD):
    if not math.isfinite(width) or width <= 0:
        raise ValueError('invalid exposure width')
    left,right=triangle_interval(b,tau,c)
    a,z=center-width/2,center+width/2
    u,v=max(a,left),min(z,tau)
    left_area=C/2*((v-left)**2-(u-left)**2) if v>u else 0.0
    u,v=max(a,tau),min(z,right)
    right_area=O/2*((right-u)**2-(right-v)**2) if v>u else 0.0
    return b-(left_area+right_area)/width

def reference_observation(fps,b,tau,width_ms):
    if not isinstance(fps,int) or fps<=0:
        raise ValueError('invalid fps')
    dt=1000/fps
    if width_ms>=dt:
        return {'decision':'ABSTAIN_UNCALIBRATED','reason':'OVERLAPPING_REFERENCE_SHUTTERS'}
    centers=[j*dt for j in range(-4,8)]
    observed=[exposure_mean(b,tau,t,width_ms) for t in centers]
    deviations=[abs(b-x) for x in observed]
    return {'decision':'SYNTHETIC_REFERENCE_ONLY','fps':fps,'baseline_mm':b,
            'tau_ms':tau,'width_ms':width_ms,'centers_ms':centers,
            'means_mm':observed,'max_deviation_mm':max(deviations),
            'indistinguishable_exact':max(deviations)<1e-12,
            'threshold_only_missed':all(x>THRESHOLD for x in observed),
            'actual_threshold_contact':True,'physical_certification':False}

def safe_reference(record):
    def abstain(why):
        return {'decision':'ABSTAIN_UNCALIBRATED','reason':why,'physical_certification':False}
    if not isinstance(record,dict):
        return abstain('INVALID_RECORD')
    flags=record.get('nuisance')
    if not isinstance(flags,dict) or any(flags.get(k)!='CLEAR' for k in NUISANCES):
        return abstain('NUISANCE_UNRESOLVED')
    if record.get('synthetic_instrument_only') is not True:
        return abstain('NO_AUTHENTICATED_PHYSICAL_REFERENCE')
    if record.get('speed_caps_are_hypothetical') is not True:
        return abstain('CAP_PROVENANCE_INVALID')
    try:
        fps=record['fps'];b=float(record['baseline_mm'])
        tau=float(record['tau_ms']);width=float(record['width_ms'])
        if not isinstance(fps,int) or isinstance(fps,bool):
            return abstain('INVALID_FPS')
        if not all(math.isfinite(v) for v in (b,tau,width)) or width<=0:
            return abstain('INVALID_NUMERIC_INPUT')
        return reference_observation(fps,b,tau,width)
    except (ValueError,TypeError,KeyError,OverflowError):
        return abstain('INVALID_NUMERIC_INPUT')

def fixture(fps=400,b=2.3,tau=1.0,width=0.3):
    return {'fps':fps,'baseline_mm':b,'tau_ms':tau,'width_ms':width,
            'synthetic_instrument_only':True,'speed_caps_are_hypothetical':True,
            'nuisance':{k:'CLEAR' for k in NUISANCES}}

def run():
    primary=[]
    for fps,b,tau in ((400,2.3,1.0),(1000,2.1,0.4)):
        p=safe_reference(fixture(fps,b,tau))
        primary.append({'fps':fps,'baseline_mm':b,'tau_ms':tau,
                        'indistinguishable_exact':p['indistinguishable_exact'],
                        'max_deviation_mm':p['max_deviation_mm'],
                        'threshold_only_missed':p['threshold_only_missed']})
    rng=random.Random(SEED)
    cells=[]
    for fps in (400,1000,2000):
        for b in (2.3,2.1):
            for width in (0.3,0.8):
                dt=1000/fps
                if width>=dt:
                    cells.append({'fps':fps,'baseline_mm':b,'width_ms':width,
                                  'decision':'ABSTAIN_UNCALIBRATED',
                                  'reason':'OVERLAPPING_REFERENCE_SHUTTERS'})
                    continue
                phases=[rng.random()*dt for _ in range(1000)]
                observations=[reference_observation(fps,b,t,width) for t in phases]
                cells.append({'fps':fps,'baseline_mm':b,'width_ms':width,
                              'n':len(observations),
                              'indistinguishable':sum(p['indistinguishable_exact'] for p in observations),
                              'threshold_only_missed':sum(p['threshold_only_missed'] for p in observations),
                              'critical_gap_ms':(b-THRESHOLD)*(1/C+1/O),
                              'dark_gap_ms':dt-width,'physical_certification':False})
    return {'experiment':'E002-462','tier':'SYNTHETIC_INSTRUMENT_ONLY',
            'seed':SEED,'closing_mm_s':C*1000,'opening_mm_s':O*1000,
            'threshold_mm':THRESHOLD,'primary':primary,'cells':cells,
            'limitations':['point threshold contact, not sustained closure',
                           'no physical camera or anatomical ground truth',
                           'velocity maxima hypothetical, not hard physiological caps',
                           'no sensor noise, blur, timing error or anatomical nuisance'],
            'product':'ABSTAIN_UNCALIBRATED'}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--json',action='store_true')
    args=ap.parse_args()
    print(json.dumps(run(),sort_keys=True,indent=2 if args.json else None))
