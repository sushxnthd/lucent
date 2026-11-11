# E002-744 | Frozen human and instrument validation protocol (2026-11-11 UTC)

Status: **protocol only; zero acquired human or instrument observations**. This is a prospective test, not evidence of efficacy. Existing E002-371 theorem and E002-743 exposure-kernel limitation are the starting point. Do not change thresholds after opening held-out labels.

## Hypothesis and decision

For aperture a(t)>=0, |a'(t)|<=V, two point observations with conservative aperture lower bounds l0,l1 at physical times t0<t1, and an upper bound D on their separation, the sharp bridge lower envelope is max(0,(l0+l1-V D)/2) at its minimum when the two cones meet (subject to feasibility). **Exclude a hidden full closure only if l0+l1>V D**. Equality is ambiguous. In normalized coordinates R=(l0+l1)/(V D), R>1 is a conditional exclusion, R<=1 is indeterminate; V=0 or D=0 require separate exact handling. For exposure-integrated measurements, first derive valid point lower bounds using calibrated aperture linearity and the independently measured temporal exposure kernel; do not substitute brightness or nominal frame time. Include measurement uncertainty by reducing l_i, and timing/rolling-shutter uncertainty by increasing D.

Primary prospective falsifier: any independently adjudicated complete closure in an interval certified R>1 invalidates the claimed bound/measurement assumptions for that condition. Do not silently relabel a falsifier as tracking failure; record cause and downgrade product claim.

## Acquisition and calibration (two independent channels)

Instrument arm: motorized opaque aperture or electronically timed shutter with independently logged encoder/photodiode transition timestamps; synchronized ordinary camera at 30/60 fps and reference camera >=240 fps, with recorded actual frame timestamps, exposure durations, rolling-shutter readout and dropped frames. Measure exposure temporal response using independently triggered LED pulses and photodiode, not image brightness alone. Calibrate geometric aperture conversion against known opening widths and an optical ruler. Use two shutter motion regimes, including one not used to tune the estimator. A reference camera alone is not continuous ground truth; the independent photodiode/encoder is decisive.

Human arm (after consent and ethics/privacy review): >=20 participants for feasibility, with >=10 held out entirely from all calibration and model choices; target >=100 adjudicable blink intervals in the held-out set but report actual count. Synchronized >=240 fps reference and 30/60 fps ordinary video; two blinded annotators mark full eyelid closure with disagreement resolved by a third, retaining UNCERTAIN labels. Do not infer physical closure solely from pupil-center trajectories. Obtain independent per-participant/condition upper velocity estimates on calibration segments; **empirical maxima do not certify hard bounds**. Unless an externally justified physical ceiling exists, label all human exclusions *statistical exploratory*, never deterministic.

## Precommitted splits and nuisance grid

Split by participant before examining test labels; separate instrument calibration runs from held-out motion programs. Random seed 744 for assigning human participants, stratified only by prespecified glasses/no-glasses category. Condition grid: illumination high/low; gaze straight/off-axis; glasses yes/no where applicable; blur native/defocused; frame rate 30/60; injected missingness 0/10%; timestamp perturbations within measured clock uncertainty; geometry and skin/eyelid contrast measured as covariates. Report unsupported strata rather than pool away failures. Each trial records device, lens, shutter mode, timestamp source, synchronization residual, actual exposure, rolling-shutter model, tracking confidence, aperture uncertainty, and ground-truth adjudication.

## Frozen metrics and kill rules

Primary: false exclusion count / adjudicated full-closure intervals among intervals where certificate says EXCLUDE; report exact Clopper-Pearson 95% interval and denominator. Also report exclusion coverage, abstention rate, and nuisance-stratum false exclusions with denominators. Secondary: calibration-vs-test velocity exceedance; closure-label disagreement; photodiode/reference mismatch; per-session multiplicity and participant-specific failures. A zero-error result on n exclusions has one-sided 95% upper error bound 1-0.05^(1/n), not zero risk. Any false exclusion blocks deterministic product use and triggers root-cause analysis; >5% ambiguous reference labels in a stratum blocks a validation claim for that stratum. No claim of subgroup coverage without subgroup sample sizes and independent calibration.

## Release gate and evidence tiers

T0 mathematical bound; T1 synthetic simulation; T2 independent instrument timing and aperture; T3 blinded participant-disjoint human validation; T4 external replication. Current evidence <=T1. Production state remains ABSTAIN_UNCALIBRATED/BLOCKED. A product may report observed fatigue proxies with uncertainty only after separate validation; never claim unseen eyelid closures were excluded using an uncertified physiological V. Preserve raw timestamps, calibration files, anonymized annotations, frozen code hash, prediction CSV generated before label reveal, and a signed manifest; do not publish identifiable eye video without explicit consent.

## Immediate executable experiment

Before any further theorem polishing: build the shutter/LED/photodiode rig, run a blinded 30/60-fps subsampling trial with >=100 independently timed closure/nonclosure intervals and a held-out motion program. Generate predictions before revealing photodiode closure labels. If physical hardware is unavailable, run a separately implemented simulator with adversarial exposure kernels, timing offsets, dropped frames and bounded-aperture trajectories; label it T1 only. Then begin the participant protocol after consent and independent oversight. 
