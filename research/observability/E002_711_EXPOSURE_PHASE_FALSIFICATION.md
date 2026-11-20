# E002-711 | Exposure-phase and photometric nonidentifiability (synthetic falsification)

**Evidence tier:** locally executed synthetic mathematics, **not** independent verification, physical capture, or human validation. Tested 2026-11-07 UTC.

## Question
Does the E002-710 minimum integrated anatomical-aperture deficit imply a detectable ordinary-camera pixel deficit under unknown phase and illumination?

## Result
**No.** For a triangular Lipschitz closure with aperture A, velocity ceiling V, centered at time zero, the anatomical deficit at time t is d(t)=max(0,A-V|t|). Its integral over the entire event is A²/V. A shutter window [s,s+T] captures only D(s)=integral d(t)dt over that window; D(s)=0 for windows disjoint from [-A/V,A/V]. The full-event lower bound is applicable only when the *entire* event is inside a calibrated exposure.

Even for full containment, an additive time-averaged photometric nuisance b=D/T yields measured average aperture proxy A-D/T+b=A, exactly the open-eye baseline. Thus an uncalibrated brightness-derived measurement cannot certify exclusion from the anatomical bound. This is a counterexample, not evidence that any actual phone behaves this way.

## Reproducible check
Run `python research/observability/e002_711_exposure_phase_falsification.py`. Locally executed: exact piecewise primitive agrees with 100,000-bin midpoint quadrature at six phases (absolute tolerance 2e-9); 4,001-phase sweep satisfies 0<=D<=A²/V; disjoint shutter gives D=0; additive photometric offset cancels full-event deficit. Numerical example A=1, V=2, T=1.5: D=0.5, canceling offset 1/3. No stochastic samples, cameras, or human participants.

## Product and empirical consequence
- **REJECT:** infer closure exclusion from raw smartphone brightness or a camera-frame exposure integral without phase, aperture-to-pixel transfer, and illumination uncertainty calibration.
- **ABSTAIN:** if closure could fall outside the observed exposure union or if photometric nuisance bound is >= predicted mean deficit.
- **PHYSICAL TEST:** independently timed occluder/photodiode reference, randomized shutter phase, controlled LED brightness perturbations, measured exposure and rolling-shutter intervals, then blinded phase-wise exclusion predictions. A false exclusion kills the certificate.
- Preserve E002-704 participant-disjoint preregistration; do not treat synthetic checks as physiological speed calibration.

No claim of mathematical novelty or validation of E002-371 on human eyelids. Production remains BLOCKED / ABSTAIN_UNCALIBRATED.
