# E002-530 | Human primary-source reconciliation: acquisition FPS is not anatomical sampling rate

Date: 2026-10-29. Primary E002-371 observability kernel; persistent branch `research/observability-human-boundary`, draft PR #26. **Evidence tier: post-hoc primary-source methods reanalysis and human-study design consequence.** This is not a new participant experiment, a measured shutter, a hard physiological bound, or a new theorem. No prospective freeze is claimed: the published paper was inspected before writing this note.

## Primary-source measurement facts (not reconstructed from a dataset)

Kwon et al., *J. R. Soc. Interface* 10:20130227 (2013), DOI [10.1098/rsif.2013.0227](https://doi.org/10.1098/rsif.2013.0227), [open full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC4043155/), section 2 and table 1:

1. A Phantom v7.3 camera **acquired at 600 frames/s**, with 800 x 600 pixels, for **25 volunteers** performing instructed *voluntary* blinks. Two blinks were recorded per person, but **only the second was analyzed**.
2. **Anatomical palpebral aperture was measured every 5 ms**, not every acquired 1/600 s (1.6667 ms). Consequently, the published anatomical time series was sampled at **200 samples/s**, i.e. **one measurement per three native acquisition frames** under nominal regular sampling. A 600-fps acquisition rate is not evidence of 600-Hz anatomical annotations.
3. Closing/opening speeds were calculated as **gradients between consecutive measured aperture points**. The reported **243 +/- 9 mm/s mean peak closing speed** is an estimate from that sampled series (the paper reports group uncertainty as standard error), not a bound on continuous-time velocity between 5-ms observations, not the maximum across all human beings, and not a bound on spontaneous/reflex blinks.
4. The study reports a **58 +/- 4 ms closed phase** (group mean +/- standard error). This is direct published human evidence that a nonzero closed phase was observed in that voluntary-blink cohort. However, a group mean and its standard error **do not provide an individual minimum, a lower-tail quantile, a worst-case bound, or a threshold-specific dwell distribution** for Lucent's arbitrary normalized threshold `c`.
5. Their full voluntary-blink duration includes a slow late-opening phase. **Full blink duration, closing duration, closed phase, and below-`c` dwell are distinct observables**. E002-529's near-zero-dwell mathematical counterexample cannot be presented as an observed typical human blink; conversely, the published 58-ms group mean cannot eliminate that counterexample for unseen conditions.

The primary-source passage is [methods and analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC4043155/#sec2), with numerical closed-phase results in [section 3](https://pmc.ncbi.nlm.nih.gov/articles/PMC4043155/). This is a methodological reconciliation, not a fresh dataset search.

## Scientific consequence for E002-371 / E002-528 / E002-529

**Reject both overclaims:**
- `600 fps literature -> continuous-time certified V`: false. The analyzed aperture series has 5-ms increments and finite-difference speeds. Even the 600-fps raw acquisition would not alone certify a continuous-time derivative bound.
- `arbitrarily short mathematical dwell -> typical human blink has zero reference sensitivity`: false. The paper documents a nonzero closed phase in its voluntary-blink cohort, but does not supply individual threshold-dwell labels or a lower bound transferable to spontaneous/reflex blinks.

For *instrument planning only*, a hypothetical **58-ms individual continuous below-threshold dwell** would exceed the strict full-exposure every-phase threshold `P+e+2u` for a 240-Hz reference with 1-ms exposure and 0.1-ms per-endpoint uncertainty: `4.1667 + 1 + 0.2 = 5.3667 ms`. **The paper does not establish the 58-ms premise for every participant or for Lucent's closure threshold.** No reference detection probability or product accuracy follows from the group mean. The 5.3667-ms arithmetic is a conditional design check, not measured shutter timing.

The viable research path is therefore a **one-sided, blinded positive-witness falsification study**, supplemented by separately calibrated quantitative exposure witnesses where possible. A high-speed *absence* remains censored unless a validated minimum dwell/sensitivity model exists. Distinguish (a) a reference camera's frame-acquisition rate, (b) the rate of independently adjudicated anatomical measurements, and (c) physically authenticated exposure support.

## Concrete prospective human-validation changes

- In the existing private E002-502 S01 rater handoff, retain native indices and explicitly record **which native frames actually received anatomical ratings**. Do not assign nominal source FPS to an interpolated/decimated label series. Preserve abstentions and rater disagreement.
- For new paired physical capture, obtain two independent blinded anatomical annotations **on native reference frames**, with timestamp/exposure uncertainty per frame and a prespecified closure threshold. Separately report **continuous below-threshold dwell, full excursion, and reference-censored intervals**; do not infer a positive dwell from speed alone.
- Publish participant/session-level counts, label cadence, actual reference witness opportunities, and missingness/blur/gaze/glasses/lighting/geometry/rolling-shutter/clock nuisance stratification. Keep individual images, source indices and identifiable records private.
- The first eight-participant pilot is for feasibility/counterexamples, **not** a population false-exclusion guarantee. Do not count non-detections as verified negatives. For a hard hidden-closure exclusion, independently certify the continuous-time speed premise; otherwise abstain.

## Priority and release interpretation

Kwon 2013 already establishes high-speed voluntary-blink kinematics and observed closed-phase durations. It does **not** establish Lucent's sharp shutter-gap theorem, nor does this targeted comparison establish priority for that theorem. The E002-371 contribution remains a conditional observability/measurement-claim boundary awaiting external theorem-priority review and independent physical validation. No more literature rate archaeology is justified by this note.

**New direct product consequence:** never describe published 600-fps eyelid studies as 600-Hz *anatomical* measurements without checking the actual annotation cadence; never use published group mean closed phase to claim guaranteed high-rate reference sensitivity. `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.

**Evidence gate:** new human raters **0**; independent physical shutter/clock **0**; certified continuous-time speed ceiling **0**; held-out physical predictions **0**. Hush PR #45 unchanged.
