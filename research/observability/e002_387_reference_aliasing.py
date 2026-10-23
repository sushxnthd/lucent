"""E002-387: frozen synthetic high-speed reference exposure falsification.
Requires numpy and scipy; not human data. Protocol: E002_387_FROZEN.md.
"""
import json
from pathlib import Path
import numpy as np

V=40.0
THETA=.2
HS=(.17,.185,.195)
FS=(240,960)
EXPOSURES=(0.,.0005,.002,.004)
N=10000

def aperture(t,h,center=0.):
    return np.minimum(1.,h+V*np.abs(np.asarray(t)-center))

def primitive(x,h):
    x=np.asarray(x,dtype=float)
    y=np.abs(x)
    r=(1.-h)/V
    val=np.where(y<=r,h*y+.5*V*y*y,h*r+.5*V*r*r+y-r)
    return np.sign(x)*val

def shutter_mean(t,h,center,e):
    if e==0:return aperture(t,h,center)
    return (primitive(np.asarray(t)-center+e/2,h)-primitive(np.asarray(t)-center-e/2,h))/e

def run():
    records=[]
    for h in HS:
        for fps in FS:
            for e in EXPOSURES:
                if e>1/fps+1e-12:continue
                centers=(np.arange(N)+.5)/N/fps
                times=np.arange(-3,4)/fps
                observed=shutter_mean(times[None,:],h,centers[:,None],e)
                detected=np.any(observed<THETA-1e-13,axis=1)
                D=2*(THETA-h)/V
                records.append(dict(h=h,fps=fps,exposure_s=e,true_duration_ms=1000*D,
                    detected=int(detected.sum()),missed=int((~detected).sum()),
                    detection_rate=float(detected.mean()),
                    ideal_point_phase_probability=min(1.,D*fps)))
    return records

def reference_qualifier(exposure=None,period=None,speed=None,optical=None,timing=None,negative=True):
    if any(x is None for x in (exposure,period,speed,optical,timing)):
        return "ABSTAIN_UNCALIBRATED_REFERENCE"
    if min(exposure,period,speed,optical,timing)<0 or period==0 or speed==0 or exposure>period:
        return "ABSTAIN_INVALID_CALIBRATION"
    return "ABSTAIN_NEGATIVE_REFERENCE_NOT_GROUND_TRUTH" if negative else "REFERENCE_EVENT_DETECTED_NOT_PHYSICAL_CERTIFICATE"

def verify(records):
    from scipy.integrate import quad
    rng=np.random.default_rng(387)
    errors=[]
    for _ in range(150):
        h=float(rng.choice(HS));fps=int(rng.choice(FS))
        e=float(rng.choice([x for x in EXPOSURES if x<=1/fps]))
        center=float(rng.uniform(0,1/fps));t=float(rng.uniform(-1/fps,2/fps))
        exact=float(shutter_mean(t,h,center,e))
        if e==0:independent=float(aperture(t,h,center))
        else:
            cuts=[p for p in (center,center+(1-h)/V,center-(1-h)/V) if t-e/2<p<t+e/2]
            independent=quad(lambda x:float(aperture(x,h,center)),t-e/2,t+e/2,
                             points=cuts,epsabs=1e-13,epsrel=1e-13)[0]/e
        errors.append(abs(exact-independent))
    assert max(errors)<1e-9
    lookup={(r["h"],r["fps"],r["exposure_s"]):r for r in records}
    for h in HS:
        for fps in FS:
            r=lookup[(h,fps,0.)]
            assert abs(r["detection_rate"]-r["ideal_point_phase_probability"])<=1/N+1e-10
    assert all(lookup[(h,240,.004)]["detected"]==0 for h in HS)
    assert lookup[(.17,960,.0005)]["detected"]==N
    assert lookup[(.195,960,.0005)]["detected"]==0
    assert reference_qualifier()=="ABSTAIN_UNCALIBRATED_REFERENCE"
    assert reference_qualifier(.002,1/240,40,.01,.0001)=="ABSTAIN_NEGATIVE_REFERENCE_NOT_GROUND_TRUTH"
    return dict(quadrature_checks=len(errors),max_abs_error=max(errors),
                point_phase_checks=len(HS)*len(FS),frozen_predictions_passed=True)

if __name__=="__main__":
    records=run()
    result=dict(scope="synthetic-only",phase_grid=N,speed_per_s=V,
                threshold=THETA,records=records,verification=verify(records))
    output=Path(__file__).with_name("e002_387_results.json")
    output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print("E002-387 PASS",result["verification"])
