# E002-407 — verified local-only human full-event rater pilot

**Date:** 2026-10-24. **Evidence:** checksum-verified real-human acquisition and annotation-instrument execution, not completed human ratings or physical aperture ground truth.

## Frozen protocol and independent execution

The selection, safety and feasibility predictions were frozen in `E002_407_FROZEN.md` before the pilot code and hosted evaluation. GitHub Actions [run 40049521713](https://github.com/sushxnthd/lucent/actions/runs/40049521713) completed successfully at head `8e026fa52a72fb96ed51fc08dbf6ae1403dc51f3`, with three successful jobs: independent synthetic integrity, S01 local-only human pilot, and S19 local-only human pilot. The actual logs independently record:

| Participant | Complete eligible event/control pairs available | Frozen pilot pairs | Blinded full-event clips | Eye frames extracted | Checksum |
|---|---:|---:|---:|---:|---|
| S01 | 16 | 2 | 4 | 316 | Source MD5 verified |
| S19 | 6 | 2 | 4 | 316 | Source MD5 verified |
| **Total** | **22** | **4** | **8** | **632** | Both verified |

All H1–H5 instrument checks passed computationally: each participant generated four complete blinded clips from two first-eligible pairs, local pack and blank-sheet validation succeeded, source checksum checks passed, and no eye images or private event/control linkage were uploaded. The CI logs print only aggregate counts. Image and linkage files were removed with ephemeral runner storage. This is not an external independent verification of participant identity, source clock calibration or human landmark truth.

The real-video outputs are **not recoverable from CI** because the no-upload privacy requirement intentionally prohibits artifacts. To obtain actual human annotations, an authorized researcher must regenerate the identical selection (but fresh blinded IDs) locally from the checksum-verified archives, distribute the same immutable pack to two independent raters, and preserve the completed blinded sheets and private mapping off GitHub.

## What this validates, and what it does not

This verifies an executable full-event **human-video annotation instrument** over 632 real eye frames. It does **not** establish 632 annotated frames, 8 measured blinks, rater agreement, calibrated aperture, velocity limits, physical shutter timing or any E002-371 no-hidden-closure certificate. EEG event/control arm remains blinded to raters, but EEG labels are not physical aperture truth. The selection is from previously explored S01/S19 participants and is not a held-out participant or device study.

The next falsifiable measurement step is two blinded independent landmark sheets with unresolved/nuisance flags, followed by preregistered disagreement, framewise interval propagation and full-event quality gates. Do not interpolate across unresolved frames without separately verified hard physical bounds. For a true physical certificate, independently measure eyelid geometry, camera shutter response, rolling-shutter offsets, optical inversion, clock uncertainty and physiological hard velocity bound. E002-405 established that a finite-sample velocity maximum cannot serve as a hard guarantee.

## Product restriction

Retain `ABSTAIN_UNCALIBRATED` for hidden closure exclusion, blink duration, PERCLOS and fatigue diagnosis. A green rater-pack workflow is **not** permission to enable those outputs. No release claim until independently rated human trajectories and unseen-device validation.
