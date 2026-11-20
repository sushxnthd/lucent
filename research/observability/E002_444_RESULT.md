# E002-444 — first real-human optical-content test of the sparse-event hypothesis (2026-10-25)

**Outcome:** Real S19 human AVI decoded successfully for the prospectively frozen first 12,000 frames. **12 independent synthetic/adversarial tests passed**, and the actual experiment passed in [GitHub Actions run 40203891842](https://github.com/sushxnthd/lucent/actions/runs/40203891842) on implementation commit `e19e735d`. Nonidentifying [machine-readable aggregate](E002_444_HUMAN_AGGREGATE.json) is committed, not only stored as an expiring workflow artifact. The [frozen protocol](E002_444_FROZEN.md) was committed at `7341188` before analyzing these optical frames. Source S19 ZIP passed its published MD5/size check. S21 and S22 remain sealed.

## Empirical optical result (human images, not synthetic pixels)

12,000 decoded 320×288 grayscale frames yielded **11,999 adjacent pairs** and **zero exactly identical pairs**. Full-frame mean absolute pixel change, normalized to [0,1], had median **0.00269935**, p90 **0.04411539**, p99 **0.09194752** and maximum **0.18319223**. Median fraction of pixels changing by >=16 gray levels was **0.00155165**; p90 was **0.242969**. These are actual image-content measurements; they do not establish independent sensor exposures, eyelid aperture or blink labels.

Assuming, solely as a testable hypothesis, that the 56,911 populated `RelTime` event rows correspond one-to-one in order to the 56,911 AVI frames, the preregistered candidate event-gap bins gave:

| Candidate event gap | Adjacent frame pairs | Median normalized full-frame change | Fixed 137-frame shift-control median |
| --- | ---: | ---: | ---: |
| <=10 ms | 11,972 | **0.00269857** | 0.00269923 |
| 10–100 ms | 21 | **0.05040075** | 0.00268289 |
| >100 ms | 6 | **0.00654827** | 0.01306236 |

For 10–100-ms candidate gaps, the observed median optical change was **18.68 times** the <=10-ms median. This association disappears under the single preregistered 137-frame shift control (shift median **0.002683**). The result is **positive exploratory evidence for some ordering correspondence between sparse table events and optical discontinuities**, not authentication of a physical clock. There are only 21 medium-gap and six long-gap observations, and the >100-ms group does **not** show a monotone increase (its shifted median is larger than the aligned median). All six >100-ms transitions exceeded the short-gap median, but this is weak with n=6 and no independent clock ground truth.

## Falsification and interpretation

- The frozen >5% exact-duplicate warning was **not triggered** (0/11,999). However, lossy MPEG-4 decoding can make physically repeated images differ, and moving gaze/lighting/compression can change pixels without eyelid motion. **Zero exact duplicates does not certify 12,000 independent camera exposures.**
- The frozen median-zero optical-information warning was **not triggered**. This only means the decoded images vary.
- Candidate event gaps of 10–100 ms co-occurred with larger pixel discontinuities. That makes the proposed row/frame pairing **worth testing against independent triggers**, but does not resolve whether `RelTime` marks exposure, export, frame processing, or something else.
- A fixed shift is one negative control, not a permutation significance test. Neither p-values nor timing uncertainty bounds are inferred post hoc.
- No gaze, glasses, blur, brightness, rolling shutter, anatomical geometry, physical aperture, or sensor clock nuisance has been independently calibrated. Full-frame intensity difference is an **optical activity proxy**, not a physical eyelid-velocity observable.

## Reproducibility and integrity

- [Frozen design](E002_444_FROZEN.md); [streaming analysis code](e002_444_human_optical_motion.py); [independent tests](test_e002_444_human_optical_motion.py); [technical figure](E002_444_OPTICAL_GAPS.svg); [hosted workflow](../../.github/workflows/e002_444_human_optical_motion.yml).
- One initial hosted run (40203823642) correctly caught a test failure because negative event gaps were rejected under the wrong error category. The implementation was repaired at `78480fd`, and the final workflow was rerun and passed all 12 tests plus real S19 analysis.
- Reproduce on a no-cost GitHub Actions runner; do not commit the 373-MB source archive or any participant imagery. SHA-verified archive, fixed 12,000-frame window, and aggregate-only outputs are enforced.
- Only S19 pilot was used. No holdout images were inspected, no thresholds retuned after seeing the result, and no physical-product gate changed.

## Scientific next step

**Freeze an anatomical eyelid-aperture annotation/segmentation rule and independent frame-event alignment check on S19, then test unseen S21/S22 without retuning.** A calibrated human velocity upper bound cannot be inferred from a pilot maximum. If original exposure triggers, anatomical scale and blinded closure labels remain unavailable, publish the result explicitly as an algorithmic image-observability study rather than physical E002-371 validation.

**E002-371 physical validation: NOT ESTABLISHED.** No no-hidden-closure, blink-duration, PERCLOS, fatigue, or medical certification is authorized. Product retains `ABSTAIN_UNCALIBRATED`; draft PR #26 remains unmerged.
