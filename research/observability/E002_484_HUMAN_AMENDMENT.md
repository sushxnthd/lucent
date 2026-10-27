# E002-484 physical/human-validation amendment: closure-vs-nonclosure controls

**Applies to:** [E002-483 human study](E002_483_HUMAN_STUDY.md). This is a proposed prospective protocol, **not** an executed human study. No new human recordings, shutter measurements or ethical approvals are represented.

## Primary outcome and pre-registration
The primary binary target is whether anatomical aperture reaches a prespecified independently calibrated closure threshold at any time inside a low-frame-rate exposure interval. Define the threshold in millimeters and its uncertainty *before* evaluation. Do not silently substitute eye-aspect ratio, eyelid pixel distance, or an exposure-averaged proxy for ground truth.

Primary falsification: the ordinary-camera algorithm must either distinguish true closure from matched-gate **nonclosure** or abstain. Any released closure label for an independently authenticated nonclosing sequence is a false positive. An apparently correct label when the optical/kinematic assumptions fail is not a valid certificate.

## Instrument-first acquisition
1. Measure shutter temporal response and row timing using an independent pulsed source, photodiode/logic analyzer, authenticated pulse-to-frame mapping, held-out phases and optical dark/bright controls. Report actual exposure response, jitter, clipping, missingness and phase coverage, not nominal fps alone.
2. Validate with a motorized or independently tracked moving aperture with **both** full-closure and strictly nonclosing trajectories. Match the two 10-ms gate averages as closely as feasible. Include E002-484's scaled triangular pair (minimum 0 vs 0.35 mm), plus smooth nonclosing controls. The ground-truth instrument must not share the tested camera's exposure clock as its sole timing source.
3. Randomize illumination level, flicker phase, geometry, camera distance, defocus/blur, aperture orientation, missing frames, motion speed and timing phase. Record all nuisance budgets from independent calibration rather than post hoc fitting.
4. Before any human data, freeze a decision rule: physical event claims are allowed only if measured data exclude **all** nonclosing reference trajectories under the calibrated nuisance and speed class. Otherwise emit `ABSTAIN_UNCALIBRATED`.

## Human feasibility pilot
After institutional/guardian consent and ethics requirements are resolved, a proposed 24-adult feasibility pilot may collect synchronized >=400-fps anatomical reference and simultaneous ordinary-camera video. Use a common independently visible synchronization marker and audit timestamp uncertainty. Blind adjudicators to algorithm predictions; annotate closure thresholds and confidence intervals with two raters and adjudication of disagreements.

Keep participants, recording sessions and lighting/eyewear conditions disjoint between calibration and evaluation. Include spontaneous and prompted blinks, gaze shifts, partial blinks, glasses, shadows and dropped-frame controls. Do not claim the 24-person pilot establishes a population-level hard speed bound. Report abstention, false closure certification, missed closure, calibration error and participant-cluster uncertainty separately. Preserve negative results and raw data access/consent restrictions.

## Release blockers
- No independently authenticated shutter and aperture ground truth: **BLOCK** physical closure claim.
- No demonstrated discrimination from matched-gate nonclosing controls: **BLOCK** physical closure claim.
- No independently calibrated gain/brightness/blur/timing nuisance bounds: **BLOCK** physical closure claim.
- No participant-disjoint blinded human replication: **BLOCK** general human claim.
- No validated physiological link: **BLOCK** fatigue/medical interpretation even if blink timing becomes measurable.

This amendment does not establish physical validity. It changes what must be tested before a future release.
