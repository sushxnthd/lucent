# E002-479 FROZEN — sub-grid optical shutter-response island

Date: 2026-10-27. Kernel E002-371. Hypothesis is adversarially constructed after E002-478; **not** a blinded human study or physical calibration.

## Question and independent prediction

Does the E002-477 0.05-ms phase grid, with a narrow finite optical pulse, constrain shutter sensitivity at unmeasured phases? Compare two **stationary, frame-periodic** shutter-response models, both with a rectangular base response on phase [0.4,1.4] ms. Model B additionally contains a rectangular 0.20-amplitude island at phase [2.020,2.030] ms, in an otherwise dark region; model A has no island. Period T = 1000/240 ms. This is an instrument-model counterexample, **not** an observed physical shutter.

Use exactly 168 phase starts at multiples of 0.05 ms over two periods, pulse width 0.006 ms, 20 repeats and two row strata, with pulse-phase uncertainty u = 0.004 ms. Camera contrast is the average of the shutter sensitivity over the actual pulse window; dark reference 0; gain locked 1; no dropped/saturated frames. All files must pass the actual E002-477 intake. Independently record each pulse's corresponding frame attribution; use the same stationary response in both periods.

**Frozen predictions, before implementation:**

1. The two shutter models produce **byte-identical 6,720-row camera and clock CSVs** at the original phase grid; their manifest hashes also match, and E002-477 returns PASS_INTAKE_ONLY for both. Thus intake plus finite-grid optical responses cannot identify an isolated sensitivity island.
2. Under a phase-start error bound u, the interval between consecutive pulse supports has a guaranteed uncovered interior of width Δ-w-2u = **0.036 ms** for Δ=0.05 ms and w=0.006 ms. The chosen 0.010-ms island is disjoint from all measured pulse supports over both periods, even with ±0.004-ms phase error.
3. A **new independently timed held-out probe** at phase T*k + 2.022 ms, k in {0,1}, with 20 repeats per period and bounded ±0.002-ms phase jitter and ±0.002 normalized-contrast error, discriminates the 0.20 island from the null using the predeclared contrast threshold 0.04. A low-amplitude 0.004 island is not detectable at that threshold and must not be labeled physically absent.
4. No real camera support, physiological hard velocity, hidden-closure exclusion, or product authorization follows. Report every negative result and make the acquisition gate require independent staggered/held-out optical phases plus calibrated optical-response detection limits, not inferred exact zero response.

## Validity controls

The model is periodic and explicitly uses CORRESPONDING_FRAME attribution, addressing E002-478. Evaluate both row strata separately. Pulse times are externally stipulated and not inferred from video timestamps. The test uses noise/jitter only for the held-out probe; all noise and brightness assumptions are synthetic. A passed intake cannot authenticate hardware, bound actual sensor optical tails, or establish human velocity. Human nuisance tests (geometry, gaze, glasses, blur, missingness, sampling and clock) remain mandatory downstream and are not silently claimed here.

**Stop rule:** if any training-grid sample overlaps the island, or the actual intake rejects the fixtures, record the falsification and do not claim exact aliasing. If held-out probes do not separate the high-amplitude models under frozen errors, reject the stated detection prediction.