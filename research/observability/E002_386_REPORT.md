# E002-386 — Selective risk calibration fails under unseen optical-device shift

**Status: completed synthetic-only experiment.** Frozen protocol: E002_386_FROZEN.md, committed before testing. No human or physical-camera data were used.

## Abstract
E002-371 supplies a conditional Lipschitz shutter-gap bound, but E002-385 found that clipwise optical coverage need not control incorrect decisions *among issued no-hidden-closure certificates*. We prospectively tested a 32-policy selective-risk calibration using one-sided exact Clopper-Pearson bounds with Bonferroni familywise delta=0.05 and conditional risk target alpha=0.02. In 30,000 IID held-out synthetic recordings, the selected policy issued 10,420 decisions with 45 errors (0.432%), versus 1,028/11,403 (9.015%) for a naive analytic margin threshold. Under a separately simulated unseen-device optical shift, transferring the same policy without its device gate produced 2,433/12,998 errors (18.72%). This is an application of established statistical risk control, **not a new universal observability theorem**.

## Measurement model and prediction
Aperture a(t) in [0,1], threshold theta=0.2, global shutter 30 Hz, exposure w=10 ms, V=40/s. Hidden reference events are clipped triangular valleys with minima U(0.17,0.195) at the blind-gap midpoint; open controls have a(t)=1. Analytically integrated exposure averages are corrupted by hand-specified independent jitter, correlated optical bias and a quality proxy. The resulting scalar aperture estimator **is not RGB video**; the artificial crossings are very brief and not evidence about physiological blink prevalence.

The E002-385 exposure-integral-to-endpoint inversion with nominal error .002 yields an *untrusted* gap safety margin. Candidate policies issue if margin >= m and quality <= q, with m in {0,.04,.08,.12,.16,.22,.26,.30} and q in {.30,.50,.75,1.0}. Calibration uses 6,000 independent clips. For candidate j, n_j issued and k_j incorrect, U_j is the exact one-sided binomial upper confidence bound solving P[Bin(n_j,U_j)<=k_j]=0.05/32. The selected candidate maximizes calibration issuance among U_j<=.02. By simultaneous coverage and the union bound, under IID clips the selected conditional error rate is <=.02 with at least 95% calibration confidence. **This is neither eventwise certainty nor distribution-shift robustness.**

## Frozen held-out results

| Condition | Issued | False | False / issued | Issuance |
|---|---:|---:|---:|---:|
| IID naive margin>0 | 11,403 | 1,028 | 9.015% | 38.01% |
| IID calibrated selection | 10,420 | 45 | 0.432% | 34.73% |
| Unseen device naive | 13,887 | 3,322 | 23.92% | 46.29% |
| Unseen device, calibrated policy **with device gate bypassed** | 12,998 | 2,433 | 18.72% | 43.33% |

Selected margin>=0.22, quality<=1.0. Calibration: 2,169/6,000 issued, 3 false, simultaneous upper bound 0.5747%. A 500,000-clip independent Monte Carlo oracle estimated IID conditional risk 0.3618% (99.9% MC interval 0.3165–0.4114%). Oracle is not an exact population risk.

Across 100 independently seeded calibrations, 97 were **definitely covered** relative to all 32 oracle 99.9%-CI upper endpoints, 1 was a definite apparent failure, and 2 were unresolved at the oracle's MC precision. This satisfies the preregistered >=90/100 gate, but does not prove exact finite-sample coverage empirically.

Independent checks: 100 adaptive quadratures versus exact shutter integrals (maximum difference 4.44e-16), 42 binomial-tail inversions (maximum 3.73e-14), 3,000 reference samples, seven product-gate checks. The result file and reproducibility workflow compare exact JSON outputs.

## Prediction adjudication
P1 naive IID conditional error >2%: **passed**.
P2 IID calibrated conditional error <=2% with >=10% issuance: **passed**.
P3 unseen-device shift violates the selected risk target if transferred: **passed**.
P4 no hard physical guarantee and fail-closed missingness/timing/device gates: **passed in software only**.
P5 >=90/100 simultaneous-coverage repetitions: **97 definite passes, 1 definite failure, 2 MC-indeterminate**.

## Product consequence
The prototype returns ABSTAIN_NO_HUMAN_VALIDATION for all actual deployment until independent paired-human validation exists. Only after independent human calibration, verified device identity, exposure timing and optical domain qualification may it emit STATISTICAL_RISK_QUALIFIED; this is a population conditional-risk claim, not proof of absence of an unseen event. It abstains on unknown devices, timing, missing frames, invalid measurements or unsupported nuisance conditions. No fatigue, PERCLOS, or pupil-waveform claims.

## Priority audit
- Clopper and Pearson (1934), exact binomial confidence bounds, DOI: 10.1093/biomet/26.4.404.
- Geifman and El-Yaniv, *Selective Classification for Deep Neural Networks*, NeurIPS 2017, arXiv:1705.08500.
- Angelopoulos et al., *Learn then Test*, arXiv:2110.01052.
- Bates et al., *Distribution-Free, Risk-Controlling Prediction Sets*, arXiv:2101.02703.

This result is not publication-novel by itself. The world-class gate still requires prospectively predicted crossings in paired high-speed human/ordinary-RGB recordings, independently estimated velocity and optical transfer bounds, and untouched participant/device holdouts. See E002_386_HUMAN_STUDY.md.
