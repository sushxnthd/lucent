# E002-407 — frozen local-only full-event human rater pilot

Date: 2026-10-24. This protocol is frozen before implementing or executing the pilot packet generator. This is a **human-validation instrument**, not independent human annotation or a physiological experiment.

## Input and frozen selection
Use the same checksum-verified Eye-BCI S01/S19 source archives, EEG synchronization and deterministic 20 event/control pair selection as E002-406. The E002-406 observed 36/40 and 26/40 individually eligible ±250-ms windows, respectively; this implies at least 16 and 6 complete event/control pairs by pigeonhole, so a two-pair pilot is feasible without searching new datasets. Select the **first two complete pairs in the existing deterministic E002-398 pair order**, not by EEG strength, image appearance, optical quality, or observed closure. Reject incomplete pairs; do not impute gaps. Preserve event/control linkage privately and never release it to raters.

## Pilot deliverables and frozen checks
- H1: Each participant produces exactly **four blinded clips**, comprising two complete selected pairs, with **at least 0.500 seconds** of source-synchronized frame coverage per clip, <=20-ms internal gaps and contiguous frame IDs. Do not confuse this clock with independently calibrated camera exposure.
- H2: The manifest contains **no event/control arm, source timestamps, EEG markers, source frame IDs, participant ID or private linkage**. Use fresh cryptographic blinded IDs, checksum each cropped PNG, write private mapping separately, never copy it into rater pack.
- H3: Two offline rater sheets can be validated independently; missing images, digest mismatch, missing/duplicate frame numbers, unsafe filenames and nonfinite/out-of-bounds landmarks are rejected. Unresolvable frames are explicit.
- H4: If any required input, checksum, frame count, clip coverage, or privacy check fails, fail closed without emitting a purported complete rater pack.
- H5: Rater pilot outputs are local-only. Do not upload identifiable eye images or event/control linkage to GitHub, Actions artifacts, public releases, or external services.

## Scientific decision
This pilot tests *annotation feasibility and instrument integrity* for ~75–80 frames per 0.5-second clip. Two blinded human raters must still actually complete and freeze sheets; inter-rater agreement and independent optical/shutter/geometry/velocity calibration remain missing. Later untouched-participant/device validation is required. No blink duration, PERCLOS, fatigue diagnosis or no-hidden-closure guarantee can be claimed. Product remains `ABSTAIN_UNCALIBRATED`.

## Reproducibility
Commit source code, synthetic fixture tests, private/public separation checks and exact local CLI instructions. Run source archives locally with no cloud image export. Preserve negative results. Do not modify the earlier E002-404 seven-frame protocol or its independent tests.
