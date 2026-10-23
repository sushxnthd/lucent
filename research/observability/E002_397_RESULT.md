# E002-397 — human motion surrogate passes clean association, FAILS optical-nuisance portability (2026-10-23)

**Evidence tier: two previously used human participants, EEG-marker association only. E002-371 physical shutter-gap validation remains UNMET.**

## Pre-data commitment and independently reproduced execution

- Frozen protocol committed as `72eb70754a48f040204baa8ba308444407666904` **before** running the new motion feature on S01 or S19. Frozen direction, Farneback parameters, ROI, skin/background-motion subtraction, 80th percentile, seven-frame maximum, participant set, controls and five falsifiable predictions were unchanged.
- Code and independent checker committed at `15b2eb9` and `ddee42c`. CI workflow committed at `247fe96`.
- [GitHub Actions run 39975509583](https://github.com/sushxnthd/lucent/actions/runs/39975509583): **completed successfully**, both independently checked matrix jobs. CI PASS means computation and source-integrity checks passed, **not** that all scientific predictions passed.
- Sources: CC0 Eye-BCI SSVEP S01, [Zenodo 18978288](https://zenodo.org/records/18978288), MD5 `fef02cb7ebf62e4f3efb6303284fd6cb`; S19, [Zenodo 21905748](https://zenodo.org/records/21905748), MD5 `8a16cf12526f7558b4e49926c4bc5e8e`. Provenance wording clarified in `E002_397_SOURCE_CLARIFICATION.md`, with no hypothesis changes.
- S01: **86** fixed EEG-marker/non-event-control pairs. S19: **36**. Both participants were already inspected in E002-395/396 with a different feature; **this is not a prospective untouched-participant test**. Independent oracle recomputed all rank AUCs and all frozen Boolean decisions from anonymous scores.

## Results: event/control AUC (higher motion at EEG markers)

| Fixed image condition | S01 (86 pairs) | S19 (36 pairs) |
| --- | ---: | ---: |
| Clean | **0.983775** | **0.753858** |
| Uniform gain ×0.70 | 0.980395 | 0.682099 |
| Uniform gain ×1.30 | 0.985668 | 0.787809 |
| Gaussian blur σ=2 | 0.962412 | **0.476080** |
| Whole-frame translation (+8,+6) px | 0.984451 | 0.709877 |
| Fixed rectangular white glare | **0.482693** | 0.804012 |

### Frozen predictions, evaluated without tuning

| Frozen test | S01 | S19 | Joint decision |
| --- | --- | --- | --- |
| H1: clean AUC ≥0.70 | PASS | PASS | **PASS** |
| H2: clean AUC ≥0.50, same association direction | PASS | PASS | **PASS** |
| H3: gain ±30% AUC decline ≤0.10 | PASS | PASS | **PASS** |
| H4: translation AUC decline ≤0.10 | PASS | PASS | **PASS** |
| H5: glare AUC decline ≤0.10 | **FAIL** (decline 0.501082) | PASS | **FAIL** |

**Additional prespecified descriptive nuisance observation, not a frozen H1–H5 threshold:** S19's σ=2 blur reduced AUC from 0.753858 to 0.476080, a decline of 0.277778. This is a major failure of the candidate feature under that simulated blur. The source videos are real human recordings; the optical perturbations are controlled digital transformations, not estimates of natural-world nuisance prevalence.

## Scientific interpretation and falsification

A fixed, training-free, background-motion-corrected eye-flow feature gives a positive EEG-marker association in two human recordings and avoids the *clean-condition sign reversal* of E002-395/396's retired dark-pixel proxy. **This does not rescue it as a physical eyelid-aperture observable.** A glare rectangle destroys discrimination on S01; blur destroys discrimination on S19. The feature measures residual image motion and may respond to gaze, eye position, shadows, illumination, head movement and other confounders. No actual physical palpebral aperture or blink closure threshold was labeled. EEG marker windows may be imperfect and control windows may contain unmarked events.

No device holdout, independent shutter/exposure calibration, independently measured camera timebase, physically bounded optical error, independently established physiological maximum velocity, prospective E002-371 no-hidden-closure predictions or external human replication was performed. The two recordings are insufficient for population inference; do not claim publication-level novelty, clinical performance or calibrated selective risk. No human-image files were committed.

## Primary-literature boundary relevant to the next experiment

- Kwon et al. (2013), [*High-speed camera characterization of voluntary eye blinking kinematics*](https://pmc.ncbi.nlm.nih.gov/articles/PMC4043155/): 600-fps high-speed physical palpebral-aperture trajectories in 25 volunteers. It does not supply a universal hard maximum speed for all people.
- Wambier et al. (2014), [*Two-Dimensional Video Analysis of the Upper Eyelid Motion During Spontaneous Blinking*](https://doi.org/10.1097/IOP.0000000000000031): simultaneous high-speed video and magnetic search coil in 21 subjects, providing a precedent for independent physical-motion validation.
- [*Video-Based Eye Blink Identification and Classification*](https://pubmed.ncbi.nlm.nih.gov/35213320/) (2022): eyelid/iris segmentation and expert-adjudicated blink labels. This prior art precludes novelty claims for basic video eyelid segmentation or event detection.

## Product decision and decisive next falsification

- **REJECT** E002-397 motion energy as a general, nuisance-robust closure or aperture observable; keep it as a research-only event-motion signal under explicitly qualified optics. Retain `REJECTED_E002_395` for the dark-pixel proxy.
- **ABSTAIN_UNCALIBRATED** for blink duration, PERCLOS, fatigue, hidden-closure exclusion, and physical eyelid speed. A clean AUC is not a hard certificate.
- Next physical test: blind two independent annotators to event labels and estimate upper/lower eyelid landmarks and aperture from time-stamped high-speed reference frames, with adjudication and inter-rater error. Independently calibrate exposure, optical mapping, speed bounds and timing; freeze E002-371 gap predictions **before** testing on new participant/device holdouts. A reference label that cannot exclude shutter erasure must be marked unresolved rather than negative. Use a physically calibrated moving phantom if no adequate public reference exists.

## Reproduction

- Frozen protocol: `research/observability/E002_397_FROZEN.md`
- Human feature: `research/observability/e002_397_human_motion.py`
- Independent rank oracle: `research/observability/e002_397_independent_check.py`
- Workflow: `.github/workflows/e002_397_human.yml`
- Anonymous artifacts: S01 `12510679086`; S19 `12510174287` (14-day retention).

**Result:** a new, independently reproduced *human-video nuisance falsification* of the proposed motion surrogate, not a validated shutter-gap boundary or production-grade blink measurement.
