# Lucent E002-341 — preregistered paired-reference experiment (2026-10-21)

STATUS: FROZEN BEFORE OUTCOME ACCESS. This is an instrument-surrogate experiment, not native webcam acquisition.

## Active question / exact pair
Can 30-Hz ordinary-RGB-like observations, synthesized **only by decimating** independently synchronized 150-Hz visible-light Phantom single-eye video, recover eyelid-event occupancy and coarse blink timing against the untouched 150-Hz eyelid video and 1000-Hz EOG / 300-Hz Tobii reference? Pupil size is secondary; fatigue state is NOT evaluated.

## Literature frontier
Guttmann-Flury et al., Scientific Data 12:587 (2025), DOI 10.1038/s41597-025-04861-9 (Phantom, EOG, Tobii synchronized); Navascues-Cornago et al., Ocular Surface 40:22–30 (2026), DOI 10.1016/j.jtos.2026.01.003 (500-Hz reference, lower-frame-rate blink velocity loss). Prior work establishes sampling effects; novelty requires a prospective, nuisance-aware **certification boundary** with external holdout.

## Measurement model
For normalized eyelid aperture a(t) in [0,1], row-registered video signal z_k = b_k + g_k*(1/E_k)∫_{W_k} a(t)dt + q_k + e_k; b=photometric offset, g=contrast, q=gaze/geometry/eyeglasses residual, e=bounded localization noise. Video frame subsampling alone does NOT reproduce the exposure integration, optics, compression, or device noise of an actual 30-Hz webcam; only event-phase sampling claims are eligible. Ref r(t) = independently measured 150-Hz lid aperture, EOG peak times, and Tobii validity. Clock maps must be calibrated from acquisition metadata, never fitted using outcome labels.

## Observability metric / confounds
Primary: worst-phase retention of independently referenced full-closure evidence under 150→30 Hz (all 5 phases), with binomial participant-clustered uncertainty and abstention rate. Secondary: onset/offset error and blink-event recall against EOG, reference timing bounds. Confounds: pupil/iris occlusion, head pose, illumination, glasses, registration, synchronization, dropped frames. Controls: geometry-only, brightness-only, missingness-only, temporal smoothness-only.

## Decisive falsification
A single predeclared 'certified' event with no 150-Hz closure evidence (false certificate), or a certified event whose reference falls outside the claimed interval, invalidates that certificate model. Empirical coverage below 95% on held-out participants invalidates proposed coverage claims. Report all failures.

## Mechanism-derived boundary prediction
For discrete sampling every m=5 reference frames, an event with L consecutive closure-positive 150-Hz frames has exactly min(L,5) sampling phases containing at least one closure-positive frame. A closure lasting L<5 frames will disappear in 5-L phases, irrespective of classifier. This applies ONLY to labels at sampled instants; not exposure-integrated RGB or physiology. The number of positive phases is predicted BEFORE holdout. With bounded errors, certify event presence only if modeled contrast > 2*error bound.

## Split and outcome freeze
Development subject S01, held-out S22 (distinct participant); data source Zenodo record 18971758, files S01.zip MD5 bce89dd9fbb67e27a656623aa27927e0 and S22.zip MD5 31270474cfa5f3245d340ea0a198a953. Do not inspect S22 outcomes until the S01 pipeline, error bounds, and threshold are committed. Missing/unavailable data = BLOCKED, never impute.

## Publication threshold
Independent synchronization, 150-Hz reference confirmed, >=2 unseen participants and a second device/lighting stratum for generalization; >=95% interval coverage with confidence intervals, calibration/abstention and all four controls; exact checker; clear distinction between native 30-Hz and downsampled surrogate. This one-subject pilot alone cannot qualify.

## Product consequence
Allow native-frame blink presence as calibrated research only. Reject precise blink peak velocity, sub-exposure timing, 10-Hz blink completeness, five-second fatigue diagnosis. Add interval + abstention output only after held-out coverage succeeds.

## Data access cap
At most two substantive blocked attempts on Zenodo/Synapse path. If inaccessible, stop access work and reformulate; do not represent this protocol as human validation.
