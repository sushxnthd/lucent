# E002-528 | Randomized-phase reference-camera witness sensitivity

Date: 2026-10-29. Primary E002-371 kernel; existing `research/observability-human-boundary`, draft PR #26. **Frozen before evaluator/tests:** [E002_528_FROZEN.md](E002_528_FROZEN.md), commit `322e63cf99ddd4db2b45e1b1cd7fa9ff7ebbc386`.

**Evidence tier:** exact conditional instrument-design geometry, deterministic synthetic phase enumeration, independent BigInt arithmetic. **No new human observations, independently measured shutter, authenticated clock, actual phase randomization, or validated human speed cap.**

## New question answered

E002-524 established a worst-case guarantee: a periodic reference camera captures a strictly fully contained exposure for *every* phase only if `d > P + e + 2u`. E002-528 quantifies the weaker, distinct claim of **opportunity probability** when event onset is genuinely uniform relative to the reference acquisition phase.

Let `P` be exposure-start period, `e` the exposure width, `u` an independent conservative bound on each exposure endpoint, and `d` the true continuous closure duration. Robust strict full containment requires an exposure start in the open interval `(u, d-e-u)`. For a uniform random lattice offset `phi in [0,P)`, the exact probability is:

`p_full = clamp((d-e-2u)/P, 0, 1)`.

The ideal positive-overlap probability is `p_overlap = clamp((d+e)/P, 0, 1)` for `d>0`. Overlap is **not** a sufficient anatomical witness. These are elementary sampling-geometry laws, not newly discovered general mathematical theorems.

## Frozen and held-out predictions

All durations and camera parameters below are **hypothetical**, not physical measurements.

| Reference design and real closure | Strict full-exposure opportunity | Positive overlap |
| --- | ---: | ---: |
| 240 Hz, e=1 ms, u=0.1 ms, d=3 ms | 54/125 = **43.2%** | 96% |
| 240 Hz, e=1 ms, u=0.1 ms, d=4 ms | 84/125 = **67.2%** | 100% |
| 240 Hz, e=1 ms, u=0.1 ms, d=5 ms (held-out) | 114/125 = **91.2%** | 100% |
| 1000 Hz, e=0.5 ms, u=0, d=1.2 ms (held-out) | 7/10 = **70%** | 100% |

For **three genuinely independent** randomized-phase 4-ms opportunities, the chance of at least one strict fully contained exposure is `1-(41/125)^3 = 1884204/1953125 = 96.4712448%`. This is **not** three independent human participants, not three anatomical detections, and not a claim that the reference missed no blinks. Without externally attested independent randomization, the evaluator returns no repeated-trial probability.

An independently justified total-variation phase-law deviation of at most 0.1 changes the single-opportunity 4-ms probability from 0.672 to a bound **[0.572, 0.772]**. With **no** phase-distribution guarantee, phase locking can force zero opportunities for a 4-ms closure. At the exact `d=P+e+2u` equality, a uniform phase has probability 1 but a point-mass adversarial phase can still defeat *strict* containment. E002-524's every-phase threshold remains strict `>`.

## Verification and preserved negative control

- [Exact-rational Python evaluator](e002_528_phase_sensitivity.py) and [20 adversarial tests](test_e002_528_phase_sensitivity.py) passed locally, including frozen, held-out, 10,000-phase enumeration, exact equality, phase lock, nonfinite input rejection, independence abstention, and product fail-closed behavior.
- [Independent Node.js BigInt replay](e002_528_independent_replay.cjs) passed locally. The separate numerical 10,000-phase grids observed 4319/10000, 6719/10000, 9119/10000, and 6999/10000 strict witnesses, respectively, all within one grid point of the exact fractions. Grid endpoints are excluded by strict inequalities.
- **Negative control preserved:** an initial JavaScript floating-point strict-equality assertion at `d=P+e+2u` returned a false positive because binary rounding made a boundary appear interior. The replay now uses independent exact BigInt rational comparisons at equality. Do not use floating-point boundary comparisons to certify a physical witness.
- [Dedicated CI workflow](../../.github/workflows/e002_528_phase_sensitivity.yml) runs both implementations and CLI JSON smoke test. Hosted success must be checked separately; no hosted success is claimed here.

## Direct human-study and product consequence

A reference camera can have **100% exposure overlap** yet only **67.2% strict full-exposure opportunity** for a hypothetical 4-ms closure. This distinction matters when designing the prospective E002-519 eight-person pilot: predeclare reference sensitivity and independent phase randomization, physically measure exposure and clock at the relevant row, retain native-frame indices, record missingness and optical-response calibration, and blind two real anatomical raters. Phase-locking, unknown rolling-shutter geometry, blur, brightness, gaze, glasses, exposure integration and cross-camera transport each require independent controls. This result cannot repair a missing hard human velocity bound.

**No observed closure in the reference does not verify that an ordinary-camera gap was closure-free.** A genuine cross-camera-calibrated anatomical closure witness inside a frozen EXCLUDE gap can falsify that specific exclusion. No sample-size or phase-averaged sensitivity claim is authorized from the present synthetic work.

**Physical study gates remain open:** independent S01 human raters 0; authenticated physical shutter/clock captures 0; certified continuous-time human eyelid-speed ceilings 0; participant-disjoint physical predictions 0. Lucent `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. Do not add another phase theorem refinement unless new physical data or a falsifying nuisance measurement appears. Hush PR #45 was not modified in this run.
