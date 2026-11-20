# E002-534 | Hosted human-video result: frozen image-return hypothesis fails

Date: 2026-10-30. Evidence tier: **real recorded human video, exploratory within-dataset negative result; no anatomical closure truth, no authenticated shutter/clock, no participant-disjoint holdout**.

## Frozen prediction and provenance

Protocol frozen at [E002_534_FROZEN.md](E002_534_FROZEN.md) before the new observable was executed on S01/S19 native videos. No threshold, ROI, phase, participant, or nuisance was selected in response to these results. The workflow used checksum-verified Eye-BCI S01 (MD5 `fef02cb7ebf62e4f3efb6303284fd6cb`) and S19 (MD5 `8a16cf12526f7558b4e49926c4bc5e8e`) archives, each with 12,006 decoded native frames. Subjects and source data had been examined in earlier experiments, so **this is not an untouched validation cohort**.

The frozen eye-return predicate required eye endpoint mean absolute difference <=8 intensity units and maximum intermediate linear-endpoint deviation >=18; an eye-specific candidate additionally required background excursion <=8. Windows contained six native frames (five inter-frame steps), two predeclared phases, and predeclared source-ID/time eligibility filters. This is an image-space observable, not a blink/closure detector.

Source: [GitHub Actions run 40963849531](https://github.com/sushxnthd/lucent/actions/runs/40963849531), commit [f73ae072](https://github.com/sushxnthd/lucent/commit/f73ae0727c30b8e337017c27413881a9906e83f8). Run **completed successfully** on 2026-10-29 UTC. All three jobs passed: synthetic-integrity, S01 human video, S19 human video. Raw images and per-window linkage were not uploaded; only aggregate counts were printed.

## Immutable observed aggregate

| Participant | Phase | Eligible windows | Rejected for time/ID | Eye-return | Eye-specific | Background-return |
|---|---:|---:|---:|---:|---:|---:|
| S01 | 0 | 2,379 | 22 | 0 | 0 | 0 |
| S19 | 0 | 2,380 | 21 | 0 | 0 | 0 |
| S01 | 2 | 2,378 | 22 | 0 | 0 | 0 |
| S19 | 2 | 2,379 | 21 | 0 | 0 | 0 |
| **Total** | both | **9,516** | **86** | **0** | **0** | **0** |

Phase-0 total: **0/4,759** eligible eye-specific windows; phase-2 total: **0/4,757**. Windows in the two phases are partially overlapping and belong to only two previously studied participants; **do not** treat 9,516 as independent samples for a population confidence interval.

### Preregistered decisions

- **H1 fails**: the preregistered >=1 eye-specific phase-0 candidate was not observed in either participant. The frozen image-return hypothesis is rejected at the stated ROI, threshold, and source scope. Do **not** retune the intensity thresholds or cherry-pick windows to rescue it.
- **H2/H3 not testable**, not passed: there were zero baseline candidates, so Gaussian-blur and clipped-gain candidate survival fractions have undefined denominators. Their returned `NOT_TESTABLE` statuses are correct.
- **H4**: the alternate phase also yielded zero; this does not establish phase invariance of a non-observed phenomenon.
- **H5**: the synthetic-integrity job passed, supporting implementation behavior on synthetic positive/negative controls, not sensitivity on actual eyelid closure.

## Falsification and product consequence

This is the first hosted, frozen-threshold, checksum-verified **real-human-video negative result** for this specific E002-534 pixel-return observable. It **does not falsify** E002-371's mathematical observability boundary: the experiment does not measure eyelid aperture, label closure, or certify exposure timing. Zero observed image-return candidates cannot prove zero hidden closures. Nor can it validate an image-space detector, establish population frequency, or support a physiological speed ceiling.

**Kill decision:** do not promote this eye-ROI pixel-return score to a Lucent product measurement, do not advertise its sensitivity, and do not spend additional cycles retuning the same two subjects. Preserve the null result.

**Product state remains `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.** A shutter-gap certificate requires independent optical timing, anatomy, and speed assumptions; a reference-video absence-of-closure label must abstain over missing native frames and unresolved threshold dwell.

## Next decisive empirical experiment, not another synthetic rescue

1. **Physical reference:** record an LED pulse train and independent photodiode/oscilloscope timebase against the actual camera sensor, recording frame start, exposure, row offset, dropped frames, clock drift, gain/response, blur, and timestamp uncertainty. Freeze the candidate camera and uncertainty intervals before human recording.
2. **Human truth:** two blinded independent anatomical raters mark eyelid-aperture thresholds on **native** high-speed frames, without interpolating missing frames. Require explicit disagreement/unknown labels; adjudication cannot silently turn unknown into open. Keep images and identities access-controlled.
3. **Prospective prediction:** independently derive subject/session speed envelopes (or use conservative interval bounds, not sampled peak velocity as a hard ceiling); precommit ordinary-camera gap predictions, nuisance strata (gaze, lighting, glasses, motion, missingness), abstention rule and exact failure criteria **before** opening participant-disjoint holdouts.
4. **Release gate:** report false exclusions at the participant-session level with exact confidence bounds, abstention coverage and cost; no physiological or safety claim without independent review. The previously derived 299 zero-failure independent-participant minimum for <1% upper risk at 95% confidence applies only under its stated exchangeability assumptions, not to this two-person study.

Reproduce the frozen pipeline with [e002_534_human_return_excursion.py](e002_534_human_return_excursion.py), [test_e002_534_human_return_excursion.py](test_e002_534_human_return_excursion.py), and [.github/workflows/e002_534_human_return_excursion.yml](../../.github/workflows/e002_534_human_return_excursion.yml). The hosted job logs are the public aggregate evidence; raw human images were intentionally not published.
