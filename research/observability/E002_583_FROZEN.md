# E002-583 | Frozen binocular versus monocular closure-index alias test

**Frozen 2026-11-01 before binocular source analysis.** Scientific kernel E002-371. Source and checksum are locked to the independently replayed E002-582 Silesian5 annotation ZIP (SHA-256 `a73bf84981b84f626a3cc7b3b3d1962360354740bc6cf3de5d9c92d6d380c223`). Five published sequences, nominal 100 fps. The source's FC=C denotes an investigator's 90–100% eye-closed flag, not a calibrated eyelid aperture or hard velocity bound.

## New hypothesis and exact prediction
The previously published 567 per-eye FC runs need not correspond to 567 distinct blink events. Evaluate the stricter **simultaneous binocular** positive label `B_i = (LE_FC_i == C and RE_FC_i == C)`. For a maximal contiguous B-positive run of length L, predict exactly 7, 4, 1, or 0 omitted phases (of 10) for L=1,2,3,>=4 respectively, provided the run is at least 10 source frames from each sequence boundary. Do not choose phase after looking at the source. All 10 phases use E002-582's frozen index sampler `r(k)=first+phi+floor(10k/3)`.

Primary endpoint: **count of nuisance-eligible simultaneous binocular FC runs omitted in >=1 phase**. Secondary endpoints: count of binocular FC runs, per-phase omissions, run-length histogram, and event-level left/right union. A union event is a maximal consecutive run with `LE_FC=C OR RE_FC=C`; its omission is evaluated identically but must not be called a binocular blink. Compare the event definitions descriptively; never equate per-eye, binocular and union events or treat phases as independent participants.

## Eligibility and failure gates
For each candidate run require both immediate flanks, contiguous unique source frame indices and at least 10 frames from either sequence boundary for the exact phase-law check. Abstain if any frame or either flank has nonfrontal NF=N or either eye not visible NV=N. Unknown flags, missing or duplicate frame IDs, unsafe ZIP, changed SHA, unexpected sequence/row count fail closed. A candidate with no binocular FC-positive frames is not evidence that both eyes were anatomically open. Do not infer continuous-time closure from sampled flags.

## Falsifiers and controls
Before accessing authentic labels, test (1) overlapping left/right closures with a single shared B frame; (2) disjoint monocular closures with no B event; (3) a long binocular run retained by every phase; (4) nonfrontal or one-eye-not-visible abstention; (5) missing index and sequence-edge abstention; (6) deterministic sequence-order invariance; (7) a shared one-frame B run missed in seven phases. Preserve zero positives or any phase-law failure without retuning. Emit only aggregate anonymized counts, no raw annotation rows, identities or images.

## Evidence tier and product decision
Positive results are **human-investigator-label, nominal index-only alias witnesses**. Neither a 30-fps physical camera miss probability nor a physiological shutter-gap/eyelid-speed validation follows. Actual shutter exposure, row timing, clock errors, motion blur, glasses, gaze, brightness, rater independence, and calibrated velocity remain unverified. Keep Lucent `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. Hush remains untouched.
