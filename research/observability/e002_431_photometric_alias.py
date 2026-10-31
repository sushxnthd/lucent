"""E002-431 synthetic photometric alias; not human evidence or camera calibration."""
from __future__ import annotations
import json
import math
import random

D = 1.0 / 30.0
E = 0.002
THETA = 2.0
V = 1.2  # hypothetical, NOT a human physiological hard cap
TARGET = 2.04
G_BROAD = (0.97, 1.03)
G_NARROW = (0.995, 1.005)

def _finite(x):
    return isinstance(x, (int, float)) and math.isfinite(x)

def conditional_lower(y0, y1, gain_upper, speed_cap, center_spacing, exposure_s=E):
    """Conservative center-to-center bound for equal nonoverlapping boxcar shutters.

    Assumes y_i=avg(g*a), 0<g<=gain_upper, a>=0, |a'|<=speed_cap.
    Does not apply to arbitrary shutter kernels or real uncalibrated images.
    """
    if not all(_finite(x) for x in (y0,y1,gain_upper,speed_cap,center_spacing,exposure_s)):
        raise ValueError('all parameters must be finite')
    if min(y0,y1)<0 or gain_upper<=0 or speed_cap<0 or center_spacing<=0 or exposure_s<=0 or exposure_s>center_spacing:
        raise ValueError('invalid physical parameter')
    return max(0.0, min(y0,y1)/gain_upper-speed_cap*center_spacing/2)

def study_only_decision(y0,y1,gain_upper,speed_cap,center_spacing,
                        independent_calibration_attested=False,all_nuisances_bounded=False):
    """Never authorize real-world certification from this synthetic surrogate."""
    if not isinstance(independent_calibration_attested,bool) or not isinstance(all_nuisances_bounded,bool):
        raise ValueError('attestations must be explicit booleans')
    lower=conditional_lower(y0,y1,gain_upper,speed_cap,center_spacing)
    candidate=bool(independent_calibration_attested and all_nuisances_bounded and lower>THETA)
    return dict(lower_mm=lower,study_only='CONDITIONAL_CANDIDATE' if candidate else 'ABSTAIN',
                physical_certificate_authorized=False,product='ABSTAIN_UNCALIBRATED')

def hidden_aperture(t):
    if t<=0 or t>=D:
        return 2.01
    return 2.01-0.02*(1-abs(2*t/D-1))

def gain_hidden(t):
    return TARGET/hidden_aperture(t)

def integrate_product_piecewise(times,avals,gvals,start,end):
    """Exact integration of the product of piecewise-linear aperture and gain."""
    if len(times)<2 or len(times)!=len(avals) or len(times)!=len(gvals):
        raise ValueError('invalid knots')
    if not all(_finite(x) for x in times+avals+gvals+[start,end]):
        raise ValueError('nonfinite')
    if not all(t1>t0 for t0,t1 in zip(times,times[1:])):
        raise ValueError('nonincreasing knots')
    if not (times[0]<=start<end<=times[-1]):
        raise ValueError('integration outside support')
    total=0.0
    for j in range(len(times)-1):
        t0,t1=times[j:j+2]
        l=max(start,t0);r=min(end,t1)
        if r<=l:continue
        dt=t1-t0
        pa=(avals[j+1]-avals[j])/dt
        pg=(gvals[j+1]-gvals[j])/dt
        a=avals[j]+pa*(l-t0)
        g=gvals[j]+pg*(l-t0)
        w=r-l
        total+=a*g*w+(a*pg+g*pa)*w*w/2+pa*pg*w*w*w/3
    return total

def stress(n=2000,seed=431):
    if not isinstance(n,int) or n<1 or not isinstance(seed,int):
        raise ValueError('invalid stress arguments')
    rng=random.Random(seed)
    times=[-0.002,0,D/4,D/2,3*D/4,D,D+0.002]
    false_cert=0;candidates=0;witnessed_closures=0
    worst_margin=float('inf');min_gain=1.0;max_gain=1.0
    for _ in range(n):
        a=[rng.uniform(1.8,2.35)]
        for left,right in zip(times,times[1:]):
            a.append(a[-1]+rng.uniform(-V,V)*(right-left))
        g=[rng.uniform(*G_BROAD) for _ in times]
        y0=integrate_product_piecewise(times,a,g,-E/2,E/2)/E
        y1=integrate_product_piecewise(times,a,g,D-E/2,D+E/2)/E
        lower=conditional_lower(y0,y1,G_BROAD[1],V,D)
        truth=min(a[1:-1])
        candidate=lower>THETA
        candidates+=int(candidate)
        witnessed_closures+=int(truth<=THETA)
        false_cert+=int(candidate and truth<=THETA)
        worst_margin=min(worst_margin,truth-lower)
        min_gain=min(min_gain,*g);max_gain=max(max_gain,*g)
    return dict(n=n,seed=seed,candidates=candidates,witnessed_closures=witnessed_closures,
                false_certificates=false_cert,min_true_minus_bound_mm=worst_margin,
                observed_gain_range=[min_gain,max_gain])

def experiment():
    rates=(24,30,60,120,500)
    exposures=(0.0005,0.002,0.004)
    max_error=0.0
    for rate in rates:
        for exposure in exposures:
            for i in range(3):
                center=i/rate
                n=101
                average=sum(gain_hidden(center+exposure*((k+0.5)/n-0.5))*hidden_aperture(center+exposure*((k+0.5)/n-0.5)) for k in range(n))/n
                max_error=max(max_error,abs(average-TARGET))
    bmax=max(gain_hidden(t) for t in (0,D/2,D))
    naive=conditional_lower(TARGET,TARGET,1.0,V,D)
    broad=conditional_lower(TARGET,TARGET,G_BROAD[1],V,D)
    narrow=conditional_lower(TARGET,TARGET,G_NARROW[1],V,D)
    return dict(evidence_tier='SYNTHETIC_PHOTOMETRIC_ALIAS',
                hidden_aperture_min_mm=hidden_aperture(D/2),open_aperture_min_mm=TARGET,
                hidden_velocity_peak_mm_s=0.02/(D/2),
                hidden_gain_min=gain_hidden(0),hidden_gain_max=bmax,
                photometric_observation_constant=TARGET,
                max_shutter_average_discrepancy=max_error,
                naive_fixed_gain_lower_mm=naive,naive_false_certificate=naive>THETA,
                broad_gain_lower_mm=broad,broad_abstains=broad<=THETA,
                narrow_gain_lower_mm=narrow,narrow_conditional_candidate=narrow>THETA,
                hidden_world_violates_narrow_gain=bmax>G_NARROW[1],
                random_stress=stress(),real_physical_gain_authenticated=False,
                real_physical_speed_cap_authenticated=False,
                physical_certificate_authorized=False,product='ABSTAIN_UNCALIBRATED')

if __name__=='__main__':
    print(json.dumps(experiment(),sort_keys=True,indent=2))
