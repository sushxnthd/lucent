# E002-415 — verified synthetic calibration-provenance spoofing and product-output isolation

**Date:** 2026-10-24. **Evidence tier:** adversarial synthetic instrument / product-interface falsification. **Not human aperture validation; not a real-camera calibration.** Frozen at `e6770ef082ad22bd1fa4bf5dd80c8c5359f5940a` before code changes.

## Verified result

[GitHub Actions run 40085836207](https://github.com/sushxnthd/lucent/actions/runs/40085836207) **completed successfully** on implementation/test head `15a4d1d92a25a15df5fac554cfd6f46595aff4f3`. Both the preexisting E002-408 two-rater regression and an independently implemented E002-415 consumer-side output checker passed, along with E002-399 reference-adequacy regression. [E002-408 regression run 40085836195](https://github.com/sushxnthd/lucent/actions/runs/40085836195) also passed.

The adversary provided *only strings and Booleans* claiming independent camera-hardware clock, optical response, row timing, anatomical geometry and deterministic physical velocity. None was authenticated or measured. The synthetic 120-frame/two-rater fixture yielded:

| Output | Verified |
|---|---:|
| Synthetic annotated frames (fixture, **not human ratings**) | 120 |
| Conditional research-only `CONFIRMED_NO_CROSSING` | **4/4 clips** |
| Public/unqualified product `CONFIRMED_NO_CROSSING` | **0/4 clips** |
| Public/unqualified `ABSTAIN_UNCALIBRATED` | **4/4 clips** |
| Independently checked forged output controls | 3 rejected |
| Independently authenticated physical calibrations | **0** |
| Actual human aperture outcomes | **0** |

The prior implementation exposed the four *conditional* scientific certificates in the unqualified `decisions` field while separately stating `product: ABSTAIN_UNCALIBRATED`. A consumer reading only `decisions` could misinterpret these as physically justified certificates. The corrected output retains conditional calculations **only** in `conditional_research_decisions` and explicitly reports `conditional_research_only: true`, `physical_calibration_authenticated: false`, `product_claim_authorized: false`. The top-level `decisions` field always abstains in this unauthenticated tool.

The independently coded consumer contract checker rejects injected top-level certificates, injected product authorization and injected authentication, and confirms that absence of calibration still abstains. The existing positive scientific oracle remains reachable under synthetic exact assumptions; the underlying conditional theorem was not changed.

## Audit trail

The first E002-415 CI run failed because an existing synthetic test incorrectly expected the *conditional research* result to be `None` after an empirical velocity-max gate failed. In fact the conditional oracle correctly returns four **abstentions**. The assertion was corrected at `15a4d1d`, and the final E002-415 and E002-408 CI jobs both passed. No failures were concealed or interpreted as scientific evidence.

## Scientific interpretation

This is a concrete **evidence-to-product interface falsification**, not a new nonidentifiability theorem or proof of a deployed vulnerability. It does not show that a physical no-hidden-closure certificate is possible with the existing human data. A provenance string cannot authenticate shutter timing, optical kernel, hard physical velocity bound or anatomy. The appropriate product behavior remains abstention until independent physical review.

**Decisive next experiment:** obtain two genuinely independent blinded human eyelid-margin annotation sheets from the existing E002-407 full-event pilot, adjudicate with E002-408, and measure independent camera-clock/shutter/physical-aperture/velocity references on untouched participants/devices. The S01/S19 632 video frames remain **unannotated** and cannot be treated as 632 physical aperture observations. No blink duration, PERCLOS, fatigue diagnosis or deterministic hidden-closure guarantee is authorized.

## Reproduction

- `E002_415_FROZEN.md` frozen hypotheses.
- `e002_408_two_rater_adjudication.py` revised safe output contract.
- `test_e002_408_two_rater_adjudication.py` preserved conditional scientific oracle and regression checks.
- `test_e002_415_product_boundary.py` independent forged metadata and consumer contract checks.
- `.github/workflows/e002_415_product_boundary.yml` hosted CI.

Run `python research/observability/test_e002_415_product_boundary.py` and `python research/observability/test_e002_408_two_rater_adjudication.py`. No human images, raw annotations, private linkage or real physical calibration artifacts were published.
