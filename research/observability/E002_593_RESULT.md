# E002-593 | A prospective synthetic camera-gap stress test exposes nominal-certification false exclusions

**Date:** 2026-11-01 UTC. **Kernel:** E002-371. **Evidence tier:** deterministic synthetic-oracle test, integer arithmetic, two independently implemented runtimes; **no human or physical camera validation**. See [frozen reproduction and physical handoff](E002_593_FROZEN.md). The generator was explored locally before the GitHub freeze, so these results must NOT be described as preregistered human validation.

## New empirical synthetic result
A 12,000-scenario virtual shutter experiment concentrates synthetic triangular eyelid trajectories around the E002-371 sharp boundary. Each has a known true minimum aperture and true shutter gap, but the simulated ordinary-camera measurements have independently bounded endpoint errors (up to 0.020 normalized aperture) and timing errors (up to 1.5 ms). The exclusion decision uses the *observed* endpoints and gap, with or without robust error allowances. All truth labels come from the synthetic oracle, not from human raters.

| Metric | Exact synthetic count |
|---|---:|
| Total scenarios | 12,000 |
| True hidden closure (threshold reached) | 5,927 |
| True no closure | 6,073 |
| Naive nominal exclusions | 6,155 |
| **Naive false exclusions** | **873** |
| Robust bounded-error exclusions | 1,769 |
| **Robust false exclusions** | **0** |
| Oracle exclusions with true parameters | 6,073 |

In this deliberately boundary-enriched synthetic distribution, **873/6,155 (14.18%) nominal exclusions were false**, while the robust rule emitted 0/1,769 false exclusions and abstained in 10,231/12,000 cases. Among the 6,073 truly closure-free scenarios, it certified 1,769 (29.13%). These are synthetic distribution-specific counts and must not be presented as real-camera false-negative rates, calibration coverage, confidence intervals, or population estimates.

## Exact decision law and sharp counterexample
For observed endpoint aperture values aL,aR, measured blind gap gObs, independently certified upper eyelid velocity V, endpoint error <=eps and gap error <=delta, exclusion is allowed only if

`V*(gObs+delta) < (aL-eps)+(aR-eps)-2*tau`.

Strict equality abstains. The rule is sufficient only under the stated Lipschitz, anatomical-aperture and shutter-support premises. It does not identify the closure status when it abstains. The synthetic generator's true closure is an explicit symmetric V-Lipschitz tent reaching the threshold when r>=1000.

At c=0.5, tau=0.1, true gap 20 ms, r=1, observed gap 18.5 ms, and observed endpoints 0.52, the robust rule is exactly at equality and abstains. If actual endpoint errors are +0.030 while the software incorrectly assumes <=0.020, observed endpoints 0.53 produce a **false exclusion even under the robust rule**. This is a concrete falsification of any robustness claim without externally verified nuisance envelopes.

## Verification and nonclaims
Local Python and independently written Node BigInt replay matched **all eight** aggregate fields exactly. Both included strict-equality abstention and out-of-bound endpoint-error adversarial controls. [Python implementation](e002_593_virtual_shutter.py), [independent Node replay](e002_593_independent_replay.cjs), and [hosted cross-language workflow](../../.github/workflows/e002_593_virtual_shutter.yml) are committed. Hosted CI success is **not yet verified** at report creation.

This experiment supplies an independently reproduced **synthetic instrument substitute**, not an independent human or physiological validation. It does not certify a physical shutter model, real rolling-row exposure, actual eyelid velocity ceiling, high-speed reference sensitivity, or product-level fatigue measurement. The true V is an oracle-provided simulation parameter; it was not estimated from real humans. No independent human rater pair, photodiode-calibrated physical capture, or held-out physical prediction was obtained.

## Product and next decisive study
Never certify absence of hidden closure from nominal camera timestamps, nominal endpoint aperture, or a velocity inferred solely from sampled frames. Missing or unverified aperture/geometry, shutter/clock, brightness/contrast, blur, gaze, glasses, missingness or independently justified continuous-time velocity evidence must return `ABSTAIN_UNCALIBRATED`. The numerical robust classifier must not be surfaced as a real-world certificate until those premises are externally verified.

The next study is frozen in E002_593_FROZEN.md: independently photodiode-calibrated shutter and rolling-row supports; synchronized high-speed and ordinary-camera imaging; two blinded anatomical raters; participant-disjoint calibration and holdout; prospective strict exclusion predictions; and participant-clustered false-exclusion/abstention reporting. Any confirmed closure in a certified-exclusion gap falsifies the relevant assumptions or implementation. Reference camera temporal sensitivity must be independently bounded.

**Production BLOCKED; PR #26 remains draft and unmerged.** Hush workstream not modified by this primary experiment.
