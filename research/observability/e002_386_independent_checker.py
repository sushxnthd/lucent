"""Independent E002-386 checks: adaptive quadrature, binomial tails, product gates."""
import json
import numpy as np
from scipy.integrate import quad
from scipy.stats import binom
from e002_386_selective_calibration import (
    CENTER,F,W,V,THETA,H,CANDIDATES,ALPHA,DELTA,
    exposure_mean_left,upper_bound,product_decision,simulate,margin,calibrate,
)
def main():
    rng=np.random.default_rng(386112)
    errs=[]
    for a in rng.uniform(.17,.195,100):
        crossing=max(0.,min(W,CENTER-(1-a)/V))
        integral=quad(lambda t:min(1.,a+V*abs(t-CENTER)),0,W,
                      epsabs=1e-13,points=[crossing])[0]/W
        errs.append(abs(integral-float(exposure_mean_left(a))))
    assert max(errs)<2e-12,max(errs)
    tails=[]
    for n in [1,2,3,5,10,50,100,500,2000]:
        for k in [0,1,2,n//2,n-1]:
            if not (0<=k<n):continue
            u=upper_bound(k,n)
            tails.append(abs(binom.cdf(k,n,u)-DELTA/len(CANDIDATES)))
    assert max(tails)<1e-9,max(tails)
    x=simulate(3000,np.random.default_rng(836))
    assert np.all(x['min_aperture'][~x['hidden']]>THETA)
    assert np.all(x['min_aperture'][x['hidden']]<THETA)
    assert np.all((x['reference']>=0)&(x['reference']<=1))
    assert np.all(np.isfinite(margin(x['observed'])))
    cal=calibrate(x)
    assert all((cal['bounds']>=0)&(cal['bounds']<=1))
    if cal['selected'] is not None:
        assert cal['bounds'][cal['selected']]<=ALPHA
    b=dict(known_device=True,timing_calibrated=True,frames_complete=True,
           score=.5,quality=.1,candidate=0,validation_status='paired_human_independent')
    assert product_decision(**{**b,'validation_status':'synthetic_only'})=='ABSTAIN_NO_HUMAN_VALIDATION'
    assert product_decision(**{**b,'known_device':False})=='ABSTAIN_UNSEEN_DEVICE'
    assert product_decision(**{**b,'timing_calibrated':False})=='ABSTAIN_TIMING'
    assert product_decision(**{**b,'frames_complete':False})=='ABSTAIN_MISSINGNESS'
    assert product_decision(**{**b,'score':float('nan')})=='ABSTAIN_INVALID_MEASUREMENT'
    assert product_decision(**{**b,'candidate':None})=='ABSTAIN_NO_VALID_CALIBRATION'
    assert product_decision(**b)=='STATISTICAL_RISK_QUALIFIED'
    assert abs(CENTER-(W+F)/2)<1e-15 and H>0
    print(json.dumps({'status':'PASS','quadrature_checks':len(errs),
          'max_exposure_integral_error':max(errs),'cp_tail_checks':len(tails),
          'max_cp_tail_error':max(tails),'reference_samples_checked':len(x['hidden']),
          'product_gates_checked':7},indent=2))
if __name__=='__main__':main()
