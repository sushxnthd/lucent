# E002-449 — completed real-S19 annotation-pack readiness; no anatomical observations

**Date:** 2026-10-26. **Evidence tier:** hosted real-human-video *instrument execution*; no new human anatomical annotations, no physical calibration, no physiological bound.

## Reproducible observation

The previously frozen E002-448 protocol and code were executed in GitHub Actions on the existing Lucent research branch. [Workflow run 40225564544](https://github.com/sushxnthd/lucent/actions/runs/40225564544), job 121266061109, completed **successfully** on head `b3884849850c25abfc1d414608cbb55f12f135b3` at approximately 2026-10-25 20:01 UTC. The run verified the public S19 archive, decoded real eye video, built the private annotation pack, scored the deliberately unlabeled pack, discarded the pack/master on the ephemeral runner, and published only a 453-byte aggregate artifact (ID 12611583145; SHA256 digest `e4d1e310a6713410e79abcd9d1abb47a6a99aec788d2cf30ebd6a1e279681b70`). The independent synthetic/adversarial suite ran **15 tests, all passed**. This is a completed acquisition/preparation result, not merely a queued experiment.

The published aggregate and logs report:
| Frozen S19 pilot statistic | Observed |
|---|---:|
| Candidate 10–100-ms event intervals | 21 |
| Candidate <=10-ms control intervals | 21 |
| Unique decoded human frames selected | 126 |
| Blinded views | 138 |
| Hidden repeat views | 12 |
| Human landmark labels collected | **0** |
| Authenticated shutter timing | **No** |
| Authenticated anatomical scale | **No** |
| Physical E002-371 validation | **NOT_ESTABLISHED** |
| Product release | **ABSTAIN_UNCALIBRATED** |

The 138 views are *not* 138 independent biological observations. The 12 repeats are re-presentations of selected frames; all 126 unique frames originate from **one participant**. The 42 intervals were selected using a candidate synchronization-event clock, which E002-443 previously found incompatible with treating the exported AVI as authenticated 500-fps exposure data.

## Scientific decision and non-negotiable falsification gates

1. **Human-image readiness established; human anatomical validity not established.** A real video can now be transformed into a blinded offline rater pack. The pack was deliberately destroyed on the public runner and cannot itself be handed to raters from this workflow. Recreate it only in controlled authorized storage; never publish identifiable imagery or the private frame mapping.
2. **Do not infer a velocity cap from the 42 intervals.** There are no landmark measurements, calibrated mm, or independently authenticated exposure times. Even a future 0/21 failure count would not certify a general population risk; all observations come from a single participant and were selected nonrandomly.
3. **Freeze and hand off, rather than tune a new proxy.** Two independent human raters must annotate the locally recreated pack, including hidden repeats and explicit abstentions. Report coverage and disagreements before computing any image-space aperture statistics. No rater-generated result may be presented as physical aperture in mm without separate calibration.
4. **Unseen-condition experiment stays sealed.** S21/S22 must not be used for calibration, geometry/brightness threshold tuning, rater instruction optimization, or example selection. Before opening them, freeze a prediction function and failure/abstention scoring rules; verify the independent physical exposure reference.
5. **Stop condition:** If private S19 pack distribution, two independent raters, or exposure/scale instrumentation cannot be obtained, record that as an external human-study blocker. Do not substitute further optical proxies, sample-count inflation, or synthetic theorem variants for physical E002-371 validation.

## Product consequence

The strongest currently supported output is a **research-only annotation/instrument readiness tool** with explicit data-provenance and abstention. No physical hidden-closure guarantee, blink duration, PERCLOS, fatigue score, or medical claim is authorized. The E002-371 observability theorem remains conditional on a valid shutter model and independently justified velocity bound.

**Reproduction:** See [E002-448 frozen protocol](E002_448_FROZEN.md), [annotation tool](e002_448_blind_annotation.py), [rater UI](e002_448_rater.html), [hosted workflow](../../.github/workflows/e002_448_blind_annotation.yml), and the linked successful run's logs and aggregate artifact. This report intentionally contains no identifiable participant images, annotation coordinates, or private mapping.
