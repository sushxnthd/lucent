# E002-441 — frozen independent high-speed human-video validation protocol

**Frozen 2026-10-25 before any raw video extraction or inspection.** Parent E002-371; previous physical validation status: FAIL. This is a genuine new source, not a retrospective relabeling of synthetic data.

## Source and provenance
Guttmann-Flury, Sheng & Zhu, Scientific Data 12:587 (2025), DOI 10.1038/s41597-025-04861-9; original Synapse DOI 10.7303/syn64005218. Open CC0 Zenodo rehost DOI 10.5281/zenodo.18978288, published 2026-03-12. 31 subjects, 63 sessions, each with approximately 500-fps Phantom AVI, XML pupil annotations, synchronization CSV and eye tracker. Rehost claims non-EEG modalities byte-identical to originals. Validate the claimed native frame rate and timestamps from actual files; a dataset description is NOT authenticated hardware exposure timing.

## Sealed split and decision criteria
- Pilot/calibration subject: S19 (373.1 MB archive, publicly listed). Unseen confirmatory subjects, in this order: S21 and S22 (421.9 and 452.1 MB archives). Never use S21/S22 to choose image thresholds or annotation settings.
- Before accessing any holdout videos, freeze a deterministic pupil/eyelid aperture tracking rule, ROI policy, error/uncertainty bounds, closure threshold in pixel or normalized units, timing-source hierarchy, and no-closure classifier. Save code SHA and calibration values.
- Primary question: Do camera-space eyelid-aperture sequences from the native high-rate video falsify the *conditional* E002-371 shutter-gap no-hidden-closure boundary after temporal decimation to 30 and 60 Hz? Simulate shutter integration only if exposure time and response are independently established; otherwise evaluate point-sampled surrogate with separate evidence tier.
- Reference outcomes must be independently adjudicated (prefer blinded two-rater anatomical aperture labels); XML pupil tracking and EOG blink flags alone do not certify physical eyelid closure. When rater labels are absent, report algorithmic exploratory agreement only, not true positives or false certificates.
- Speed cap MUST NOT be fitted to held-out videos. Use pilot-only observed necessary-speed lower bounds as falsification of candidate caps; do not interpret pilot maxima as hard physiological upper bounds. No physical certificate until an independent justified cap, geometry, illumination, shutter, clock and reference annotation are available.
- Analyze spontaneous, voluntary, reflex separately if metadata supports identification; otherwise mark type unknown. Track gaze, glasses, brightness, blur, missingness, occlusion, sampling, rolling shutter and clock as nuisance failures. Participant is the independent statistical unit.

## Frozen measurable outputs
(1) provenance/hash and file inventory for each successfully obtained subject; (2) decoded frame count, dimensions, reported FPS, PTS consistency and missing-frame flags; (3) human-visible reference snapshots or blinded labels if authorized; (4) pilot-calibrated prediction code; (5) untouched holdout performance with per-subject coverage/abstention; (6) negative results. Never publish identifiable raw participant frames into the repository; only derived, nonidentifying aggregates and code. Avoid uploading huge datasets to GitHub.

## Fallback and honesty
If downloads fail due to transport/disk/size, commit a concrete acquisition handoff and an executable partial-download verifier rather than pretending the dataset was tested. If camera scale/timing/reference is unauthenticated, downgrade claims to high-frame-rate *video* evidence and retain `ABSTAIN_UNCALIBRATED` for physical closure, blink duration, PERCLOS and fatigue. This protocol does not certify medical or fatigue behavior.

## Links
- https://zenodo.org/records/18978288
- https://doi.org/10.1038/s41597-025-04861-9
