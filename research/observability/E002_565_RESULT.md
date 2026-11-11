# E002-565 RESULT | Cross-paradigm S01 identity collision and multi-participant replay provenance boundary

Date: 2026-10-31. Primary E002-371 kernel. [Frozen before code](E002_565_FROZEN.md) at commit `e639643`. Evidence tier: **independent public human-source catalogue records + deterministic source-identity falsification + executable fail-closed replay guard**. This is not new human anatomy, measured physiological speed, calibrated shutter, or a novel information-flow theorem.

## Direct source-level correction

The [Zenodo Motor Imagery record 18970793](https://zenodo.org/records/18970793) and [Motor Execution record 18971758](https://zenodo.org/records/18971758) are **different paradigms**, although both contain `S01.zip` and a Phantom eye video for subject S01. The former uses `MI011_phantom.avi` and MD5 `fb56109542a13aa7879778833fe4cbaa`; the latter uses `ME011_phantom.avi` and MD5 `bce89dd9fbb67e27a656623aa27927e0`. Both pages were inspected 2026-10-31. The E002-510 reported 51,252 frames from MI; E002-563 reported 48,756 frames from ME. **These counts must not be compared as though they are two versions of one acquisition.** Their difference is not evidence of dropped frames, export trimming or re-encoding. The earlier findings that AVI presentation metadata report 1 fps and do not authenticate a physical sensor clock remain valid *within each respective source*.

This is a substantive **provenance correction**, not a claim that the two files were previously demonstrated to have identical content. It prevents an attractive but invalid shortcut from turning distinct human task recordings into a false reference comparison.

## New executable negative result

The E002-562 sealed synthetic replay uses one `source_sha256` for an **eight-participant** bundle. That is acceptable for the explicitly synthetic fixture, but a single real original-video SHA256 cannot authenticate eight different participant recordings. Without per-participant video/session provenance, the synthetic aggregate cannot be promoted into a human reference join.

The new [source-identity guard](e002_565_provenance_guard.py) requires exact binding of record, paradigm, published archive MD5, native video member, session, participant, original-video SHA256 and native frame namespace. The [guarded replay adapter](e002_565_guarded_replay.py) also rejects any sealed replay row or positive witness belonging to a participant other than the single bound native video, *before* invoking the existing E002-562 candidate adjudicator.

The precommitted negative cases reject MI/ME cross-paradigm S01 joins, changed video digest, different session/frame namespace, missing or contradictory metadata, and self-asserted physical certificates. The actual eight-person E002-562 synthetic fixture is now a **negative physical-binding control**: it must return `REJECT_SAMPLE_NAMESPACE`, zero physically admissible candidates and no invocation of the human replay adjudicator under a single S01 source. Matching single-video identity can only produce `SOURCE_MATCH_ONLY_UNCALIBRATED`, never a physical validation claim.

## Reproducibility and limits

- [Nine original Python adversarial tests](test_e002_565_provenance_guard.py) passed locally before persistence; a separate local prototype passed three guarded-replay cases. [Independent Node.js implementation](e002_565_independent_replay.cjs) reproduced **8/8 fixed cases with zero disagreements** locally.
- [Hosted workflow](../../.github/workflows/e002_565_provenance_guard.yml) runs the source guard, guarded replay tests, actual sealed E002-562 integration and independent Node replay. [CI run 41182258731](https://github.com/sushxnthd/lucent/actions/runs/41182258731) was **queued at report creation**; hosted success is not claimed.
- No original human media, individual frame hashes, private source indices or anatomical annotations were published. The guard cannot authenticate self-declared SHA256 values, human identity, sensor clock, independent raters or shutter response.

## Enforcement and next decisive experiment

For a physical multi-participant validation, replace E002-562's global synthetic source digest with **per-participant and per-session immutable native-video identities** and an independently verified frame-index/time map. Seal ordinary-camera predictions before opening blinded positive references, and require two independent anatomical raters plus external optical clock/shutter calibration and a defensible continuous-time speed envelope. Until then, no E002-562 synthetic candidate contradiction may be counted as human physical evidence.

**Evidence counters:** authenticated physical shutter captures 0; independent blinded human anatomical rater pairs 0; certified continuous-time physiological velocity upper bounds 0; held-out physical closure predictions 0. Product `ABSTAIN_UNCALIBRATED`, production `BLOCKED`. No more MI/ME metadata archaeology; obtain physical and anatomical evidence next.
