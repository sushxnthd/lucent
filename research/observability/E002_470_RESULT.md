# E002-470 RESULT — end-to-end moving-aperture instrument surrogate

**Date:** 2026-10-27. **Evidence tier:** prespecified deterministic **synthetic** continuous-aperture oracle plus a research-gate adversarial challenge. **Not** physical instrument validation, human anatomical measurement, or a physiological velocity-cap estimate. [Frozen protocol](E002_470_FROZEN.md) committed first at `c93b74d08ee110d4a4a64e1e0843897278bef730`.

## Scientific question and execution

The existing E002-456 evaluator was challenged with exact shutter means of continuous V-shaped apertures, a(t)=m+s|t-p|. An independent analytic geometric oracle determines whether the true aperture is below 2.0 mm anywhere in the camera's **unexposed** interval. The generator uses the frozen 250-mm/s *illustrative* Lipschitz limit and no physiology or human-derived hard cap. Exact analytic shutter integration was checked against separate dense trapezoidal quadrature.

The 12,000-case frozen matrix crosses 30/60/120/240 fps with 0.5/1.5-ms exposures, 1,500 cases per cell, seed 470371. A local faithful stand-in of E002-456's relevant arithmetic was executed because the GitHub source is not mounted locally. **Actual repository evaluator verification is pending in [hosted CI](https://github.com/sushxnthd/lucent/actions/runs/40398705563)**; do not treat local stand-in success as hosted confirmation.

### Local deterministic outcomes (pending hosted replay)

- 12,000 constructed clean continuous-aperture trajectories; 3,919 had a strictly subthreshold minimum in the unexposed gap.
- Conditional exclusion on 2,663 trajectories; 9,337 not excluded; **0 clean false exclusions and 0 unexpected abstentions** in the local stand-in.
- 12 independent numerical shutter-integration controls; maximum absolute discrepancy **4.78e-10 mm**.
- Exclusion counts by fps at 0.5/1.5-ms exposure: 30 fps **155/138**, 60 fps **228/230**, 120 fps **399/343**, 240 fps **614/556**. These are counts under a deliberately arbitrary synthetic trajectory distribution, **not** human certification rates or camera benchmarks.

### Nine prespecified calibration-fault challenges

A separate continuous trajectory has an actual dark-gap minimum of **1.99 mm**, below the 2.00-mm threshold. With correct readings the existing conditional gate returns `NOT_EXCLUDED`. Under a *wrongly self-attested* PASS, all nine prespecified perturbations yielded false conditional exclusion in the local arithmetic replay: 3% geometry scale inflation; +0.075-mm apparent-aperture bias attributed separately to brightness, blur, gaze, glasses and missingness; or +0.65-ms unreported frame separation attributed separately to sampling, clock and rolling-shutter errors.

For the same nine inputs, changing the corresponding nuisance flag to `FAIL` produced **9/9 ABSTAIN** outcomes. This demonstrates the sensitivity of a **conditional** decision to nuisance-calibration provenance; it does **not** show a flaw in E002-371's mathematical theorem, nor does it imply any actual camera exhibits these fault magnitudes. A self-reported PASS is not independent physical verification. In particular, the model's `ILLUSTRATIVE` velocity cap cannot authorize a product exclusion.

## Falsification decision

- Under the restricted piecewise-linear, symmetric-boxcar and correctly bounded synthetic assumptions, the frozen test did **not** find a conditional-exclusion counterexample. That is a negative simulator result, not independent confirmation of real-world validity.
- Every prespecified misdeclared nuisance world *did* generate a wrong conditional exclusion. Every explicit nuisance FAIL forced abstention. These are instrument-surrogate stress cases with a direct fail-closed product implication.
- **Physical acquisitions: 0. New human anatomical labels: 0. Verified physiological hard caps: 0. Independently authenticated shutter/encoder timing: 0.** No statistical confidence about human closure rates is warranted.
- E002-469's one-shot S19 timing stop remains in force. Do not re-open timestamp archaeology or the sealed S21/S22 participants.

## Reproduction and next decisive evidence

- [Executable synthetic camera and independent analytic aperture oracle](e002_470_bench.py).
- [Twelve adversarial/unit checks](test_e002_470_bench.py).
- [Dedicated hosted replay](../../.github/workflows/e002_470_bench.yml), running the **actual** E002-456 evaluator, not the local stand-in.
- Freeze and perform **real physical acquisition** next: independently timed optical pulse through the actual camera imaging path, moving aperture with independent position reference, uncertainty-bounded shutter/encoder response and held-out phases; then prospectively test E002-371 against human anatomical trajectories with independently justified velocity bounds. No more synthetic instrument-model elaboration unless a new physical result motivates it.

**Release decision:** `ABSTAIN_UNCALIBRATED` for hidden-closure guarantees, blink duration, PERCLOS, fatigue and medical claims. Keep PR #26 draft/unmerged. This result changes neither Hush's branch nor PR #45.
