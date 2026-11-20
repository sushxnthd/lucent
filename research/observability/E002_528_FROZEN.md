# E002-528 | Frozen randomized-phase reference-witness sensitivity experiment

Date: 2026-10-29. Primary E002-371 kernel. Existing branch `research/observability-human-boundary`, draft PR #26. Freeze this prediction **before** implementing the evaluator, tests, or reading their results. This is a conditional instrument-design experiment, **not** a human measurement or physical calibration.

## New question and scientific information

E002-524 gives an adversarial *every-phase* threshold. A pilot can still have substantial, but incomplete, opportunity to observe a real closure below that threshold. Determine the **exact randomized-phase detection-opportunity probability** and quantify how phase locking destroys it. This affects the number of independent *instrument opportunities* needed, not the number of independent human participants or the probability of blink absence.

Let periodic reference exposure intervals be `[phi+kP, phi+kP+e]`, with `P>e>0`, `phi` uniform on `[0,P)`, event closure `(0,d)`, and independently bounded start/end timing uncertainty `u>=0` on each side. Strict robust full containment requires some start `a` with `a-u>0` and `a+e+u<d`. No anatomical labels, shutter response integration, velocity cap, or camera provenance are assumed.

## Predictions frozen before code

1. For **uniform independent phase**, robust strict full-exposure opportunity has probability `p_full = clamp((d-e-2u)/P, 0, 1)` (endpoints of zero measure ignored). Ideal positive-overlap opportunity is `p_overlap = clamp((d+e)/P, 0, 1)` when `d>0`. Overlap is not an anatomical closure witness.
2. For `P=25/6 ms`, `e=1 ms`, `u=1/10 ms`, `d=4 ms`: `p_full=84/125=0.672`, `p_overlap=1`. At `d=3 ms`, `p_full=54/125=0.432`; at `d=5 ms`, `p_full=114/125=0.912`. For `P=1 ms`, `e=1/2 ms`, `u=0`, `d=6/5 ms`: `p_full=7/10`.
3. For exactly three **independent uniform phase trials** with d=4 ms, probability of at least one opportunity is `1-(1-84/125)^3`; without verified independent randomization this formula must not be used.
4. If the actual phase law differs from uniform by total-variation distance at most `epsilon`, then the witness-opportunity probability lies within `[max(0,p_full-epsilon), min(1,p_full+epsilon)]`. If no bound on phase distribution exists and `p_full<1`, a phase-locked source can produce zero opportunities. Even when `p_full=1` at exact equality, an adversarial point mass on the boundary can defeat **strict** containment; every-phase guarantees require the strict E002-524 inequality `d>P+e+2u`.
5. Nuisance gates: unknown native-index continuity, shutter width, rolling-shutter row, independent clock, optical calibration, closure duration, exposure weighting, cross-camera geometry, gaze, brightness, glasses, blur, or occlusion => `ABSTAIN_UNCALIBRATED`. The program computes **design probabilities only**, never certifies a measured event or absence of hidden closure.

## Falsification tests frozen before code

- Exact rational arithmetic with boundary cases `d=e+2u`, `d=P+e+2u` and phase-lock counterexample; reject invalid/nonfinite/negative inputs and invalid phase-provenance flags.
- Independently enumerate 10,000 evenly spaced phases for predeclared rational cases; exact fractions should match to within `1/10000` grid resolution (endpoint caveat).
- A separate implementation must reproduce the 240-Hz, 1000-Hz and three-trial numbers without importing the Python evaluator.
- Hold-out cases after implementing: 240 Hz with `d=5 ms`, and 1000 Hz with `d=6/5 ms`.
- If any empirical simulation contradicts the formula beyond the grid endpoint tolerance, retain the failure and do not authorize operational sensitivity.

## Practical instrument consequence

Before anatomical review, independently randomize or measure closure-onset phase relative to high-speed acquisition, retain native-frame indices, calibrate exposure and timing at the relevant sensor row, and preregister the phase law and admissible missingness. A positive reference witness can falsify a frozen ordinary-camera exclusion only after independent anatomy and cross-camera calibration. An absent witness, even after many trials, never verifies no closure without a separately established sensitivity model. A pilot of eight adults is for failure discovery, not universal velocity-cap certification.

Evidence tier: **exact synthetic instrument opportunity**. No new physical/human observations. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. Hush PR #45 unchanged.
