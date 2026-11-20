# E002-669 | Sharp finite-exposure exclusion bound (2026-11-06 UTC)

## Frozen assumptions and question
Let a(t) be normalized eyelid aperture on one rectangular exposure [0,w], with 0<=a<=1 and |a(t)-a(s)|<=V|t-s|. A closure means a(t*)<=tau at some point **within this exposure**. The ideal observation is the uniform exposure mean m=(1/w) integral a(t)dt, observed as y with |y-m|<=eta. V is an independently justified physical ceiling, **not** a finite-sample maximum. This is a conditional mathematical result, not a claim about human velocities or camera calibration.

## Sharp law
Set d=1-tau, r=min(w,d/V). If a closure occurs anywhere in the exposure, then

    1-m >= [d*r - (V/2)*r^2]/w = B(w,V,tau).

Proof: Lipschitzness and a(t*)<=tau imply 1-a(t)>=max(0,d-V|t-t*|). The integral of this symmetric decreasing tent over [0,w] is minimized when t* lies at an exposure boundary, by interval rearrangement (or direct piecewise differentiation). The boundary trajectory a(t)=min(1,tau+Vt) attains equality. Therefore the bound is sharp, including the case w<d/V. A certified **no-closure-within-exposure** conclusion is possible whenever y-eta>1-B. Equality must abstain. If a closure is defined only for a strictly interior instant, the same bound is the sharp infimum by approaching the edge.

The dimensionless form with z=Vw/d (d>0) is B=d*(1-z/2) for z<=1 and B=d/(2z) for z>=1. For tau=1, no exclusion is possible. This is a bound on **within-exposure** closure, not on gaps between exposures or on a natural blink count.

## Exact worked test and falsification
Freeze w=1/30 s, V=60 normalized aperture/s, tau=0.30, eta=0.01. The sharp closure-compatible maximum mean is 351/400=0.8775. Observing y=0.90 certifies no threshold crossing **inside that exposure** because y-eta=0.89>0.8775. At eta=0.03 the same observation must abstain. The adversarial boundary ramp attains 0.8775 while touching tau, proving no stronger uniform bound is possible under these assumptions. Exact rational assertions are in `e002_669_exposure_certificate.py`; no hosted execution or independent replay is claimed.

## Validation and adversarial controls
First independently calibrate shutter integration kernel, linearity, gain and exposure timing with LED/photodiode, including saturation and rolling-shutter rows. Freeze V from a separately justified physical bound (not a sample maximum), tau, aperture geometry and error budget eta before held-out human trials. Compare synchronized high-speed ground truth with ordinary-camera integration under geometry, brightness, gaze, glasses, motion blur, missing frames, and clock error. A real counterexample with calibrated assumptions and y-eta above the threshold falsifies the model or its calibrations. Nonrectangular or uncertain shutter kernels require a new kernel-specific optimization; the rectangular result must not be reused uncritically.

## Product decision
A calibrated exposure mean may sometimes certify **absence of closure during that exposure**; it cannot certify absence in unobserved gaps. Unverified V, shutter kernel, geometry or eta => `ABSTAIN_UNCALIBRATED`. Human evidence 0; independently validated physical camera captures 0; production `BLOCKED`. Next: instrument validation and participant-held-out high-speed sequences, not another synthetic theorem.
