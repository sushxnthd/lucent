# E002-631 | Frozen motorized-occluder acquisition and blind-scoring packet (2026-11-03)

## Scope and evidence tier
**Prospective instrument protocol only.** No camera, motorized occluder, participant, or independent velocity measurement was operated in this run. This packet is designed to prevent the next acquisition from being mistaken for validation merely because it produces video. The E002-371 certificate remains conditional on a *continuous-time* bound, not a frame-difference estimate.

## Instrument construction
Use a translating opaque blade with a calibrated mechanical stop and independent position encoder. Mount it across an artificial eye aperture or printed fiducial target, with the blade path in the same focal plane as the aperture edge. Record (i) ordinary-camera frames and raw hardware exposure-start/end timestamps, (ii) encoder positions and encoder-clock timestamps, (iii) an independent high-speed reference camera, and (iv) a common flashing timing fiducial visible in both cameras. If only software timestamps or nominal frame rates are available, mark the acquisition **ineligible**.

Encoder resolution, scale error, latency, dropouts and maximum inter-sample acceleration must be independently bounded; encoder samples alone are not continuous-time ground truth. Independently calibrate the exposure integration interval, rolling-shutter row offsets, focus and geometric scale, and clock drift before the blind experiment. Do not infer a velocity ceiling from the same ordinary-camera gaps being scored.

## Frozen decision and phase challenge
For each pair of *disjoint exposure intervals*, compute the guaranteed shutter-free gap lower bound G_lo, accounting for exposure duration, row timing and clock uncertainty. Obtain lower confidence/guarantee bounds on both endpoint apertures, a0_lo and a1_lo, in the same physical units as closure threshold c. Let independent bounds V_close and V_open apply to the full candidate gap, including unsampled instants. Under a strictly positive motion margin, exclude a hidden threshold crossing only if

  (a0_lo - c)/V_close + (a1_lo - c)/V_open > G_hi

where G_hi is the **largest** gap allowed by timing uncertainty; equality MUST abstain. If either endpoint may already be closed, bounds are unavailable, geometry is invalid, or continuous-time motion bounds are uncertified, return ABSTAIN_UNCALIBRATED. For time-varying bounds use the previously derived reachability-integral criterion, not this constant-bound shortcut.

**Critical falsification:** A physically confirmed threshold crossing within the exposure-free interval on any case classified EXCLUDE is a false exclusion and blocks the certificate. For negative cases, absence of a detected crossing is not proof of absence unless the reference/encoder observability uncertainty itself excludes crossing.

## Pre-registration before physical data
1. Freeze apparatus calibration files and hashes, encoder uncertainty model, timing error budget, closure threshold and phase list before collecting scored sequences.
2. Use at least three gap regimes: clearly below, near (including equality), and clearly above the theoretical reachability boundary. Randomize 20 sub-frame phases per regime, with repeated trials and both travel directions.
3. Include deliberately adversarial conditions: low/high illumination, defocus/motion blur, partial occlusion, gaze-analogue target displacement, glasses/reflections, dropped frames, rolling shutter, timestamp jitter and clock drift. Predeclare which conditions invalidate calibration and force abstention.
4. Freeze predictions from the ordinary camera **before** viewing the reference/encoder crossing labels. Keep acquisition/calibration and scored challenge runs disjoint.
5. Export a machine-readable trial table: trial_id, calibration_hash, phase, gap_lo/hi, exposure_lo/hi, aperture0_lo, aperture1_lo, threshold, V_close, V_open, prediction, reference_crossing_state (YES/NO/UNKNOWN), nuisance_flags, and exclusion_reason. Never silently omit UNKNOWN.
6. Independent analyst must reproduce the certificates and reference labels from raw files; archive exact versions, hashes, acquisition rates, clock-calibration traces, exclusions and all failures.

## Statistical reporting
Report the raw numerator and denominator of **false exclusions among reference-confirmed crossings**, separately from the number of EXCLUDE decisions. For n independent qualifying exclusion decisions with zero false exclusions, a one-sided exact 95% upper bound on the conditional false-exclusion probability is 1 - 0.05^(1/n); this is not a population guarantee under correlated trials or untested conditions. At n=299 this bound is approximately 0.997%. Report participant/device/condition clustering and stratified confidence intervals rather than treating frames from one session as independent. A zero-error synthetic sweep does not count toward n.

## Human extension (requires ethics and consent)
Recruit adult volunteers with consent and privacy controls, and obtain independent synchronized high-speed recordings plus qualified blinded anatomical closure adjudication. Partition by participant before calibrating any nuisance or motion parameters. Validate the motion envelope against human sequences **without reusing the held-out participants to set its ceiling**. Predeclare exclusion coverage, false-exclusion rate and abstention rate by skin/illumination conditions, eyewear, gaze, image quality, and device. Human safety or fatigue claims are prohibited unless separately validated.

## Release blocker
Physical instrument runs: **0**. Independently certified continuous-time human velocity envelopes: **0**. Participant-disjoint human shutter-gap predictions: **0**. Product verdict: **ABSTAIN_UNCALIBRATED**. Release: **BLOCKED**.

## Explicit scope limitation
The conditional constant-bound criterion is a conservative reachability rule only when the specified upper speed envelopes hold at all times. A sample-based peak speed, even at high frame rate, does not meet this assumption.