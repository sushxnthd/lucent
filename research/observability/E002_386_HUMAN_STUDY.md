# E002-371/386 — Paired-human prospective validation protocol

**Planned, not executed.** Frozen 2026-10-23. No participants recruited, no recordings analyzed, no ethics approval implied.

## Objective
Prospectively test E002-371 shutter-gap/eyelid-velocity predictions of hidden threshold closures, with independently estimated speed/optical/timing bounds and untouched participant and camera holdouts. Validate conditional false no-hidden decisions among issued predictions and abstention under nuisance shift.

## Participants, acquisition, and ethics
Obtain ethics/IRB determination, adult consent, secure storage, deletion/withdrawal rules and de-identification before collection. Recruit 60 adults, stratified for glasses, gaze direction, eyelid morphology, illumination and camera characteristics. Avoid deliberate sleep deprivation. Record two sessions on separate days if feasible. Pair >=500-fps high-speed ocular reference with ordinary 30- and 60-fps RGB cameras, plus a distinct second manufacturer/model for device holdout. Calibrate exposure start/end with visible LED and photodiode timing; measure synchronization uncertainty and drift (target <0.5 ms). For rolling shutters independently measure row timing. Nominal FPS is not calibration.

## Independent reference calibration
Use calibration-only high-speed sequences to estimate aperture a(t) in [0,1] relative to independent open-eye baseline. Predefine closure threshold theta=0.2. Use two independent annotators and adjudicate uncertain reference frames. Independently bound speed V and, where applicable, acceleration A with high-speed measurement and uncertainty allowance. A finite sample cannot prove a universal physiological maximum; deterministic certificates must remain explicitly conditional on independently justified bounds. Calibrate the intermediate-aperture RGB transfer and error envelope across geometry, illumination, glasses, gaze and blur; open/closed two-point calibration is insufficient.

## Prediction frozen before held-out labels
For each ordinary-camera blind gap [t0,t1], duration H, calibrated aperture lower bounds L,R and speed V, the lower envelope is a(t)>=max(0,L-V(t-t0),R-V(t1-t)). Only when its minimum strictly exceeds theta and all optical, kinematic and clock assumptions hold may a deterministic conditional no-hidden prediction be attempted. For finite exposures derive L,R from independently validated exposure integrals; never treat exposure averages as endpoint measurements. Reference ground truth is a(t)<=theta for >=5 ms entirely within a gap; shorter crossings and uncertain labels are separately adjudicated. A >=500-fps reference does not certify submillisecond crossings.

## Holdouts, endpoints and power
Partition by participant: 36 calibration, 12 validation, 12 untouched test; do not share a participant between splits. Independently hold out a camera model/manufacturer and a later session. Freeze all thresholds, nuisance exclusions, missingness and abstention rules before unlocking test labels. Analyze **all** shutter gaps, not just visually obvious blinks. Primary conditional risk target <=1% false no-hidden among issued, with one-sided 95% upper confidence bound. With zero errors, >=299 independent issued decisions are needed for a simple binomial upper bound below 1%; correlated gaps require participant-cluster analysis and more effective sample. Secondary targets: >=20% issuance on calibrated in-domain recordings, 100% abstention on uncalibrated timing/device, and risk/coverage curves by gaze, glasses, lighting, blur, geometry, missingness and device. Report insufficient power rather than overclaim.

## Adversarial falsification
Induce benign variations in gaze, head pose, glasses/reflections, illumination, blur, partial occlusion, dropped frames, shutter timing and clock drift. A single false hard certificate under supposedly valid bounds suspends that deterministic claim until the broken assumption is identified. If selective risk exceeds the frozen target, no calibrated risk claim. If the unseen device breaks coverage, reject cross-device transfer and abstain. If reference timing, speed or labels are uncertain, report indeterminate rather than negative.

## Reproducible deliverables
Consent-permitted de-identified manifests must include participant/session hashes, sensor model, measured exposure and row timestamps, sync error, frame drops, calibration provenance, reference labels and disagreements, per-gap predictions, nuisance strata, abstention reasons, split assignments, software commit, and complete failures. Publish scripts for risk/coverage, cluster confidence intervals, sharp-envelope checks, and exact counterexample witnesses.

## Product boundary
Until this study succeeds, no physical no-hidden guarantee, no operational risk-qualified blink claim, no PERCLOS, no pupil waveform reconstruction and no fatigue diagnosis. After successful independent human validation, only camera/condition-specific statistical risk-qualified outputs with abstention may be considered; deterministic outputs additionally require independently defensible worst-case optical, timing and physiological bounds.
