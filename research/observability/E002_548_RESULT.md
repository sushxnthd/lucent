# E002-548 RESULT | A prospective, exposure-aware human falsification route

**Evidence tier:** primary-literature human-data source + executable one-sided witness audit + exact constructed adversarial tests. **No human recordings downloaded, inspected or analyzed; no camera shutter physically measured.** Date 2026-10-30.

## Source-backed correction to the reference-camera plan

A primary-literature dataset provides a more directly usable participant-disjoint validation route than Silesian5/OpenEDS alone: Guttmann-Flury, Sheng & Zhu, *Scientific Data* 12:587 (2025), DOI https://doi.org/10.1038/s41597-025-04861-9; Synapse https://doi.org/10.7303/syn64005218, Phantom folder `syn64102305`. The paper reports **31 participants, 63 sessions, 150-fps 320x240 monocular Phantom video**, synchronized with approximately **300-Hz Tobii eye tracking** and EEG/EOG. A secondary summary saying 150–300 fps video is misleading for this experiment: the primary paper explicitly says the video was **set to 150 fps**. Raw video and XML have not been acquired or verified.

**Scientific consequence:** 150-fps video is not continuous-time anatomical ground truth, and 300-Hz eye-tracker pupil absence is not a calibrated eyelid-aperture measurement. Even if video is obtained, its exposure kernel, clock/trigger timing and anatomical transfer must be independently characterized before a positive frame can contradict an E002-371 exclusion. Reference negatives remain censored.

## Executable one-sided evidence consequence

The [frozen protocol](E002_548_FROZEN.md) defines an exposure-integrated positive witness. If a certified upper bound on the **mean anatomical aperture** over a camera exposure is at or below threshold `c`, at least one instant during that exposure reached `c` or below. If the *entire possible exposure support* lies strictly inside a predeclared ordinary-camera blind interval marked `EXCLUDE`, this is a candidate contradiction. It establishes existence, **not duration or negative-reference sensitivity**. The integral mean inequality is elementary, not a new general theorem.

The [Python executable](e002_548_witness.py) consumes private JSON and checks gap/frame uniqueness, decimal timing intervals, full exposure containment, matching participant/session/eye/ROI, two-rater agreement, asserted independent timing/transfer certificate identifiers, hashes and a precommitted prediction digest. It exports only aggregate counts and never promotes a syntactic candidate to verified physical evidence. The [adversarial tests](test_e002_548.py) cover timing spill, boundary touch, wrong participant/session/ROI/eye, rater disagreement, missing transfer, above-threshold frames, absent references, duplicates, malformed hashes, nonfinite inputs, participant clustering and output privacy. **24/24 local Python tests passed** on 2026-10-30. [Independent Node.js BigInt arithmetic](e002_548_independent.cjs) passed for the **constructed** 150-fps/4-ms phase probability 1/5 and 5-ms complete erasure. The [synthetic fixture](e002_548_synthetic_fixture.json) yields `SYNTHETIC_WITNESS_ONLY=1`, `certified_exclusions=0`.

**Critical limitation:** The parser checks certificate identifiers and claimed rater decisions, **not** independent authentication of their contents or the identity of human reviewers. The fixture is synthetic. Neither constitutes human validation.

## Decisive next acquisition and stop rules

1. Retrieve an authorized participant's Phantom native frames, per-frame XML and matched `PhanFrame`, `PhanTime`, `RelTime` records from Synapse. Validate native frame timing, missing/duplicate frames, shutter duration and trigger alignment. If access fails, record the precise access barrier and use the previously frozen photodiode/mechanical-aperture physical protocol.
2. On exploratory participants only, establish independent optical timing and anatomical-transfer uncertainty. If an exposure-mean upper bound cannot be certified, **stop** and mark source frames `REFERENCE_CENSORED`. Literature mean velocities and sampled maximum velocities cannot certify hard continuous-time bounds.
3. Freeze all E002-371 `EXCLUDE`/`ABSTAIN` predictions, calibration provenance, participant/eye/ROI and timing envelopes before viewing held-out frames. Obtain two independent blinded raters and external audit of candidate witnesses.
4. Report participant-level confirmed false-exclusion witnesses, censorship and abstention with nuisance strata and all failed acquisitions. One externally confirmed witness falsifies the affected claimed exclusion. Zero witnessed contradictions does **not** certify absence of false exclusions.

**Outstanding:** 0 acquired human video sequences; 0 independently calibrated physical shutter captures; 0 blinded human rater pairs; 0 certified continuous-time human motion ceilings; 0 participant-disjoint observed predictions. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. Hush unchanged.
