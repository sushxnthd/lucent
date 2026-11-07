# E002-486 | Frozen 150-fps reference-aliasing experiment
Frozen 2026-10-27 before implementation or result inspection. Primary kernel E002-371; branch research/observability-human-boundary, draft PR #26. This is a **synthetic shutter/instrument model**, not a claim about Guttmann-Flury participant videos.

## Question
Can a high-speed 150-fps *reference camera* certify the absence of anatomical eyelid closure between its own exposures, even if its shutter duration is independently known?

## Prespecified model
Let period T=20/3 ms (150 fps), rectangular exposure width e=1 ms centered at kT, normalized eyelid aperture a in [0,1], baseline b=0.35, operational closure threshold c=0.10, and a hard illustrative Lipschitz velocity cap V=0.10 aperture-fraction/ms. World A is a(t)=b. World B is b outside a triangular dip centered halfway between consecutive reference exposures, reaching c at t=T/2, with |a'|<=V. Repeat the dip every T. The observed reference signal is the rectangular-exposure *average* of aperture, not an instantaneous frame sample. A second, independently phased 150-fps exposure train is centered at (k+1/2)T. No claim that the public human dataset's exposure width or hard V equals these illustrative values.

## Frozen predictions / decisive controls
1. Sharp hidden-threshold condition for constant baseline throughout the two neighboring exposure intervals: V(T-e) >= 2(b-c). Define dimensionless R=V(T-e)/(2(b-c)). For R>=1 a closure touching c can be hidden; R>1 allows a strict below-threshold closure. R<1 rules it out *within this model only*. For the frozen numbers R=17/15=1.1333333333; critical V=3/34=0.0882352941 fraction/ms.
2. World A and World B have identical original-phase exposure averages, exactly b=0.35, at all k. This is a *constructive nonidentifiability* result even with exposure averaging.
3. The half-phase probe returns b=0.35 for A and 0.125 for B. For independently bounded half-phase center jitter |j|<=0.25 ms, B's mean is <=0.13125 while A stays 0.35. A decision threshold 0.15 separates them under an aperture-equivalent independent gain error <=10% and additive error <=0.01: B maximum <=0.154375? Check before claiming guaranteed detectability; failure must be recorded if the margin is insufficient.
4. Negative controls: V=0.08 yields R<1 and no hidden closure under baseline/exposure assumptions; an uncalibrated or adversarially shifted reference phase cannot justify absence; 20% gain plus 0.03 additive error should defeat the 0.15 detection threshold for some allowed realizations.
5. Separate reference-level and phone-level claims. No sampled absence in the 150-fps reference may be promoted to ground-truth nonclosure; 150-fps observed closure can falsify some 30-fps conditional exclusions. No real human observations are claimed.

## Reproducibility
Standard-library-only Python experiment and tests, exact rational arithmetic where practical, deterministic JSON aggregate, no private images or videos committed. Keep all synthetic parameters explicitly labeled and all failed predictions visible. Release always BLOCKED / ABSTAIN_UNCALIBRATED pending independently measured shutter/exposure, velocity envelope and human trajectories.
