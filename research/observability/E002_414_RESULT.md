# E002-414 — verified participant-level false-certificate validation power

**Date:** 2026-10-24. **Status:** Frozen protocol executed; all 14 independent arithmetic / adversarial tests passed. **Evidence tier:** prospective human-study design and synthetic research-gate verification only. **No physical human aperture labels or shutter/velocity measurements were obtained.**

## Provenance

- Frozen *before* implementation at commit `e8b620983fba24bf907ad63cabfc0b331c4081ff` in [E002_414_FROZEN.md](E002_414_FROZEN.md).
- Exact research gate: [e002_414_claim_power.py](e002_414_claim_power.py).
- Independent exhaustive enumeration / coverage / adversarial checks: [test_e002_414_claim_power.py](test_e002_414_claim_power.py).
- [Successful GitHub Actions run 40080693527](https://github.com/sushxnthd/lucent/actions/runs/40080693527), head `39bcc7a043968976db23ff30e468cfc47ad545f1`, completed 2026-10-24 09:07 UTC. **14/14 tests passed**; the exact binomial-tail implementation was checked against independent exhaustive enumeration for small n, and exact frequentist coverage was checked for selected p,n combinations.

## Frozen numerical predictions: all reproduced

For **n independent held-out participants** each with >=1 preselected, reference-resolved issued no-crossing certificate, define a participant failure as >=1 false certificate on that participant. Under iid participant outcomes and zero observed failures, the exact one-sided 95% upper bound on the *participant-level failure probability* is `1 - 0.05 ** (1/n)`.

| Hypothetical independent participant count | Zero-failure 95% upper bound |
|---|---:|
| 2 | 77.6393% |
| 20 | 13.9108% |
| 58 | 5.0339% |
| **59** | **4.9508%** |
| 118 | 2.5068% |
| **119** | **2.4860%** |

Incorrectly counting 632 correlated frames as 632 independent participants would give an apparent **0.4729%** upper bound. The actual E002-407 data are 632 frames from only **two** participants and **contain no adjudicated physical false-certificate outcomes at all**; even the 77.6393% entry is a hypothetical *best-case power calculation*, not an observed Lucent failure-rate bound.

For a separate *statistical, research-only* participant-max velocity calibration against a batch of ten future participant maxima, the exchangeable-rank marginal exceedance probability is at most `10/(n_cal+10)`. A 2.5% allocation requires **390 independent calibration participants**. A separate 2.5% participant-level zero-failure validation bound at 95% confidence requires **119 held-out participants**. A disjoint illustrative study therefore requires **509 participants**, *before* stratified nuisance/device replication. These two probabilities have different inferential meanings; combining budgets is only a conservative planning illustration under additional assumptions, not a validated end-to-end guarantee.

## Adversarial product consequences

The new research gate:
- counts one failure per independent participant, regardless of how many frames/gaps that participant contributes;
- refuses duplicated participant IDs, mixed unreviewed devices, participants already used for tuning, zero-certificate participants, missing reference-resolution accounting, malformed counts, and absent physical-calibration evidence assertions;
- checks that at least one reference-resolved no-crossing certificate was actually issued for every participant included in the binomial denominator, preventing all-abstain zero-error claims;
- reports total certificates and eligible gaps separately **without treating them as independent**;
- never authenticates user-supplied provenance booleans and **never** authorizes a physical product certificate, even if a synthetic 59-participant manifest passes the statistical threshold.

All synthetic controls retained `product: ABSTAIN_UNCALIBRATED` and `physical_certificate: NOT_AUTHORIZED`.

## Primary-literature priority

The exact binomial confidence construction is classical: C. J. Clopper and E. S. Pearson, *The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial*, **Biometrika** 26(4), 404–413 (1934), DOI [10.1093/biomet/26.4.404](https://doi.org/10.1093/biomet/26.4.404). The exchangeable rank calculation is also established. **E002-414 claims no mathematical novelty**; its contribution is an independently checked, fail-closed Lucent validation-budget consequence.

## Decision and next experiment

The 8 E002-407 high-speed human clips / 632 frames can only be used to establish **two-rater annotation feasibility**, not rare false-certificate reliability. Freeze and obtain two independent human eyelid-margin annotation sheets using [E002_407_RATER_HANDOFF.md](E002_407_RATER_HANDOFF.md), run the E002-408 adjudication, and then undertake a separately calibrated, untouched-participant shutter-gap study. Device, brightness, blur, glare, missingness, gaze, glasses, geometry and clock uncertainties must be explicitly controlled. Do not count multiple frames from one participant as independent validation.

**Unmet:** real human physical aperture ground truth, verified independent shutter timing/response, physical velocity envelope, actual false-certificate outcomes, unseen-device validation and external review. E002-371 remains a conditional observability theorem, not an empirically validated physical product guarantee. No blink duration, PERCLOS or fatigue inference is authorized.
