# E002-582 | Authentic 100-fps human full-closure labels exhibit exact nominal 30-fps index omission

**Executed:** 2026-11-01. **Kernel:** E002-371. **Frozen before source access:** [E002_582_FROZEN.md](E002_582_FROZEN.md) at `089a28b`; [exact phase prediction](E002_582_PHASE_PREDICTION.md) at `fba2efc`, before source access. **Hosted source experiment:** [GitHub Actions #41279060143](https://github.com/sushxnthd/lucent/actions/runs/41279060143), job `124767045875`, **completed success** at 2026-11-01 06:01 UTC. **Executable:** [e002_582_silesian5_fc.py](e002_582_silesian5_fc.py). **Machine-readable aggregate:** [E002_582_AGGREGATE.json](E002_582_AGGREGATE.json).

## Why this is a genuine new human-data observation

The previous LPW source offered 95-fps eye imagery but only *pupil-center* labels, not anatomical eyelid closure. This independent external source, **Silesian5 (Basler5)**, provides per-frame, human-created **left/right full-closure flags**: `FC=C` means an eye was annotated as 90%-100% closed. The [investigators' documentation](https://www.blinkingmatters.com/research) reports five people, nominal 100-fps acquisition, 58,884 annotated frames and 300 blink events. The publicly linked annotation ZIP was retrieved without video, and its SHA-256 was independently recorded as `a73bf84981b84f626a3cc7b3b3d1962360354740bc6cf3de5d9c92d6d380c223`.

The archive has five `.tag` annotation members containing **exactly 58,884** published-schema 19-field frame rows, with separate timestamp `.txt` and metadata `.csv` members. Source ZIP integrity, row schema, unique strictly increasing frame indices within each sequence, positive-label semantics, and all ten prespecified temporal phases were checked by the hosted executable. No participant names, source frames, face boxes, raw annotation rows or human images were committed.

## Pre-source prediction and observed result

A nominal 100-to-30 frame-index sampler retains `r(k)=phi+floor(10k/3)`, with every integer phase `phi=0,...,9` tested. Before retrieving this source, exact integer arithmetic predicted that a positive run of 1, 2, 3, or at least 4 consecutive 100-fps frames would be omitted by exactly **7, 4, 1, or 0 of the ten phases**, respectively, away from sequence boundaries.

| Consecutive investigator-FC frames in a run | Authentic eligible runs | Predicted omitted phases per run | Observed event-phase omissions |
| ---: | ---: | ---: | ---: |
| 1 | **7** | 7 | **49** |
| 2 | **28** | 4 | **112** |
| 3 | **41** | 1 | **41** |
| >=4 | **491** | 0 | **0** |
| **Total** | **567** | | **202** |

All **567** source-positive runs were interior, contiguous and eligible under the source's available nonfrontal/not-visible flags. **All 567 passed the exact phase-law check.** This is not a claim that all videos were free of unannotated nuisance conditions.

**Primary frozen positive endpoint met:** **76 of 567** per-eye human-FC-positive runs (13.40%) were completely omitted by **at least one** nominal ordinary-rate phase. The 76 are exactly the 7+28+41 runs of length 1–3. Across the ten phases, the numbers of omitted runs were **[29, 18, 21, 17, 20, 18, 25, 20, 14, 20]**: 14–29 omissions per phase, or 2.47%–5.11% of the 567 runs. There were **202 omitted event-phase pairs among 5,670** run-phase combinations (3.56%, descriptive only). Zero runs were omitted in *every* phase, as predicted structurally by the phase union. The anonymized five-sequence counts of runs omitted in at least one phase were **2, 24, 7, 33, 10**, totaling 76.

These are *positive human-source label omission witnesses*, not an estimated 30-fps physical camera miss probability. The 567 per-eye runs and ten phases are not 5,670 independent people or observations. The source's 300 blink-event description need not equal the 567 left/right FC runs because its blink intervals and eye-specific full-closure segments have different definitions.

## Provenance, independent checks and preserved failure

The initial one-shot [source-format probe #41278525392](https://github.com/sushxnthd/lucent/actions/runs/41278525392) **passed** and established the archive SHA, five `.tag` files and separate auxiliary files. The first full-analysis [run #41278732638](https://github.com/sushxnthd/lucent/actions/runs/41278732638) **failed** because the parser wrongly interpreted two-field auxiliary timestamp rows as 19-field annotations. A privacy-safe [schema diagnostic run #41278951078](https://github.com/sushxnthd/lucent/actions/runs/41278951078) confirmed five `.tag` files with 11,498, 16,011, 10,088, 13,178 and 8,109 authentic 19-field numeric rows, summing to 58,884. The corrected parser reads only the five `.tag` files, preserves the frozen outcome and thresholds, and binds the observed ZIP SHA. Both failures remain visible.

The successful hosted run passed the synthetic controls for 1/2/3/4+ phase counts, nonfrontal abstention, missing frame indices, malformed flags, source parser behavior, and source-member-order invariant replay. The identity **7×7 + 28×4 + 41×1 + 491×0 = 202** independently checks the aggregate arithmetic. The per-phase vector also sums to 202. These arithmetic checks are independent of the code's report formatting but **not** independent replication of the original human labels.

## What this does and does not validate

**Supported:** In an independent published human annotation source with reported 100-fps acquisition, some *positive per-frame 90%-100% eyelid-closure labels* are completely absent under a prospectively fixed nominal 30-fps **index-only** sampling schedule. This is a real human-label demonstration of temporal aliasing and a held-out-from-LPW test of the exact 7/4/1/0 phase law.

**Not supported:** That a physical 30-fps exposure-integrating camera misses those closures; that 100-fps frames have independently certified timing or reference sensitivity; that the source's FC flags equal E002-576's normalized-aperture <=0.20 threshold; that any observed finite difference certifies a hard continuous-time eyelid-speed ceiling; that missing FC labels prove an open eye; or that the E002-371 shutter-gap/velocity bound has been physiologically validated. The investigator annotations are not two independently sealed blinded rater exports. No independent photodiode clock, physical shutter exposure, rolling-row calibration, or prospective held-out camera prediction was obtained.

**Nuisance limit:** This source permits source-flag checks for nonfrontal face and eye not visible; it does **not** provide independently verified brightness, blur, eyewear, gaze geometry, row-exposure, dropped-frame, or clock-error budgets. Therefore do not extrapolate the 13.40% across devices, settings or populations, and do not treat a source flag of X as proof that every nuisance is absent. The five sequences are the only human subjects in this source; no population-rate confidence claim is justified.

## Next decisive physical test and product gate

The next required test remains [E002-567](E002_567_PHYSICAL_HUMAN_STUDY.md): simultaneously record human eyelids with a high-speed reference and an ordinary camera, externally calibrate the actual exposure windows/row timing and clock, independently annotate positive reference closures, independently justify velocity and geometry uncertainty, freeze low-rate exclusion predictions *before* held-out labels, and count one-sided contradictions with nuisance-specific abstention. Two genuinely independent LPW raters remain a separate human-reference task.

**Evidence ledger:** independent human anatomical rater pairs **0**; authenticated physical shutter/photodiode captures **0**; certified continuous-time eyelid-velocity ceilings **0**; held-out physical-camera closure predictions **0**. The new external Silesian5 evidence is **real human-source investigator full-closure labels**, not these missing certificates.

**Product:** `ABSTAIN_UNCALIBRATED`. **Release:** `BLOCKED`. No blink duration, PERCLOS, fatigue, sleepiness, certified absence-of-closure or shutter-exclusion claim. **Hush:** no branch or PR changes in this primary experiment.
