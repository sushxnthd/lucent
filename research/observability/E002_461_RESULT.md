# E002-461 — nonlinear shutter calibration counterexample and conservative repair

**Date:** 2026-10-26. **Frozen before implementation:** [E002_461_FROZEN.md](E002_461_FROZEN.md), commit `084589c39b92811ad16fdd2db97d67e93ea503c3`. **Evidence tier:** exact synthetic/instrument-model counterexample, mathematical variance bound, independent seeded arithmetic replay; **NO new human anatomical trajectory, physical camera acquisition, or physiological velocity validation**.

## New scientific information: static calibration can give a false exclusion

The exact E002-460 directional shutter-centroid law requires shutter-averaged *linear anatomical aperture in millimetres*. It is **not** licensed merely because a camera feature has an exact static inverse to aperture.

Take a nonnegative aperture `a(t)`, a perfectly calibrated but nonlinear feature `g(a)=a²`, and an ideal uniform shutter returning `q=E[g(a(T))]=E[a(T)²]`. Applying static calibration after integration returns `sqrt(q)`, whereas the theorem needs `m=E[a(T)]`. For any nonconstant trajectory `sqrt(E[a²]) > E[a]`. Thus the static inverse systematically overstates aperture in this model and can spuriously certify an impossible hidden closure.

The preregistered witness has an actual synthetic dark-gap threshold crossing at **t=2.083333 ms** between two nonoverlapping 2.3-ms shutters separated by **4.166667 ms** (240-fps nominal cadence). The closing/opening rates are 99% of hypothetical assumed caps of 567.103928 and 274.616337 mm/s. These numbers are borrowed from a published human *sample maximum* solely to define the synthetic case, not to claim a physiological hard cap.

| Frozen synthetic measurement | Value |
|---|---:|
| True shutter-averaged first aperture | 3.169652 mm |
| True shutter-averaged second aperture | 2.566396 mm |
| Quadratic sensor output q0 | 10.185647 mm² |
| Quadratic sensor output q1 | 6.618973 mm² |
| Invalid static-inverse critical gap | **4.186606 ms** |
| Actual frame-centroid gap | **4.166667 ms** |
| Corrected conservative critical lower bound | **4.046426 ms** |

**Falsification:** the invalid static-inverse rule returns `EXCLUDED_CONDITIONALLY` despite a constructed, fully witnessed dark-gap closure. The frozen 95%-speed negative control does not produce that false exclusion. This falsifies **the unlicensed observation-model substitution**, not the E002-460 theorem.

## Conservative dynamic-sensor repair

For any random shutter time `T` and aperture with Lipschitz speed limit `L=max(C,O)`, the pairwise-variance inequality gives `Var(a(T)) <= L² Var(T)`. Under a uniform shutter of width `w`, `Var(T)=w²/12`. Therefore, if the sensor genuinely measures calibrated `q=E[a²]` with absolute uncertainty `u`, then

```
mean_aperture_lower = sqrt(max(0, q-u-L²*w²/12)).
```

Using **these lower bounds** in the *necessary* directional dark-gap crossing inequalities cannot exclude an actual crossing when the stated assumptions hold. This is a conservative conditional veto, not a sharp new physical law, a positive closure witness, or a certification for arbitrary RGB features.

For the frozen counterexample the repaired rule returns `NOT_EXCLUDED`, avoiding the false certificate. Increasing certified sensor uncertainty cannot strengthen an exclusion. Unauthenticated kernel, clock, transfer, cap provenance, brightness, geometry, missingness, blur, gaze, glasses, sampling or rolling shutter returns `ABSTAIN_UNCALIBRATED`. Every result includes `physical_certification:false`.

## Independent reproduction and nuisance controls

- [Python evaluator](e002_461_quadratic_shutter.py) implements the conservative lower-bound rule and explicit fail-closed nuisance checks.
- [Python adversarial suite](test_e002_461_quadratic_shutter.py) freezes the primary/negative controls, invalid-model rejection, metadata and uncertainty checks, and 10,000 seeded exact affine dark-gap witnesses. **Hosted run 40305495877 PASSED all 9 Python tests**, including 10,000 exact synthetic witnesses: **13 naive false exclusions, 0 corrected false exclusions**.
- [Independent JavaScript replay](e002_461_independent_replay.cjs) uses its own arithmetic and seeded generator, without importing Python. **Independent V8 execution of the frozen equations:** 9/10,000 synthetic witnesses were falsely excluded by static inversion; **0/10,000** were excluded by the corrected variance-aware rule. These are deliberately constructed witnesses, not human error rates. Primary critical intervals reproduced to 4.186606 ms (naive) and 4.046426 ms (corrected).
- [Vector figure](E002_461_FIGURE.svg) illustrates the witnessed closure, shutter windows, and opposing decisions.
- [CI workflow](../../.github/workflows/e002_461_quadratic_shutter.yml) runs the actual Python suite, independent Node replay, and explicit research-only examples. **Hosted run [40305495877](https://github.com/sushxnthd/lucent/actions/runs/40305495877) completed successfully** on the committed evaluator/test/replay/workflow head. All 9 Python adversarial methods, independent Node replay, and reproducible primary examples passed. Its Python PRNG produced **13/10,000 naive false exclusions**, while the independent JS PRNG produced **9/10,000**; both produced **0/10,000 corrected false exclusions**. These are synthetic witnesses, not human evidence.

The JS randomized sample and Python seeded sample use different PRNGs, so exact false-exclusion counts need not match; both must have zero corrected false exclusions. This does not establish safety for unmodeled transfer functions or sensor noise.

## Novelty and priority boundary

This is a concrete, prospectively frozen **model falsification and measurement/product veto**. Jensen's inequality, the Lipschitz variance bound, shutter integration, and bounded-speed reachability are classical mathematics. E002-421/422 and E002-460 already cover linear aperture-mean boxcars and centroid conditions. Do not present E002-461 as a newly discovered universal theorem or as real human validation.

**Product consequence:** Even perfect *static* feature-to-aperture calibration is insufficient to authorize E002-460's dark-gap exclusion on shutter-integrated nonlinear features. Either independently validate the *dynamic shutter forward model* and conservative inversion under nuisances, or abstain. This is directly relevant to image-feature/landmark pipelines, but the quadratic model itself is a hypothetical stress test, **not a demonstrated law of a real RGB camera**.

## Decisive next step and release gate

The [instrument/human study protocol](E002_461_INSTRUMENT_STUDY.md) specifies a moving-aperture phantom with authenticated timing and blinded dynamic-transfer tests, followed by E002-456's independently annotated, participant-disjoint human reference challenge. No such physical study was run here. Do not continue algebraic refinement instead of obtaining these measurements.

**E002-371 physical validation: NOT_ESTABLISHED.** No deterministic hidden-closure guarantee, blink duration, PERCLOS, fatigue or medical claim. Product remains `ABSTAIN_UNCALIBRATED`; no merge/release; S21/S22 sealed. Hush's separate PR #45 untouched.
