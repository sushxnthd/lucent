# E002-536 RESULT | Published blink kinematics are not a hard observability certificate

Date: 2026-10-30. Primary E002-371 kernel, established branch `research/observability-human-boundary`, draft PR #26. **Evidence tier: primary-literature priority audit and exact-rational hypothetical sampling stress; no newly acquired human or physical camera data.**

## Priority and physiological validity

This is a targeted **primary-source audit**, not repeated dataset discovery or another attempt to rescue the rejected E002-534/535 pixel-return detector.

- **Kwon et al. (2013), [DOI 10.1098/rsif.2013.0227](https://doi.org/10.1098/rsif.2013.0227):** 25 healthy volunteers, voluntary blinks captured at 600 fps, with palpebral aperture measured at 5-ms intervals. Reported cohort mean peak closing speed **243 +/- 9 mm/s**, mean initial aperture **9.8 +/- 0.2 mm** (observed range **7.4-12.8 mm**) and mean closed-phase duration **58 +/- 4 ms**. These are sampled/group measurements. Neither the peak speed nor the mean closed-phase duration is a universal continuous-time extremum. Ratio of cohort means is not the mean participant-specific normalized velocity.
- **Doane (1980), [DOI 10.1016/0002-9394(80)90058-6](https://doi.org/10.1016/0002-9394(80)90058-6):** normal unforced **upper-eyelid descent** usually 17-20 cm/s, sometimes over 40 cm/s. The measured observable is upper-lid motion; without a lower-lid and geometry model it is **not** a hard bound on the derivative of normalized palpebral aperture. Unit conversion alone is insufficient.
- **Godfrey et al. (2019), [DOI 10.1097/IOP.0000000000001356](https://doi.org/10.1097/IOP.0000000000001356):** 10 volunteers, spontaneous blinks recorded using a nominal 240-fps smartphone; mean blink closure velocity 93 mm/s (SD 31, observed range 40-160 mm/s). Demonstrates a credible low-cost human-anatomy pilot route, **not** photodiode-authenticated shutter/clock or a physiological hard ceiling.
- **Wambier et al. (2014), [DOI 10.1097/IOP.0000000000000031](https://doi.org/10.1097/IOP.0000000000000031):** 21 adults, simultaneous high-speed video and magnetic search coil, with reported mean difference in maximum velocity 5.0 +/- 3.4 mm/s. Validating video eyelid kinematics against an independent instrument is **prior art**; Lucent cannot claim video kinematics itself as a new measurement method.
- **Sforza et al. (2008), [DOI 10.1111/j.1475-1313.2008.00577.x](https://doi.org/10.1111/j.1475-1313.2008.00577.x):** substantial age/sex dependence and incomplete spontaneous closure; voluntary, spontaneous and reflex blink populations must not be silently pooled.

**Novelty decision:** E002-371's candidate contribution, if it survives empirical validation and broader priority review, is a *sharp conditional impossibility/abstention boundary under explicitly calibrated acquisition and anatomical uncertainty*, not discovery of eyelid kinematics, a novel smartphone blink detector, or a population velocity constant. None of these papers proves or refutes the exact shutter-gap law itself; the audit is not exhaustive.

## Frozen exact calculation, executed locally

The frozen E002-536 test treats the Kwon *cohort-summary ratio* `243/9.8 = 1215/49 s^-1` as a **hypothetical representative speed**, not a measured subject/session envelope. For `b=1`, `c=0.2`, global shutter `e=1 ms`, and zero clock uncertainty, the existing conditional E002-371 ratio is `R = V*(T-e)/(2*(b-c))`.

| Hypothetical sampling | Exact R | Conditional geometry if V were a hard bound | Actual evidence decision |
|---|---|---|---|
| 30 fps | 7857/15680 = 0.50108418 | A hidden threshold crossing would be excluded | **ILLUSTRATIVE_NOT_CERTIFIED** |
| 15 fps | 15957/15680 = 1.01766582 | A hidden crossing is not excluded | **ILLUSTRATIVE_NOT_CERTIFIED** |

Critical frequency is approximately **15.26094 fps** for these *hypothetical* parameters. This is a sharp model-side reversal, **not** a measured camera/participant prediction. The 2013 source did not measure the hypothetical shutters. Cohort means cannot be substituted for a certified `V`, and the group mean closed-phase duration cannot be used as a guaranteed eventwise minimum. The apparent 30-fps exclusion is therefore **not an allowed Lucent product claim**.

The [Python exact-rational executable](e002_536_literature_velocity_gate.py), [11 adversarial tests](test_e002_536_literature_velocity_gate.py), and [independent Node BigInt replay](e002_536_independent_replay.cjs) were implemented **after the freeze**. Local execution: **11/11 tests passed**, and the Node replay independently reproduced `1215/49`, `7857/15680`, and `15957/15680`. Adversarial controls include cohort-mean masquerading as a hard bound, upper-lid/aperture observable mismatch, sampled-peak misuse, unpaired denominator, absent physical attestations, group-mean dwell misuse, malformed geometry, nonboolean evidence and private-field output exclusion. The [hosted workflow](../../.github/workflows/e002_536_literature_velocity_gate.yml) was committed; **hosted success not verified at report creation**.

## Direct enforcement and next physical work

The research gate reports `ILLUSTRATIVE_NOT_CERTIFIED` unless a hard continuous-time *aperture-derivative* envelope, paired same-session scale, independent anatomy, photodiode-authenticated exposure, clock, native missingness and nuisance envelope are all explicitly attested. Even a fully attested **hypothetical** input is only `CONDITIONAL_BOUND_ONLY`; the executable **never** certifies physical acquisition or production hidden-closure exclusion. Every branch retains `ABSTAIN_UNCALIBRATED` and `BLOCKED`.

The literature supplies an actionable low-cost **240-fps smartphone pilot**, not a validated reference. Record independently timed optical pulses and native high-speed anatomy, obtain two blinded human raters, and precommit participant-disjoint tests of the dimensionless gap boundary. Explicitly distinguish spontaneous, voluntary and reflex blink strata. A true empirical speed ceiling requires an independent physical or model-based *continuous-time* argument, not the maximum sampled finite difference. No further literature-derived constant tuning is warranted.

**Human anatomical ratings: 0. Authenticated physical camera studies: 0. Certified continuous-time velocity ceilings: 0. Participant-disjoint physical predictions: 0.** Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. Hush PR #45 untouched.
