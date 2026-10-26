# E002-472 RESULT — prospective camera feasibility, reference-gap rejection and physical handoff

**Date:** 2026-10-27. **Evidence:** preregistered algebraic design sensitivity, independent exact-rational arithmetic, executable synthetic gate, actual E002-456 cross-check, and physical/human study handoff. **No physical instrument acquisition and no new human anatomical measurement.** [Frozen protocol](E002_472_FROZEN.md) was committed before implementation at `f37ef11e914ec1a72ccdcfcab038079c5d14775a`.

## Quantitative design result
For the *specified symmetric endpoint* configuration with each shutter mean 1.0 mm above a closure threshold, each aperture uncertainty 0.1 mm, ordinary clock bound 0.1 ms, and a uniform symmetric shutter, the critical **hypothetical** velocity cap is
`Vcrit = 900 / (w/4 + (1000/fps+0.2)/2)` mm/s, with `w` in milliseconds. Strict exclusion is possible in the ideal declared model only when `V<Vcrit`. This is a consequence of the existing E002-456 conservative sufficient envelope, not a new physiological law or a necessary bound for unequal endpoints.

| Nominal fps | Exposure 1 ms | Exposure 4 ms | Exposure 8 ms |
|---|---:|---:|---:|
| 30 | 52.89 | 50.66 | 47.96 |
| 60 | 103.65 | 95.41 | 86.26 |
| 120 | 199.26 | 170.89 | 143.62† |
| 240 | 369.86 | 282.72‡ | not possible |

Values are critical illustrative velocities in mm/s, **not** human speed measurements. †At 120 fps / 8 ms, the reference exposure plus timing bounds cannot fit in the dark gap. ‡At 240 fps / 4 ms, no guaranteed dark gap exists once the 0.1-ms ordinary clock uncertainty is included; the numerical threshold is a formal sensitivity value, **not** an admissible joint validation design. [Vector figure](E002_472_FEASIBILITY.svg) shows this distinction.

**Decisive product-design consequences:**
- At 30 fps / 4-ms exposure, the stated 1-mm margin cannot support conditional exclusion under even an **illustrative** 100-mm/s velocity cap; a numerical 50.66-mm/s cap would be needed. Since no defensible physiological hard cap has been authenticated, this is a **design rejection**, not a statement about actual blinks.
- At 240 fps / 1-ms exposure, the *model* can conditionally exclude for an illustrative 200-mm/s cap (critical 369.86 mm/s), but still cannot make a physical claim without shutter, mm geometry, reference timing, and external velocity validation.
- Faster nominal fps is not sufficient: 240 fps / 4-ms exposure has no guaranteed dark gap at the frozen clock tolerance. Product configuration selection must depend on **exposure support and timing uncertainty**, not advertised fps.

## Frozen grid and independent verification
The preregistered 11 exposure/frame configurations times 4 hypothetical velocities produce **44** design rows: **13 conditionally feasible**, **23 unsupported**, and **8 abstain** due to missing dark-gap/reference support. The 8 abstentions correspond to 120-fps/8-ms and 240-fps/4-ms at all four hypothetical velocities. The exact-rational independent calculation reproduced the critical velocities and geometric gate outcomes. The Python evaluator [e002_472_design_feasibility.py](e002_472_design_feasibility.py) emits only `ABSTAIN_UNCALIBRATED` as product claim, and [12 adversarial tests](test_e002_472_design_feasibility.py) compare all 36 admissible design rows to the actual E002-456 interval evaluator.

**Hosted verification:** The initial [E002-472 run 40414991088](https://github.com/sushxnthd/lucent/actions/runs/40414991088) exposed a **test expectation error**, not a model error: the test mislabeled 240-fps/4-ms as a reference-support failure when the stronger reason is that no guaranteed dark gap exists. Eleven tests passed and one failed. The expectation was corrected in commit `8e2a84ad872e173d3a4f89bf3e60902c332a1453`. The subsequent [run 40415070670](https://github.com/sushxnthd/lucent/actions/runs/40415070670) was queued at the final check; do **not** claim it green until logs confirm. The failure and repair are preserved rather than hidden.

## Concrete human/physical acquisition handoff
The [physical protocol](E002_472_PHYSICAL_HANDOFF.md) specifies an imaging-path optical phase scan (<=0.05-ms phase steps; >=20 repetitions per phase), independent detector sensitivity/dynamic response, a position-encoded moving aperture, uncertainty/clock/row-timing acceptance targets, blinded anatomical raters, participant-disjoint holdout, nuisance injection, and falsification criteria. It explicitly rejects smartphone nominal fps, trigger-only photodiode synchronization, missing-is-open interpolation, and empirical sample maxima as hard physiological limits. Borrowed instrumentation is a prerequisite; none was accessed in this run.

## Scientific status and release gate
E002-371's conditional mathematics remains intact, but **physical E002-371 validation remains NOT_ESTABLISHED**. The current result is a quantitative *negative feasibility finding* for selected camera settings and a frozen physical acquisition decision procedure. No human hard velocity limit, authenticated physical shutter support, independent anatomical labels, or external review has been obtained. All hidden-closure, blink duration, PERCLOS, fatigue and medical outputs remain `ABSTAIN_UNCALIBRATED`. Do not merge or release. Preserve Lucent draft PR #26 and Hush draft PR #45 on their respective branches.
