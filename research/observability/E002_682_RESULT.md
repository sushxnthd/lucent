# E002-682 | Finite exposure averages do not certify an instantaneous eyelid-velocity ceiling

**Evidence:** analytic counterexample and executed exact-rational standard-library regression, not human/physical evidence. Extends E002-681 from instantaneous samples to any **finite family of ideal box-integrated exposures** (possibly overlapping, unequal durations). Not a claim about all camera transfer functions, nor human physiological feasibility.

## Proposition and proof

Let the observed values be finitely many interval integrals (or their duration-normalized averages) of an unknown aperture a(t) in [0,1]. Let all exposure start/end times form a finite ordered endpoint set. Choose any nonempty open cell between adjacent endpoints and place a narrow support [s,s+w] strictly inside it. Every observed exposure either contains the entire support or misses it, because no exposure boundary lies inside the cell.

Define q(x)=x^3(1-x)^3 for x in [0,1], and zero outside; define the perturbation h(t)=epsilon*q'((t-s)/w) on [s,s+w] and zero outside. Since q'(0)=q'(1)=q''(0)=q''(1)=0, h is C1 when spliced to zero. Its integral over the support is epsilon*w*[q(1)-q(0)]=0. Therefore every recorded exposure integral and average is **identical** for the baseline a(t)=1/2 and perturbed trace a(t)=1/2+h(t). The conservative bound |q'(x)|<=36 for x in [0,1] and epsilon=1/1000 keeps both traces in [0,1]. However h'(t)=epsilon*q''((t-s)/w)/w; q''(1/4) is nonzero, so instantaneous velocity grows without bound as w decreases. Consequently no finite deterministic speed ceiling follows solely from finitely many ideal exposure averages.

**Important scope:** Requires no separately imposed acceleration, bandwidth, anatomical or physical-speed restriction. It is an inverse-problem non-identifiability result; not a physically realistic eyelid trajectory. A sufficiently restrictive independently established dynamical model may exclude the constructed witnesses. Other non-box camera response functions are not covered by this proof.

## Executed reproduction

Run `python research/observability/e002_682_exposure_nullspace.py`. Local Python standard-library run passed: four overlapping/unequal box exposure windows, widths 1/1000, 1/10000, 1/100000 seconds, all exact-rational integrals unchanged. The q''(1/4) speed witnesses were 0.070312, 0.703125, and 7.031250 aperture/s, scaling tenfold per tenfold narrowing. These are constructed values, not physiological speeds. Hosted CI and independent replay remain outstanding.

## Product decision and priority

Finite high-speed **exposure-integrated** recordings, like instantaneous samples, cannot by themselves authenticate a deterministic hard human eyelid-speed ceiling. E002-371 must remain conditional on an independently justified physical velocity bound; otherwise `ABSTAIN_UNCALIBRATED`. This closes a stated scope gap in E002-681 but does **not** validate the theorem on humans or unlock a product claim. The next priority remains the frozen E002-671 synchronized physical shutter/photodiode and blinded held-out human protocol, not additional synthetic examples. Production `BLOCKED`.
