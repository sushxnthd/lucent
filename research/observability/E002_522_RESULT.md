# E002-522 | Calibrated shutter-response concentration rescues a conditional physical-time bound

Date: 2026-10-29. Primary E002-371 scientific kernel, branch `research/observability-human-boundary`, draft PR #26. Protocol [E002_522_FROZEN.md](E002_522_FROZEN.md) was committed first (`aadb0cf9`). **Evidence tier: exact mathematical implication, synthetic adversarial instrument-response replay, and conditional offline software; no physical camera or human measurements.**

## Question and new falsifiable instrument law

E002-521 rejected nonuniform exposure weighting because arbitrarily concentrated response destroys any positive *physical-time* bound. That refusal is necessary if response concentration is unbounded, but is overly restrictive when a sensor's temporal response envelope can be independently calibrated.

Let a reference exposure E have physical duration T>=T_min>0, contained in the ordinary-camera guaranteed blind interval under all calibrated timing uncertainties. Let the nonnegative temporal weighting q satisfy integral_E q(t)dt=1 and q(t)<=R/T almost everywhere for a **measured conservative** R>=1. Let physical ordinary aperture a_o(t) lie in [0,1] and have transported weighted mean integral_E q(t)a_o(t)dt <= M=K U+B, with K,B>=0 and an independently measured reference weighted-mean upper U. Fix threshold 0<theta<1. Let C={t in E:a_o(t)<=theta}.

On E minus C, a_o(t)>theta. Therefore

```
M >= integral_E q*a_o >= theta * integral_(E minus C) q
=> integral_C q >= 1 - M/theta
<= (R/T) * measure(C).
```

When **M<theta**, the dimensionless law and physical-time implication are

```
measure(C)/T >= (1 - M/theta)/R
measure(C)   >= T_min * (1 - M/theta)/R.
```

No universal human velocity ceiling is assumed. This is a total closure measure in **one** independently contained reference exposure, not a contiguous blink or an exclusion of other hidden closures. The result is sharp as an infimum without a derivative constraint: choose a=0 on a fraction p_e=(1-M/(theta+epsilon))/R and a=theta+epsilon elsewhere; q=R/T on the closed set and constant q_out=(1-R*p_e)/(T*(1-p_e)) elsewhere. This q is normalized and <=R/T for R>=1. The weighted mean equals M; p_e decreases to (1-M/theta)/R as epsilon->0. The result is an elementary bounded-density/measure inequality, **not claimed as a new general mathematical theorem**.

## Frozen numerical reversals

| Condition (hypothetical) | Physical-time lower bound |
|---|---:|
| theta=.20, M=.19, T_min=8ms, uniform R=1 | 0.4 ms |
| Same, calibrated nonuniform R=2 | 0.2 ms |
| Same, R=100 | 0.004 ms |
| Same, R unknown/unbounded | **No positive bound** |
| Same, M>=theta | **No positive bound** |

The R=100 adversary demonstrates why assuming uniform response can overstate the lower bound by 100x. For 100 equal physical-time cells, let q concentrate all weight on one cell, a=0 there, and a=.21 in the other 99. The weighted mean is 0 and the actual closed fraction is 1/100. A falsely assumed R=1 would infer a closed fraction >=1, which is wrong; the actual R=100 recovers 1/100.

## Reproducible synthetic checks and falsification status

- [Exact-rational offline evaluator](e002_522_weight_cap.py) requires an explicit concentration cap and separate shutter nonnegativity, normalization, radiometry, clock, geometry, native-sequence, nuisance and independent-rater attestations. These booleans are **not independently authenticated by the program**. It never produces a no-hidden-closure certificate or a product release.
- [Python adversarial tests](test_e002_522_weight_cap.py) cover R=1,2,100, strict margin, equality, missing or invalid R, every evidence gate, timing containment, impossible exposure duration, reference censoring, duplicate IDs, near-threshold exactness, sharpness and a counterexample to false uniformity. They also test 5,000 frozen seeded piecewise-constant instrument-response models by direct weighted integration. An independent local arithmetic recomputation found **4,776** of 5,000 with M<theta and **zero bound violations**.
- [Independent Node.js BigInt replay](e002_522_independent_replay.cjs) uses a different deterministic RNG and exact integer cross-multiplication over another 5,000 synthetic response models, and checks frozen rational examples and sharpness. [Synthetic CLI fixture](E002_522_SYNTHETIC_EXAMPLE.json) is explicitly hypothetical.
- [Hosted workflow](../../.github/workflows/e002_522_weight_cap.yml) runs Python, Node.js and the fail-closed CLI fixture. Hosted completion must be checked separately before asserting CI success.

These are synthetic *instrument models*, not photodiode-measured response functions, physical shutter data, high-speed eyelid videos, or participant-disjoint human predictions. No claim of measured 30-Hz camera performance is supported.

## Direct product and physical-study consequence

A nonuniform temporal shutter is **not automatically unmeasurable**: a physically attested upper response concentration R could support a smaller, conditional total-closure-time bound. However, nominal FPS, average exposure time, an LED image alone, and a software boolean cannot establish R. A real instrument experiment must measure the per-row/per-pixel temporal impulse response with an independently timed light source and photodiode, bound radiometric nonlinearity, brightness saturation and blur, verify synchronization/clock drift and native indices, and transport aperture geometry across cameras under gaze, glasses, occlusion and head motion. Unknown or unbounded response concentration, nonlinearity, lost native frames, untrusted timebases or insufficient anatomy must force **UNKNOWN/ABSTAIN**.

No real R has been calibrated, so the existing product must **not** enable this inference. Independent S01 anatomical ratings: 0; authenticated physical shutter/clock captures: 0; certified human continuous-time speed caps: 0; held-out participant-disjoint physical predictions: 0. The next decisive experiment remains the blinded S01 review and independently clocked physical capture specified in [E002-519](E002_519_HUMAN_STUDY_HANDOFF.md). Further purely synthetic shutter sweeps should not be pursued.

**Lucent product: `ABSTAIN_UNCALIBRATED`; release: `BLOCKED`. Draft PR stays unmerged. Hush unchanged.**
