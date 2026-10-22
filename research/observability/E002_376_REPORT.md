# E002-376 | Exact phase-coverage law and synchronized-miss counterexample

**2026-10-23. Status: conditional shutter theorem + independent synthetic checker, NOT human/RGB validation.** The preregistered predictions are in E002_376_FROZEN_PHASE_PREDICTION.txt, committed first.

## Signal/reference
Signal: periodic ordinary-camera shutter exposures, reduced to an overlap predicate with a fully closed eyelid plateau. Reference: ideal continuous plateau start and end times. No acquired paired human signal/reference.

## Law
Let the closure plateau be [0,D], exposures [phi+kF, phi+kF+w], 0<w<=F, and qualifying overlap m in (0,w]. The phase phi is uniformly distributed on [0,F). The exposure starts yielding overlap >=m are exactly those in [m-w,D-m]. Their interval has length D+w-2m provided D>=m and w>=m. Modulo period F, the covered phase fraction is

p(D,F,w,m) = 0 if D<m or w<m; otherwise min(1,max(0,(D+w-2m)/F)).

This is exact under periodic exposures and a single contiguous plateau. In dimensionless form with rho=D/F, eta=w/F, lambda=m/w: p=min(1,max(0,rho+eta*(1-2lambda))) with feasibility D>=m.

For m=w, the guaranteed-full-exposure boundary is D>=F+w. For m<=w, the phase-guarantee boundary is D+w-2m>=F, with D>=m. These are *shutter coverage* laws, not guaranteed image visibility.

## Preregistered synthetic predictions and checker
D=58ms, w=10ms, full-exposure threshold m=10ms: capture probabilities at 10/20/25/30fps = 0.48/0.96/1/1. At m=5ms, probabilities at 10/20fps = 0.58/1. All six were verified on a 2000-phase independent interval enumeration, with 300 additional randomized regimes (400 phases each). 132,111 assertions passed in the local checker. The repository checker independently reproduces the same assertions.

## Exact correlated-miss counterexample
At 20fps, F=50ms, w=10ms, D=58ms, phi=49ms, the two nearest exposures are [-1,9]ms and [49,59]ms, each overlapping the plateau by exactly 9ms. Neither exposure is fully within closure. Repeating events every 1000ms, a multiple of F, retains the same phase: 100 consecutive events can all fail the full-exposure criterion. **Do not exponentiate single-event capture probability without independent phase randomization.**

## Measurement/nuisance controls
- **Geometry:** eyelid-closure plateau must be separately defined; optical aperture/contrast can change with gaze.
- **Photometry:** in a linear contrast model, if minimum image contrast is c>0 and each hypothesis can incur bounded error epsilon, guaranteed binary separation requires overlap m>2*epsilon*w/c. If c is not calibrated away from zero, abstain.
- **Blur and glasses:** can reduce effective c or distort aperture; no invariance demonstrated.
- **Missingness:** dropped frames invalidate nominal F and may phase-lock to events. Analyze actual exposure timestamps.
- **Rolling shutter:** each affected row has a different phase; only rows with event-sensitive pixels count.
- **Clock:** absolute phase requires timebase calibration; the uniform phase hypothesis cannot be inferred from frame rate alone.
- **Sampling:** 30fps decimated to 10fps loses the full-exposure capture guarantee, with probability 0.48 under uniform phase.
- **Physiology:** 58ms is an illustrative plateau, motivated by a published cohort mean, not a universal minimum.

## Prior-art audit
The shutter-as-integration model and its aliasing consequences are established imaging science, including Raskar, Agrawal & Tumblin (ACM TOG, 2006), DOI 10.1145/1141911.1141957, and mathematical coded-exposure work (Research in Mathematical Sciences, 2015), DOI 10.1186/s40687-015-0051-8. LPW (Tonsen et al., ETRA 2016, DOI 10.1145/2857491.2857520) offers ~95fps head-mounted eye video, but is not simultaneous ordinary RGB with trusted reference. OpenEDS (Garbin et al., 2019, arXiv 1905.03702) is 200Hz VR eye-facing camera imagery, not the paired validation target. No novelty claim for this elementary coverage theorem.

## Frozen human study
Acquire native ordinary RGB at known exposure, and synchronized >=250fps independent eye-reference. Estimate per-person plateau duration on training participants only; freeze predicted p on participant/device/lighting holdouts. Randomize camera trigger phase when possible. Compare geometry-only, brightness-only, missingness-only and temporal smoothness controls, with gaze, glasses and blur strata. Distinguish (i) shutter coverage, (ii) optical detection, and (iii) fatigue inference. Falsify the model if independently timestamped reference events and measured exposure intervals contradict the predicted coverage. Human data gate remains **FAIL / not executed**.

## Product consequence
**Allowed:** calibrated shutter-coverage risk and interval-valued eyelid observation, with explicit abstention.
**Rejected:** unconditional blink sensitivity, universal PERCLOS, physical pupil-waveform recovery and five-second fatigue diagnosis.
**Publication threshold:** independently replicated human boundary crossing under nuisance holdouts plus priority audit; not met.
