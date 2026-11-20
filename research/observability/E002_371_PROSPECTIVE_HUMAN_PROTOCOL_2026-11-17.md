# E002-371: frozen prospective human shutter-gap validation protocol (2026-11-17 UTC)

Status: **protocol only; no human data collected, no velocity bound validated, no camera-derived fatigue claim authorized**. This is a prospective test of a necessary-and-sufficient *mathematical* closure feasibility criterion under explicitly bounded eyelid-aperture velocity, not a claim that any population shares one velocity ceiling.

## Estimand and prediction

Let a(t) be calibrated palpebral aperture (mm) at a fixed landmark, c the predeclared closure threshold (mm), and V an independently bounded absolute aperture velocity (mm/s). For two instantaneous observations a(0)=L and a(T)=R, a hidden visit to a<=c is feasible in the Lipschitz model iff (L-c)_+ + (R-c)_+ <= V T, **provided** |L-R|<=VT. If endpoints are incompatible, label **MODEL-INCONSISTENT**, never 'no blink'. Equality is feasible. The dimensionless closure margin is M=[(L-c)_+ + (R-c)_+]/(VT). M>1 forbids hidden closure *conditional on a valid V bound*; M<=1 does not establish that closure occurred. Finite exposure, motion blur, occlusion, and uncertain timestamps require interval-valued inputs, not point estimates.

**Predeclared three-way product decision:** NO-HIDDEN-CLOSURE-POSSIBLE only when every nuisance-compatible assignment is endpoint-consistent and M>1 with a positive uncertainty margin; POSSIBLE/ABSTAIN when at least one compatible assignment admits closure; INVALID/ABSTAIN when the calibration, clock, visibility, or speed-bound assumptions fail. Never convert POSSIBLE into 'blink detected'.

## Acquisition and independence

Recruit consenting adults under approved local procedures. Target >=20 participants, >=30 natural blinks each, with participant-disjoint calibration (first session) and held-out evaluation (second session); these are design targets, not collected counts. Simultaneously acquire a high-frame-rate reference stream (target >=240 fps with verified actual exposure start/end timestamps), ordinary-camera stream at nominal 30 fps, and hardware-synchronized LED timing fiducial visible to both cameras. Log dropped frames and clock drift; nominal fps alone is not acceptable. Calibrate mm/pixel with an in-plane scale and fixed eye geometry, with repeatability uncertainty. Reference annotators blinded to model prediction mark the minimum aperture per gap and adjudicate ambiguous frames. Keep raw consent, recording permissions, and privacy retention explicit; store derived landmark series separately from identifiable video.

Estimate V **only** from an independent calibration subset with high-rate framewise aperture differences, corrected for timestamp and landmark uncertainty. A sample maximum is not a certified future velocity upper bound: either justify a physically conservative bound with instrument validation or report only empirical coverage at a stated confidence/participant scope. Predeclare a range of candidate V values and the calibration rule before held-out labels are inspected. Never select V to improve held-out agreement.

## Held-out test and failure criteria

For each ordinary-camera gap, calculate the interval of feasible M using independently estimated V and worst-case uncertainty in L,R,c,T. Record reference outcome CLOSED (aperture <=c at any intervening reference frame), OPEN (reference measurements confidently >c throughout), or UNKNOWN (missingness/exposure/annotation ambiguity). Reference sampling cannot prove absence of a closure shorter than its own blind interval; OPEN is reference-limited. Evaluate false NO-HIDDEN-CLOSURE-POSSIBLE predictions among CLOSED gaps as the primary safety error, with participant-clustered uncertainty intervals and the exact numerator/denominator. Any unambiguous CLOSED gap predicted impossible falsifies at least one asserted model/calibration assumption and blocks the camera feature pending diagnosis. Report abstention fraction and stratify by M intervals, glasses, gaze, illumination, motion blur, eye geometry, dropped frames, and camera timing jitter. Do not silently discard difficult gaps.

**Adversarial controls:** rerun predictions under conservative landmark perturbations, alternative closure thresholds, illumination shifts, off-axis gaze, glasses/reflections, artificial frame deletion, variable exposure, blur, rolling shutter, and injected timestamp skew. If uncertainty intervals cross M=1, force abstention. Separate participant-held-out and device-held-out results. Negative and inconclusive outcomes must be published.

## Instrument fallback if suitable public human data cannot be acquired

Use a mechanically actuated opaque shutter/eyelid surrogate with measured displacement (linear encoder), calibrated velocity envelope, LED synchronization, 240+ fps reference and 30 fps ordinary capture. Sweep dimensionless M across [0.5,1.5] with dense sampling around 1; randomize gap phase, exposure, blur, brightness, and dropped frames. Compare predictions to encoder-defined closure ground truth. This validates timing/geometry/implementation under instrument assumptions, **not human physiology**. If physical apparatus is unavailable, run the existing continuous witness and independent lattice solvers and explicitly mark the evidence synthetic only.

## Release consequence

Keep camera-derived blink/fatigue estimates disabled until independent velocity-bound validity, hardware timing, unseen-participant tests, nuisance controls, and uncertainty-aware abstention pass. A local self-report + reaction-time alpha may ship separately with no diagnostic or physiologically calibrated alertness claim. Publish scripts, preregistered splits, instrument calibration logs, failure examples, and a reproducibility manifest with the eventual report.
