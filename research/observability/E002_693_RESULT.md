# E002-693 — Exposure-operator aliasing falsification

Evidence tier: **exact-rational synthetic counterexample**, not human or physical measurement.

## Frozen construction
An anatomical aperture follows a piecewise-linear triangular dip, x(t)=1-d max(0,1-|t-h/2|/w), with dip depth d and half-width w. The two ordinary-camera shutter exposures occupy [-1,0] and [h,h+1]. A sensor reporting the *mean aperture* over each exposure is deliberately an idealized favorable measurement operator; real pixels mix appearance, geometry and illumination. The intervening shutter gap is (0,h). The closure threshold is 1/4.

Enumerate h in {1/2,1,2}, w in {1/8,1/4,1/2}, d in {3/4,1}. Compute each exposure integral exactly by partitioning at all trajectory knots. Compare the two exposure means with the true minimum at h/2.

## Executed result
Python standard-library exact fractions: **18/18** constructed trajectories contain a threshold closure and **18/18** yield two exposure means strictly above the closure threshold. Example h=1/2,w=1/8,d=3/4: both measured means are 1 while the unobserved minimum is 1/4. This is a constructive counterexample, **not** a measured failure frequency, statistical prevalence, or novel theorem.

## Falsified inference and enforcement
A high exposure-averaged eyelid aperture is **not** an instantaneous endpoint aperture. Substituting exposure means into E002-371/E002-687 or inferring a hard physiological speed ceiling from differences between two averages is unjustified. A shutter-gap exclusion certificate may only consume independently bounded instantaneous anatomical aperture intervals and independently validated velocity/acceleration ceilings, with physical shutter support and timing uncertainty. Otherwise **ABSTAIN_UNCALIBRATED**; production **BLOCKED**.

## Limitations and next decisive test
The synthetic instrument has exact linear integration, perfect geometric aperture readout, and known timing, deliberately removing brightness, blur, gaze, glasses and rolling shutter; realistic nuisances cannot rescue the invalid inference without additional assumptions. The construction does not falsify the conditional E002-371 theorem itself. Execute the frozen E002-690 synchronized instrument/human protocol, independently replay this script, and measure exposure support and anatomical aperture uncertainty before any product claim. No human data obtained.
