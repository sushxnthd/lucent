# E002-586 | Optical phase-scan timing instrument: verified synthetic result, no physical certification

**Protocol freeze:** [E002_586_FROZEN.md](E002_586_FROZEN.md) committed at `4b47fcc` before implementation. **Evidence tier:** synthetic rectangular-exposure/affine-rolling-shutter instrument only. [Python source](e002_586_optical_phase_scan.py), [independent Node replay](e002_586_independent_replay.cjs), [hosted workflow](../../.github/workflows/e002_586_optical_phase_scan.yml).

## New reproducible result

The independent implementations evaluate a deliberately finite candidate grid of 405 shutter models: start offset 0–4 ms in 0.5-ms steps, exposure 2–6 ms in 0.5-ms steps, and per-row delay 0–0.2 ms in 0.05-ms steps. They generate 75 optical bright-to-dark phase observations at sensor rows 0, 20 and 40 (25 phases per row), from the synthetic truth s0=2 ms, E=4 ms, d=0.1 ms/row.

| Row | Exact-phase, exact-intensity outer exposure support (ms) | Phase ±0.5 ms and intensity ±0.1 outer support (ms) |
| --- | --- | --- |
| 0 | [2,6] | [1,7] |
| 20 | [4,8] | [3,9] |
| 40 | [6,10] | [5,11] |

**Exact synthetic inversion:** 1 feasible grid candidate. **Relaxed uncertainty:** 14 feasible grid candidates, with the true candidate retained. The support width expands from 4 to 6 ms at each row, and the all-row envelope expands from [2,10] to [1,11] ms. For an illustrative perfectly periodic 30-Hz camera, the between-frame uncovered interval across these three rows would be **25.333 ms** under the exact synthetic model but could be only **23.333 ms** under the relaxed model. A naive point-sample calculation would use 33.333 ms. These are illustrative, not measured camera timings.

The Python implementation passed 16 declared synthetic controls locally, including exact and zero-delay controls, uncertainty monotonicity, missing/plateau-only phase data, eight independent calibration flags, non-affine row-time model rejection, inconsistent optical intensity and no physical-certification promotion. A separately coded Node.js exhaustive-grid replay reproduced the 1/14 candidate counts and every support interval. Hosted CI result must be inspected separately; local success is not hosted success.

## Important limitations and falsification implications

1. This is **not a continuous-parameter outer bound**. The finite candidate grid can miss a real sensor configuration between grid points, so a feasible grid support cannot certify physical coverage. A future validated interval solver or independent metrology must cover all physically admissible continuous parameters.
2. The forward model assumes rectangular integration, linear unclipped intensity, an independently timed optical edge, fixed exposure mode, and affine row delay. Real sensors may have nonlinear tone maps, auto-HDR, overlapping readout, flicker, LED finite transitions and changing exposure. An unmodeled effect can invalidate all candidate supports.
3. Optical phase uncertainty is treated as an independent bounded nuisance, not inferred from the commanded LED timestamp. The actual edge must be independently recorded with a photodiode/oscilloscope or equivalent.
4. The input control booleans are *assertions*, not authenticated evidence. The script cannot establish physical calibration merely because they are set true.
5. Three observed rows do not establish a whole-frame rolling-shutter law, nor eyelid-region row mapping under gaze/geometry changes. A third-row non-affine falsifier demonstrates the need for overdetermined row controls.

**Priority audit:** Camera timing/rolling-shutter calibration is established prior work, not claimed as Lucent novelty: Huai et al., *Optics Letters* 48, 847–850 (2023), DOI [10.1364/OL.474375](https://doi.org/10.1364/OL.474375); Kurosawa et al., *Japanese Journal of Forensic Science and Technology* 29, 135–153 (2024), DOI [10.3408/jafst.875](https://doi.org/10.3408/jafst.875). Lucent's unresolved research claim concerns coupling independently validated shutter supports to independently bounded continuous-time human eyelid motion and prospective hidden-closure tests.

## Required physical next step

Use the [E002-585 human handoff](E002_585_HUMAN_HANDOFF.md) and collect **actual** photodiode-timed phase-scan exposures and paired ordinary/high-speed eye recordings. Independently blinded anatomical raters and participant-disjoint holdout must test frozen E002-371 predictions. Predeclare a falsifier: any held-out physical closure witness inside a genuinely certified exclusion gap rejects the exclusion claim or its assumptions. Stratify by brightness, blur, gaze, glasses, row geometry, missing frames, clock uncertainty and autoexposure state.

**Current evidence counts:** independently blinded human rater pairs 0; physically calibrated shutter captures 0; independently justified hard continuous-time eyelid-velocity ceilings 0; held-out physical closure predictions 0. **Product:** `ABSTAIN_UNCALIBRATED`; production `BLOCKED`. Hush untouched.
