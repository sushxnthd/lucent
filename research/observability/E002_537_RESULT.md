# E002-537 RESULT | The 12/12 human pilot cannot certify 95% participant-level false-exclusion control

Date: 2026-10-30. Primary Lucent E002-371 research branch `research/observability-human-boundary`, draft PR #26. **Evidence tier: exact established split-conformal rank argument plus executed seeded synthetic stress; zero new physical shutter measurements or independently rated human anatomical labels.** Frozen in [E002_537_FROZEN.md](E002_537_FROZEN.md) before implementation. This is an experiment-design and product-calibration consequence, **not a new conformal theorem, new physiological measurement, or validated product**.

## New study-design falsification

E002-483 proposed 24 adults split into **12 calibration and 12 participant-disjoint holdout participants**. If the intended product claim is that a new exchangeable participant has at most 5% marginal probability of **any** falsely excluded independently verified hidden closure over their eligible windows, 12 calibration participants are not enough for a **nontrivial distribution-free split-conformal exclusion threshold**. With one worst-case closure score per participant, `k=ceil((n+1)*0.95)`: n=12 gives k=13 and q=+infinity. Thus the only valid frozen decision is abstention. The first finite threshold is n=19 (k=19, the calibration maximum); n=39 gives k=38. This is a mathematical sample-size limitation, not an empirical human false-negative estimate. At n=19 the guarantee is **marginal over exchangeable participants and calibration draws**, not conditional on the observed calibration sample and not uniform over devices or populations.

Define the participant nonconformity as the maximum fixed E002-371 exclusion-aggressiveness score among *independently reference-confirmed hidden closures*; a participant with no confirmed closure has score -infinity, and any unresolved reference interval or failed instrument assumption has score +infinity. Use strict `a>q` to avoid tie-induced anti-conservatism. No source video can be called independent reference merely because it has high nominal FPS. Physically measured shutter/clock, calibrated geometry and blinded human anatomy remain required before any such scores can be measured.

## Frozen synthetic tests executed locally

20,000 deterministic Monte Carlo replicates per setting, seed 53720261030, NumPy 2.3.5, participant scores from N(0,1) for calibration and exchangeable test; the shifted test has N(1.5,1). The same frozen experiment includes a hierarchical 12-participant, 50-windows-each pseudoreplication attack. The executable and 11 adversarial tests passed locally.

| Calibration unit and n | Frozen k | IID expected risk | IID observed | Shifted observed |
|---|---:|---:|---:|---:|
| Participant n=12 | 13 (infinite q) | 0 | 0/20,000 = 0 | 0 |
| Participant n=19 | 19 | 0.0500 | 991/20,000 = **0.04955** | 7,654/20,000 = **0.38270** |
| Participant n=39 | 38 | 0.0500 | 1,055/20,000 = **0.05275** | 8,313/20,000 = **0.41565** |

The iid deviations are within five frozen Monte Carlo SE of the exact rank predictions (SE approximately 0.001541). Under the preregistered participant distribution shift, the same thresholds exceed 5% by a wide margin; exchangeability is not optional. The n=12 case abstains even under shift, which is safe but uninformative.

**Pseudoreplication attack:** 12 participants each contributed 50 correlated synthetic windows (latent participant N(0,1), within-person N(0,0.1)). Treating 600 windows as 600 independent calibration units and applying a nominal 5% single-window quantile yielded **2,172/20,000 = 10.86%** new-participant probability of at least one window exceeding the threshold. This fails the participant-level 5% target despite the apparently large window count. This is a constructed counterexample, not an estimate of actual human blink risk.

## Enforcement consequence and concrete human study amendment

- **Current 12/12 study** is acceptable as a *feasibility pilot* only. It must not produce a nontrivial 95% distribution-free participant-level false-exclusion certificate. Retain the existing 12/12 plan for equipment feasibility and rater agreement, but mark any such risk guarantee `ABSTAIN_UNCALIBRATED`.
- **Prospective calibration expansion:** at least **19 independent calibration participants** before a finite 5% participant-level split-conformal threshold is possible, with a separately held-out participant-disjoint evaluation cohort. This lower bound is necessary for this method, not sufficient for a useful or transportable classifier. Prefer substantially more than 19 to avoid near-maximum thresholds and quantify nuisance-stratified behavior. Freeze trial count per participant, reference-label policy, score function, device, gaze, glasses and illumination strata before data collection.
- **Reference unknowns and calibration failures** must map to +infinity or abstention, never presumed absence. Participants are the sampling unit; repeated windows and repeated blinks do not multiply independent sample size. Unknown or out-of-support devices and nuisance conditions require abstention.
- **Physical-first gate remains unchanged:** no product-level hidden-closure exclusion without independently authenticated exposure/clock and anatomical aperture with two blinded raters. Even a future conformal result would establish only a participant-exchangeable *marginal statistical* guarantee, never a deterministic no-hidden-closure certificate or fatigue diagnosis.

## Interpretation, independence and next decisive experiment

The synthetic generator tests the finite-sample guarantee and two failure modes, not the physiology. The exact rank formula is established split-conformal methodology and is **not claimed as Lucent novelty**. The simulated N(0,1) scores are abstract, not fitted to any real person. The strongest prospective research contribution remains an instrument-calibrated E002-371 observability boundary evaluated against blinded, participant-disjoint physical reference anatomy, with an honest separation between conditional geometric impossibility and calibrated population-level error.

**Evidence inventory:** new independent anatomical ratings 0; photodiode-authenticated camera studies 0; certified continuous-time human velocity envelopes 0; participant-disjoint physical shutter-gap predictions 0. The E002-534/535 pixel-return observable stays rejected. Lucent product `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. Hush PR #45 unchanged.

## Verification

Local: `python -m unittest -v test_e002_537_participant_calibration.py` **11/11 passed**; `python e002_537_participant_calibration.py` produced the frozen results above. Dedicated [hosted workflow](../../.github/workflows/e002_537_participant_calibration.yml) pins Python 3.11 / NumPy 2.3.5. **Hosted success was not verified when this report was first committed.** Do not convert queued or failed CI into a passing claim.
