# E002-733 | Frozen synchronized human/instrument validation decision sheet

Date frozen: 2026-11-10 UTC. Status: **prospective, no subjects acquired**. This is an acquisition-ready falsification protocol, not validation.

## Target and independent measurements
The target is the E002-371 point-aperture exclusion law, not a claim that RGB frame brightness equals eyelid aperture. Obtain a high-frame-rate (target >=240 fps, recorded per-frame hardware timestamps) face/eye stream simultaneously with the ordinary phone camera, with a visible common LED timing pulse in both views and an independently recorded photodiode trace of LED pulses. Save unmodified source files, exposure intervals, frame drops, camera settings, and synchronization residuals. If hardware timestamps or an independently bounded timing error cannot be established, **ABSTAIN** on time-sensitive exclusion. A single camera's advertised FPS is not a timestamp certificate.

## Freeze before collecting the evaluation set
Use participant-disjoint calibration and test sets, target >=10 calibration and >=10 held-out participants, >=20 voluntary blinks per participant, and at least 3 ordinary-camera settings (nominal 30 fps, 60 fps, and longer-exposure low-light). These are target sample sizes, not completed counts. Register exclusion thresholds, segmentation acceptance, annotation rubric and statistical intervals before opening held-out labels. Do not estimate velocity limits from held-out trajectories.

For each calibrated subject and gaze condition, independently derive a *conservative* upper bound L on absolute aperture change per second from high-rate trajectories with pixel/landmark uncertainty, temporal interpolation uncertainty, and a stated extrapolation assumption. **A finite sample maximum is not a certified physiological upper bound**: absent a defensible margin and population scope, report only conditional empirical coverage, not a deterministic exclusion guarantee. Prefer subject-specific conditional bounds; never silently generalize to unseen people.

## Frozen prediction
For two genuinely instantaneous aperture observations with conservative lower aperture bounds a0-, a1-, maximum true elapsed time T+ (including synchronization, clock and frame-drop uncertainty), define R=(a0-+a1-)/(L*T+). For L>0, predict **hidden full closure excluded only if R>1**. At R<=1, say **possible/undetermined**, not that a closure occurred. For L=0 handle separately: any positive lower aperture excludes closure only if constancy is independently justified. Any exposure-averaged or unverified RGB proxy yields **ABSTAIN**, regardless of R. Never use midpoint timestamps to stand in for instantaneous samples without a certified exposure-aware bound.

For held-out high-rate ground truth, decimate/synthesize ordinary-frame timing and measure actual hidden complete closures (minimum anatomical aperture <= preregistered closure tolerance) between observed windows. Report exclusion violations / eligible exclusions with exact binomial confidence bounds, coverage (eligible exclusions / all evaluated windows), and per-participant stratification. A single confirmed violation under all certified premises falsifies the proposed bound or its calibration. If no eligible windows exist, record a negative/indeterminate result; do not claim accuracy.

## Adversarial controls and release consequence
Run preregistered paired perturbations: illumination, blur, gaze, glasses/occlusion, camera geometry, compression, 1- and 2-frame missingness, exposure variation, and timestamp shifts at the error budget. Track false exclusions separately from abstentions and preserve raw failures. If the ordinary-camera measurement is not traceably linked to anatomical aperture, the product must not claim closure exclusion, blink counts, sleep state, or physiological fatigue from this law. Production remains `ABSTAIN_UNCALIBRATED` / `BLOCKED` pending human validation and external review.

## Practical acquisition ethics
Consent explicitly for eye/face video and storage, permit withdrawal, avoid unnecessary identifiers, encrypt raw footage, restrict access, and publish only deidentified aggregate traces or consented examples. Do not instruct participants to induce fatigue or sleep deprivation. Record IRB/ethics determination as applicable before recruitment.

## Evidence boundary
Prior E002-731/732 exact arithmetic is synthetic. This sheet makes a prospective human test executable but contributes **zero** new human measurements and **zero** independently certified velocity ceilings. No publication or release claim follows.
