# E002-410 — verified participant-cluster velocity-calibration falsification

**Date:** 2026-10-24. **Evidence tier:** preregistered synthetic hierarchical velocity experiment with independent numerical/rank oracle and fail-closed release-gate tests; **not physical human-aperture validation**.

## Frozen protocol and reproducibility

The [protocol](E002_410_FROZEN.md) was committed at `8401f079` **before** implementing/running the experiment. The complete seeded simulation is `e002_410_cluster_risk.py`; an independent oracle is `e002_410_independent_check.py`; 12 release-gate regression tests are in `test_e002_410_cluster_risk.py`. [GitHub Actions run 40062485944](https://github.com/sushxnthd/lucent/actions/runs/40062485944) completed **successfully** at `a5426942`, including all frozen numerical predictions, independent checks and gate tests. A machine-readable JSON aggregate is uploaded as a 14-day CI artifact. No human data are uploaded.

## Preregistered numerical results (40,000 Monte Carlo trials)

| Calibration / deployment model | Exceedances | Rate | Frozen prediction |
|---|---:|---:|---|
| 20 participants × 100 strongly correlated frames; 1 future frame from unseen participant | 1,920 | **4.8000%** | PASS, within 0.6 pp of 1/21 |
| 2,000 genuinely independent calibration frames; 1 independent future frame | 19 | **0.0475%** | PASS, near 1/2001 |
| 20 participant-level maxima; one unseen participant's 100-frame maximum | 1,939 | **4.8475%** | PASS, within 0.6 pp of 1/21 |
| Same clustered calibration, but future participant latent velocity shifted +0.25 | 11,911 | **29.7775%** | PASS, exceeds frozen 20% threshold |

The naive 2,000-frame rank-risk figure is 0.049975%; the observed clustered unseen-participant exceedance is **96.048× higher**. That ratio is a **synthetic counterexample to pseudoreplicated frame-level calibration**, not an estimate of the prevalence of false eyelid certificates.

An independently seeded rank oracle observed **1,915/40,000 = 4.7875%**, near 1/21. Exhaustive enumeration of all 5! rank permutations with 3 calibration and 2 future participants yielded **48/120 = 40%**, exactly 2/(3+2).

## Boundary law, interpretation, and novelty

For continuous exchangeable *participant-level maxima* `V_1,...,V_n,V'_1,...,V'_m`, the probability that at least one future participant's maximum exceeds the largest calibration maximum is exactly

`P(max_j V'_j > max_i V_i) = m/(n+m)`.

The result is conservative (<=) in the presence of ties. This is the familiar exchangeable-rank law, not a novel mathematical theorem; clustered/hierarchical conformal calibration has prior literature (e.g. [Conformal Prediction: A Data Perspective](https://doi.org/10.1145/3736575)). The new Lucent-specific contribution is a preregistered, independently executed failure demonstration and explicit release restriction at the human-eyelid velocity-calibration interface.

The law is **marginal** over calibration and future sampling, not a probability bound conditional on one fixed calibration set. It fails under deployment population/device shift, as the shifted synthetic control demonstrates. It does not bound optical reconstruction, shutter uncertainty, false physical closure certificates or reference-video blind spots. It cannot replace E002-371's hard physical velocity assumption in a deterministic proof.

## Enforced product consequence

The new `research_risk_gate` rejects calibration measured in frames rather than independent participant-session maxima; rejects missing/invalid maxima, inadequate participant counts, absent physical-aperture review, missing exchangeability review and device-domain mismatch. Even a passing research eligibility gate returns `product: ABSTAIN_UNCALIBRATED`. These self-reported flags are **not authentication**; no deterministic physical certificate is emitted.

For a one-participant future session and alpha=0.05, 19 independent calibration participants are a theoretical minimum under exchangeability. For a *batch of ten* future participants, 190 independent calibration participants are required for the same 5% batch exceedance risk. Two human participants (S01/S19) and thousands of frames cannot supply this evidence.

## Next decisive human experiment

The [E002-410 human protocol](E002_410_HUMAN_PROTOCOL.md) freezes camera timing/geometry calibration, blinded two-rater physical-aperture annotation, participant-level calibration and unseen-device nuisance tests. The immediate bottleneck remains two independent real E002-407 rater sheets and independently calibrated physical reference timing. If physical hard velocity bounds cannot be established, report only conditional statistical research statements and abstain on deterministic closure exclusion, blink duration, PERCLOS and fatigue.

**Scientific gate: NOT MET.** This experiment is a strong synthetic falsification of an unsafe calibration assumption, not a new general theory or an empirical validation of E002-371.
