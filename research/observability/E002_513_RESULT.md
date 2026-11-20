# E002-513 | Long-span optical anchors do not certify a local shutter gap without a clock regularity bound

Date: 2026-10-29. Primary E002-371 branch, draft PR #26. [Frozen before implementation](E002_513_FROZEN.md) at commit `5e0dc2f`. Evidence tier: **exact synthetic two-world non-identifiability counterexample**. Not a human experiment, camera measurement, new general mathematical theorem, or a falsification of E002-506 *under its stated affine-clock assumption*.

## New scientific consequence

E002-506 found that two independently timed optical events separated by 300 frames can constrain an **affine** frame period tightly enough to permit a conditional shutter-gap exclusion. E002-513 asks whether the same long-span observations suffice for a **particular local gap** if the camera can vary its inter-frame interval. They do not.

The frozen worlds each have 301 native frame starts, no dropped or reordered frames, identical independently timed anchor observations at frame 0 (0 s) and frame 300 (10 s), and a hypothetical 10-ms global shutter. World A uses 300 uniform 1/30-s intervals. World B adds exactly 2 ms to the preregistered 150->151 interval and subtracts exactly 2/299 ms from each other interval. Both worlds have the **same anchor data**, the same mean 30-fps period, strictly increasing exposure starts and nonoverlapping 10-ms exposures.

Under the *same hypothetical* continuous-time eyelid-speed ceiling V=60/s, normalized exposure mean 0.999 +/-0.001, and threshold 0.20, the existing E002-373 scalar bound gives:

| Quantity | World A (affine) | World B (non-affine) |
| --- | ---: | ---: |
| Frame 0 optical anchor | 0 s | 0 s |
| Frame 300 optical anchor | 10 s | 10 s |
| Target interval 150->151 | 33.333333 ms | 35.333333 ms |
| Target blind gap with 10-ms exposure | 23.333333 ms | 25.333333 ms |
| Conditional risk upper | 0.748989795 | 0.808989795 |
| Strict 0.8 exclusion | Yes, **if premises hold** | **No** |

The 2-ms local difference is invisible to the two endpoint anchors even if those anchor times are perfect. This is a counterexample to **extrapolating an average or affine-fit period to each gap without validating clock regularity**. It does not prove a human blink occurred. The counterexample remains distinguishable by an independently calibrated optical observation near frame 151; it does not establish that all optical timing is insufficient.

The elementary sharp interval-sum envelope explains why: for N inter-frame intervals with observed total span S and independently established lower bound p_min on the other intervals, the largest possible local period is S-(N-1)p_min. If only strictly increasing frame starts are known, this has supremum S. A long baseline can have tiny mean error and still hide a large local deviation. This is an elementary identifiability statement, not claimed as mathematical novelty.

## Frozen controls and verification

- [Exact rational Python reproducer](e002_513_nonaffine_clock.py), committed after freeze: constructs both 301-start sequences without rounding drift and propagates the existing scalar exposure bound using 70-digit decimal arithmetic.
- [14 adversarial unit tests](test_e002_513_nonaffine_clock.py): identical anchors, frame continuity, shutter nonoverlap, frozen 2-ms spike, exact compensation, classification reversal, intermediate-pulse distinguishability, interval-sum envelope and its attainability, invalid geometry, invalid envelopes, exposure overlap, strict threshold, and unconditional product blocking. **14/14 passed locally** before GitHub persistence.
- Independent Node.js arithmetic reproduced risk 0.7489897948556635 versus 0.8089897948556636 locally. The [hosted workflow](../../.github/workflows/e002_513_nonaffine_clock.yml) executes both Python and independent Node controls. **Hosted run 40776503360 was queued at report creation; no hosted success is claimed.**
- No source images, human identifiers, native S01 indices, individual ratings or private dataset artifacts were generated or published.

## Direct measurement and product consequence

A physical instrument study must independently establish **per-gap exposure start/end bounds** or an independently verified affine-clock/jitter envelope covering every gap being certified. Long-baseline pulses and nominal video FPS alone cannot substitute for this. With a rolling shutter, also authenticate line delay, scan direction, tracked sensor row and geometric correspondence; if multirow RGB, unknown gaze, blur, lighting, glasses, missingness or sensor mapping defeats the scalar forward model, abstain. The actual physical study must record externally timed optical transitions at the preregistered target gap and independently audit frame continuity. Do not use a smartphone animation as an external clock.

The existing [E002-507](E002_507_FROZEN.md) blinded S01 anatomical pilot remains the immediate human-validation task. The two genuine raters, independently measured physical shutter/clock, continuous-time velocity envelope and participant-disjoint high-rate human predictions are still absent. No finite-difference trace is silently upgraded to a certified continuous-time speed maximum. No more synthetic parameter tuning is warranted; the next progress must be externally obtained evidence.

**Anatomical human ratings: 0. Authenticated physical shutter/clock: 0. Certified continuous-time eyelid-speed envelope: 0. Held-out physical predictions: 0.** E002-371 remains physically unvalidated. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. Hush remains a separate, unmodified workstream.
