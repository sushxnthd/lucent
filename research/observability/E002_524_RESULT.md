# E002-524 | Sharp phase boundary for a high-speed reference closure witness

Date: 2026-10-29. Primary E002-371 kernel; existing `research/observability-human-boundary`, draft PR #26. [Frozen protocol](E002_524_FROZEN.md) committed first at `d7fb0b35fe71f660229bf284bda09e97dcc2ef94`.

**Evidence tier:** exact periodic sampling geometry, independent rational replay and prospective instrument design. **Not** a new general theorem, anatomical observation, calibrated camera, human validation or proof of population-level blink absence.

## New falsifiable instrument consequence

E002-519 requires reference exposure containment in the ordinary camera's **blind gap**, not necessarily in a continuous anatomical closure. E002-520/522 can certify a threshold crossing or positive total closure measure from a calibrated **partial-exposure mean**. The stricter E002-524 experiment asks when high FPS guarantees the *sufficient but not necessary* opportunity to capture one reference exposure wholly inside a continuous closure. See [Amendment A](E002_524_AMENDMENT_A.md); the original frozen protocol is preserved.

Let reference exposure intervals be `[phi+kP,phi+kP+e]`, with independently established start-to-start period `P`, shutter duration `0<e<P`, and unknown acquisition phase `phi`. A real continuous closure lasts `d`.

**Two distinct sharp boundaries:**

1. **Positive exposure overlap** for every phase occurs iff `d>P-e`. If `d<=P-e`, the event can fit entirely into a blind interval between exposures. Equality only touches an endpoint.
2. **Strict fully contained reference exposure** for every phase occurs iff `d>P+e`. Exposure starts must lie in the open interval `(0,d-e)`. A periodic start lattice with spacing `P` intersects every such interval iff its length exceeds `P`. At equality a phase can align exposure starts with both boundaries, so strict containment fails.

Thus a closure can overlap a high-speed camera's frames under *every* phase without guaranteeing even one entirely contained reference exposure. Overlap alone is not an anatomical witness, particularly under blur or exposure averaging.

With independently bounded start/end timing uncertainty `u` each, robust strict containment requires `d>P+e+2u`. If native frames may be missing, substitute the **largest independently verified retained start-time gap `G`** and a conservative maximum exposure width: `d>G+e_max+2u`, provided the closure is interior to the verified acquisition window. Without native provenance, measured clock and exposure calibration, this operational claim must abstain. A single global clock offset and independently varying endpoint errors have different nuisance structures; the `2u` condition is a conservative envelope, not a claim that their statistics are identical.

The dimensionless boundaries are `eta=d/P > 1-rho` for ideal positive overlap and `eta>1+rho` for ideal strict full witness, where `rho=e/P`. With `xi=u/P`, the robust strict full witness sufficient boundary is `eta>1+rho+2xi`. This is elementary sampling geometry, not original sampling theory.

## Frozen prospective numerical predictions

All values are **hypothetical**, not measured camera or human data.

| Reference design | Positive overlap guaranteed if d exceeds | Strict full witness guaranteed if d exceeds | Robust strict full witness if d exceeds |
| --- | ---: | ---: | ---: |
| 240 Hz, 1-ms exposure | 3.166667 ms | 5.166667 ms | 5.166667 ms (u=0) |
| 240 Hz, 1-ms exposure, 0.1-ms endpoint error | 3.166667 ms (ideal only) | 5.166667 ms (ideal only) | 5.366667 ms |
| 1000 Hz, 0.5-ms exposure | 0.5 ms | 1.5 ms | 1.5 ms (u=0) |
| 240 Hz, 1-ms exposure, one missing frame | Not established from original cadence | Not established from original cadence | 9.333333 ms (G=8.333333 ms, u=0) |

The 240-Hz/1-ms example has an entire interval from approximately 3.17 to 5.17 ms in which every phase overlaps a frame, but some phases still lack a fully contained reference exposure. This informs reference-camera speed and duty-cycle selection for **full-closure exposure opportunities**. It is **not** a minimum measurable blink duration: a calibrated partial-exposure quantitative witness can still falsify an exclusion under E002-520/522. A physically calibrated camera may have different exposure widths or rolling-shutter timing.

[Vector phase-censoring figure](E002_524_REFERENCE_WITNESS.svg) illustrates why an overlapping high-speed frame need not be a fully contained anatomical witness. The figure is hypothetical, not a source frame.

## Verification and adversarial checks

- [Exact-rational Python evaluator](e002_524_reference_sampling.py) constructs explicit counterexample phases at and below both boundaries, distinguishes overlap from strict containment, and requires explicit externally verified maximum native-frame gap for any conditional operational conclusion.
- [Seventeen adversarial Python tests](test_e002_524_reference_sampling.py) passed locally: boundary equality, 257 rational phases just above each boundary, 0.1-ms timing uncertainty, dropped-frame sensitivity, invalid acquisition, and fail-closed evidence flags.
- [Independent Node.js BigInt replay](e002_524_independent_replay.cjs) passed locally. It independently checks exact rational thresholds, equality counterexamples and 257 phases. Independent arithmetic is not independent hardware validation.
- [Hosted CI workflow](../../.github/workflows/e002_524_reference_sampling.yml) was added. Hosted completion must be checked separately; do not claim a hosted pass from local tests.

## Human/physical study acceptance consequence

Before inspecting held-out reference anatomy, measure exposure starts and durations with an independent optical clock, verify native indices, characterize rolling-shutter row timing and missingness, and preregister the reference-witness sensitivity envelope. Freeze ordinary-camera EXCLUDE/ABSTAIN gaps before two genuine blinded human raters inspect high-speed reference anatomy. Require cross-camera scale/brightness/geometry, gaze, glasses, blur, exposure integration and uncertainty containment. A valid cross-camera-contained anatomical witness, including a calibrated **partial-exposure** quantitative witness under E002-520/522, can falsify a specific exclusion. A full-closure exposure is one stronger sufficient case, never a mandatory prerequisite. **An apparently open or phase-censored reference sequence never verifies no hidden blink.** No reference-camera sensitivity bound supplies the missing hard human eyelid-velocity ceiling.

The eight-person pilot is suitable for finding counterexamples, not for claiming a 1% participant-session risk bound. E002-509's separate statistical conditions still apply.

**Completion evidence:** independent human S01 ratings 0; authenticated physical shutter captures 0; certified continuous-time eyelid-speed upper bounds 0; participant-disjoint physical predictions 0. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. No merge, deployment, schedule change or claim of empirical human validation. Next decisive evidence remains real blinded S01 anatomy and independently calibrated optical capture, not more synthetic shutter sweeps.
